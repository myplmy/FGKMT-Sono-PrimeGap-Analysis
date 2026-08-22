"""Canonical mathematical definitions for the FGKMT/Sono experiment.

The subscript in ``log_k`` denotes k-fold composition of the natural
logarithm.  It never denotes a logarithm with base k.
"""

from __future__ import annotations

import mpmath as mp


WORKING_DPS = 50
X_SCALE_POSITIVE_MIN = 3_814_280

# Establish the minimum precision required by the research protocol.  A caller
# may deliberately raise this value after importing the module.
if mp.mp.dps < WORKING_DPS:
    mp.mp.dps = WORKING_DPS

SONO_CONSTANT = mp.mpf("2.0e-17")


def iter_log(x: int | str | mp.mpf, n: int) -> mp.mpf:
    """Return the k-fold natural logarithm of ``x`` in the real domain."""

    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")

    value = mp.mpf(x)
    if not mp.isfinite(value):
        raise ValueError("x must be finite")

    for level in range(1, n + 1):
        if value <= 0:
            raise ValueError(
                f"iterated natural logarithm leaves the real domain before level {level}"
            )
        value = mp.log(value)

    return value


def log1(x: int | str | mp.mpf) -> mp.mpf:
    """Return ln(x)."""

    return iter_log(x, 1)


def log2(x: int | str | mp.mpf) -> mp.mpf:
    """Return ln(ln(x)); this is not a base-2 logarithm."""

    return iter_log(x, 2)


def log3(x: int | str | mp.mpf) -> mp.mpf:
    """Return ln(ln(ln(x))); this is not a base-3 logarithm."""

    return iter_log(x, 3)


def log4(x: int | str | mp.mpf) -> mp.mpf:
    """Return ln(ln(ln(ln(x)))); this is not a base-4 logarithm."""

    return iter_log(x, 4)


def F(x: int | str | mp.mpf) -> mp.mpf:
    """Return the canonical FGKMT/FMT large-gap scale F(x)."""

    log_1 = log1(x)
    log_2 = log2(x)
    log_3 = log3(x)
    log_4 = log4(x)
    if log_3 == 0:
        raise ZeroDivisionError("log_3(x) is zero")
    return log_1 * log_2 * log_4 / log_3


def H(x: int | str | mp.mpf, gap: int | str | mp.mpf) -> mp.mpf:
    """Return the normalized empirical coefficient gap/F(x)."""

    gap_value = mp.mpf(gap)
    if not mp.isfinite(gap_value) or gap_value <= 0:
        raise ValueError("gap must be finite and positive")
    return gap_value / F(x)


def sono_bound(x: int | str | mp.mpf) -> mp.mpf:
    """Return Sono's explicit comparison scale c_Sono * F(x)."""

    return SONO_CONSTANT * F(x)


def sono_ratio(x: int | str | mp.mpf, gap: int | str | mp.mpf) -> mp.mpf:
    """Return H(x)/c_Sono for a supplied gap."""

    return H(x, gap) / SONO_CONSTANT


__all__ = [
    "F",
    "H",
    "SONO_CONSTANT",
    "WORKING_DPS",
    "X_SCALE_POSITIVE_MIN",
    "iter_log",
    "log1",
    "log2",
    "log3",
    "log4",
    "sono_bound",
    "sono_ratio",
]
