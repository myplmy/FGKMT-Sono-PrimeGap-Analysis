"""Finite-boundary and local-envelope sensitivity metrics.

The canonical project function remains Sono-compatible and end-bounded.  This
module adds a parallel start-bounded finite function matching the convention in
the FGKMT paper and robustness diagnostics for the canonical end-bounded data.
All minima are over integer x.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

import mpmath as mp

from source.definitions import F, H, SONO_CONSTANT, X_SCALE_POSITIVE_MIN
from source.models import IntervalMetric, MaximalGapRecord


SHIFTED_LOG10_OFFSETS = (mp.mpf("0.25"), mp.mpf("0.50"), mp.mpf("0.75"))
ADDITIONAL_ROLLING_WINDOWS = (3, 8, 15, 30)
X_WIDTH_DECADES = (mp.mpf("0.5"), mp.mpf("1.0"), mp.mpf("2.0"))


@dataclass(frozen=True, slots=True)
class BoundaryPairMetric:
    record_index: int
    start_prime: int
    end_prime: int
    gap: int
    start_interval_left: int
    start_interval_right: int
    end_interval_left: int
    end_interval_right: int
    h_start_interval_min: mp.mpf
    h_end_interval_min: mp.mpf
    start_minus_end: mp.mpf
    start_over_end_minus_one: mp.mpf


@dataclass(frozen=True, slots=True)
class BoundaryDifferenceWindow:
    record_index: int
    start_prime: int
    end_prime: int
    previous_gap: int
    new_gap: int
    x_left: int
    x_right: int
    integer_width: int
    h_end_at_left: mp.mpf
    h_start_at_left: mp.mpf
    start_over_end_ratio: mp.mpf


@dataclass(frozen=True, slots=True)
class ShiftedLogBinMetric:
    shift_decades: str
    bin_index: int
    nominal_left_exclusive: str
    nominal_right_inclusive: str
    analyzed_x_left: int
    analyzed_x_right: int
    minimizing_record_index: int
    gap_start_prime: int
    gap_end_prime: int
    gap: int
    minimum_x: int
    f_at_minimum: mp.mpf
    h_bin_min: mp.mpf
    sono_ratio_min: mp.mpf


@dataclass(frozen=True, slots=True)
class XWidthEnvelopeMetric:
    width_decades: str
    window_factor: str
    endpoint_record_index: int
    window_x_left: int
    window_x_right: int
    full_window: bool
    minimizing_record_index: int
    gap_start_prime: int
    gap_end_prime: int
    gap: int
    minimum_x: int
    f_at_minimum: mp.mpf
    h_x_width_min: mp.mpf
    sono_ratio_min: mp.mpf


def _validate_records(records: Sequence[MaximalGapRecord]) -> None:
    if not records:
        raise ValueError("at least one maximal-gap record is required")
    for previous, current in zip(records, records[1:], strict=False):
        if current.start_prime <= previous.start_prime:
            raise ValueError("start primes must be strictly increasing")
        if current.end_prime <= previous.end_prime:
            raise ValueError("end primes must be strictly increasing")
        if current.gap <= previous.gap:
            raise ValueError("record gaps must be strictly increasing")
        if current.source_commit != previous.source_commit:
            raise ValueError("records mix source commits")
        if current.verified_exhaustive_limit != previous.verified_exhaustive_limit:
            raise ValueError("records mix exhaustive limits")


def _validate_contiguous(intervals: Sequence[IntervalMetric]) -> None:
    if not intervals:
        raise ValueError("at least one interval is required")
    for previous, current in zip(intervals, intervals[1:], strict=False):
        if current.x_left != previous.x_right + 1:
            raise ValueError("interval sequence is not contiguous")


def build_start_bounded_intervals(
    records: Sequence[MaximalGapRecord],
    *,
    analysis_limit: int,
    x_min: int = X_SCALE_POSITIVE_MIN,
) -> list[IntervalMetric]:
    """Build integer plateaus for ``max_{start_prime <= x} gap``."""

    _validate_records(records)
    if analysis_limit < x_min:
        raise ValueError("analysis_limit is below the positive FGKMT scale range")
    if analysis_limit > records[0].verified_exhaustive_limit:
        raise ValueError("analysis_limit exceeds the documented exhaustive limit")

    intervals: list[IntervalMetric] = []
    running_min = mp.inf
    for index, record in enumerate(records):
        if record.start_prime > analysis_limit:
            break
        next_jump = records[index + 1].start_prime if index + 1 < len(records) else None
        x_left = max(record.start_prime, x_min)
        x_right = analysis_limit if next_jump is None else min(next_jump - 1, analysis_limit)
        if x_left > x_right:
            continue

        f_left = F(x_left)
        f_right = F(x_right)
        if f_left <= 0 or f_right <= 0 or f_right < f_left:
            raise ValueError("F(x) is not positive and increasing on a start interval")
        h_left = H(x_left, record.gap)
        h_min = H(x_right, record.gap)
        running_min = min(running_min, h_min)
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
                cramer_ratio_min=mp.mpf(record.gap) / mp.log(x_right) ** 2,
            )
        )
        if x_right == analysis_limit:
            break

    if not intervals or intervals[-1].x_right != analysis_limit:
        raise ValueError("records do not reconstruct start-bounded G through the limit")
    _validate_contiguous(intervals)
    return intervals


def build_boundary_pairs(
    start_intervals: Sequence[IntervalMetric],
    end_intervals: Sequence[IntervalMetric],
) -> list[BoundaryPairMetric]:
    """Pair start/end interval minima for the same maximal-gap record."""

    _validate_contiguous(start_intervals)
    _validate_contiguous(end_intervals)
    end_by_record = {item.record_index: item for item in end_intervals}
    metrics: list[BoundaryPairMetric] = []
    for start in start_intervals:
        end = end_by_record.get(start.record_index)
        if end is None:
            continue
        # The paired minima can differ by much less than either H value.  Do
        # not subtract the already rounded interval metrics: recompute both
        # endpoint values with guard digits, and use expm1 for the relative
        # F-ratio so that tiny boundary effects do not suffer cancellation.
        with mp.workdps(max(mp.mp.dps, 100)):
            f_start = F(start.x_right)
            f_end = F(end.x_right)
            h_start = mp.mpf(start.gap) / f_start
            h_end = mp.mpf(end.gap) / f_end
            delta = h_start - h_end
            relative_delta = mp.expm1(mp.log(f_end) - mp.log(f_start))
        metrics.append(
            BoundaryPairMetric(
                record_index=start.record_index,
                start_prime=start.start_prime,
                end_prime=start.end_prime,
                gap=start.gap,
                start_interval_left=start.x_left,
                start_interval_right=start.x_right,
                end_interval_left=end.x_left,
                end_interval_right=end.x_right,
                h_start_interval_min=h_start,
                h_end_interval_min=h_end,
                start_minus_end=delta,
                start_over_end_minus_one=relative_delta,
            )
        )
    if not metrics:
        raise ValueError("start/end interval sets share no record")
    return metrics


def build_boundary_difference_windows(
    records: Sequence[MaximalGapRecord],
    *,
    analysis_limit: int,
    x_min: int = X_SCALE_POSITIVE_MIN,
) -> list[BoundaryDifferenceWindow]:
    """Return exact integer windows where start/end finite functions differ."""

    _validate_records(records)
    windows: list[BoundaryDifferenceWindow] = []
    for previous, current in zip(records, records[1:], strict=False):
        x_left = max(current.start_prime, x_min)
        x_right = min(current.end_prime - 1, analysis_limit)
        if x_left > x_right:
            continue
        h_end = H(x_left, previous.gap)
        h_start = H(x_left, current.gap)
        windows.append(
            BoundaryDifferenceWindow(
                record_index=current.record_index,
                start_prime=current.start_prime,
                end_prime=current.end_prime,
                previous_gap=previous.gap,
                new_gap=current.gap,
                x_left=x_left,
                x_right=x_right,
                integer_width=x_right - x_left + 1,
                h_end_at_left=h_end,
                h_start_at_left=h_start,
                start_over_end_ratio=h_start / h_end,
            )
        )
    return windows


def _minimum_over_integer_range(
    intervals: Sequence[IntervalMetric],
    x_left: int,
    x_right: int,
) -> tuple[mp.mpf, int, IntervalMetric, mp.mpf]:
    if x_left > x_right:
        raise ValueError("minimum range is empty")
    candidates: list[tuple[mp.mpf, int, IntervalMetric, mp.mpf]] = []
    for interval in intervals:
        overlap_left = max(x_left, interval.x_left)
        overlap_right = min(x_right, interval.x_right)
        if overlap_left > overlap_right:
            continue
        f_value = F(overlap_right)
        candidates.append((H(overlap_right, interval.gap), overlap_right, interval, f_value))
    if not candidates:
        raise ValueError("minimum range has no interval coverage")
    return min(candidates, key=lambda item: (item[0], item[1], item[2].record_index))


def build_shifted_log10_bin_minima(
    intervals: Sequence[IntervalMetric],
    *,
    shift_decades: mp.mpf,
) -> list[ShiftedLogBinMetric]:
    """Compute exact integer minima in ``(10^(k+a), 10^(k+1+a)]``."""

    _validate_contiguous(intervals)
    shift = mp.mpf(shift_decades)
    if not (0 < shift < 1):
        raise ValueError("shift_decades must be strictly between zero and one")
    analysis_min = intervals[0].x_left
    analysis_limit = intervals[-1].x_right
    first_k = int(mp.floor(mp.log10(analysis_min) - shift)) - 1
    final_k = int(mp.ceil(mp.log10(analysis_limit) - shift)) + 1
    shift_text = mp.nstr(shift, 10)

    metrics: list[ShiftedLogBinMetric] = []
    for k in range(first_k, final_k + 1):
        nominal_left = mp.power(10, mp.mpf(k) + shift)
        nominal_right = mp.power(10, mp.mpf(k + 1) + shift)
        analyzed_left = max(analysis_min, int(mp.floor(nominal_left)) + 1)
        analyzed_right = min(analysis_limit, int(mp.floor(nominal_right)))
        if analyzed_left > analyzed_right:
            continue
        h_value, minimum_x, minimizing, f_value = _minimum_over_integer_range(
            intervals, analyzed_left, analyzed_right
        )
        metrics.append(
            ShiftedLogBinMetric(
                shift_decades=shift_text,
                bin_index=k,
                nominal_left_exclusive=mp.nstr(nominal_left, 40),
                nominal_right_inclusive=mp.nstr(nominal_right, 40),
                analyzed_x_left=analyzed_left,
                analyzed_x_right=analyzed_right,
                minimizing_record_index=minimizing.record_index,
                gap_start_prime=minimizing.start_prime,
                gap_end_prime=minimizing.end_prime,
                gap=minimizing.gap,
                minimum_x=minimum_x,
                f_at_minimum=f_value,
                h_bin_min=h_value,
                sono_ratio_min=h_value / SONO_CONSTANT,
            )
        )
    return metrics


def build_x_width_local_envelope(
    intervals: Sequence[IntervalMetric],
    *,
    width_decades: mp.mpf,
) -> list[XWidthEnvelopeMetric]:
    """Compute trailing minima over a fixed multiplicative x-width."""

    _validate_contiguous(intervals)
    width = mp.mpf(width_decades)
    if width <= 0:
        raise ValueError("width_decades must be positive")
    factor = mp.power(10, width)
    analysis_min = intervals[0].x_left
    width_text = mp.nstr(width, 10)
    factor_text = mp.nstr(factor, 40)
    metrics: list[XWidthEnvelopeMetric] = []
    for endpoint in intervals:
        nominal_left = mp.mpf(endpoint.x_right) / factor
        window_left = max(analysis_min, int(mp.ceil(nominal_left)))
        h_value, minimum_x, minimizing, f_value = _minimum_over_integer_range(
            intervals, window_left, endpoint.x_right
        )
        metrics.append(
            XWidthEnvelopeMetric(
                width_decades=width_text,
                window_factor=factor_text,
                endpoint_record_index=endpoint.record_index,
                window_x_left=window_left,
                window_x_right=endpoint.x_right,
                full_window=nominal_left >= analysis_min,
                minimizing_record_index=minimizing.record_index,
                gap_start_prime=minimizing.start_prime,
                gap_end_prime=minimizing.end_prime,
                gap=minimizing.gap,
                minimum_x=minimum_x,
                f_at_minimum=f_value,
                h_x_width_min=h_value,
                sono_ratio_min=h_value / SONO_CONSTANT,
            )
        )
    return metrics


def sensitivity_metric_to_dict(metric: object) -> dict[str, object]:
    """Serialize dataclass metrics without losing large integer precision."""

    row = asdict(metric)
    keep_small_int = {"record_index", "bin_index", "minimizing_record_index", "endpoint_record_index"}
    for key, value in tuple(row.items()):
        if isinstance(value, mp.mpf):
            row[key] = mp.nstr(value, 40)
        elif isinstance(value, int) and not isinstance(value, bool) and key not in keep_small_int:
            row[key] = str(value)
    return row


__all__ = [
    "ADDITIONAL_ROLLING_WINDOWS",
    "BoundaryDifferenceWindow",
    "BoundaryPairMetric",
    "SHIFTED_LOG10_OFFSETS",
    "ShiftedLogBinMetric",
    "X_WIDTH_DECADES",
    "XWidthEnvelopeMetric",
    "build_boundary_difference_windows",
    "build_boundary_pairs",
    "build_shifted_log10_bin_minima",
    "build_start_bounded_intervals",
    "build_x_width_local_envelope",
    "sensitivity_metric_to_dict",
]

