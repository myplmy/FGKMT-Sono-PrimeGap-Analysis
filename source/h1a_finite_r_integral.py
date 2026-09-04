"""Fail-closed checks for the Sono/FMT H1a finite-r integral lemma.

The mathematical proof is documented in
``docs/method/theory/13_Sono_FMT_H1a_finite_r_integral_lemma.md``.  This
module checks the finite directed-interval part and the scalar inequalities at
the analytic-tail boundary.  It is not a proof of the full good-sieve-weight
package and it never computes a theorem threshold ``X_cert``.
"""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp


H1A_Q_NUMERATOR = 9
H1A_Q_DENOMINATOR = 10
H1A_FINITE_SCAN_START = 36
H1A_FINITE_SCAN_STOP = 8_103
H1A_ANALYTIC_LOG_R_START = 9
H1A_ANALYTIC_R_START = 8_104
H1A_INTERVAL_DPS = 60


@dataclass(frozen=True)
class FiniteRIntervalResult:
    """Directed-interval result for one integer ``r``."""

    r: int
    positive_margin: bool
    target_passed: bool
    relative_margin_lower: float | None
    ratio_lower_interval: str | None
    target_interval: str


@dataclass(frozen=True)
class FiniteRScanSummary:
    """Summary of a contiguous directed-interval scan."""

    start: int
    stop: int
    count: int
    failures: tuple[int, ...]
    minimum_relative_margin_lower: float
    minimum_relative_margin_r: int


def _validate_r(r: int) -> None:
    if isinstance(r, bool) or not isinstance(r, int) or r < 2:
        raise ValueError("r must be an integer at least 2")


def _evaluate_one_interval(r: int) -> FiniteRIntervalResult:
    """Evaluate the exact H1a envelope formula at the active interval precision."""

    _validate_r(r)
    iv = mp.iv
    one = iv.mpf(1)
    r_iv = iv.mpf([r, r])
    q = iv.mpf(H1A_Q_NUMERATOR) / H1A_Q_DENOMINATOR
    log_r = iv.log(r_iv)
    scale_t = r_iv * log_r
    support_u = one / iv.sqrt(r_iv)
    scaled_support = scale_t * support_u

    def first_moment_integral(z: mp.ctx_iv.ivmpf) -> mp.ctx_iv.ivmpf:
        y = one + scale_t * z
        return (iv.log(y) + one / y - one) / (scale_t * scale_t)

    a_lower = q * support_u / (one + q * scaled_support)
    a_upper = support_u / (one + scaled_support)
    b_lower = iv.log(one + q * scaled_support) / scale_t
    c_lower = first_moment_integral(q * support_u)
    c_upper = first_moment_integral(support_u)
    d_upper = (
        one
        + scaled_support
        - 2 * iv.log(one + scaled_support)
        - one / (one + scaled_support)
    ) / (scale_t * scale_t * scale_t)

    mean_lower = c_lower / a_upper
    mean_upper = c_upper / a_lower
    variance_upper = d_upper / a_lower - mean_lower * mean_lower
    sum_mean_upper = (r_iv - one) * mean_upper
    sum_variance_upper = (r_iv - one) * variance_upper
    cutoff = q - support_u
    deviation = cutoff - sum_mean_upper
    target = log_r / (4 * r_iv)

    positive_margin = bool(deviation > 0) and bool(sum_variance_upper >= 0)
    if not positive_margin:
        return FiniteRIntervalResult(
            r=r,
            positive_margin=False,
            target_passed=False,
            relative_margin_lower=None,
            ratio_lower_interval=None,
            target_interval=str(target),
        )

    concentration_lower = deviation * deviation / (
        deviation * deviation + sum_variance_upper
    )
    ratio_lower = b_lower * b_lower / a_upper * concentration_lower
    relative_margin = ratio_lower / target - one
    target_passed = bool(relative_margin > 0)

    return FiniteRIntervalResult(
        r=r,
        positive_margin=True,
        target_passed=target_passed,
        relative_margin_lower=float(relative_margin.a),
        ratio_lower_interval=str(ratio_lower),
        target_interval=str(target),
    )


def verify_finite_r_interval(
    r: int, *, dps: int = H1A_INTERVAL_DPS
) -> FiniteRIntervalResult:
    """Check one finite ``r`` with outward-rounded ``mpmath.iv`` arithmetic."""

    if isinstance(dps, bool) or not isinstance(dps, int) or dps < 30:
        raise ValueError("dps must be an integer at least 30")
    old_dps = mp.iv.dps
    try:
        mp.iv.dps = dps
        return _evaluate_one_interval(r)
    finally:
        mp.iv.dps = old_dps


def scan_finite_r_intervals(
    start: int = H1A_FINITE_SCAN_START,
    stop: int = H1A_FINITE_SCAN_STOP,
    *,
    dps: int = H1A_INTERVAL_DPS,
) -> FiniteRScanSummary:
    """Check every integer in ``[start, stop]`` without skipping a value."""

    _validate_r(start)
    _validate_r(stop)
    if start > stop:
        raise ValueError("start must not exceed stop")
    if isinstance(dps, bool) or not isinstance(dps, int) or dps < 30:
        raise ValueError("dps must be an integer at least 30")

    failures: list[int] = []
    minimum_margin = float("inf")
    minimum_r = start
    old_dps = mp.iv.dps
    try:
        mp.iv.dps = dps
        for r in range(start, stop + 1):
            result = _evaluate_one_interval(r)
            if not result.target_passed:
                failures.append(r)
                continue
            assert result.relative_margin_lower is not None
            if result.relative_margin_lower < minimum_margin:
                minimum_margin = result.relative_margin_lower
                minimum_r = r
    finally:
        mp.iv.dps = old_dps

    if failures:
        minimum_margin = float("nan")

    return FiniteRScanSummary(
        start=start,
        stop=stop,
        count=stop - start + 1,
        failures=tuple(failures),
        minimum_relative_margin_lower=minimum_margin,
        minimum_relative_margin_r=minimum_r,
    )


def verify_analytic_tail_boundary(
    *, dps: int = H1A_INTERVAL_DPS
) -> dict[str, bool]:
    """Check the scalar endpoint inequalities used for ``log(r) >= 9``.

    Monotonicity beyond this endpoint is proved by differentiation in the H1a
    document.  These checks deliberately do not extrapolate numerically.
    """

    if isinstance(dps, bool) or not isinstance(dps, int) or dps < 30:
        raise ValueError("dps must be an integer at least 30")
    old_dps = mp.iv.dps
    try:
        mp.iv.dps = dps
        iv = mp.iv
        q = iv.mpf(H1A_Q_NUMERATOR) / H1A_Q_DENOMINATOR
        ell = iv.mpf(H1A_ANALYTIC_LOG_R_START)
        exp_half = iv.exp(ell / 2)
        exp_full = iv.exp(ell)
        mean_coarse = (iv.mpf(1) / 2 + iv.mpf(29) / 90) * (
            iv.mpf(501) / 500
        )
        cutoff_coarse = iv.mpf(71) / 80
        deviation_coarse = cutoff_coarse - mean_coarse
        # For ell >= 9,
        #
        #   V/(2c) = exp(-ell)/(4*q*ell*log(q*ell))
        #            + exp(-ell/2)/(4*log(q*ell))
        #
        # is decreasing.  The already checked endpoint bounds
        # exp(9/2)>80 and log(8.1)>2 give the rational upper bound
        # 1/414720 + 1/640 = 649/414720.  This is below
        # (3/50)^2, the square of the coarse deviation lower bound.
        variance_over_2c_endpoint_upper = iv.mpf(649) / 414_720
        deviation_square_lower = (iv.mpf(3) / 50) ** 2
        c_at_endpoint = 2 * iv.log(q * ell) / ell
        variance_at_endpoint = (
            iv.exp(-ell) / (q * ell * ell)
            + iv.exp(-ell / 2) / ell
        )

        return {
            "ceil_exp_9_is_8104": bool(exp_full > 8_103)
            and bool(exp_full < H1A_ANALYTIC_R_START),
            "exp_4p5_exceeds_80": bool(exp_half > 80),
            "log_18_below_2p9": bool(iv.log(18) < iv.mpf(29) / 10),
            "reciprocal_q_s_below_1_over_500": bool(
                iv.mpf(1) / (q * ell * exp_half) < iv.mpf(1) / 500
            ),
            "log_8p1_exceeds_2": bool(iv.log(q * ell) > 2),
            "coarse_deviation_exceeds_3_over_50": bool(
                deviation_coarse > iv.mpf(3) / 50
            ),
            "variance_over_2c_rational_chain": bool(
                variance_over_2c_endpoint_upper < deviation_square_lower
            ),
            "variance_over_2c_direct_endpoint": bool(
                variance_at_endpoint / (2 * c_at_endpoint)
                < deviation_square_lower
            ),
        }
    finally:
        mp.iv.dps = old_dps


__all__ = [
    "FiniteRIntervalResult",
    "FiniteRScanSummary",
    "H1A_ANALYTIC_LOG_R_START",
    "H1A_ANALYTIC_R_START",
    "H1A_FINITE_SCAN_START",
    "H1A_FINITE_SCAN_STOP",
    "H1A_INTERVAL_DPS",
    "scan_finite_r_intervals",
    "verify_analytic_tail_boundary",
    "verify_finite_r_interval",
]
