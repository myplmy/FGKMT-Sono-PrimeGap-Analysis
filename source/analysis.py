"""End-bounded FGKMT normalization and empirical-envelope calculations."""

from __future__ import annotations

from dataclasses import asdict
from typing import Sequence

import mpmath as mp

from source.definitions import F, H, SONO_CONSTANT, X_SCALE_POSITIVE_MIN
from source.models import IntervalMetric, JumpMetric, MaximalGapRecord


def _linear_loglog_trend(intervals: Sequence[IntervalMetric]) -> dict[str, object]:
    """Return a descriptive log-log fit without attaching inferential claims."""

    if len(intervals) < 2:
        return {
            "status": "INSUFFICIENT_POINTS",
            "point_count": len(intervals),
        }
    x_values = [mp.log(item.x_right) for item in intervals]
    y_values = [mp.log(item.h_interval_min) for item in intervals]
    x_mean = mp.fsum(x_values) / len(x_values)
    y_mean = mp.fsum(y_values) / len(y_values)
    covariance = mp.fsum(
        (x_value - x_mean) * (y_value - y_mean)
        for x_value, y_value in zip(x_values, y_values, strict=True)
    )
    x_variance = mp.fsum((value - x_mean) ** 2 for value in x_values)
    y_variance = mp.fsum((value - y_mean) ** 2 for value in y_values)
    if x_variance == 0 or y_variance == 0:
        return {
            "status": "DEGENERATE",
            "point_count": len(intervals),
        }
    slope = covariance / x_variance
    correlation = covariance / mp.sqrt(x_variance * y_variance)
    return {
        "status": "DESCRIPTIVE_ONLY",
        "point_count": len(intervals),
        "ln_h_vs_ln_x_slope": mp.nstr(slope, 30),
        "pearson_correlation": mp.nstr(correlation, 30),
        "warning": "record intervals are not independent samples; no p-value is reported",
    }


def _median(values: Sequence[mp.mpf]) -> mp.mpf:
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def _validate_record_sequence(records: Sequence[MaximalGapRecord]) -> None:
    if not records:
        raise ValueError("at least one maximal-gap record is required")
    for previous, current in zip(records, records[1:], strict=False):
        if current.start_prime <= previous.start_prime:
            raise ValueError("start primes must be strictly increasing")
        if current.end_prime <= previous.end_prime:
            raise ValueError("end primes must be strictly increasing")
        if current.gap <= previous.gap:
            raise ValueError("record gaps must be strictly increasing")
        if current.verified_exhaustive_limit != previous.verified_exhaustive_limit:
            raise ValueError("records mix different exhaustive limits")
        if current.source_commit != previous.source_commit:
            raise ValueError("records mix different source commits")


def record_at_x(
    records: Sequence[MaximalGapRecord],
    x: int,
) -> MaximalGapRecord:
    """Return the record that defines end-bounded ``G(x)``."""

    _validate_record_sequence(records)
    active: MaximalGapRecord | None = None
    for record in records:
        if record.end_prime > x:
            break
        active = record
    if active is None:
        raise ValueError(f"record sequence does not reconstruct G({x})")
    return active


def analysis_limit_for_interval_count(
    records: Sequence[MaximalGapRecord],
    *,
    interval_count: int,
    x_min: int = X_SCALE_POSITIVE_MIN,
) -> int:
    """Close exactly ``interval_count`` plateaus starting at ``x_min``.

    The first selected plateau is the record active at ``x_min``. Its fifth
    successor jump, for example, closes a five-interval pilot at one integer
    before that jump.
    """

    _validate_record_sequence(records)
    if isinstance(interval_count, bool) or not isinstance(interval_count, int):
        raise ValueError("interval_count must be a positive integer")
    if interval_count < 1:
        raise ValueError("interval_count must be a positive integer")

    active = record_at_x(records, x_min)
    active_position = records.index(active)
    closing_jump_position = active_position + interval_count
    if closing_jump_position >= len(records):
        raise ValueError("record sequence cannot close the requested interval count")

    analysis_limit = records[closing_jump_position].end_prime - 1
    if analysis_limit > active.verified_exhaustive_limit:
        raise ValueError("requested intervals cross the documented exhaustive limit")
    return analysis_limit


def build_end_bounded_intervals(
    records: Sequence[MaximalGapRecord],
    *,
    analysis_limit: int,
    x_min: int = X_SCALE_POSITIVE_MIN,
) -> list[IntervalMetric]:
    """Build exact integer intervals for ``G(x)=max_{p[n+1] <= x} gap``.

    On ``[end_i, end_{i+1}-1]``, the maximal gap is ``gap_i``. Since
    ``F`` is increasing on the configured positive-scale range, the interval
    minimum occurs exactly at its integer right endpoint.
    """

    _validate_record_sequence(records)
    if analysis_limit < x_min:
        raise ValueError("analysis_limit is below the positive FGKMT scale range")
    if analysis_limit > records[0].verified_exhaustive_limit:
        raise ValueError("analysis_limit exceeds the documented exhaustive limit")

    intervals: list[IntervalMetric] = []
    running_min = mp.inf
    for index, record in enumerate(records):
        if record.end_prime > analysis_limit:
            break

        next_jump = records[index + 1].end_prime if index + 1 < len(records) else None
        x_left = max(record.end_prime, x_min)
        x_right = analysis_limit if next_jump is None else min(next_jump - 1, analysis_limit)
        if x_left > x_right:
            continue

        f_left = F(x_left)
        f_right = F(x_right)
        if f_left <= 0 or f_right <= 0:
            raise ValueError("interval entered the non-positive FGKMT scale domain")
        if f_right < f_left:
            raise ValueError("F(x) is not increasing on an analyzed interval")

        h_left = H(x_left, record.gap)
        h_min = H(x_right, record.gap)
        running_min = min(running_min, h_min)
        cramer_ratio = mp.mpf(record.gap) / mp.log(x_right) ** 2

        intervals.append(
            IntervalMetric(
                record_index=record.record_index,
                start_prime=record.start_prime,
                end_prime=record.end_prime,
                gap=record.gap,
                x_left=x_left,
                x_right=x_right,
                f_left=f_left,
                f_right=f_right,
                h_left=h_left,
                h_interval_min=h_min,
                running_min=running_min,
                sono_ratio_min=h_min / SONO_CONSTANT,
                cramer_ratio_min=cramer_ratio,
            )
        )

        if x_right == analysis_limit:
            break

    if not intervals or intervals[-1].x_right != analysis_limit:
        raise ValueError("record sequence does not reconstruct G(x) through analysis_limit")
    return intervals


def build_jump_metrics(
    records: Sequence[MaximalGapRecord],
    *,
    analysis_limit: int,
    x_min: int = X_SCALE_POSITIVE_MIN,
) -> list[JumpMetric]:
    """Quantify the pre-record decline and immediate recovery at each jump."""

    _validate_record_sequence(records)
    jumps: list[JumpMetric] = []
    for previous, current in zip(records, records[1:], strict=False):
        jump_x = current.end_prime
        if jump_x < x_min or jump_x > analysis_limit:
            continue
        h_before = H(jump_x - 1, previous.gap)
        h_after = H(jump_x, current.gap)
        jumps.append(
            JumpMetric(
                record_index=current.record_index,
                jump_x=jump_x,
                previous_gap=previous.gap,
                new_gap=current.gap,
                h_before_jump=h_before,
                h_after_jump=h_after,
                recovery_factor=h_after / h_before,
            )
        )
    return jumps


def summarize_analysis(
    intervals: Sequence[IntervalMetric],
    jumps: Sequence[JumpMetric],
    *,
    source_commit: str,
    analysis_limit: int,
    verified_exhaustive_limit: int,
) -> dict[str, object]:
    """Create a theorem-neutral numerical summary."""

    if not intervals:
        raise ValueError("cannot summarize an empty interval sequence")
    minimum = min(intervals, key=lambda item: item.h_interval_min)
    final_running_min = intervals[-1].running_min
    running_low_count = 0
    previous_running = mp.inf
    for interval in intervals:
        if interval.running_min < previous_running:
            running_low_count += 1
            previous_running = interval.running_min

    recovery_summary: dict[str, object]
    if jumps:
        recovery_values = [item.recovery_factor for item in jumps]
        recovery_summary = {
            "count": len(recovery_values),
            "minimum": mp.nstr(min(recovery_values), 30),
            "median": mp.nstr(_median(recovery_values), 30),
            "maximum": mp.nstr(max(recovery_values), 30),
            "fraction_above_one": mp.nstr(
                mp.mpf(sum(value > 1 for value in recovery_values))
                / len(recovery_values),
                30,
            ),
        }
    else:
        recovery_summary = {"count": 0}

    return {
        "status": "COMPUTED_NOT_INTERPRETED",
        "boundary_mode": "end",
        "g_definition": "max gap with end_prime <= x",
        "fgkmt_scale": "ln(x)*ln(ln(x))*ln(ln(ln(ln(x))))/ln(ln(ln(x)))",
        "log_definition": "log_k(x) is k-fold iterated natural logarithm",
        "source_commit": source_commit,
        "analysis_min_x": str(intervals[0].x_left),
        "analysis_max_x": str(analysis_limit),
        "verified_exhaustive_limit": str(verified_exhaustive_limit),
        "analyzed_interval_count": len(intervals),
        "analyzed_jump_count": len(jumps),
        "minimum_h": mp.nstr(minimum.h_interval_min, 40),
        "minimum_h_x": str(minimum.x_right),
        "minimum_h_gap": str(minimum.gap),
        "minimum_sono_ratio": mp.nstr(minimum.sono_ratio_min, 40),
        "final_running_min": mp.nstr(final_running_min, 40),
        "running_minimum_update_count": running_low_count,
        "interval_minimum_loglog_trend": _linear_loglog_trend(intervals),
        "record_jump_recovery": recovery_summary,
        "ever_below_wolf_reference_h_1": any(item.h_interval_min < 1 for item in intervals),
        "ever_below_sono_constant": any(
            item.h_interval_min < SONO_CONSTANT for item in intervals
        ),
        "interpretation_limits": [
            "finite computation does not prove or disprove an asymptotic theorem",
            "Sono's sufficiently-large threshold is not numerically supplied here",
            "the explicit constant is a rigorous lower-bound constant, not an empirical limit",
        ],
    }


def interval_to_dict(metric: IntervalMetric) -> dict[str, str | int]:
    row = asdict(metric)
    for key in (
        "f_left",
        "f_right",
        "h_left",
        "h_interval_min",
        "running_min",
        "sono_ratio_min",
        "cramer_ratio_min",
    ):
        row[key] = mp.nstr(row[key], 40)
    for key in ("start_prime", "end_prime", "gap", "x_left", "x_right"):
        row[key] = str(row[key])
    return row


def jump_to_dict(metric: JumpMetric) -> dict[str, str | int]:
    row = asdict(metric)
    for key in ("h_before_jump", "h_after_jump", "recovery_factor"):
        row[key] = mp.nstr(row[key], 40)
    for key in ("jump_x", "previous_gap", "new_gap"):
        row[key] = str(row[key])
    return row


__all__ = [
    "analysis_limit_for_interval_count",
    "build_end_bounded_intervals",
    "build_jump_metrics",
    "interval_to_dict",
    "jump_to_dict",
    "record_at_x",
    "summarize_analysis",
]
