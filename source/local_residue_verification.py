"""Independent arithmetic and artifact verifier for P008 saved results."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

from source.finite_gap_certificate import read_certificate, unit_residues


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _optional_int(value: str) -> int | None:
    value = value.strip()
    return None if value == "" else int(value)


def _parse_metadata(path: Path) -> tuple[dict[str, str], list[str]]:
    values: dict[str, str] = {}
    issues: list[str] = []
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            issues.append(f"malformed metadata line {line_number}")
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key or key in values:
            issues.append(f"empty or duplicate metadata key on line {line_number}")
            continue
        values[key] = value.strip()
    return values, issues


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


def verify_result_core(output_directory: Path) -> dict[str, object]:
    issues: list[str] = []
    summary = json.loads(
        (output_directory / "summary.json").read_text(encoding="utf-8")
    )
    metadata_path = output_directory / "input_count_metadata.txt"
    counts_path = output_directory / "input_prime_counts.csv"
    if summary.get("mode") == "full":
        if not metadata_path.is_file():
            issues.append("full result lacks input_count_metadata.txt")
        else:
            metadata, metadata_issues = _parse_metadata(metadata_path)
            issues.extend(metadata_issues)
            required_values = {
                "status": "PRIMECOUNTS_READY",
                "algorithms": "gourdon,deleglise-rivat",
                "algorithm_outputs_must_match": "true",
                "gpu_used": "false",
                "actual_prime_gap_search": "false",
                "bound_calculator": "Windows_FGKMT_Python_in_separate_step",
            }
            for key, expected in required_values.items():
                if metadata.get(key) != expected:
                    issues.append(f"metadata {key} contract differs")
            if metadata.get("counts_sha256", "").lower() != _sha256(counts_path):
                issues.append("metadata counts_sha256 differs from copied CSV")
            try:
                threads = int(metadata["threads"])
                memory_limit = int(metadata["virtual_memory_limit_kib"])
            except (KeyError, ValueError):
                issues.append("metadata threads or memory limit is invalid")
            else:
                if not 1 <= threads <= 8:
                    issues.append("metadata thread limit exceeds contract")
                if not 0 < memory_limit <= 31_457_280:
                    issues.append("metadata memory limit is outside (0, 30 GiB]")
            if not metadata.get("primecount_version"):
                issues.append("metadata primecount_version is empty")
    certificate = read_certificate(output_directory / "input_certificate.txt")
    residues = unit_residues(certificate.modulus)
    residue_index = {value: index for index, value in enumerate(residues)}
    with counts_path.open(
        "r", encoding="utf-8", newline=""
    ) as handle:
        inputs = {row["block_id"]: row for row in csv.DictReader(handle)}
    with (output_directory / "local_block_bounds.csv").open(
        "r", encoding="utf-8", newline=""
    ) as handle:
        bounds = list(csv.DictReader(handle))

    if len(inputs) != len(bounds):
        issues.append("input and bound row counts differ")
    if summary.get("mode") == "full":
        full_x = 100_000_000_000_000_000_000
        lengths = (1_000, 1_000_000, 1_000_000_000, 1_000_000_000_000)
        expected_grid = {
            (f"x1e20_L{length}", str(full_x), str(full_x + length))
            for length in lengths
        }
        observed_grid = {
            (row["block_id"], row["a"], row["b"]) for row in inputs.values()
        }
        if observed_grid != expected_grid or len(inputs) != len(expected_grid):
            issues.append("full result grid differs from fixed phase-A grid")
        for block_id, row in inputs.items():
            if row["count_provenance"] != (
                "primecount_gourdon_deleglise_rivat_match"
            ):
                issues.append(f"{block_id} lacks dual-primecount provenance")
            if any(
                row[field].strip()
                for field in (
                    "first_prime",
                    "last_prime",
                    "right_boundary_gap",
                    "actual_large_gap_count",
                )
            ):
                issues.append(f"{block_id} improperly claims phase-A endpoint data")
    toy_prime_cache: list[int] | None = None
    for row in bounds:
        block_id = row["block_id"]
        source = inputs.get(block_id)
        if source is None:
            issues.append(f"missing input for block {block_id}")
            continue
        a = int(source["a"])
        b = int(source["b"])
        pi_a = int(source["pi_a_minus_1"])
        pi_b = int(source["pi_b_minus_1"])
        start_count = pi_b - pi_a
        internal_count = max(0, start_count - 1)
        first = _optional_int(source["first_prime"])
        last = _optional_int(source["last_prime"])
        boundary_gap = _optional_int(source["right_boundary_gap"])

        if source["count_provenance"] == "toy_exact_sieve":
            if toy_prime_cache is None:
                toy_prime_cache = _simple_primes(15000)
            starts = [prime for prime in toy_prime_cache if a <= prime < b]
            observed_pi_a = sum(prime < a for prime in toy_prime_cache)
            observed_pi_b = sum(prime < b for prime in toy_prime_cache)
            if (observed_pi_a, observed_pi_b) != (pi_a, pi_b):
                issues.append(f"toy prime counts differ for {block_id}")
            if starts and (starts[0], starts[-1]) != (first, last):
                issues.append(f"toy endpoint primes differ for {block_id}")
            if starts:
                position = toy_prime_cache.index(starts[-1])
                observed_gap = toy_prime_cache[position + 1] - starts[-1]
                if observed_gap != boundary_gap:
                    issues.append(f"toy boundary gap differs for {block_id}")

        if internal_count == 0:
            rational = Fraction(0)
            potential_contract = "NO_INTERNAL_GAP"
        elif first is not None and last is not None:
            first_index = residue_index[first % certificate.modulus]
            last_index = residue_index[last % certificate.modulus]
            rational = Fraction(
                certificate.lambda_num * (last - first)
                + certificate.mu_num * internal_count
                + certificate.phi_num[first_index]
                - certificate.phi_num[last_index],
                certificate.denominator,
            )
            potential_contract = "EXACT_ENDPOINT_STATES"
        else:
            rational = Fraction(
                certificate.lambda_num * (b - a)
                + certificate.mu_num * internal_count
                + 2 * certificate.t_num,
                certificate.denominator,
            )
            potential_contract = "WORST_CASE_2T"
        if internal_count > 0 and rational < 0:
            issues.append(
                f"{block_id} has a negative bound for a nonempty internal path"
            )
        floor_value = rational.numerator // rational.denominator
        internal_upper = min(internal_count, max(0, floor_value))
        if start_count == 0:
            allowance = 0
            boundary_status = "EMPTY_BLOCK"
        elif boundary_gap is None:
            allowance = 1
            boundary_status = "UNRESOLVED"
        elif boundary_gap >= certificate.threshold:
            allowance = 1
            boundary_status = "CERTIFIED_LARGE"
        else:
            allowance = 0
            boundary_status = "CERTIFIED_SMALL"
        total_upper = min(start_count, internal_upper + allowance)
        expected = {
            "start_prime_count": start_count,
            "internal_gap_count": internal_count,
            "raw_internal_bound_num": rational.numerator,
            "raw_internal_bound_den": rational.denominator,
            "raw_internal_floor": floor_value,
            "internal_integer_upper_bound": internal_upper,
            "potential_contract": potential_contract,
            "right_boundary_status": boundary_status,
            "right_boundary_allowance": allowance,
            "total_start_bounded_upper_bound": total_upper,
        }
        for field, value in expected.items():
            if str(row[field]) != str(value):
                issues.append(
                    f"{block_id} field {field}: saved={row[field]!r}, expected={value!r}"
                )
        if row["certified_zero"].lower() == "true" and not (
            total_upper == 0 and boundary_status != "UNRESOLVED"
        ):
            issues.append(f"{block_id} has an unsound zero-certificate flag")
        actual_text = source["actual_large_gap_count"].strip()
        if actual_text and int(actual_text) > total_upper:
            issues.append(f"{block_id} observed count exceeds upper bound")

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "recomputed_block_count": len(bounds),
        "verifier": "independent direct Fraction arithmetic",
    }


def verify_saved_result_independently(output_directory: Path) -> dict[str, object]:
    manifest_path = output_directory / "manifest.json"
    if not manifest_path.is_file():
        return {"status": "FAIL", "issues": ["manifest.json is missing"]}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    issues: list[str] = []
    for name, expected_hash in manifest.get("artifacts", {}).items():
        path = output_directory / name
        if not path.is_file():
            issues.append(f"missing artifact: {name}")
        elif _sha256(path) != expected_hash:
            issues.append(f"artifact hash mismatch: {name}")
    try:
        core = verify_result_core(output_directory)
        issues.extend(core["issues"])
    except Exception as exc:
        issues.append(f"independent recomputation raised {type(exc).__name__}: {exc}")
        core = {"recomputed_block_count": 0}
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "artifact_count": len(manifest.get("artifacts", {})),
        "recomputed_block_count": core["recomputed_block_count"],
        "direct_search_acceleration_proved": False,
    }
