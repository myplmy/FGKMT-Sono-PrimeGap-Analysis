"""Exact boundary-witness schema and toy verifier for P009.

The canonical P009 block is half-open, ``[a, b)``.  A witness proves that a
prime ``p`` is the last prime below ``b`` and supplies a proved prime ``q`` at
or to the right of ``b`` with ``q - p < threshold``.  This closes the one gap
that can cross the right boundary of a start-bounded block.

The toy implementation uses deterministic trial division only for small
integers.  Production-size evidence must use a proof-producing backend such as
PARI/GP ECPP and a verifier callback; a probable-prime flag is never accepted.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

from source.provenance import sha256_file


SCHEMA_VERSION = "p009-boundary-witness-v1"
TOY_TRIAL_DIVISION_LIMIT = 10_000_000


class BoundaryWitnessError(ValueError):
    """Raised when boundary evidence does not satisfy the exact contract."""


@dataclass(frozen=True)
class PrimeEvidence:
    value: int
    method: str
    certificate_path: str | None = None
    certificate_sha256: str | None = None


@dataclass(frozen=True)
class CompositeEvidence:
    value: int
    factor: int


@dataclass(frozen=True)
class BoundaryWitness:
    schema_version: str
    block_a: int
    block_b: int
    threshold: int
    internal_start_bounded_upper_bound: int
    last_prime: PrimeEvidence
    right_prime: PrimeEvidence
    composite_evidence: tuple[CompositeEvidence, ...]


PrimeCertificateVerifier = Callable[[PrimeEvidence, Path | None], bool]


def _is_prime_trial_division(value: int) -> bool:
    """Deterministic small-integer primality proof used by toy tests only."""

    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    limit = math.isqrt(value)
    while divisor <= limit:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def _verify_prime_evidence(
    evidence: PrimeEvidence,
    *,
    artifact_root: Path | None,
    certificate_verifier: PrimeCertificateVerifier | None,
) -> bool:
    if evidence.method == "trial_division_exact":
        if evidence.value > TOY_TRIAL_DIVISION_LIMIT:
            raise BoundaryWitnessError(
                "trial_division_exact is restricted to the toy integer range"
            )
        if evidence.certificate_path is not None or evidence.certificate_sha256 is not None:
            raise BoundaryWitnessError(
                "toy trial-division evidence must not claim an external certificate"
            )
        return _is_prime_trial_division(evidence.value)

    if evidence.method == "pari_ecpp":
        if not evidence.certificate_path or not evidence.certificate_sha256:
            raise BoundaryWitnessError("PARI ECPP evidence lacks path or SHA-256")
        if artifact_root is None:
            raise BoundaryWitnessError("PARI ECPP verification requires an artifact root")
        certificate = (artifact_root / evidence.certificate_path).resolve()
        root = artifact_root.resolve()
        try:
            certificate.relative_to(root)
        except ValueError as exc:
            raise BoundaryWitnessError("certificate path escapes the artifact root") from exc
        if not certificate.is_file():
            raise BoundaryWitnessError(f"missing prime certificate: {certificate}")
        if sha256_file(certificate) != evidence.certificate_sha256.lower():
            raise BoundaryWitnessError("prime certificate SHA-256 mismatch")
        if certificate_verifier is None:
            raise BoundaryWitnessError(
                "PARI ECPP certificate needs an independently invoked exact verifier"
            )
        return bool(certificate_verifier(evidence, artifact_root))

    raise BoundaryWitnessError(
        f"unsupported or non-proof primality method: {evidence.method!r}"
    )


def verify_boundary_witness(
    witness: BoundaryWitness,
    *,
    artifact_root: Path | None = None,
    certificate_verifier: PrimeCertificateVerifier | None = None,
) -> dict[str, object]:
    """Verify boundary geometry, prime proofs, and exhaustive composites."""

    issues: list[str] = []
    if witness.schema_version != SCHEMA_VERSION:
        issues.append("schema version mismatch")
    if not (2 <= witness.block_a < witness.block_b):
        issues.append("block must satisfy 2 <= a < b")
    if witness.threshold < 2:
        issues.append("threshold must be at least 2")
    if witness.internal_start_bounded_upper_bound < 0:
        issues.append("internal upper bound cannot be negative")

    p = witness.last_prime.value
    q = witness.right_prime.value
    if not (witness.block_a <= p < witness.block_b):
        issues.append("claimed last prime is outside [a,b)")
    if q < witness.block_b:
        issues.append("right witness prime must satisfy q >= b")
    if q <= p:
        issues.append("right witness prime must be greater than p")
    if q - p >= witness.threshold:
        issues.append("right boundary gap does not satisfy q-p < threshold")

    try:
        if not _verify_prime_evidence(
            witness.last_prime,
            artifact_root=artifact_root,
            certificate_verifier=certificate_verifier,
        ):
            issues.append("last-prime primality proof failed")
    except BoundaryWitnessError as exc:
        issues.append(f"last-prime evidence: {exc}")
    try:
        if not _verify_prime_evidence(
            witness.right_prime,
            artifact_root=artifact_root,
            certificate_verifier=certificate_verifier,
        ):
            issues.append("right-prime primality proof failed")
    except BoundaryWitnessError as exc:
        issues.append(f"right-prime evidence: {exc}")

    expected_values = set(range(p + 1, witness.block_b))
    observed_values: set[int] = set()
    for item in witness.composite_evidence:
        if item.value in observed_values:
            issues.append(f"duplicate composite evidence for {item.value}")
            continue
        observed_values.add(item.value)
        if item.value not in expected_values:
            issues.append(f"composite evidence outside required interval: {item.value}")
        if not (1 < item.factor < item.value):
            issues.append(f"nontrivial factor condition failed for {item.value}")
        elif item.value % item.factor:
            issues.append(f"claimed factor does not divide {item.value}")
    missing = sorted(expected_values.difference(observed_values))
    extra = sorted(observed_values.difference(expected_values))
    if missing:
        issues.append(f"composite coverage holes: {missing}")
    if extra:
        issues.append(f"composite coverage extras: {extra}")

    crossing_certified_small = not issues
    certified_zero = (
        crossing_certified_small
        and witness.internal_start_bounded_upper_bound == 0
    )
    return {
        "status": "PASS" if not issues else "FAIL",
        "schema_version": witness.schema_version,
        "block": {"a": str(witness.block_a), "b": str(witness.block_b)},
        "threshold": witness.threshold,
        "last_prime": str(p),
        "right_prime": str(q),
        "right_witness_distance": str(q - p),
        "composite_evidence_count": len(witness.composite_evidence),
        "expected_composite_count": max(0, witness.block_b - p - 1),
        "crossing_certified_small": crossing_certified_small,
        "internal_start_bounded_upper_bound": (
            witness.internal_start_bounded_upper_bound
        ),
        "certified_zero": certified_zero,
        "issues": issues,
        "probable_prime_accepted": False,
    }


def _smallest_factor(value: int) -> int:
    if value % 2 == 0:
        return 2
    divisor = 3
    while divisor <= math.isqrt(value):
        if value % divisor == 0:
            return divisor
        divisor += 2
    raise BoundaryWitnessError(f"no composite factor found for {value}")


def build_toy_witness(
    *,
    block_a: int = 100,
    block_b: int = 120,
    threshold: int = 20,
    internal_start_bounded_upper_bound: int = 0,
) -> BoundaryWitness:
    """Generate a deterministic small witness without external data or network."""

    primes = [value for value in range(block_a, block_b) if _is_prime_trial_division(value)]
    if not primes:
        raise BoundaryWitnessError("toy block must contain at least one prime")
    p = primes[-1]
    q = block_b
    while not _is_prime_trial_division(q):
        q += 1
    composites = tuple(
        CompositeEvidence(value=value, factor=_smallest_factor(value))
        for value in range(p + 1, block_b)
    )
    return BoundaryWitness(
        schema_version=SCHEMA_VERSION,
        block_a=block_a,
        block_b=block_b,
        threshold=threshold,
        internal_start_bounded_upper_bound=internal_start_bounded_upper_bound,
        last_prime=PrimeEvidence(p, "trial_division_exact"),
        right_prime=PrimeEvidence(q, "trial_division_exact"),
        composite_evidence=composites,
    )


def witness_to_dict(witness: BoundaryWitness) -> dict[str, object]:
    payload = asdict(witness)
    payload["composite_evidence"] = [asdict(item) for item in witness.composite_evidence]
    return payload


def witness_from_dict(payload: dict[str, object]) -> BoundaryWitness:
    try:
        last = dict(payload["last_prime"])  # type: ignore[arg-type]
        right = dict(payload["right_prime"])  # type: ignore[arg-type]
        composite = tuple(
            CompositeEvidence(value=int(item["value"]), factor=int(item["factor"]))
            for item in payload["composite_evidence"]  # type: ignore[union-attr]
        )
        return BoundaryWitness(
            schema_version=str(payload["schema_version"]),
            block_a=int(payload["block_a"]),
            block_b=int(payload["block_b"]),
            threshold=int(payload["threshold"]),
            internal_start_bounded_upper_bound=int(
                payload["internal_start_bounded_upper_bound"]
            ),
            last_prime=PrimeEvidence(
                value=int(last["value"]),
                method=str(last["method"]),
                certificate_path=(
                    None if last.get("certificate_path") is None else str(last["certificate_path"])
                ),
                certificate_sha256=(
                    None if last.get("certificate_sha256") is None else str(last["certificate_sha256"])
                ),
            ),
            right_prime=PrimeEvidence(
                value=int(right["value"]),
                method=str(right["method"]),
                certificate_path=(
                    None if right.get("certificate_path") is None else str(right["certificate_path"])
                ),
                certificate_sha256=(
                    None if right.get("certificate_sha256") is None else str(right["certificate_sha256"])
                ),
            ),
            composite_evidence=composite,
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise BoundaryWitnessError(f"malformed witness payload: {exc}") from exc


def _write_json_exclusive(path: Path, payload: object) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def run_toy_witness(output_directory: Path) -> dict[str, object]:
    """Create non-overwriting toy artifacts and immediately verify them."""

    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite result: {output_directory}")
    witness = build_toy_witness()
    report = verify_boundary_witness(witness)
    if report["status"] != "PASS" or not report["certified_zero"]:
        raise BoundaryWitnessError("internally generated toy witness did not verify")

    output_directory.mkdir(parents=True)
    witness_path = output_directory / "boundary_witness.json"
    composite_path = output_directory / "composite_evidence.csv"
    report_path = output_directory / "verification_report.json"
    _write_json_exclusive(witness_path, witness_to_dict(witness))
    with composite_path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("value", "factor"))
        writer.writeheader()
        writer.writerows(asdict(item) for item in witness.composite_evidence)
    _write_json_exclusive(report_path, report)
    artifacts = {
        path.name: sha256_file(path)
        for path in (witness_path, composite_path, report_path)
    }
    _write_json_exclusive(
        output_directory / "manifest.json",
        {
            "status": "PASS",
            "mode": "toy-boundary-witness",
            "schema_version": SCHEMA_VERSION,
            "artifacts_sha256": artifacts,
            "actual_1e20_experiment_executed": False,
            "network_used": False,
            "gpu_used": False,
        },
    )
    return report


def verify_saved_toy_result(output_directory: Path) -> dict[str, object]:
    manifest = json.loads((output_directory / "manifest.json").read_text(encoding="utf-8"))
    issues: list[str] = []
    if manifest.get("mode") != "toy-boundary-witness":
        issues.append("unexpected manifest mode")
    artifacts = manifest.get("artifacts_sha256")
    if not isinstance(artifacts, dict):
        issues.append("manifest lacks artifact hashes")
        artifacts = {}
    for name, expected in artifacts.items():
        path = output_directory / str(name)
        if not path.is_file():
            issues.append(f"missing artifact: {name}")
        elif sha256_file(path) != expected:
            issues.append(f"artifact hash mismatch: {name}")
    try:
        payload = json.loads(
            (output_directory / "boundary_witness.json").read_text(encoding="utf-8")
        )
        witness = witness_from_dict(payload)
        recomputed = verify_boundary_witness(witness)
        if recomputed["status"] != "PASS" or not recomputed["certified_zero"]:
            issues.append("saved witness exact recomputation failed")
        with (output_directory / "composite_evidence.csv").open(
            "r", encoding="utf-8", newline=""
        ) as handle:
            csv_rows = tuple(
                CompositeEvidence(value=int(row["value"]), factor=int(row["factor"]))
                for row in csv.DictReader(handle)
            )
        if csv_rows != witness.composite_evidence:
            issues.append("composite CSV and witness JSON disagree")
    except Exception as exc:
        issues.append(f"saved witness read failed: {type(exc).__name__}: {exc}")
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "actual_1e20_experiment_executed": False,
    }


__all__ = [
    "BoundaryWitness",
    "BoundaryWitnessError",
    "CompositeEvidence",
    "PrimeEvidence",
    "SCHEMA_VERSION",
    "TOY_TRIAL_DIVISION_LIMIT",
    "build_toy_witness",
    "run_toy_witness",
    "verify_boundary_witness",
    "verify_saved_toy_result",
    "witness_from_dict",
    "witness_to_dict",
]
