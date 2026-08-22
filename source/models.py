"""Typed records shared by the FGKMT/Sono data and analysis pipeline."""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp


@dataclass(frozen=True, slots=True)
class PrimeGapSourceRow:
    """One ``INSERT INTO gaps`` row from ``allgaps.sql``."""

    line_number: int
    gap: int
    is_max: bool
    prime_category: str
    first_occurrence_status: str
    gap_certificate_status: str
    discoverer: str
    year: int
    merit_text: str
    prime_digits: int
    start_prime_expression: str


@dataclass(frozen=True, slots=True)
class MaximalGapRecord:
    """A normalized, confirmed maximal prime-gap record."""

    record_index: int
    start_prime: int
    gap: int
    end_prime: int
    source_id: str
    source_row_id: str
    source_commit: str
    verified_exhaustive_limit: int


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """A machine-readable validation finding."""

    severity: str
    code: str
    message: str
    source_row_id: str | None = None


@dataclass(frozen=True, slots=True)
class IntervalMetric:
    """Exact end-bounded interval metrics for one record plateau."""

    record_index: int
    start_prime: int
    end_prime: int
    gap: int
    x_left: int
    x_right: int
    h_left: mp.mpf
    h_interval_min: mp.mpf
    running_min: mp.mpf
    sono_ratio_min: mp.mpf
    cramer_ratio_min: mp.mpf


@dataclass(frozen=True, slots=True)
class JumpMetric:
    """Drop before and recovery at an end-bounded record jump."""

    record_index: int
    jump_x: int
    previous_gap: int
    new_gap: int
    h_before_jump: mp.mpf
    h_after_jump: mp.mpf
    recovery_factor: mp.mpf


__all__ = [
    "IntervalMetric",
    "JumpMetric",
    "MaximalGapRecord",
    "PrimeGapSourceRow",
    "ValidationIssue",
]
