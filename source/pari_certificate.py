"""PARI/GP ECPP certificate generation and exact verification for P009.

PARI ECPP certificates are encoded here as canonical JSON containing only
integers and lists.  The same JSON is also valid GP vector syntax, so the
verifier can pass a strictly validated payload to ``primecertisvalid`` without
evaluating an arbitrary certificate file as GP source code.

For ``N < 2^64`` PARI may return the integer ``N`` itself.  For larger inputs
the ECPP certificate is a vector whose first row starts with the certified
subject.  Subject binding is checked in Python before a fresh GP process is
invoked for the exact certificate verification.
"""

from __future__ import annotations

import json
import re
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

from source.provenance import sha256_file


SCHEMA_VERSION = "p009-pari-ecpp-v1"
PARI_METHOD = "pari_ecpp"
DEFAULT_WSL_DISTRO = "Ubuntu"
DEFAULT_TIMEOUT_SECONDS = 900
SMALL_CERTIFICATE_LIMIT = 2**64
MAX_CERTIFICATE_DEPTH = 8
MAX_CERTIFICATE_INTEGERS = 1_000_000
CERT_BEGIN = "P009_CERTIFICATE_BEGIN"
CERT_END = "P009_CERTIFICATE_END"
VALID_BEGIN = "P009_VALIDITY_BEGIN"
VALID_END = "P009_VALIDITY_END"


class PariCertificateError(ValueError):
    """Raised when generation, serialization, or verification is unsound."""


@dataclass(frozen=True)
class PariInvocation:
    command: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str
    elapsed_seconds: float
    maximum_resident_set_kib: int | None


@dataclass(frozen=True)
class PariVerification:
    status: str
    subject: str
    certificate_kind: str
    certificate_sha256: str | None
    gp_version: str | None
    elapsed_seconds: float
    maximum_resident_set_kib: int | None
    issues: tuple[str, ...]


PariProgramRunner = Callable[[str, int], PariInvocation]


def _parse_maximum_rss(stderr: str) -> int | None:
    match = re.search(
        r"Maximum resident set size \(kbytes\):\s*(\d+)", stderr
    )
    return None if match is None else int(match.group(1))


def run_gp_program(
    program: str,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    *,
    distro: str = DEFAULT_WSL_DISTRO,
) -> PariInvocation:
    """Invoke a fresh WSL GP verifier without ``shell=True``."""

    if timeout_seconds < 1:
        raise ValueError("timeout_seconds must be positive")
    command = (
        "wsl.exe",
        "-d",
        distro,
        "--",
        "/usr/bin/time",
        "-v",
        "gp",
        "-fq",
    )
    started = time.perf_counter()
    try:
        completed = subprocess.run(
            command,
            input=program,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            check=False,
        )
    except FileNotFoundError as exc:
        raise PariCertificateError("wsl.exe or PARI/GP was not found") from exc
    except subprocess.TimeoutExpired as exc:
        raise PariCertificateError(
            f"PARI/GP exceeded timeout {timeout_seconds} seconds"
        ) from exc
    elapsed = time.perf_counter() - started
    return PariInvocation(
        command=command,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        elapsed_seconds=elapsed,
        maximum_resident_set_kib=_parse_maximum_rss(completed.stderr),
    )


def probe_gp_version(*, distro: str = DEFAULT_WSL_DISTRO) -> str:
    command = ("wsl.exe", "-d", distro, "--", "gp", "--version")
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        raise PariCertificateError("PARI/GP version probe failed") from exc
    if completed.returncode != 0:
        raise PariCertificateError(
            "PARI/GP version probe returned nonzero: "
            f"{completed.returncode}: {completed.stderr.strip()}"
        )
    # PARI builds differ on whether the banner is written to stdout or stderr.
    # Treat both as diagnostic text, but still require a zero exit code and the
    # exact official banner prefix before accepting the probe.
    version_output = "\n".join((completed.stdout, completed.stderr))
    for line in version_output.splitlines():
        if "GP/PARI CALCULATOR Version" in line:
            return line.strip()
    raise PariCertificateError("PARI/GP version string was not found")


def extract_marked_payload(stdout: str, begin: str, end: str) -> str:
    lines = stdout.splitlines()
    begin_positions = [index for index, line in enumerate(lines) if line.strip() == begin]
    end_positions = [index for index, line in enumerate(lines) if line.strip() == end]
    if len(begin_positions) != 1 or len(end_positions) != 1:
        raise PariCertificateError(
            f"expected exactly one {begin}/{end} marker pair"
        )
    begin_index = begin_positions[0]
    end_index = end_positions[0]
    if end_index <= begin_index + 0:
        raise PariCertificateError("PARI output markers are out of order")
    payload = "\n".join(lines[begin_index + 1 : end_index]).strip()
    if not payload:
        raise PariCertificateError("PARI returned an empty marked payload")
    return payload


def _validate_node(value: object, *, depth: int = 0) -> int:
    if depth > MAX_CERTIFICATE_DEPTH:
        raise PariCertificateError("certificate nesting is too deep")
    if isinstance(value, bool):
        raise PariCertificateError("boolean is not a certificate integer")
    if isinstance(value, int):
        return 1
    if not isinstance(value, list):
        raise PariCertificateError("certificate contains a non-integer/list value")
    total = 0
    for item in value:
        total += _validate_node(item, depth=depth + 1)
        if total > MAX_CERTIFICATE_INTEGERS:
            raise PariCertificateError("certificate exceeds the integer-count guard")
    return total


def certificate_subject(certificate: object) -> int:
    """Return the exact prime subject after strict PARI-shape validation."""

    _validate_node(certificate)
    if isinstance(certificate, int):
        if not (2 <= certificate < SMALL_CERTIFICATE_LIMIT):
            raise PariCertificateError(
                "integer certificate is accepted only for 2 <= N < 2^64"
            )
        return certificate
    if not certificate:
        raise PariCertificateError("ECPP certificate vector is empty")
    for row in certificate:
        if not isinstance(row, list) or len(row) != 5:
            raise PariCertificateError("each ECPP row must be a five-element vector")
        if not all(isinstance(item, int) and not isinstance(item, bool) for item in row[:4]):
            raise PariCertificateError("ECPP row scalar fields must be integers")
        point = row[4]
        if (
            not isinstance(point, list)
            or len(point) != 2
            or not all(isinstance(item, int) and not isinstance(item, bool) for item in point)
        ):
            raise PariCertificateError("ECPP row point must contain two integers")
    subject = certificate[0][0]
    if not isinstance(subject, int) or isinstance(subject, bool) or subject < 2:
        raise PariCertificateError("ECPP certificate subject is invalid")
    return subject


def canonical_certificate_json(certificate: object) -> str:
    certificate_subject(certificate)
    return json.dumps(certificate, ensure_ascii=True, separators=(",", ":"))


def parse_certificate_json(text: str) -> object:
    try:
        certificate = json.loads(text)
    except json.JSONDecodeError as exc:
        raise PariCertificateError(f"certificate JSON is malformed: {exc}") from exc
    certificate_subject(certificate)
    return certificate


def _ensure_success(invocation: PariInvocation, stage: str) -> None:
    if invocation.returncode != 0:
        raise PariCertificateError(
            f"PARI {stage} returned {invocation.returncode}: "
            f"{invocation.stderr.strip()}"
        )


def generate_certificate_payload(
    subject: int,
    *,
    runner: PariProgramRunner = run_gp_program,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> tuple[object, PariInvocation]:
    if isinstance(subject, bool) or subject < 2:
        raise ValueError("subject must be an integer >= 2")
    program = (
        f"c=primecert({subject});\n"
        f'print("{CERT_BEGIN}");\n'
        "print(c);\n"
        f'print("{CERT_END}");\n'
        "quit\n"
    )
    invocation = runner(program, timeout_seconds)
    _ensure_success(invocation, "generation")
    raw_payload = extract_marked_payload(invocation.stdout, CERT_BEGIN, CERT_END)
    certificate = parse_certificate_json(raw_payload)
    if certificate == 0:
        raise PariCertificateError("PARI did not produce a primality certificate")
    actual_subject = certificate_subject(certificate)
    if actual_subject != subject:
        raise PariCertificateError(
            f"certificate subject mismatch: {actual_subject} != {subject}"
        )
    return certificate, invocation


def verify_certificate_payload(
    certificate: object,
    expected_subject: int,
    *,
    runner: PariProgramRunner = run_gp_program,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    gp_version: str | None = None,
    certificate_sha256: str | None = None,
) -> PariVerification:
    issues: list[str] = []
    try:
        actual_subject = certificate_subject(certificate)
        if actual_subject != expected_subject:
            raise PariCertificateError(
                f"certificate subject mismatch: {actual_subject} != {expected_subject}"
            )
        canonical = canonical_certificate_json(certificate)
        program = (
            f"c={canonical};\n"
            f'print("{VALID_BEGIN}");\n'
            "print(primecertisvalid(c));\n"
            f'print("{VALID_END}");\n'
            "quit\n"
        )
        invocation = runner(program, timeout_seconds)
        _ensure_success(invocation, "verification")
        validity = extract_marked_payload(invocation.stdout, VALID_BEGIN, VALID_END)
        if validity != "1":
            issues.append(f"primecertisvalid returned {validity!r}")
    except PariCertificateError as exc:
        issues.append(str(exc))
        invocation = PariInvocation((), 1, "", "", 0.0, None)
        actual_subject = expected_subject
    kind = "small_integer" if isinstance(certificate, int) else "ecpp_vector"
    return PariVerification(
        status="PASS" if not issues else "FAIL",
        subject=str(actual_subject),
        certificate_kind=kind,
        certificate_sha256=certificate_sha256,
        gp_version=gp_version,
        elapsed_seconds=invocation.elapsed_seconds,
        maximum_resident_set_kib=invocation.maximum_resident_set_kib,
        issues=tuple(issues),
    )


def _write_json_exclusive(path: Path, payload: object) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def generate_certificate_bundle(
    subject: int,
    output_directory: Path,
    *,
    runner: PariProgramRunner = run_gp_program,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    gp_version: str | None = None,
) -> dict[str, object]:
    """Generate, independently re-invoke GP, and persist one certificate."""

    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite certificate bundle: {output_directory}")
    certificate, generation = generate_certificate_payload(
        subject, runner=runner, timeout_seconds=timeout_seconds
    )
    canonical = canonical_certificate_json(certificate) + "\n"
    output_directory.mkdir(parents=True)
    certificate_path = output_directory / "certificate.json"
    with certificate_path.open("x", encoding="ascii", newline="\n") as handle:
        handle.write(canonical)
    certificate_hash = sha256_file(certificate_path)
    effective_version = gp_version
    if effective_version is None and runner is run_gp_program:
        effective_version = probe_gp_version()
    verification = verify_certificate_payload(
        certificate,
        subject,
        runner=runner,
        timeout_seconds=timeout_seconds,
        gp_version=effective_version,
        certificate_sha256=certificate_hash,
    )
    if verification.status != "PASS":
        raise PariCertificateError(
            "fresh-process verification failed: " + "; ".join(verification.issues)
        )
    generation_report = {
        "status": "PASS",
        "schema_version": SCHEMA_VERSION,
        "subject": str(subject),
        "certificate_kind": verification.certificate_kind,
        "gp_version": effective_version,
        "elapsed_seconds": generation.elapsed_seconds,
        "maximum_resident_set_kib": generation.maximum_resident_set_kib,
        "stderr": generation.stderr,
    }
    _write_json_exclusive(output_directory / "generation_report.json", generation_report)
    _write_json_exclusive(
        output_directory / "verification_report.json", asdict(verification)
    )
    artifacts = {
        name: sha256_file(output_directory / name)
        for name in (
            "certificate.json",
            "generation_report.json",
            "verification_report.json",
        )
    }
    manifest = {
        "status": "PASS",
        "schema_version": SCHEMA_VERSION,
        "method": PARI_METHOD,
        "subject": str(subject),
        "gp_version": effective_version,
        "artifacts_sha256": artifacts,
        "probable_prime_only": False,
        "actual_1e20_experiment_executed": False,
        "gpu_used": False,
    }
    _write_json_exclusive(output_directory / "manifest.json", manifest)
    return manifest


def verify_certificate_file(
    certificate_path: Path,
    expected_subject: int,
    *,
    expected_sha256: str | None = None,
    runner: PariProgramRunner = run_gp_program,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    gp_version: str | None = None,
) -> PariVerification:
    if not certificate_path.is_file():
        raise PariCertificateError(f"certificate file is missing: {certificate_path}")
    actual_hash = sha256_file(certificate_path)
    if expected_sha256 is not None and actual_hash != expected_sha256.lower():
        raise PariCertificateError("certificate SHA-256 mismatch")
    certificate = parse_certificate_json(
        certificate_path.read_text(encoding="ascii")
    )
    return verify_certificate_payload(
        certificate,
        expected_subject,
        runner=runner,
        timeout_seconds=timeout_seconds,
        gp_version=gp_version,
        certificate_sha256=actual_hash,
    )


def verify_pari_prime_evidence(evidence: object, artifact_root: Path | None) -> bool:
    """Adapter callback for ``boundary_witness.verify_boundary_witness``."""

    if artifact_root is None:
        raise PariCertificateError("artifact_root is required")
    value = int(getattr(evidence, "value"))
    method = str(getattr(evidence, "method"))
    relative_path = getattr(evidence, "certificate_path")
    expected_hash = getattr(evidence, "certificate_sha256")
    if method != PARI_METHOD or not relative_path or not expected_hash:
        raise PariCertificateError("prime evidence is not a complete PARI ECPP record")
    root = artifact_root.resolve()
    path = (root / str(relative_path)).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise PariCertificateError("certificate path escapes artifact root") from exc
    verification = verify_certificate_file(
        path,
        value,
        expected_sha256=str(expected_hash),
    )
    return verification.status == "PASS"


def run_adapter_validation(
    output_directory: Path,
    *,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    runner: PariProgramRunner = run_gp_program,
    gp_version: str | None = None,
) -> dict[str, object]:
    """Validate small-integer and >64-bit ECPP paths against installed GP."""

    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite validation: {output_directory}")
    effective_version = gp_version
    if effective_version is None and runner is run_gp_program:
        effective_version = probe_gp_version()
    if effective_version is None:
        raise PariCertificateError("gp_version is required for a custom runner")
    output_directory.mkdir(parents=True)
    subjects = (
        ("small", 101),
        ("intermediate", 1_000_000_000_000_000_000_000_000_000_057),
    )
    manifests: dict[str, object] = {}
    for label, subject in subjects:
        manifests[label] = generate_certificate_bundle(
            subject,
            output_directory / label,
            runner=runner,
            timeout_seconds=timeout_seconds,
            gp_version=effective_version,
        )
    intermediate_certificate = parse_certificate_json(
        (output_directory / "intermediate" / "certificate.json").read_text(
            encoding="ascii"
        )
    )
    wrong_subject = verify_certificate_payload(
        intermediate_certificate,
        subjects[1][1] + 2,
        runner=runner,
        timeout_seconds=timeout_seconds,
        gp_version=effective_version,
    )
    if wrong_subject.status != "FAIL" or not any(
        "subject mismatch" in issue for issue in wrong_subject.issues
    ):
        raise PariCertificateError("wrong-subject negative control was not rejected")
    summary = {
        "status": "PASS",
        "schema_version": SCHEMA_VERSION,
        "experiment": "P009_PARI_ADAPTER_VALIDATION",
        "gp_version": effective_version,
        "small_subject": str(subjects[0][1]),
        "intermediate_subject": str(subjects[1][1]),
        "small_certificate_kind": "small_integer",
        "intermediate_certificate_kind": "ecpp_vector",
        "wrong_subject_rejected": True,
        "actual_1e20_experiment_executed": False,
        "gpu_used": False,
    }
    _write_json_exclusive(output_directory / "summary.json", summary)
    artifacts = {
        "small/manifest.json": sha256_file(output_directory / "small" / "manifest.json"),
        "intermediate/manifest.json": sha256_file(
            output_directory / "intermediate" / "manifest.json"
        ),
        "summary.json": sha256_file(output_directory / "summary.json"),
    }
    _write_json_exclusive(
        output_directory / "manifest.json",
        {
            **summary,
            "artifacts_sha256": artifacts,
            "saved_artifact_verification": "PASS",
        },
    )
    return summary


def verify_saved_adapter_validation(
    output_directory: Path,
    *,
    runner: PariProgramRunner = run_gp_program,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    gp_version: str | None = None,
) -> dict[str, object]:
    issues: list[str] = []
    try:
        root_manifest = json.loads(
            (output_directory / "manifest.json").read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        return {"status": "FAIL", "issues": [f"manifest read failed: {exc}"]}
    if root_manifest.get("experiment") != "P009_PARI_ADAPTER_VALIDATION":
        issues.append("unexpected adapter validation experiment label")
    root_artifacts = root_manifest.get("artifacts_sha256")
    if not isinstance(root_artifacts, dict):
        issues.append("root manifest lacks artifact hashes")
        root_artifacts = {}
    for relative, expected in root_artifacts.items():
        path = output_directory / str(relative)
        if not path.is_file():
            issues.append(f"missing root artifact: {relative}")
        elif sha256_file(path) != str(expected):
            issues.append(f"root artifact hash mismatch: {relative}")

    effective_version = gp_version
    if effective_version is None and runner is run_gp_program:
        try:
            effective_version = probe_gp_version()
        except PariCertificateError as exc:
            issues.append(f"GP version probe failed: {exc}")
    if effective_version is None:
        effective_version = str(root_manifest.get("gp_version") or "unknown")

    verified_subjects = 0
    for label in ("small", "intermediate"):
        bundle = output_directory / label
        try:
            manifest = json.loads(
                (bundle / "manifest.json").read_text(encoding="utf-8")
            )
            artifacts = manifest.get("artifacts_sha256")
            if not isinstance(artifacts, dict):
                raise PariCertificateError("bundle manifest lacks artifact hashes")
            for name, expected in artifacts.items():
                path = bundle / str(name)
                if not path.is_file() or sha256_file(path) != str(expected):
                    raise PariCertificateError(
                        f"bundle artifact missing/hash mismatch: {label}/{name}"
                    )
            certificate_path = bundle / "certificate.json"
            verification = verify_certificate_file(
                certificate_path,
                int(manifest["subject"]),
                expected_sha256=str(artifacts["certificate.json"]),
                runner=runner,
                timeout_seconds=timeout_seconds,
                gp_version=effective_version,
            )
            if verification.status != "PASS":
                raise PariCertificateError(
                    "; ".join(verification.issues) or "certificate verification failed"
                )
            verified_subjects += 1
        except (KeyError, OSError, ValueError, PariCertificateError) as exc:
            issues.append(f"{label} bundle verification failed: {exc}")
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "verified_subject_count": verified_subjects,
        "gp_version": effective_version,
        "manifest_sha256": (
            sha256_file(output_directory / "manifest.json")
            if (output_directory / "manifest.json").is_file()
            else None
        ),
        "actual_1e20_experiment_executed": False,
    }


def require_adapter_completion(manifest_path: Path) -> dict[str, object]:
    """Require a PASS manifest plus a hash-bound fresh saved verification."""

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PariCertificateError(f"adapter manifest cannot be read: {exc}") from exc
    if manifest.get("status") != "PASS" or manifest.get("experiment") != "P009_PARI_ADAPTER_VALIDATION":
        raise PariCertificateError("adapter manifest is not terminal PASS")
    report_path = manifest_path.with_name("saved_verification_report.json")
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PariCertificateError(f"adapter saved-verification report cannot be read: {exc}") from exc
    if report.get("status") != "PASS" or report.get("verified_subject_count") != 2:
        raise PariCertificateError("adapter saved-verification report is not complete PASS")
    if report.get("manifest_sha256") != sha256_file(manifest_path):
        raise PariCertificateError("adapter saved-verification report is not bound to manifest")
    return manifest


__all__ = [
    "CERT_BEGIN",
    "CERT_END",
    "DEFAULT_TIMEOUT_SECONDS",
    "PARI_METHOD",
    "PariCertificateError",
    "PariInvocation",
    "PariVerification",
    "canonical_certificate_json",
    "certificate_subject",
    "extract_marked_payload",
    "generate_certificate_bundle",
    "generate_certificate_payload",
    "parse_certificate_json",
    "probe_gp_version",
    "require_adapter_completion",
    "run_adapter_validation",
    "run_gp_program",
    "verify_certificate_file",
    "verify_certificate_payload",
    "verify_pari_prime_evidence",
    "verify_saved_adapter_validation",
]
