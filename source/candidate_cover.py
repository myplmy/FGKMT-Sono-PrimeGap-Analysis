"""Exact finite candidate-cover verifier for the P010B acceleration gate.

The verifier implements the finite coverage and rejection lemmas recorded in
``docs/method/theory/10_coverage_preserving_compression_정식화.md``.  It does
not turn the P010A count upper bound into absolute positions.  The bundled toy
generator deliberately uses exhaustive primality knowledge and is therefore a
verifier fixture, not a search acceleration algorithm.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from pathlib import Path

from source.provenance import sha256_file


EXPERIMENT = "P010B_EXACT_CANDIDATE_COVER_GATE"
SCHEMA_VERSION = "p010b-candidate-cover-v1"
MAX_DIRECT_UNIVERSE = 1_000_000
MAX_TRIAL_PRIME = 10_000_000
MAX_DISK_BYTES = 50_000_000_000
MIN_BENCHMARK_RUNS = 5
MIN_SPEEDUP_FACTOR = 1.05


class CandidateCoverError(ValueError):
    """Raised when a candidate-cover ledger is malformed or unsound."""


def _parse_exact_integer(value: object, field: str) -> int:
    """Parse an integer without accepting bools, floats, or noncanonical text."""

    if isinstance(value, bool):
        raise CandidateCoverError(f"{field} must not be a boolean")
    if isinstance(value, int):
        return value
    if not isinstance(value, str) or not value:
        raise CandidateCoverError(f"{field} must be an integer or decimal string")
    negative = value.startswith("-")
    digits = value[1:] if negative else value
    if (
        not digits.isascii()
        or not digits.isdecimal()
        or (len(digits) > 1 and digits.startswith("0"))
    ):
        raise CandidateCoverError(f"{field} is not a canonical decimal integer")
    if negative and digits == "0":
        raise CandidateCoverError(f"{field} must not use negative zero")
    return int(value)


def _canonical_bytes(payload: object) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _write_json_exclusive(path: Path, payload: object) -> None:
    with path.open("xb") as handle:
        handle.write(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode(
                "utf-8"
            )
            + b"\n"
        )


def smallest_factor(value: int) -> int | None:
    """Return an exact nontrivial factor, or ``None`` when value is prime."""

    if value < 2:
        raise ValueError("primality domain starts at 2")
    if value % 2 == 0:
        return None if value == 2 else 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return divisor
        divisor += 2
    return None


def is_prime_exact_small(value: int) -> bool:
    if value > MAX_TRIAL_PRIME:
        raise CandidateCoverError(
            "trial-division prime witness exceeds the reviewed toy bound"
        )
    return value >= 2 and smallest_factor(value) is None


def next_prime_exact_small(value: int) -> int:
    candidate = max(2, value + 1)
    if candidate > 2 and candidate % 2 == 0:
        candidate += 1
    while candidate <= MAX_TRIAL_PRIME:
        if is_prime_exact_small(candidate):
            return candidate
        candidate += 1 if candidate == 2 else 2
    raise CandidateCoverError("next prime exceeds the reviewed toy bound")


def dangerous_starts_exact_small(a: int, b: int, threshold: int) -> list[int]:
    if not (2 <= a < b and threshold >= 2):
        raise ValueError("require 2 <= a < b and threshold >= 2")
    if b - a > MAX_DIRECT_UNIVERSE:
        raise CandidateCoverError("direct toy universe exceeds the safety bound")
    dangerous: list[int] = []
    for start in range(a, b):
        if is_prime_exact_small(start):
            following = next_prime_exact_small(start)
            if following - start >= threshold:
                dangerous.append(start)
    return dangerous


def build_exhaustive_toy_ledger(a: int, b: int, threshold: int) -> dict[str, object]:
    """Build a sound toy ledger using a deliberately circular exhaustive oracle."""

    if not (2 <= a < b and threshold >= 2):
        raise ValueError("require 2 <= a < b and threshold >= 2")
    if b - a > MAX_DIRECT_UNIVERSE:
        raise CandidateCoverError("direct toy universe exceeds the safety bound")
    candidates: list[int] = []
    witnesses: list[dict[str, object]] = []
    for start in range(a, b):
        factor = smallest_factor(start)
        if factor is not None:
            witnesses.append(
                {
                    "start": str(start),
                    "type": "COMPOSITE_FACTOR",
                    "factor": str(factor),
                }
            )
            continue
        following = next_prime_exact_small(start)
        if following - start < threshold:
            witnesses.append(
                {
                    "start": str(start),
                    "type": "WINDOW_PRIME",
                    "prime": str(following),
                    "proof_kind": "EXACT_TRIAL_DIVISION_TO_SQRT",
                }
            )
        else:
            candidates.append(start)
    return {
        "schema_version": SCHEMA_VERSION,
        "range": {"a": str(a), "b": str(b)},
        "threshold": str(threshold),
        "candidate_starts": [str(value) for value in candidates],
        "rejection_witnesses": witnesses,
        "generator": {
            "name": "exhaustive_toy_oracle",
            "uses_exhaustive_oracle": True,
            "eligible_for_acceleration_claim": False,
        },
        "theorem_claimed": False,
    }


def verify_candidate_cover(ledger: dict[str, object]) -> dict[str, object]:
    issues: list[str] = []
    try:
        range_payload = ledger["range"]
        if not isinstance(range_payload, dict):
            raise CandidateCoverError("range must be an object")
        a = _parse_exact_integer(range_payload["a"], "range.a")
        b = _parse_exact_integer(range_payload["b"], "range.b")
        threshold = _parse_exact_integer(ledger["threshold"], "threshold")
        if not (2 <= a < b and threshold >= 2):
            raise CandidateCoverError("require 2 <= a < b and threshold >= 2")
        universe_size = b - a
        if universe_size > MAX_DIRECT_UNIVERSE:
            raise CandidateCoverError("direct coverage verification exceeds safety bound")

        raw_candidates = ledger.get("candidate_starts")
        raw_witnesses = ledger.get("rejection_witnesses")
        if not isinstance(raw_candidates, list) or not isinstance(raw_witnesses, list):
            raise CandidateCoverError("candidate and witness collections must be lists")
        candidates = [
            _parse_exact_integer(value, f"candidate_starts[{index}]")
            for index, value in enumerate(raw_candidates)
        ]
        if candidates != sorted(set(candidates)):
            issues.append("candidate starts must be unique and sorted")
        if any(value < a or value >= b for value in candidates):
            issues.append("candidate start lies outside the half-open universe")
        candidate_set = set(candidates)

        witnessed: set[int] = set()
        witness_sound = True
        composite_count = 0
        window_prime_count = 0
        for index, raw in enumerate(raw_witnesses):
            if not isinstance(raw, dict):
                issues.append(f"witness {index} is not an object")
                continue
            try:
                start = _parse_exact_integer(raw["start"], f"witness {index} start")
                kind = str(raw["type"])
            except Exception:
                issues.append(f"witness {index} lacks an exact start or type")
                witness_sound = False
                continue
            if start < a or start >= b:
                issues.append(f"witness {index} start lies outside the universe")
                witness_sound = False
            if start in candidate_set:
                issues.append(f"start {start} is both candidate and rejected")
                witness_sound = False
            if start in witnessed:
                issues.append(f"start {start} has duplicate rejection witnesses")
                witness_sound = False
            witnessed.add(start)
            if kind == "COMPOSITE_FACTOR":
                try:
                    factor = _parse_exact_integer(
                        raw["factor"], f"witness {index} factor"
                    )
                except Exception:
                    issues.append(f"witness {index} lacks an exact factor")
                    witness_sound = False
                    continue
                if not (1 < factor < start and start % factor == 0):
                    issues.append(f"witness {index} has an invalid composite factor")
                    witness_sound = False
                composite_count += 1
            elif kind == "WINDOW_PRIME":
                try:
                    prime = _parse_exact_integer(
                        raw["prime"], f"witness {index} prime"
                    )
                except Exception:
                    issues.append(f"witness {index} lacks an exact prime")
                    witness_sound = False
                    continue
                if raw.get("proof_kind") != "EXACT_TRIAL_DIVISION_TO_SQRT":
                    issues.append(f"witness {index} has an unsupported prime proof")
                    witness_sound = False
                try:
                    prime_valid = is_prime_exact_small(prime)
                except Exception as exc:
                    issues.append(f"witness {index} prime verification failed: {exc}")
                    prime_valid = False
                    witness_sound = False
                if not prime_valid:
                    issues.append(f"witness {index} prime is not exact-prime verified")
                    witness_sound = False
                if not start < prime < start + threshold:
                    issues.append(
                        f"witness {index} prime is outside the strict rejection window"
                    )
                    witness_sound = False
                window_prime_count += 1
            else:
                issues.append(f"witness {index} has unknown type {kind}")
                witness_sound = False

        expected_rejected = set(range(a, b)) - candidate_set
        missing = sorted(expected_rejected - witnessed)
        extras = sorted(witnessed - expected_rejected)
        if missing:
            issues.append(f"candidate cover has {len(missing)} uncovered starts")
        if extras:
            issues.append(f"candidate cover has {len(extras)} extraneous witnesses")
            witness_sound = False
        generator = ledger.get("generator")
        if not isinstance(generator, dict) or not isinstance(
            generator.get("uses_exhaustive_oracle"), bool
        ):
            issues.append("ledger lacks an explicit generator-oracle declaration")
            uses_exhaustive: bool | None = None
        else:
            uses_exhaustive = bool(generator["uses_exhaustive_oracle"])
        serialized_bytes = len(_canonical_bytes(ledger))
        return {
            "status": "PASS" if not issues else "FAIL",
            "issues": issues,
            "range": {"a": str(a), "b": str(b)},
            "threshold": str(threshold),
            "universe_size": universe_size,
            "candidate_count": len(candidate_set),
            "rejected_count": len(witnessed),
            "composite_factor_witness_count": composite_count,
            "window_prime_witness_count": window_prime_count,
            "coverage_complete": not missing and not extras,
            "sound_rejections": witness_sound,
            "ledger_serialized_bytes": serialized_bytes,
            "generator_uses_exhaustive_oracle": uses_exhaustive,
            "acceleration_proved": False,
            "theorem_claimed": False,
        }
    except Exception as exc:
        issues.append(f"candidate-cover verification failed: {type(exc).__name__}: {exc}")
        return {
            "status": "FAIL",
            "issues": issues,
            "coverage_complete": False,
            "sound_rejections": False,
            "acceleration_proved": False,
            "theorem_claimed": False,
        }


def evaluate_break_even(
    verification: dict[str, object], benchmark: dict[str, object]
) -> dict[str, object]:
    issues: list[str] = []
    if verification.get("status") != "PASS":
        issues.append("candidate-cover verification is not PASS")
    if verification.get("generator_uses_exhaustive_oracle") is not False:
        issues.append("candidate generator is circular or its oracle use is undeclared")
    try:
        runs = _parse_exact_integer(benchmark["run_count"], "benchmark run_count")
        baseline = float(benchmark["baseline_median_seconds"])
        generate = float(benchmark["candidate_generate_median_seconds"])
        verify = float(benchmark["candidate_verify_median_seconds"])
        survivor = float(benchmark["survivor_search_median_seconds"])
        disk_bytes = _parse_exact_integer(
            benchmark["artifact_bytes"], "benchmark artifact_bytes"
        )
        false_negatives = _parse_exact_integer(
            benchmark["false_negative_count"], "benchmark false_negative_count"
        )
        same_range = benchmark.get("same_range_and_threshold") is True
        same_cpu = bool(str(benchmark.get("cpu_id", "")).strip())
        hashes_present = all(
            bool(str(benchmark.get(field, "")).strip())
            for field in ("baseline_code_sha256", "candidate_code_sha256")
        )
        if runs < MIN_BENCHMARK_RUNS:
            issues.append(f"benchmark needs at least {MIN_BENCHMARK_RUNS} runs")
        if not all(math.isfinite(value) for value in (baseline, generate, verify, survivor)):
            issues.append("benchmark times must be finite")
        if not (baseline > 0 and generate >= 0 and verify >= 0 and survivor >= 0):
            issues.append("benchmark times must be finite and nonnegative")
        if disk_bytes < 0 or disk_bytes > MAX_DISK_BYTES:
            issues.append("artifact bytes exceed the 50 GB P010B cap")
        if false_negatives != 0:
            issues.append("candidate method has false negatives")
        if not same_range:
            issues.append("baseline and candidate method use different range/threshold")
        if not same_cpu:
            issues.append("benchmark lacks a fixed CPU identifier")
        if not hashes_present:
            issues.append("benchmark lacks baseline or candidate code hash")
        candidate_total = generate + verify + survivor
        if candidate_total <= 0:
            issues.append("candidate total time must be positive")
        speedup = baseline / candidate_total if candidate_total > 0 else math.nan
        if speedup < MIN_SPEEDUP_FACTOR:
            issues.append(
                f"measured speedup {speedup:.6g} is below {MIN_SPEEDUP_FACTOR:.2f}"
            )
    except Exception as exc:
        issues.append(f"break-even metadata is incomplete: {type(exc).__name__}: {exc}")
        baseline = math.nan
        candidate_total = math.nan
        speedup = math.nan
    return {
        "status": "ACCELERATION_CANDIDATE" if not issues else "BLOCKED",
        "issues": issues,
        "baseline_median_seconds": baseline,
        "candidate_total_median_seconds": candidate_total,
        "measured_speedup": speedup,
        "minimum_speedup_factor": MIN_SPEEDUP_FACTOR,
        "acceleration_proved": False,
        "independent_repeat_required": True,
        "theorem_claimed": False,
    }


def run_toy(output_directory: Path, *, a: int, b: int, threshold: int) -> dict[str, object]:
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite P010B toy result: {output_directory}")
    started = time.perf_counter()
    ledger_started = time.perf_counter()
    ledger = build_exhaustive_toy_ledger(a, b, threshold)
    generate_seconds = time.perf_counter() - ledger_started
    verify_started = time.perf_counter()
    verification = verify_candidate_cover(ledger)
    verify_seconds = time.perf_counter() - verify_started
    exact = dangerous_starts_exact_small(a, b, threshold)
    candidates = [int(value) for value in ledger["candidate_starts"]]
    if verification["status"] != "PASS" or candidates != exact:
        raise CandidateCoverError("toy ledger failed exact dangerous-start comparison")
    benchmark = {
        "run_count": 1,
        "baseline_median_seconds": max(generate_seconds, 1e-12),
        "candidate_generate_median_seconds": generate_seconds,
        "candidate_verify_median_seconds": verify_seconds,
        "survivor_search_median_seconds": 0.0,
        "artifact_bytes": len(_canonical_bytes(ledger)),
        "false_negative_count": 0,
        "same_range_and_threshold": True,
        "cpu_id": "TOY_NOT_A_BENCHMARK",
        "baseline_code_sha256": "toy",
        "candidate_code_sha256": "toy",
    }
    break_even = evaluate_break_even(verification, benchmark)
    output_directory.mkdir(parents=True)
    _write_json_exclusive(output_directory / "candidate_cover_ledger.json", ledger)
    _write_json_exclusive(output_directory / "verification_report.json", verification)
    _write_json_exclusive(output_directory / "break_even_report.json", break_even)
    summary = {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "schema_version": SCHEMA_VERSION,
        "range": {"a": str(a), "b": str(b)},
        "threshold": str(threshold),
        "candidate_count": len(candidates),
        "exact_dangerous_start_count": len(exact),
        "candidate_set_equals_exact_toy_truth": True,
        "generator_uses_exhaustive_oracle": True,
        "acceleration_status": break_even["status"],
        "acceleration_proved": False,
        "elapsed_seconds": time.perf_counter() - started,
        "theorem_claimed": False,
    }
    _write_json_exclusive(output_directory / "summary.json", summary)
    artifacts = sorted(path for path in output_directory.iterdir() if path.is_file())
    manifest = {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "schema_version": SCHEMA_VERSION,
        "artifacts_sha256": {path.name: sha256_file(path) for path in artifacts},
        "source_sha256": sha256_file(Path(__file__)),
        "actual_prime_search_executed": False,
        "acceleration_proved": False,
        "theorem_claimed": False,
    }
    _write_json_exclusive(output_directory / "manifest.json", manifest)
    return summary


def verify_saved_toy(output_directory: Path) -> dict[str, object]:
    issues: list[str] = []
    try:
        manifest_path = output_directory / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("source_sha256") != sha256_file(Path(__file__)):
            issues.append("current candidate-cover source hash differs from manifest")
        for relative, expected in manifest["artifacts_sha256"].items():
            path = output_directory / relative
            if not path.is_file() or sha256_file(path) != expected:
                issues.append(f"artifact missing/hash mismatch: {relative}")
        ledger = json.loads(
            (output_directory / "candidate_cover_ledger.json").read_text(
                encoding="utf-8"
            )
        )
        saved_verification = json.loads(
            (output_directory / "verification_report.json").read_text(encoding="utf-8")
        )
        recomputed = verify_candidate_cover(ledger)
        if recomputed != saved_verification:
            issues.append("saved candidate-cover verification differs from recomputation")
        summary = json.loads(
            (output_directory / "summary.json").read_text(encoding="utf-8")
        )
        if summary.get("acceleration_proved") is not False:
            issues.append("toy summary improperly claims acceleration")
    except Exception as exc:
        issues.append(f"saved P010B toy verification failed: {type(exc).__name__}: {exc}")
    manifest_path = output_directory / "manifest.json"
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "manifest_sha256": (
            hashlib.sha256(manifest_path.read_bytes()).hexdigest()
            if manifest_path.is_file()
            else None
        ),
        "actual_prime_search_executed": False,
        "acceleration_proved": False,
        "theorem_claimed": False,
    }


__all__ = [
    "CandidateCoverError",
    "EXPERIMENT",
    "build_exhaustive_toy_ledger",
    "dangerous_starts_exact_small",
    "evaluate_break_even",
    "is_prime_exact_small",
    "next_prime_exact_small",
    "run_toy",
    "smallest_factor",
    "verify_candidate_cover",
    "verify_saved_toy",
]
