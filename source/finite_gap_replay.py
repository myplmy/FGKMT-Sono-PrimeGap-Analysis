"""P010A exact modulus-2310 replay and P010B candidate-scan preparation."""

from __future__ import annotations

import json
import shutil
import time
from fractions import Fraction
from pathlib import Path

from source.finite_gap_certificate import (
    DEFAULT_A,
    DEFAULT_B,
    PI_1E20,
    PI_1E21,
    RationalCertificate,
    read_certificate,
    transition_resource_estimate,
    unit_residues,
    verify_certificate,
)
from source.finite_gap_separation import (
    SeparationCandidate,
    SeparationResourceGuardError,
    scan_exact_certificate_constraints,
    scan_transition_violations,
    separation_memory_estimate,
)
from source.provenance import require_experiment_approval, sha256_file


P007_MOD2310_CERTIFICATE_SHA256 = (
    "725a2dcd4fd04b870a7f42edb85e6d9c029290fba861c592348a54d370c88ae5"
)
P010A_EXPERIMENT = "P010A_MOD2310_REPLAY"
P010B_EXPERIMENT = "P010B_MOD30030_ONE_CANDIDATE_SCAN"
P010A_EXACT_LIFT_EXPERIMENT = "P010A_MOD30030_EXACT_LIFT"


class ReplayError(ValueError):
    """Raised when replay provenance or equivalence checks fail."""


def candidate_from_certificate(
    certificate: RationalCertificate,
) -> SeparationCandidate:
    denominator = certificate.denominator
    if denominator <= 0:
        raise ReplayError("certificate denominator must be positive")
    return SeparationCandidate(
        lambda_value=certificate.lambda_num / denominator,
        mu_value=certificate.mu_num / denominator,
        potentials=tuple(value / denominator for value in certificate.phi_num),
    )


def lift_candidate_to_modulus(
    certificate: RationalCertificate,
    target_modulus: int,
) -> SeparationCandidate:
    """Lift potentials by reduction to the source modulus residue state."""

    if target_modulus % certificate.modulus:
        raise ReplayError("target modulus must be a multiple of source modulus")
    source_residues = unit_residues(certificate.modulus)
    source_index = {residue: index for index, residue in enumerate(source_residues)}
    if len(certificate.phi_num) != len(source_residues):
        raise ReplayError("certificate potential count does not match source states")
    lifted: list[float] = []
    for residue in unit_residues(target_modulus):
        reduced = residue % certificate.modulus
        index = source_index.get(reduced)
        if index is None:
            raise ReplayError("target unit residue did not reduce to a source unit")
        lifted.append(certificate.phi_num[index] / certificate.denominator)
    return SeparationCandidate(
        lambda_value=certificate.lambda_num / certificate.denominator,
        mu_value=certificate.mu_num / certificate.denominator,
        potentials=tuple(lifted),
    )


def lift_certificate_exact_to_modulus(
    certificate: RationalCertificate,
    target_modulus: int,
) -> RationalCertificate:
    """Lift an exact certificate through residue reduction to a multiple modulus."""

    if target_modulus % certificate.modulus:
        raise ReplayError("target modulus must be a multiple of source modulus")
    if certificate.lambda_num < 0:
        raise ReplayError("exact modulus lift requires nonnegative lambda")
    source_residues = unit_residues(certificate.modulus)
    source_index = {residue: index for index, residue in enumerate(source_residues)}
    if len(certificate.phi_num) != len(source_residues):
        raise ReplayError("certificate potential count does not match source states")
    lifted = []
    for residue in unit_residues(target_modulus):
        index = source_index.get(residue % certificate.modulus)
        if index is None:
            raise ReplayError("target unit residue did not reduce to a source unit")
        lifted.append(certificate.phi_num[index])
    return RationalCertificate(
        modulus=target_modulus,
        threshold=certificate.threshold,
        denominator=certificate.denominator,
        lambda_num=certificate.lambda_num,
        mu_num=certificate.mu_num,
        t_num=certificate.t_num,
        phi_num=tuple(lifted),
        internal_bound=certificate.internal_bound,
        total_bound=certificate.total_bound,
    )


def _write_json_exclusive(path: Path, payload: object) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def _write_manifest(
    output_directory: Path,
    *,
    experiment: str,
    summary: dict[str, object],
    artifact_names: tuple[str, ...],
) -> dict[str, object]:
    artifacts = {
        name: sha256_file(output_directory / name) for name in artifact_names
    }
    manifest = {
        "status": "PASS",
        "experiment": experiment,
        "artifacts_sha256": artifacts,
        "input_certificate_sha256": summary["input_certificate_sha256"],
        "direct_prime_search_executed": False,
        "gpu_used": False,
    }
    _write_json_exclusive(output_directory / "manifest.json", manifest)
    return manifest


def run_mod2310_replay(
    certificate_path: Path,
    output_directory: Path,
    *,
    approval_token: str | None,
    chunk_rows: int = 64,
    top_k: int = 100,
) -> dict[str, object]:
    require_experiment_approval(approval_token)
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite replay: {output_directory}")
    certificate_hash = sha256_file(certificate_path)
    if certificate_hash != P007_MOD2310_CERTIFICATE_SHA256:
        raise ReplayError("P007 modulus-2310 certificate hash is not pinned value")
    certificate = read_certificate(certificate_path)
    if certificate.modulus != 2310:
        raise ReplayError("P010A replay requires modulus 2310")

    started = time.perf_counter()
    pairwise = verify_certificate(certificate, edge_method="pairwise")
    offsets = verify_certificate(certificate, edge_method="offsets")
    if (
        pairwise["edge_constraints"] != offsets["edge_constraints"]
        or pairwise["minimum_integer_slack"] != offsets["minimum_integer_slack"]
        or pairwise["total_start_bounded_upper_bound"]
        != offsets["total_start_bounded_upper_bound"]
    ):
        raise ReplayError("independent exact edge builders disagree")

    candidate = candidate_from_certificate(certificate)
    oracle = scan_transition_violations(
        2310,
        certificate.threshold,
        candidate,
        chunk_rows=chunk_rows,
        top_k=top_k,
        allow_large_state_scan=True,
    )
    expected_constraints = transition_resource_estimate(
        2310, certificate.threshold
    )["total_transition_constraints"]
    if oracle["scanned_constraints"] != expected_constraints:
        raise ReplayError("chunk oracle did not scan the exact constraint count")
    if oracle["violation_count"] != 0:
        raise ReplayError("floating replay reported a violated exact certificate")
    elapsed = time.perf_counter() - started

    output_directory.mkdir(parents=True)
    input_copy = output_directory / "input_certificate_mod2310.txt"
    with input_copy.open("xb") as handle:
        handle.write(certificate_path.read_bytes())
    _write_json_exclusive(output_directory / "pairwise_exact_report.json", pairwise)
    _write_json_exclusive(output_directory / "offsets_exact_report.json", offsets)
    _write_json_exclusive(output_directory / "chunk_oracle_report.json", oracle)
    summary = {
        "status": "PASS",
        "experiment": P010A_EXPERIMENT,
        "input_certificate_sha256": certificate_hash,
        "modulus": 2310,
        "threshold": certificate.threshold,
        "states": oracle["states"],
        "exact_constraint_count": pairwise["edge_constraints"],
        "minimum_integer_slack": pairwise["minimum_integer_slack"],
        "floating_violation_count": oracle["violation_count"],
        "floating_minimum_slack": oracle["minimum_slack"],
        "total_start_bounded_upper_bound": pairwise[
            "total_start_bounded_upper_bound"
        ],
        "elapsed_seconds": elapsed,
        "exact_certificate_replayed": True,
        "direct_search_acceleration_proved": False,
        "mod30030_scan_executed": False,
        "gpu_used": False,
    }
    _write_json_exclusive(output_directory / "summary.json", summary)
    _write_manifest(
        output_directory,
        experiment=P010A_EXPERIMENT,
        summary=summary,
        artifact_names=(
            "input_certificate_mod2310.txt",
            "pairwise_exact_report.json",
            "offsets_exact_report.json",
            "chunk_oracle_report.json",
            "summary.json",
        ),
    )
    return summary


def verify_saved_mod2310_replay(output_directory: Path) -> dict[str, object]:
    issues: list[str] = []
    try:
        manifest = json.loads(
            (output_directory / "manifest.json").read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        return {"status": "FAIL", "issues": [f"manifest read failed: {exc}"]}
    if manifest.get("experiment") != P010A_EXPERIMENT:
        issues.append("unexpected replay experiment label")
    artifacts = manifest.get("artifacts_sha256")
    if not isinstance(artifacts, dict):
        issues.append("manifest lacks artifact hashes")
        artifacts = {}
    for name, expected in artifacts.items():
        path = output_directory / str(name)
        if not path.is_file():
            issues.append(f"missing artifact: {name}")
        elif sha256_file(path) != str(expected):
            issues.append(f"artifact hash mismatch: {name}")
    try:
        certificate = read_certificate(
            output_directory / "input_certificate_mod2310.txt"
        )
        pairwise = verify_certificate(certificate, edge_method="pairwise")
        offsets = verify_certificate(certificate, edge_method="offsets")
        if pairwise["minimum_integer_slack"] != offsets["minimum_integer_slack"]:
            issues.append("saved replay exact builders disagree")
        oracle = json.loads(
            (output_directory / "chunk_oracle_report.json").read_text(
                encoding="utf-8"
            )
        )
        expected = transition_resource_estimate(2310, certificate.threshold)[
            "total_transition_constraints"
        ]
        if oracle.get("scanned_constraints") != expected:
            issues.append("saved oracle constraint count mismatch")
        if oracle.get("violation_count") != 0:
            issues.append("saved oracle has violations")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        issues.append(f"exact saved replay verification failed: {exc}")
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "exact_recomputed": not issues,
        "manifest_sha256": (
            sha256_file(output_directory / "manifest.json")
            if (output_directory / "manifest.json").is_file()
            else None
        ),
        "direct_search_acceleration_proved": False,
    }


def require_mod2310_replay_completion(path: Path) -> dict[str, object]:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReplayError(f"P010A replay manifest cannot be read: {exc}") from exc
    if manifest.get("status") != "PASS" or manifest.get("experiment") != P010A_EXPERIMENT:
        raise ReplayError("P010A replay manifest is not a terminal PASS")
    if manifest.get("input_certificate_sha256") != P007_MOD2310_CERTIFICATE_SHA256:
        raise ReplayError("P010A replay manifest certificate hash mismatch")
    verification_path = path.with_name("saved_verification_report.json")
    try:
        verification = json.loads(verification_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReplayError(f"P010A saved-verification report cannot be read: {exc}") from exc
    if verification.get("status") != "PASS" or not verification.get("exact_recomputed"):
        raise ReplayError("P010A saved-verification report is not exact PASS")
    if verification.get("manifest_sha256") != sha256_file(path):
        raise ReplayError("P010A saved-verification report is not bound to manifest")
    return manifest


def run_mod30030_one_candidate_scan(
    certificate_path: Path,
    replay_manifest_path: Path,
    output_directory: Path,
    *,
    approval_token: str | None,
    chunk_rows: int = 64,
    top_k: int = 1_000,
) -> dict[str, object]:
    require_experiment_approval(approval_token)
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite scan: {output_directory}")
    replay_manifest = require_mod2310_replay_completion(replay_manifest_path)
    certificate_hash = sha256_file(certificate_path)
    if certificate_hash != P007_MOD2310_CERTIFICATE_SHA256:
        raise ReplayError("P010B input certificate hash mismatch")
    certificate = read_certificate(certificate_path)
    if certificate.modulus != 2310:
        raise ReplayError("P010B source certificate must use modulus 2310")
    estimate = separation_memory_estimate(
        30030, chunk_rows=chunk_rows, top_k=top_k
    )
    if not estimate["under_1_gib"]:
        raise ReplayError("P010B oracle estimate exceeds the 1 GiB stage gate")

    candidate = lift_candidate_to_modulus(certificate, 30030)
    started = time.perf_counter()
    oracle = scan_transition_violations(
        30030,
        certificate.threshold,
        candidate,
        chunk_rows=chunk_rows,
        top_k=top_k,
        allow_large_state_scan=True,
    )
    elapsed = time.perf_counter() - started
    expected_constraints = transition_resource_estimate(
        30030, certificate.threshold
    )["total_transition_constraints"]
    if oracle["scanned_constraints"] != expected_constraints:
        raise ReplayError("modulus-30030 scan did not cover every transition")

    output_directory.mkdir(parents=True)
    with (output_directory / "input_certificate_mod2310.txt").open("xb") as handle:
        handle.write(certificate_path.read_bytes())
    shutil.copyfile(
        replay_manifest_path, output_directory / "input_p010a_replay_manifest.json"
    )
    shutil.copyfile(
        replay_manifest_path.with_name("saved_verification_report.json"),
        output_directory / "input_p010a_saved_verification_report.json",
    )
    _write_json_exclusive(output_directory / "memory_estimate.json", estimate)
    _write_json_exclusive(output_directory / "chunk_oracle_report.json", oracle)
    summary = {
        "status": "PASS",
        "experiment": P010B_EXPERIMENT,
        "input_certificate_sha256": certificate_hash,
        "p010a_manifest_status": replay_manifest["status"],
        "source_modulus": 2310,
        "target_modulus": 30030,
        "threshold": certificate.threshold,
        "states": oracle["states"],
        "scanned_constraints": oracle["scanned_constraints"],
        "violation_count": oracle["violation_count"],
        "minimum_slack": oracle["minimum_slack"],
        "candidate_feasible_floating": oracle["violation_count"] == 0,
        "elapsed_seconds": elapsed,
        "exact_mod30030_certificate_verified": False,
        "lp_solved": False,
        "direct_search_acceleration_proved": False,
        "gpu_used": False,
    }
    _write_json_exclusive(output_directory / "summary.json", summary)
    _write_manifest(
        output_directory,
        experiment=P010B_EXPERIMENT,
        summary=summary,
        artifact_names=(
            "input_certificate_mod2310.txt",
            "input_p010a_replay_manifest.json",
            "input_p010a_saved_verification_report.json",
            "memory_estimate.json",
            "chunk_oracle_report.json",
            "summary.json",
        ),
    )
    return summary


def verify_saved_mod30030_scan(output_directory: Path) -> dict[str, object]:
    issues: list[str] = []
    try:
        manifest = json.loads(
            (output_directory / "manifest.json").read_text(encoding="utf-8")
        )
        summary = json.loads(
            (output_directory / "summary.json").read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        return {"status": "FAIL", "issues": [f"saved scan read failed: {exc}"]}
    if manifest.get("experiment") != P010B_EXPERIMENT:
        issues.append("unexpected scan experiment label")
    if manifest.get("input_certificate_sha256") != P007_MOD2310_CERTIFICATE_SHA256:
        issues.append("scan manifest source certificate hash mismatch")
    artifacts = manifest.get("artifacts_sha256")
    if not isinstance(artifacts, dict):
        issues.append("manifest lacks artifact hashes")
        artifacts = {}
    for name, expected in artifacts.items():
        path = output_directory / str(name)
        if not path.is_file() or sha256_file(path) != str(expected):
            issues.append(f"artifact missing/hash mismatch: {name}")
    try:
        replay_copy = output_directory / "input_p010a_replay_manifest.json"
        verification_copy = output_directory / "input_p010a_saved_verification_report.json"
        # The copied prerequisite report has an explicit name.  The scan's own
        # saved_verification_report.json is expected to exist on every later
        # audit and must not be mistaken for a prerequisite alias.
        verification_payload = json.loads(verification_copy.read_text(encoding="utf-8"))
        if verification_payload.get("status") != "PASS":
            raise ReplayError("copied P010A verification report is not PASS")
        if verification_payload.get("manifest_sha256") != sha256_file(replay_copy):
            # The copied manifest is byte-identical to the original, so its hash
            # remains the exact binding recorded by P010A.
            raise ReplayError("copied P010A verification report binding mismatch")
        certificate_hash = sha256_file(
            output_directory / "input_certificate_mod2310.txt"
        )
        if certificate_hash != P007_MOD2310_CERTIFICATE_SHA256:
            issues.append("saved source certificate hash mismatch")
        expected = transition_resource_estimate(30030, int(summary["threshold"]))[
            "total_transition_constraints"
        ]
        if int(summary.get("source_modulus", -1)) != 2310:
            issues.append("saved scan source modulus mismatch")
        if int(summary.get("target_modulus", -1)) != 30030:
            issues.append("saved scan target modulus mismatch")
        if int(summary.get("threshold", -1)) != 1856:
            issues.append("saved scan threshold mismatch")
        if int(summary["scanned_constraints"]) != expected:
            issues.append("saved scan constraint count mismatch")
    except (OSError, ValueError, ReplayError) as exc:
        issues.append(f"saved scan structural verification failed: {exc}")
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "scan_reexecuted": False,
        "manifest_sha256": (
            sha256_file(output_directory / "manifest.json")
            if (output_directory / "manifest.json").is_file()
            else None
        ),
        "exact_mod30030_certificate_verified": False,
        "direct_search_acceleration_proved": False,
    }


def require_mod30030_scan_completion(path: Path) -> dict[str, object]:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
        summary = json.loads(path.with_name("summary.json").read_text(encoding="utf-8"))
        verification = json.loads(
            path.with_name("saved_verification_report.json").read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise ReplayError(f"P010B scan prerequisite cannot be read: {exc}") from exc
    if manifest.get("status") != "PASS" or manifest.get("experiment") != P010B_EXPERIMENT:
        raise ReplayError("P010B scan manifest is not a terminal PASS")
    if manifest.get("input_certificate_sha256") != P007_MOD2310_CERTIFICATE_SHA256:
        raise ReplayError("P010B scan manifest certificate hash mismatch")
    if verification.get("status") != "PASS":
        raise ReplayError("P010B saved-verification report is not PASS")
    if verification.get("manifest_sha256") != sha256_file(path):
        raise ReplayError("P010B saved-verification report is not bound to manifest")
    if (
        summary.get("status") != "PASS"
        or int(summary.get("source_modulus", -1)) != 2310
        or int(summary.get("target_modulus", -1)) != 30030
        or int(summary.get("threshold", -1)) != 1856
        or int(summary.get("scanned_constraints", -1)) != 35_224_647
    ):
        raise ReplayError("P010B scan summary is incomplete")
    if int(summary.get("violation_count", -1)) != 0:
        raise ReplayError("P010B lifted candidate has floating violations")
    return summary


def _recompute_bound(certificate: RationalCertificate) -> tuple[int, int]:
    internal_gap_count = PI_1E21 - PI_1E20 - 1
    span = DEFAULT_B - DEFAULT_A
    value = Fraction(
        certificate.lambda_num * span
        + certificate.mu_num * internal_gap_count
        + 2 * certificate.t_num,
        certificate.denominator,
    )
    internal = -(-value.numerator // value.denominator)
    return internal, internal + 1


def run_mod30030_exact_lift(
    certificate_path: Path,
    replay_manifest_path: Path,
    scan_manifest_path: Path,
    output_directory: Path,
    *,
    approval_token: str | None,
    chunk_rows: int = 64,
) -> dict[str, object]:
    """Exact-stream the lifted modulus-2310 certificate at modulus 30030."""

    require_experiment_approval(approval_token)
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite exact lift: {output_directory}")
    require_mod2310_replay_completion(replay_manifest_path)
    scan_summary = require_mod30030_scan_completion(scan_manifest_path)
    if sha256_file(certificate_path) != P007_MOD2310_CERTIFICATE_SHA256:
        raise ReplayError("P010A exact-lift input certificate hash mismatch")
    source_certificate = read_certificate(certificate_path)
    lifted = lift_certificate_exact_to_modulus(source_certificate, 30030)
    internal, total = _recompute_bound(lifted)
    if internal != lifted.internal_bound or total != lifted.total_bound:
        raise ReplayError("lifted certificate finite-range bound changed")

    started = time.perf_counter()
    exact_report = scan_exact_certificate_constraints(
        lifted,
        chunk_rows=chunk_rows,
        top_k=100,
        allow_large_state_scan=True,
    )
    elapsed = time.perf_counter() - started
    if exact_report["status"] != "PASS":
        raise ReplayError("lifted modulus-30030 certificate has an exact violation")

    output_directory.mkdir(parents=True)
    shutil.copyfile(certificate_path, output_directory / "input_certificate_mod2310.txt")
    shutil.copyfile(replay_manifest_path, output_directory / "input_p010a_replay_manifest.json")
    shutil.copyfile(
        replay_manifest_path.with_name("saved_verification_report.json"),
        output_directory / "input_p010a_saved_verification_report.json",
    )
    shutil.copyfile(scan_manifest_path, output_directory / "input_p010b_scan_manifest.json")
    shutil.copyfile(
        scan_manifest_path.with_name("saved_verification_report.json"),
        output_directory / "input_p010b_saved_verification_report.json",
    )
    with (output_directory / "certificate_mod30030_exact_lift.txt").open(
        "x", encoding="utf-8", newline="\n"
    ) as handle:
        from source.finite_gap_certificate import certificate_text

        handle.write(certificate_text(lifted))
    theorem = {
        "status": "PASS",
        "source_modulus": source_certificate.modulus,
        "target_modulus": lifted.modulus,
        "target_is_multiple_of_source": lifted.modulus % source_certificate.modulus == 0,
        "lambda_nonnegative": lifted.lambda_num >= 0,
        "potential_map": "phi_target(r)=phi_source(r mod source_modulus)",
        "implication": (
            "each target transition is a source congruence-class transition; "
            "its least admissible representative is no smaller, so lambda>=0 "
            "preserves the source inequality"
        ),
        "objective_and_bound_unchanged_by_lift": True,
    }
    _write_json_exclusive(output_directory / "modulus_lift_theorem_report.json", theorem)
    _write_json_exclusive(output_directory / "exact_streaming_report.json", exact_report)
    summary = {
        "status": "PASS",
        "experiment": P010A_EXACT_LIFT_EXPERIMENT,
        "input_certificate_sha256": sha256_file(certificate_path),
        "source_modulus": source_certificate.modulus,
        "target_modulus": lifted.modulus,
        "states": exact_report["states"],
        "exact_constraint_count": exact_report["scanned_constraints"],
        "minimum_integer_slack": exact_report["minimum_integer_slack"],
        "exact_violation_count": exact_report["violation_count"],
        "p010b_floating_minimum_slack": scan_summary["minimum_slack"],
        "total_start_bounded_upper_bound": str(total),
        "strict_bound_improvement": total < source_certificate.total_bound,
        "elapsed_seconds": elapsed,
        "lp_solved": False,
        "direct_search_acceleration_proved": False,
        "gpu_used": False,
    }
    _write_json_exclusive(output_directory / "summary.json", summary)
    _write_manifest(
        output_directory,
        experiment=P010A_EXACT_LIFT_EXPERIMENT,
        summary=summary,
        artifact_names=(
            "input_certificate_mod2310.txt",
            "input_p010a_replay_manifest.json",
            "input_p010a_saved_verification_report.json",
            "input_p010b_scan_manifest.json",
            "input_p010b_saved_verification_report.json",
            "certificate_mod30030_exact_lift.txt",
            "modulus_lift_theorem_report.json",
            "exact_streaming_report.json",
            "summary.json",
        ),
    )
    return summary


def verify_saved_mod30030_exact_lift(output_directory: Path) -> dict[str, object]:
    issues: list[str] = []
    try:
        manifest = json.loads((output_directory / "manifest.json").read_text(encoding="utf-8"))
        summary = json.loads((output_directory / "summary.json").read_text(encoding="utf-8"))
        artifacts = manifest.get("artifacts_sha256", {})
        if manifest.get("experiment") != P010A_EXACT_LIFT_EXPERIMENT:
            issues.append("unexpected exact-lift experiment label")
        if not isinstance(artifacts, dict):
            issues.append("manifest lacks artifact hashes")
            artifacts = {}
        for name, expected in artifacts.items():
            path = output_directory / str(name)
            if not path.is_file() or sha256_file(path) != str(expected):
                issues.append(f"artifact missing/hash mismatch: {name}")
        certificate = read_certificate(output_directory / "certificate_mod30030_exact_lift.txt")
        if sha256_file(output_directory / "input_certificate_mod2310.txt") != P007_MOD2310_CERTIFICATE_SHA256:
            issues.append("saved source certificate hash mismatch")
        for prefix in ("p010a", "p010b"):
            prerequisite_manifest = output_directory / f"input_{prefix}_{'replay' if prefix == 'p010a' else 'scan'}_manifest.json"
            prerequisite_verification = output_directory / f"input_{prefix}_saved_verification_report.json"
            verification_payload = json.loads(prerequisite_verification.read_text(encoding="utf-8"))
            if verification_payload.get("status") != "PASS":
                issues.append(f"saved {prefix} prerequisite verification is not PASS")
            if verification_payload.get("manifest_sha256") != sha256_file(prerequisite_manifest):
                issues.append(f"saved {prefix} prerequisite binding mismatch")
        exact = scan_exact_certificate_constraints(
            certificate, chunk_rows=64, top_k=100, allow_large_state_scan=True
        )
        internal, total = _recompute_bound(certificate)
        if exact["status"] != "PASS":
            issues.append("saved exact certificate has a violated transition")
        if int(summary.get("exact_constraint_count", -1)) != exact["scanned_constraints"]:
            issues.append("saved exact constraint count mismatch")
        if str(summary.get("total_start_bounded_upper_bound")) != str(total):
            issues.append("saved exact bound mismatch")
        if internal != certificate.internal_bound or total != certificate.total_bound:
            issues.append("saved certificate bound fields mismatch")
    except (OSError, ValueError, json.JSONDecodeError, SeparationResourceGuardError) as exc:
        issues.append(f"saved exact-lift verification failed: {exc}")
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "exact_recomputed": not issues,
        "manifest_sha256": (
            sha256_file(output_directory / "manifest.json")
            if (output_directory / "manifest.json").is_file()
            else None
        ),
        "strict_bound_improvement": False,
        "direct_search_acceleration_proved": False,
    }


__all__ = [
    "P007_MOD2310_CERTIFICATE_SHA256",
    "P010A_EXPERIMENT",
    "P010A_EXACT_LIFT_EXPERIMENT",
    "P010B_EXPERIMENT",
    "ReplayError",
    "candidate_from_certificate",
    "lift_candidate_to_modulus",
    "lift_certificate_exact_to_modulus",
    "require_mod2310_replay_completion",
    "require_mod30030_scan_completion",
    "run_mod2310_replay",
    "run_mod30030_one_candidate_scan",
    "run_mod30030_exact_lift",
    "verify_saved_mod2310_replay",
    "verify_saved_mod30030_scan",
    "verify_saved_mod30030_exact_lift",
]
