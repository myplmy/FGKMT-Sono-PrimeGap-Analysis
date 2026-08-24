"""P008 block-local use of the P007 residue-state certificate.

The target count is start-bounded::

    N_{>=H}(A, B) = #{p in [A,B): nextprime(p) - p >= H}.

This module deliberately distinguishes gaps whose two endpoint primes start in
the block from the single possible gap that crosses the right boundary.  An
unresolved crossing is never converted into a zero certificate.
"""

from __future__ import annotations

import csv
import json
import math
import shutil
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence

import mpmath as mp

from source.finite_gap_certificate import (
    RationalCertificate,
    read_certificate,
    unit_residues,
    verify_certificate,
)
from source.provenance import require_experiment_approval, sha256_file


COUNT_FIELDS = (
    "block_id",
    "a",
    "b",
    "pi_a_minus_1",
    "pi_b_minus_1",
    "first_prime",
    "last_prime",
    "right_boundary_gap",
    "actual_large_gap_count",
    "count_provenance",
)

P008_FULL_X = 100_000_000_000_000_000_000
P008_FULL_LENGTHS = (1_000, 1_000_000, 1_000_000_000, 1_000_000_000_000)
P008_FULL_COUNT_PROVENANCE = "primecount_gourdon_deleglise_rivat_match"


class LocalCertificateError(ValueError):
    """Raised when a local input or claimed bound violates the proof contract."""


@dataclass(frozen=True)
class LocalBlockInput:
    block_id: str
    a: int
    b: int
    pi_a_minus_1: int
    pi_b_minus_1: int
    first_prime: int | None = None
    last_prime: int | None = None
    right_boundary_gap: int | None = None
    actual_large_gap_count: int | None = None
    count_provenance: str = "unspecified"

    @property
    def start_prime_count(self) -> int:
        return self.pi_b_minus_1 - self.pi_a_minus_1


def _floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def _fraction_decimal(value: Fraction, digits: int = 30) -> str:
    mp.mp.dps = max(50, digits + 10)
    return mp.nstr(mp.mpf(value.numerator) / value.denominator, digits)


def _optional_int(value: object) -> int | None:
    text = "" if value is None else str(value).strip()
    return None if text == "" else int(text)


def validate_prime_count_metadata(
    metadata_path: Path, counts_path: Path
) -> dict[str, str]:
    """Validate the WSL primecount handoff before any full analysis output exists."""

    values: dict[str, str] = {}
    for line_number, raw_line in enumerate(
        metadata_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise LocalCertificateError(
                f"malformed prime-count metadata line {line_number}: {raw_line!r}"
            )
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key or key in values:
            raise LocalCertificateError(
                f"empty or duplicate prime-count metadata key on line {line_number}"
            )
        values[key] = value

    required_values = {
        "status": "PRIMECOUNTS_READY",
        "algorithms": "gourdon,deleglise-rivat",
        "algorithm_outputs_must_match": "true",
        "gpu_used": "false",
        "actual_prime_gap_search": "false",
        "bound_calculator": "Windows_FGKMT_Python_in_separate_step",
    }
    for key, expected in required_values.items():
        if values.get(key) != expected:
            raise LocalCertificateError(
                f"prime-count metadata {key!r} must equal {expected!r}"
            )
    expected_hash = values.get("counts_sha256", "").lower()
    observed_hash = sha256_file(counts_path).lower()
    if len(expected_hash) != 64 or expected_hash != observed_hash:
        raise LocalCertificateError(
            "prime-count metadata counts_sha256 does not match the supplied CSV"
        )
    try:
        threads = int(values["threads"])
        memory_limit = int(values["virtual_memory_limit_kib"])
    except (KeyError, ValueError) as exc:
        raise LocalCertificateError(
            "prime-count metadata threads or memory limit is missing/invalid"
        ) from exc
    if not 1 <= threads <= 8:
        raise LocalCertificateError("prime-count metadata threads must be in [1, 8]")
    if not 0 < memory_limit <= 31_457_280:
        raise LocalCertificateError(
            "prime-count metadata virtual-memory limit must be in (0, 30 GiB]"
        )
    if not values.get("primecount_version"):
        raise LocalCertificateError("prime-count metadata lacks primecount_version")
    return values


def read_block_inputs(path: Path) -> list[LocalBlockInput]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != COUNT_FIELDS:
            raise LocalCertificateError(
                f"count CSV schema mismatch: {reader.fieldnames!r}"
            )
        rows = [
            LocalBlockInput(
                block_id=row["block_id"].strip(),
                a=int(row["a"]),
                b=int(row["b"]),
                pi_a_minus_1=int(row["pi_a_minus_1"]),
                pi_b_minus_1=int(row["pi_b_minus_1"]),
                first_prime=_optional_int(row["first_prime"]),
                last_prime=_optional_int(row["last_prime"]),
                right_boundary_gap=_optional_int(row["right_boundary_gap"]),
                actual_large_gap_count=_optional_int(row["actual_large_gap_count"]),
                count_provenance=row["count_provenance"].strip(),
            )
            for row in reader
        ]
    if not rows:
        raise LocalCertificateError("count CSV is empty")
    if len({row.block_id for row in rows}) != len(rows):
        raise LocalCertificateError("block_id values must be unique")
    return rows


def write_block_inputs(path: Path, rows: Sequence[LocalBlockInput]) -> None:
    with path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COUNT_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    field: "" if getattr(row, field) is None else getattr(row, field)
                    for field in COUNT_FIELDS
                }
            )


def validate_full_phase_a_inputs(rows: Sequence[LocalBlockInput]) -> None:
    """Refuse a partial or substituted grid being labelled as P008 phase-A full."""

    expected = {
        (f"x1e20_L{length}", P008_FULL_X, P008_FULL_X + length)
        for length in P008_FULL_LENGTHS
    }
    observed = {(row.block_id, row.a, row.b) for row in rows}
    if observed != expected or len(rows) != len(expected):
        raise LocalCertificateError("full phase-A count CSV does not match its fixed grid")
    for row in rows:
        if row.count_provenance != P008_FULL_COUNT_PROVENANCE:
            raise LocalCertificateError(
                "full phase-A row lacks dual-primecount provenance"
            )
        if any(
            value is not None
            for value in (
                row.first_prime,
                row.last_prime,
                row.right_boundary_gap,
                row.actual_large_gap_count,
            )
        ):
            raise LocalCertificateError(
                "phase-A prime-count input must not claim endpoint/search evidence"
            )


def validate_block_input(block: LocalBlockInput, certificate: RationalCertificate) -> None:
    if not block.block_id:
        raise LocalCertificateError("block_id must not be empty")
    if not (certificate.modulus < block.a < block.b):
        raise LocalCertificateError(
            "local certificate currently requires modulus < A < B"
        )
    if not (0 <= block.pi_a_minus_1 <= block.pi_b_minus_1):
        raise LocalCertificateError("prime counts must be nonnegative and ordered")
    count = block.start_prime_count
    if count == 0:
        if any(
            value is not None
            for value in (block.first_prime, block.last_prime, block.right_boundary_gap)
        ):
            raise LocalCertificateError("empty block must not declare endpoint primes")
    elif (block.first_prime is None) != (block.last_prime is None):
        raise LocalCertificateError("first_prime and last_prime must be supplied together")
    elif block.first_prime is not None:
        if not (block.a <= block.first_prime <= block.last_prime < block.b):
            raise LocalCertificateError("endpoint primes do not lie in [A,B)")
        if count == 1 and block.first_prime != block.last_prime:
            raise LocalCertificateError("a one-prime block must have equal endpoints")
        if count >= 2 and block.first_prime >= block.last_prime:
            raise LocalCertificateError("a multi-prime block needs increasing endpoints")
        if math.gcd(block.first_prime, certificate.modulus) != 1 or math.gcd(
            block.last_prime, certificate.modulus
        ) != 1:
            raise LocalCertificateError("endpoint primes must be unit residues")
    if block.right_boundary_gap is not None:
        if block.last_prime is None or block.right_boundary_gap <= 0:
            raise LocalCertificateError(
                "right_boundary_gap requires a last prime and must be positive"
            )
    if block.actual_large_gap_count is not None and not (
        0 <= block.actual_large_gap_count <= count
    ):
        raise LocalCertificateError("actual count lies outside [0,start_prime_count]")


def evaluate_local_block(
    block: LocalBlockInput, certificate: RationalCertificate
) -> dict[str, object]:
    """Apply an exact P007 certificate to one block.

    The integer upper bound uses ``floor`` because an integer ``N`` satisfying
    ``N <= q`` also satisfies ``N <= floor(q)``.  P007's historic ``ceil`` is
    retained in a separate diagnostic field because it is safe but one unit
    weaker whenever the rational bound is non-integral.
    """

    validate_block_input(block, certificate)
    start_count = block.start_prime_count
    internal_gap_count = max(0, start_count - 1)
    residues = unit_residues(certificate.modulus)
    residue_index = {value: index for index, value in enumerate(residues)}

    if internal_gap_count == 0:
        span_term = 0
        potential_term = 0
        potential_contract = "NO_INTERNAL_GAP"
        rational_bound = Fraction(0)
        raw_floor = 0
        raw_ceil = 0
        internal_upper = 0
    else:
        if block.first_prime is not None and block.last_prime is not None:
            span_term = block.last_prime - block.first_prime
            first_index = residue_index[block.first_prime % certificate.modulus]
            last_index = residue_index[block.last_prime % certificate.modulus]
            potential_term = (
                certificate.phi_num[first_index] - certificate.phi_num[last_index]
            )
            potential_contract = "EXACT_ENDPOINT_STATES"
        else:
            span_term = block.b - block.a
            potential_term = 2 * certificate.t_num
            potential_contract = "WORST_CASE_2T"
        rational_bound = Fraction(
            certificate.lambda_num * span_term
            + certificate.mu_num * internal_gap_count
            + potential_term,
            certificate.denominator,
        )
        if rational_bound < 0:
            raise LocalCertificateError(
                "negative bound for a nonempty internal prime path; check counts/endpoints"
            )
        raw_floor = _floor_fraction(rational_bound)
        raw_ceil = -(-rational_bound.numerator // rational_bound.denominator)
        internal_upper = min(internal_gap_count, raw_floor)

    unknown_boundary_upper = min(
        start_count, internal_upper + (1 if start_count else 0)
    )
    if start_count == 0:
        crossing_allowance = 0
        boundary_status = "EMPTY_BLOCK"
    elif block.right_boundary_gap is None:
        crossing_allowance = 1
        boundary_status = "UNRESOLVED"
    elif block.right_boundary_gap >= certificate.threshold:
        crossing_allowance = 1
        boundary_status = "CERTIFIED_LARGE"
    else:
        crossing_allowance = 0
        boundary_status = "CERTIFIED_SMALL"

    total_upper = min(start_count, internal_upper + crossing_allowance)
    certified_zero = total_upper == 0 and boundary_status != "UNRESOLVED"
    if block.actual_large_gap_count is not None and block.actual_large_gap_count > total_upper:
        raise LocalCertificateError("observed toy count exceeds certified upper bound")

    mp.mp.dps = 60
    b_mp = mp.mpf(block.b)
    local_scale = (
        mp.mpf(block.b - block.a)
        / mp.log(b_mp)
        * mp.exp(-mp.mpf(certificate.threshold) / mp.log(b_mp))
    )
    c_local = mp.mpf(total_upper) / local_scale if local_scale else mp.inf
    return {
        "block_id": block.block_id,
        "a": str(block.a),
        "b": str(block.b),
        "length": str(block.b - block.a),
        "pi_a_minus_1": str(block.pi_a_minus_1),
        "pi_b_minus_1": str(block.pi_b_minus_1),
        "start_prime_count": str(start_count),
        "internal_gap_count": str(internal_gap_count),
        "span_term": str(span_term),
        "potential_term_num": str(potential_term),
        "potential_contract": potential_contract,
        "raw_internal_bound_num": str(rational_bound.numerator),
        "raw_internal_bound_den": str(rational_bound.denominator),
        "raw_internal_bound_decimal": _fraction_decimal(rational_bound),
        "raw_internal_floor": str(raw_floor),
        "historic_conservative_ceil": str(raw_ceil),
        "internal_integer_upper_bound": str(internal_upper),
        "right_boundary_status": boundary_status,
        "right_boundary_allowance": str(crossing_allowance),
        "unknown_boundary_total_upper_bound": str(unknown_boundary_upper),
        "total_start_bounded_upper_bound": str(total_upper),
        "certified_zero": certified_zero,
        "actual_large_gap_count": (
            "" if block.actual_large_gap_count is None else str(block.actual_large_gap_count)
        ),
        "count_provenance": block.count_provenance,
        "heuristic_local_scale": mp.nstr(local_scale, 30),
        "heuristic_C_local": mp.nstr(c_local, 30),
        "C_is_not_rigorous_claim": True,
        "direct_search_acceleration_proved": False,
    }


def verify_coverage_ledger(
    entries: Sequence[dict[str, object]], *, a: int, b: int
) -> dict[str, object]:
    """Check partition geometry and evidence requirements for a future ledger."""

    issues: list[str] = []
    cursor = a
    allowed = {
        "CERTIFIED_ZERO",
        "CANDIDATE_COVER",
        "EXACT_SEARCHED",
        "COUNTEREXAMPLE_FOUND",
    }
    for index, entry in enumerate(entries):
        left = int(entry["a"])
        right = int(entry["b"])
        status = str(entry["status"])
        if left != cursor:
            issues.append(f"entry {index} begins at {left}, expected {cursor}")
        if right <= left:
            issues.append(f"entry {index} has a nonpositive interval")
        if status not in allowed:
            issues.append(f"entry {index} has unknown status {status}")
        if status == "CERTIFIED_ZERO" and not entry.get("certificate_sha256"):
            issues.append(f"entry {index} lacks a zero-certificate hash")
        if status in {"CANDIDATE_COVER", "EXACT_SEARCHED"} and not entry.get(
            "artifact_sha256"
        ):
            issues.append(f"entry {index} lacks a survivor/search artifact hash")
        cursor = right
    if cursor != b:
        issues.append(f"ledger ends at {cursor}, expected {b}")
    return {
        "status": "PASS" if not issues else "FAIL",
        "range": {"a": str(a), "b": str(b)},
        "entry_count": len(entries),
        "issues": issues,
    }


def _simple_primes(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                ((limit - start) // prime) + 1
            )
    return [value for value, is_prime in enumerate(sieve) if is_prime]


def toy_block_inputs(threshold: int) -> list[LocalBlockInput]:
    intervals = ((3000, 4000), (4000, 5500), (5500, 8000), (8000, 12000))
    primes = _simple_primes(max(right for _, right in intervals) + threshold + 100)
    rows: list[LocalBlockInput] = []
    for index, (a, b) in enumerate(intervals, start=1):
        starts = [prime for prime in primes if a <= prime < b]
        pi_a_minus_1 = sum(prime < a for prime in primes)
        pi_b_minus_1 = sum(prime < b for prime in primes)
        first = starts[0] if starts else None
        last = starts[-1] if starts else None
        boundary_gap = None
        actual = 0
        if starts:
            last_position = primes.index(last)
            boundary_gap = primes[last_position + 1] - last
            for prime in starts:
                position = primes.index(prime)
                if primes[position + 1] - prime >= threshold:
                    actual += 1
        rows.append(
            LocalBlockInput(
                block_id=f"toy_{index:02d}",
                a=a,
                b=b,
                pi_a_minus_1=pi_a_minus_1,
                pi_b_minus_1=pi_b_minus_1,
                first_prime=first,
                last_prime=last,
                right_boundary_gap=boundary_gap,
                actual_large_gap_count=actual,
                count_provenance="toy_exact_sieve",
            )
        )
    return rows


def _write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_bounds(path: Path, rows: Sequence[dict[str, object]]) -> None:
    if not rows:
        raise LocalCertificateError("no local bounds to write")
    with path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_manifest(output_directory: Path, artifact_names: Iterable[str]) -> None:
    artifacts = {
        name: sha256_file(output_directory / name) for name in sorted(artifact_names)
    }
    _write_json(
        output_directory / "manifest.json",
        {
            "status": "PASS",
            "experiment": "P008_LOCAL_RESIDUE_STATE_CERTIFICATE",
            "artifacts": artifacts,
            "direct_prime_search_executed": False,
            "direct_search_acceleration_proved": False,
            "gpu_used": False,
        },
    )


def run_local_experiment(
    certificate_path: Path,
    output_directory: Path,
    *,
    mode: str,
    approval_token: str | None,
    counts_path: Path | None = None,
    count_metadata_path: Path | None = None,
) -> dict[str, object]:
    require_experiment_approval(approval_token)
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite {output_directory}")
    if mode not in {"pilot", "full"}:
        raise ValueError(f"unknown P008 mode: {mode}")
    certificate = read_certificate(certificate_path)
    certificate_report = verify_certificate(certificate)
    if mode == "pilot":
        inputs = toy_block_inputs(certificate.threshold)
    else:
        if counts_path is None or count_metadata_path is None:
            raise LocalCertificateError("full mode requires counts and metadata paths")
        validate_prime_count_metadata(count_metadata_path, counts_path)
        inputs = read_block_inputs(counts_path)
        validate_full_phase_a_inputs(inputs)

    output_directory.mkdir(parents=True)
    copied_certificate = output_directory / "input_certificate.txt"
    shutil.copyfile(certificate_path, copied_certificate)
    copied_counts = output_directory / "input_prime_counts.csv"
    if mode == "pilot":
        write_block_inputs(copied_counts, inputs)
    else:
        shutil.copyfile(counts_path, copied_counts)
    artifacts = ["input_certificate.txt", "input_prime_counts.csv"]
    if count_metadata_path is not None:
        shutil.copyfile(count_metadata_path, output_directory / "input_count_metadata.txt")
        artifacts.append("input_count_metadata.txt")

    bounds = [evaluate_local_block(block, certificate) for block in inputs]
    bounds_path = output_directory / "local_block_bounds.csv"
    _write_bounds(bounds_path, bounds)
    artifacts.append("local_block_bounds.csv")

    certified_zero_count = sum(bool(row["certified_zero"]) for row in bounds)
    internal_zero_count = sum(
        int(row["internal_integer_upper_bound"]) == 0 for row in bounds
    )
    unresolved_count = sum(row["right_boundary_status"] == "UNRESOLVED" for row in bounds)
    summary = {
        "status": "PASS",
        "experiment": "P008_LOCAL_RESIDUE_STATE_CERTIFICATE",
        "mode": mode,
        "certificate_sha256": sha256_file(certificate_path),
        "certificate_global_audit_status": certificate_report["status"],
        "threshold": certificate.threshold,
        "modulus": certificate.modulus,
        "block_count": len(bounds),
        "internal_zero_candidate_count": internal_zero_count,
        "certified_zero_count": certified_zero_count,
        "unresolved_right_boundary_count": unresolved_count,
        "representative_blocks_are_not_a_coverage_ledger": True,
        "direct_prime_search_executed": False,
        "direct_search_acceleration_proved": False,
        "historic_P007_ceil_is_safe_but_local_floor_is_tighter": True,
        "gpu_used": False,
    }
    _write_json(output_directory / "summary.json", summary)
    artifacts.append("summary.json")

    from source.local_residue_verification import verify_result_core

    verification = verify_result_core(output_directory)
    if verification["status"] != "PASS":
        raise LocalCertificateError(f"independent verification failed: {verification}")
    _write_json(output_directory / "verification_report.json", verification)
    artifacts.append("verification_report.json")
    _write_manifest(output_directory, artifacts)
    return summary


def verify_saved_result(output_directory: Path) -> dict[str, object]:
    from source.local_residue_verification import verify_saved_result_independently

    return verify_saved_result_independently(output_directory)
