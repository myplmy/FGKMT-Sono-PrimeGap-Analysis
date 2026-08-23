"""Exact local-envelope metrics for end-bounded maximal-gap intervals."""

from __future__ import annotations

from dataclasses import asdict
from typing import Sequence

import mpmath as mp

from source.definitions import F, H, SONO_CONSTANT
from source.models import IntervalMetric, LogBinMetric, RollingEnvelopeMetric


DEFAULT_ROLLING_WINDOWS = (5, 10, 20)


def _decade_exponent_for_closed_right_bin(x: int) -> int:
    """Return k such that ``10**k < x <= 10**(k+1)``."""

    if x < 2:
        raise ValueError("closed-right decade bins require x >= 2")
    exponent = len(str(x)) - 1
    if x == 10**exponent:
        exponent -= 1
    return exponent


def _validate_contiguous_intervals(intervals: Sequence[IntervalMetric]) -> None:
    if not intervals:
        raise ValueError("at least one interval is required")
    for previous, current in zip(intervals, intervals[1:], strict=False):
        if current.x_left != previous.x_right + 1:
            raise ValueError("end-bounded intervals are not contiguous")


def build_log10_bin_minima(
    intervals: Sequence[IntervalMetric],
) -> list[LogBinMetric]:
    """Compute exact minima on ``(10^k, 10^(k+1)]`` integer bins.

    The first and last bins are clipped to the analyzed interval range. Within
    each overlap, ``G`` is constant and ``F`` increases, so only the overlap's
    integer right endpoint is a candidate for the bin minimum.
    """

    _validate_contiguous_intervals(intervals)
    analysis_min = intervals[0].x_left
    analysis_limit = intervals[-1].x_right
    first_exponent = _decade_exponent_for_closed_right_bin(analysis_min)
    final_exponent = _decade_exponent_for_closed_right_bin(analysis_limit)

    metrics: list[LogBinMetric] = []
    for exponent in range(first_exponent, final_exponent + 1):
        nominal_left = 10**exponent
        nominal_right = 10 ** (exponent + 1)
        analyzed_left = max(analysis_min, nominal_left + 1)
        analyzed_right = min(analysis_limit, nominal_right)
        if analyzed_left > analyzed_right:
            continue

        candidates: list[tuple[mp.mpf, int, IntervalMetric, mp.mpf]] = []
        for interval in intervals:
            overlap_left = max(analyzed_left, interval.x_left)
            overlap_right = min(analyzed_right, interval.x_right)
            if overlap_left > overlap_right:
                continue
            f_value = F(overlap_right)
            h_value = H(overlap_right, interval.gap)
            candidates.append((h_value, overlap_right, interval, f_value))

        if not candidates:
            raise ValueError(f"decade bin 10^{exponent} has no interval coverage")
        h_value, minimum_x, minimizing, f_value = min(
            candidates,
            key=lambda item: (item[0], item[1], item[2].record_index),
        )
        metrics.append(
            LogBinMetric(
                decade_exponent=exponent,
                bin_left_exclusive=nominal_left,
                bin_right_inclusive=nominal_right,
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


def build_rolling_local_envelope(
    intervals: Sequence[IntervalMetric],
    *,
    window_size: int,
) -> list[RollingEnvelopeMetric]:
    """Return full-window trailing minima over interval-minimum observations."""

    _validate_contiguous_intervals(intervals)
    if isinstance(window_size, bool) or not isinstance(window_size, int):
        raise ValueError("window_size must be a positive integer")
    if window_size < 1:
        raise ValueError("window_size must be a positive integer")

    metrics: list[RollingEnvelopeMetric] = []
    for end_position in range(window_size - 1, len(intervals)):
        window = intervals[end_position - window_size + 1 : end_position + 1]
        minimizing = min(
            window,
            key=lambda item: (item.h_interval_min, item.x_right, item.record_index),
        )
        metrics.append(
            RollingEnvelopeMetric(
                window_size=window_size,
                window_start_record_index=window[0].record_index,
                window_end_record_index=window[-1].record_index,
                window_x_left=window[0].x_left,
                window_x_right=window[-1].x_right,
                minimizing_record_index=minimizing.record_index,
                gap_start_prime=minimizing.start_prime,
                gap_end_prime=minimizing.end_prime,
                gap=minimizing.gap,
                minimum_x=minimizing.x_right,
                f_at_minimum=minimizing.f_right,
                h_rolling_min=minimizing.h_interval_min,
                sono_ratio_min=minimizing.sono_ratio_min,
            )
        )
    return metrics


def local_metric_to_dict(
    metric: LogBinMetric | RollingEnvelopeMetric,
) -> dict[str, str | int]:
    """Serialize exact-integer and high-precision local-envelope fields."""

    row = asdict(metric)
    for key, value in tuple(row.items()):
        if isinstance(value, mp.mpf):
            row[key] = mp.nstr(value, 40)
        elif isinstance(value, int) and key not in {"decade_exponent", "window_size"}:
            row[key] = str(value)
    return row


__all__ = [
    "DEFAULT_ROLLING_WINDOWS",
    "build_log10_bin_minima",
    "build_rolling_local_envelope",
    "local_metric_to_dict",
]
