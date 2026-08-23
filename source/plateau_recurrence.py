"""Exact finite-range maximal-gap plateau and recurrence reconstruction."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Iterator, Sequence

import numpy as np

from source.provenance import require_experiment_approval, sha256_file


KNOWN_PRIME_COUNTS = {
    100: 25,
    1_000: 168,
    10_000: 1_229,
    100_000: 9_592,
    1_000_000: 78_498,
    10_000_000: 664_579,
    100_000_000: 5_761_455,
    1_000_000_000: 50_847_534,
    10_000_000_000: 455_052_511,
}


@dataclass(frozen=True, slots=True)
class RecordReference:
    record_index: int
    start_prime: int
    gap: int
    end_prime: int
    source_commit: str
    verified_exhaustive_limit: int


@dataclass(slots=True)
class _PlateauAccumulator:
    record_index: int
    start_prime: int
    end_prime: int
    gap: int
    n_gap_starts: int = 1
    m_equal_gaps: int = 1

    def observe(self, gaps: np.ndarray) -> None:
        if gaps.size == 0:
            return
        self.n_gap_starts += int(gaps.size)
        self.m_equal_gaps += int(np.count_nonzero(gaps == self.gap))


@dataclass(frozen=True, slots=True)
class Reconstruction:
    records: list[dict[str, object]]
    complete_plateaus: list[dict[str, object]]
    right_censored_plateau: dict[str, object]
    gap_histogram: dict[int, int]
    prime_count: int
    gap_count: int
    last_prime: int


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _simple_primes(limit: int) -> np.ndarray:
    if limit < 2:
        return np.empty(0, dtype=np.int64)
    flags = np.ones(limit + 1, dtype=np.bool_)
    flags[:2] = False
    for prime in range(2, math.isqrt(limit) + 1):
        if flags[prime]:
            flags[prime * prime :: prime] = False
    return np.flatnonzero(flags).astype(np.int64, copy=False)


def iter_prime_chunks(limit: int, *, segment_span: int) -> Iterator[np.ndarray]:
    """Yield all primes ``<= limit`` in strictly increasing NumPy chunks."""

    if limit < 2:
        return
    if limit > np.iinfo(np.int64).max:
        raise ValueError("analysis limit exceeds signed 64-bit range")
    if segment_span < 10:
        raise ValueError("segment_span must be at least 10 integers")

    base_primes = _simple_primes(math.isqrt(limit))
    low = 3
    first = True
    while low <= limit:
        high = min(limit, low + segment_span - 1)
        if high % 2 == 0:
            high -= 1
        if high < low:
            break
        flags = np.ones(((high - low) // 2) + 1, dtype=np.bool_)
        for prime_value in base_primes[1:]:
            prime = int(prime_value)
            if prime * prime > high:
                break
            start = max(prime * prime, ((low + prime - 1) // prime) * prime)
            if start % 2 == 0:
                start += prime
            flags[(start - low) // 2 :: prime] = False
        offsets = np.flatnonzero(flags).astype(np.int64, copy=False)
        chunk = low + 2 * offsets
        if first:
            chunk = np.concatenate((np.array([2], dtype=np.int64), chunk))
            first = False
        if chunk.size:
            yield chunk
        low = high + 2

    if first:
        yield np.array([2], dtype=np.int64)


def _record_dict(current: _PlateauAccumulator) -> dict[str, object]:
    return {
        "record_index": current.record_index,
        "start_prime": current.start_prime,
        "gap": current.gap,
        "end_prime": current.end_prime,
    }


def _rate_fields(current: _PlateauAccumulator) -> dict[str, object]:
    n_value = current.n_gap_starts
    m_value = current.m_equal_gaps
    c_value = m_value - 1
    return {
        "N": n_value,
        "M": m_value,
        "C": c_value,
        "Q_M_over_N": m_value / n_value,
        "R_C_over_N_minus_1": (
            c_value / (n_value - 1) if n_value > 1 else None
        ),
    }


def _complete_row(
    current: _PlateauAccumulator,
    *,
    next_start_prime: int,
    next_end_prime: int,
    next_gap: int,
) -> dict[str, object]:
    row = {
        **_record_dict(current),
        "next_record_start_prime": next_start_prime,
        "next_record_gap": next_gap,
        "next_record_end_prime": next_end_prime,
        "end_plateau_x_left": current.end_prime,
        "end_plateau_x_right": next_end_prime - 1,
        "start_exposure_left": current.start_prime,
        "start_exposure_right_exclusive": next_start_prime,
        "L_end_ln_ratio": math.log(next_end_prime / current.end_prime),
        "D_end_log10_ratio": math.log10(next_end_prime / current.end_prime),
        "L_start_ln_ratio": math.log(next_start_prime / current.start_prime),
        "right_censored": False,
    }
    row.update(_rate_fields(current))
    return row


def analyze_prime_chunks(
    chunks: Iterable[Sequence[int] | np.ndarray],
    *,
    analysis_limit: int,
) -> Reconstruction:
    """Reconstruct record plateaus from a complete consecutive-prime stream."""

    records: list[dict[str, object]] = []
    complete: list[dict[str, object]] = []
    histogram: dict[int, int] = {}
    current: _PlateauAccumulator | None = None
    previous_prime: int | None = None
    last_gap_start: int | None = None
    prime_count = 0
    gap_count = 0

    for raw_chunk in chunks:
        chunk = np.asarray(raw_chunk, dtype=np.int64)
        if chunk.ndim != 1 or chunk.size == 0:
            raise ValueError("prime chunks must be non-empty one-dimensional arrays")
        if np.any(np.diff(chunk) <= 0):
            raise ValueError("a prime chunk is not strictly increasing")
        if previous_prime is not None and int(chunk[0]) <= previous_prime:
            raise ValueError("prime chunks overlap or are out of order")

        prime_count += int(chunk.size)
        if previous_prime is None:
            paired = chunk
        else:
            paired = np.concatenate((np.array([previous_prime], dtype=np.int64), chunk))
        gaps = np.diff(paired)
        starts = paired[:-1]
        ends = paired[1:]
        if np.any(gaps <= 0):
            raise ValueError("non-positive consecutive-prime gap")

        if gaps.size:
            gap_count += int(gaps.size)
            values, counts = np.unique(gaps, return_counts=True)
            for gap_value, count_value in zip(values, counts, strict=True):
                gap_int = int(gap_value)
                histogram[gap_int] = histogram.get(gap_int, 0) + int(count_value)

            position = 0
            if current is None:
                current = _PlateauAccumulator(
                    record_index=1,
                    start_prime=int(starts[0]),
                    end_prime=int(ends[0]),
                    gap=int(gaps[0]),
                )
                records.append(_record_dict(current))
                position = 1

            if position < gaps.size:
                remaining = gaps[position:]
                running = np.maximum.accumulate(
                    np.concatenate(
                        (np.array([current.gap], dtype=np.int64), remaining)
                    )
                )
                transitions = position + np.flatnonzero(remaining > running[:-1])
                for transition_value in transitions:
                    transition = int(transition_value)
                    current.observe(gaps[position:transition])
                    complete.append(
                        _complete_row(
                            current,
                            next_start_prime=int(starts[transition]),
                            next_end_prime=int(ends[transition]),
                            next_gap=int(gaps[transition]),
                        )
                    )
                    current = _PlateauAccumulator(
                        record_index=current.record_index + 1,
                        start_prime=int(starts[transition]),
                        end_prime=int(ends[transition]),
                        gap=int(gaps[transition]),
                    )
                    records.append(_record_dict(current))
                    position = transition + 1
                current.observe(gaps[position:])

            last_gap_start = int(starts[-1])
        previous_prime = int(chunk[-1])

    if current is None or previous_prime is None or last_gap_start is None:
        raise ValueError("at least two consecutive primes are required")
    if previous_prime > analysis_limit:
        raise ValueError("prime stream exceeds analysis_limit")

    censored = {
        **_record_dict(current),
        "end_plateau_x_left": current.end_prime,
        "end_plateau_observed_x_right": analysis_limit,
        "start_exposure_left": current.start_prime,
        "last_observed_gap_start_prime": last_gap_start,
        "last_observed_gap_end_prime": previous_prime,
        "right_censored": True,
    }
    censored.update(_rate_fields(current))
    return Reconstruction(
        records=records,
        complete_plateaus=complete,
        right_censored_plateau=censored,
        gap_histogram=dict(sorted(histogram.items())),
        prime_count=prime_count,
        gap_count=gap_count,
        last_prime=previous_prime,
    )


def load_record_references(path: Path) -> list[RecordReference]:
    references: list[RecordReference] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            references.append(
                RecordReference(
                    record_index=int(row["record_index"]),
                    start_prime=int(row["start_prime"]),
                    gap=int(row["gap"]),
                    end_prime=int(row["end_prime"]),
                    source_commit=row["source_commit"],
                    verified_exhaustive_limit=int(row["verified_exhaustive_limit"]),
                )
            )
    if not references:
        raise ValueError("record reference file is empty")
    return references


def verify_reconstruction(
    reconstruction: Reconstruction,
    references: Sequence[RecordReference],
    *,
    analysis_limit: int,
) -> dict[str, object]:
    issues: list[str] = []
    expected = [row for row in references if row.end_prime <= analysis_limit]
    actual_triplets = [
        (int(row["start_prime"]), int(row["gap"]), int(row["end_prime"]))
        for row in reconstruction.records
    ]
    expected_triplets = [
        (row.start_prime, row.gap, row.end_prime) for row in expected
    ]
    if actual_triplets != expected_triplets:
        issues.append("reconstructed maximal-gap records disagree with validated reference")
    if any(row.verified_exhaustive_limit < analysis_limit for row in expected):
        issues.append("record reference exhaustive limit is below analysis limit")
    if reconstruction.gap_count != reconstruction.prime_count - 1:
        issues.append("gap_count does not equal prime_count - 1")
    if sum(reconstruction.gap_histogram.values()) != reconstruction.gap_count:
        issues.append("gap histogram total disagrees with gap_count")
    odd_gaps = {
        gap: count
        for gap, count in reconstruction.gap_histogram.items()
        if gap % 2 == 1 and gap != 1
    }
    if odd_gaps:
        issues.append(f"unexpected odd prime gaps: {odd_gaps}")
    if reconstruction.gap_histogram.get(1) != 1:
        issues.append("the exceptional gap 2->3 must occur exactly once")

    known_prime_count = KNOWN_PRIME_COUNTS.get(analysis_limit)
    if known_prime_count is None:
        issues.append("analysis limit has no pinned independent pi(x) constant")
    elif reconstruction.prime_count != known_prime_count:
        issues.append(
            f"prime_count={reconstruction.prime_count} != pi({analysis_limit})={known_prime_count}"
        )

    for position, row in enumerate(reconstruction.complete_plateaus):
        n_value = int(row["N"])
        m_value = int(row["M"])
        c_value = int(row["C"])
        if not (n_value >= m_value >= 1 and c_value == m_value - 1):
            issues.append(f"plateau {position + 1} violates N/M/C invariants")
        if int(row["end_plateau_x_right"]) != int(row["next_record_end_prime"]) - 1:
            issues.append(f"plateau {position + 1} violates end-prime boundary")
        expected_q = m_value / n_value
        if not math.isclose(float(row["Q_M_over_N"]), expected_q, rel_tol=0, abs_tol=1e-15):
            issues.append(f"plateau {position + 1} has inconsistent Q")
        expected_r = c_value / (n_value - 1) if n_value > 1 else None
        if expected_r is None:
            if row["R_C_over_N_minus_1"] is not None:
                issues.append(f"plateau {position + 1} must have undefined R")
        elif not math.isclose(
            float(row["R_C_over_N_minus_1"]), expected_r, rel_tol=0, abs_tol=1e-15
        ):
            issues.append(f"plateau {position + 1} has inconsistent R")

    censored = reconstruction.right_censored_plateau
    if not bool(censored["right_censored"]):
        issues.append("final plateau is not marked right-censored")
    if actual_triplets and int(censored["record_index"]) != len(actual_triplets):
        issues.append("right-censored plateau record index is inconsistent")

    return {
        "status": "PASS" if not issues else "FAIL",
        "analysis_limit": analysis_limit,
        "known_pi_value": known_prime_count,
        "observed_prime_count": reconstruction.prime_count,
        "observed_gap_count": reconstruction.gap_count,
        "reference_record_count": len(expected),
        "reconstructed_record_count": len(actual_triplets),
        "complete_plateau_count": len(reconstruction.complete_plateaus),
        "right_censored_plateau_count": 1,
        "issues": issues,
    }


def _write_csv(path: Path, rows: Sequence[dict[str, object]], fieldnames: Sequence[str]) -> None:
    with path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, payload: object) -> None:
    serialized = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(serialized)


def _plot_complete_plateaus(rows: Sequence[dict[str, object]], figure_dir: Path) -> list[Path]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if not rows:
        return []
    indices = np.array([int(row["record_index"]) for row in rows])
    m_values = np.array([int(row["M"]) for row in rows])
    c_values = np.array([int(row["C"]) for row in rows])
    q_values = np.array([float(row["Q_M_over_N"]) for row in rows])
    r_values = np.array(
        [
            np.nan if row["R_C_over_N_minus_1"] is None else float(row["R_C_over_N_minus_1"])
            for row in rows
        ]
    )
    l_end = np.array([float(row["L_end_ln_ratio"]) for row in rows])
    l_start = np.array([float(row["L_start_ln_ratio"]) for row in rows])

    definitions = [
        (
            "p006_plateau_occurrences",
            "Complete plateau equal-gap occurrences",
            ((m_values, "M: first occurrence included"), (c_values, "C=M-1")),
            "count",
            "log",
        ),
        (
            "p006_plateau_rates",
            "Complete plateau recurrence rates",
            ((q_values, "Q=M/N"), (r_values, "R=C/(N-1)")),
            "rate",
            "log",
        ),
        (
            "p006_plateau_lifetimes",
            "End-plateau and start-exposure log lifetimes",
            ((l_end, "L_end"), (l_start, "L_start")),
            "natural-log ratio",
            "linear",
        ),
    ]
    outputs: list[Path] = []
    for stem, title, series, ylabel, yscale in definitions:
        fig, axis = plt.subplots(figsize=(10, 6))
        for values, label in series:
            positive = np.isfinite(values) & (values > 0)
            axis.plot(indices[positive], values[positive], marker="o", linewidth=1.2, label=label)
        axis.set_title(title)
        axis.set_xlabel("maximal-gap record index")
        axis.set_ylabel(ylabel)
        if yscale == "log":
            axis.set_yscale("log")
        axis.grid(True, alpha=0.3)
        axis.legend()
        fig.tight_layout()
        for suffix in ("png", "pdf"):
            output = figure_dir / f"{stem}.{suffix}"
            fig.savefig(output, dpi=180)
            outputs.append(output)
        plt.close(fig)
    return outputs


def run_plateau_recurrence_analysis(
    records_path: Path,
    output_directory: Path,
    *,
    approval_token: str | None,
    analysis_limit: int,
    segment_span: int,
    make_plots: bool = True,
) -> dict[str, object]:
    """Run the approved exact finite-range P006 analysis without overwriting."""

    require_experiment_approval(approval_token)
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite result directory: {output_directory}")
    if analysis_limit not in KNOWN_PRIME_COUNTS:
        raise ValueError("analysis_limit must have a pinned independent pi(x) value")
    if not records_path.is_file():
        raise FileNotFoundError(records_path)

    started = time.perf_counter()
    references = load_record_references(records_path)
    reconstruction = analyze_prime_chunks(
        iter_prime_chunks(analysis_limit, segment_span=segment_span),
        analysis_limit=analysis_limit,
    )
    verification = verify_reconstruction(
        reconstruction,
        references,
        analysis_limit=analysis_limit,
    )

    output_directory.mkdir(parents=True, exist_ok=False)
    table_dir = output_directory / "tables"
    figure_dir = output_directory / "figures"
    table_dir.mkdir()
    figure_dir.mkdir()

    complete_fields = list(reconstruction.complete_plateaus[0].keys())
    _write_csv(
        table_dir / "complete_plateaus.csv",
        reconstruction.complete_plateaus,
        complete_fields,
    )
    _write_csv(
        table_dir / "right_censored_plateau.csv",
        [reconstruction.right_censored_plateau],
        list(reconstruction.right_censored_plateau.keys()),
    )
    _write_csv(
        table_dir / "record_transitions.csv",
        reconstruction.records,
        ["record_index", "start_prime", "gap", "end_prime"],
    )
    histogram_rows = [
        {"gap": gap, "count": count}
        for gap, count in reconstruction.gap_histogram.items()
    ]
    _write_csv(table_dir / "gap_histogram.csv", histogram_rows, ["gap", "count"])

    figure_paths = (
        _plot_complete_plateaus(reconstruction.complete_plateaus, figure_dir)
        if make_plots
        else []
    )
    _write_json(output_directory / "verification_report.json", verification)
    elapsed = time.perf_counter() - started
    summary = {
        "status": verification["status"],
        "experiment": "P006_MAXIMAL_GAP_PLATEAU_RECURRENCE",
        "generated_at_utc": _utc_now(),
        "analysis_limit": analysis_limit,
        "segment_span": segment_span,
        "prime_count": reconstruction.prime_count,
        "gap_count": reconstruction.gap_count,
        "record_count": len(reconstruction.records),
        "complete_plateau_count": len(reconstruction.complete_plateaus),
        "right_censored_plateau_count": 1,
        "records_path": str(records_path),
        "records_sha256": sha256_file(records_path),
        "source_commit": references[0].source_commit,
        "elapsed_seconds": elapsed,
        "figure_count": len(figure_paths),
        "gpu_used": False,
        "boundary_contract": "end plateau [e_k,e_(k+1)); start exposure [s_k,s_(k+1))",
        "rate_contract": "Q=M/N and R=C/(N-1), with C=M-1",
    }
    _write_json(output_directory / "summary.json", summary)

    artifact_paths = sorted(
        path for path in output_directory.rglob("*") if path.is_file()
    )
    manifest = {
        "status": verification["status"],
        "generated_at_utc": _utc_now(),
        "artifacts": {
            path.relative_to(output_directory).as_posix(): sha256_file(path)
            for path in artifact_paths
        },
    }
    _write_json(output_directory / "manifest.json", manifest)
    if verification["status"] != "PASS":
        raise RuntimeError(f"P006 verification failed: {verification['issues']}")
    return summary


def verify_saved_result(result_directory: Path) -> dict[str, object]:
    """Re-hash a completed P006 result directory and check saved PASS reports."""

    manifest_path = result_directory / "manifest.json"
    summary_path = result_directory / "summary.json"
    report_path = result_directory / "verification_report.json"
    for required in (manifest_path, summary_path, report_path):
        if not required.is_file():
            raise FileNotFoundError(required)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    report = json.loads(report_path.read_text(encoding="utf-8"))
    issues: list[str] = []
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        issues.append("manifest artifacts is not an object")
        artifacts = {}
    for relative, expected_hash in artifacts.items():
        path = result_directory / relative
        if not path.is_file():
            issues.append(f"missing artifact: {relative}")
        elif sha256_file(path) != expected_hash:
            issues.append(f"artifact hash mismatch: {relative}")
    if summary.get("status") != "PASS":
        issues.append("summary status is not PASS")
    if report.get("status") != "PASS" or report.get("issues") != []:
        issues.append("verification report is not clean PASS")
    return {
        "status": "PASS" if not issues else "FAIL",
        "artifact_count": len(artifacts),
        "issues": issues,
        "manifest_sha256": hashlib.sha256(
            manifest_path.read_bytes()
        ).hexdigest(),
    }


__all__ = [
    "KNOWN_PRIME_COUNTS",
    "RecordReference",
    "Reconstruction",
    "analyze_prime_chunks",
    "iter_prime_chunks",
    "load_record_references",
    "run_plateau_recurrence_analysis",
    "verify_reconstruction",
    "verify_saved_result",
]
