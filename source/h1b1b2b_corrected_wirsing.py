"""Explicit project contract for the corrected kappa=1 Wirsing estimate.

The proof is recorded in
``docs/method/theory/22_Sono_FMT_H1b1b2b_corrected_kappa1_Wirsing_multiplier.md``.
It follows the recurrence in Kevin Ford's Theorem 4.4, keeps the additional
``c_gamma * (L + 1)^kappa`` term that is missing from the printed GGPY and
Maynard statements, and makes a deliberately coarse kappa=1 multiplier
explicit.  This module is a contract checker; its numerical evaluations are
not a substitute for the analytic proof.

The notation ``a1_gap`` is Maynard/Ford's parameter in
``gamma(p)/p <= 1-a1_gap``.  GGPY instead writes the same condition as
``gamma(p)/p <= 1-1/A1``.  Hence ``A1_GGPY = 1/a1_gap``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp


H1B1B2B_LN2_LOWER_BOUND = Fraction(69, 100)
H1B1B2B_INV_LN2_UPPER_BOUND = Fraction(100, 69)
H1B1B2B_LOG6_UPPER_BOUND = 2
H1B1B2B_PRIME_WEIGHTED_DEVIATION_BOUND = 64
H1B1B2B_PRIME_RECIPROCAL_DEVIATION_BOUND = 16
H1B1B2B_MERTENS_PRODUCT_MULTIPLIER = 8192
H1B1B2B_INTERVAL_LOG_WEIGHTED_DEVIATION_BASE = 130
H1B1B2B_TAIL_EXPONENT_BASE = 256
H1B1B2B_SUMMATORY_PREFACTOR = 40960
H1B1B2B_FINITE_X_MINIMUM = 2
H1B1B2B_WEIGHTED_PARTIAL_SUMMATION_FACTOR = 2
H1B1B2B_STRICT_CUMULATIVE_ENDPOINT_ALLOWANCE = 2


@dataclass(frozen=True)
class CorrectedKappa1WirsingCertificate:
    """Parameterised explicit multiplier for the corrected kappa=1 theorem."""

    maynard_a1_gap: Fraction
    ggpy_a1_cap: Fraction
    a2: Fraction
    local_recurrence_tail_bound: Fraction
    delta_multiplier: Fraction
    tail_exponent: Fraction
    summatory_prefactor: int
    finite_x_minimum: int
    error_scale: str
    error_contains_c_gamma: bool
    corrected_extra_term_included: bool
    c_gamma_lower_bound_required: bool

    @property
    def summatory_multiplier_formula(self) -> str:
        """Return the exact symbolic form of the project multiplier."""

        return (
            "40960 * D(a1_gap,A2) * exp(256+A2), where "
            "D=4+A2+(A2/a1_gap)*(1+100*A2/69)"
            "+2*(1-a1_gap)^2/a1_gap"
        )

    @property
    def weighted_multiplier_formula(self) -> str:
        """Return the Lemma 8.3 multiplier after partial summation."""

        return "2 * (C_sum(a1_gap,A2) + 2)"


def _positive_fraction(value: int | str | Fraction, name: str) -> Fraction:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a positive rational number")
    try:
        result = Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{name} must be a positive rational number") from exc
    if result <= 0:
        raise ValueError(f"{name} must be positive")
    return result


def corrected_kappa1_wirsing_certificate(
    a1_gap: int | str | Fraction,
    a2: int | str | Fraction,
) -> CorrectedKappa1WirsingCertificate:
    """Build the exact rational part of the corrected kappa=1 certificate.

    The assumptions are Maynard/Ford's ``0 < a1_gap <= 1`` and ``A2>0``.
    Under their inclusive-endpoint prime-sum hypothesis, the proof gives

    ``|sum_{n<=x} mu2(n)h(n) - c_gamma*log(x)|``
    ``<= C_sum(a1_gap,A2) * c_gamma * (L+1)``

    for every real ``x>=2``.  The value returned here is parameterised: it is
    not an actual Maynard invocation until separate work certifies common
    numerical values of ``a1_gap``, ``A2`` and ``L`` for every call.
    """

    gap = _positive_fraction(a1_gap, "a1_gap")
    if gap > 1:
        raise ValueError("a1_gap must not exceed 1")
    upper_error = _positive_fraction(a2, "a2")

    local_tail = (
        upper_error
        / gap
        * (1 + H1B1B2B_INV_LN2_UPPER_BOUND * upper_error)
        + Fraction(2) * (1 - gap) ** 2 / gap
    )
    delta_multiplier = 4 + upper_error + local_tail
    tail_exponent = H1B1B2B_TAIL_EXPONENT_BASE + upper_error

    return CorrectedKappa1WirsingCertificate(
        maynard_a1_gap=gap,
        ggpy_a1_cap=1 / gap,
        a2=upper_error,
        local_recurrence_tail_bound=local_tail,
        delta_multiplier=delta_multiplier,
        tail_exponent=tail_exponent,
        summatory_prefactor=H1B1B2B_SUMMATORY_PREFACTOR,
        finite_x_minimum=H1B1B2B_FINITE_X_MINIMUM,
        error_scale="c_gamma * (L+1)",
        error_contains_c_gamma=True,
        corrected_extra_term_included=True,
        c_gamma_lower_bound_required=False,
    )


def summatory_log_multiplier(
    a1_gap: int | str | Fraction,
    a2: int | str | Fraction,
) -> mp.mpf:
    """Evaluate ``log(C_sum)`` without overflowing ordinary floating point."""

    certificate = corrected_kappa1_wirsing_certificate(a1_gap, a2)
    delta = mp.mpf(certificate.delta_multiplier.numerator) / mp.mpf(
        certificate.delta_multiplier.denominator
    )
    exponent = mp.mpf(certificate.tail_exponent.numerator) / mp.mpf(
        certificate.tail_exponent.denominator
    )
    return mp.log(H1B1B2B_SUMMATORY_PREFACTOR) + mp.log(delta) + exponent


def summatory_multiplier(
    a1_gap: int | str | Fraction,
    a2: int | str | Fraction,
) -> mp.mpf:
    """Evaluate the deliberately coarse explicit summatory multiplier."""

    return mp.exp(summatory_log_multiplier(a1_gap, a2))


def strict_summatory_multiplier(
    a1_gap: int | str | Fraction,
    a2: int | str | Fraction,
) -> mp.mpf:
    """Evaluate the multiplier for the strict cumulative cutoff ``d < z``.

    The corrected summatory estimate is first proved for ``d <= x``.  Passing
    to every strict real cutoff, including ``1 < z <= 2``, costs the explicit
    endpoint allowance from equation (22.25) of the project proof.  This
    helper keeps that allowance from being silently omitted by sharp-cutoff
    callers.
    """

    return mp.fadd(
        summatory_multiplier(a1_gap, a2),
        H1B1B2B_STRICT_CUMULATIVE_ENDPOINT_ALLOWANCE,
        exact=True,
    )


def weighted_lemma83_multiplier(
    a1_gap: int | str | Fraction,
    a2: int | str | Fraction,
) -> mp.mpf:
    """Evaluate the corrected Maynard Lemma 8.3 multiplier.

    Passing from the summatory estimate to a smooth weighted sum costs a
    boundary term and one derivative integral.  The additive ``2`` safely
    handles the strict cumulative endpoint near 2.
    """

    return mp.fmul(
        H1B1B2B_WEIGHTED_PARTIAL_SUMMATION_FACTOR,
        strict_summatory_multiplier(a1_gap, a2),
        exact=True,
    )


__all__ = [
    "CorrectedKappa1WirsingCertificate",
    "H1B1B2B_FINITE_X_MINIMUM",
    "H1B1B2B_INTERVAL_LOG_WEIGHTED_DEVIATION_BASE",
    "H1B1B2B_INV_LN2_UPPER_BOUND",
    "H1B1B2B_LN2_LOWER_BOUND",
    "H1B1B2B_LOG6_UPPER_BOUND",
    "H1B1B2B_MERTENS_PRODUCT_MULTIPLIER",
    "H1B1B2B_PRIME_RECIPROCAL_DEVIATION_BOUND",
    "H1B1B2B_PRIME_WEIGHTED_DEVIATION_BOUND",
    "H1B1B2B_STRICT_CUMULATIVE_ENDPOINT_ALLOWANCE",
    "H1B1B2B_SUMMATORY_PREFACTOR",
    "H1B1B2B_TAIL_EXPONENT_BASE",
    "H1B1B2B_WEIGHTED_PARTIAL_SUMMATION_FACTOR",
    "corrected_kappa1_wirsing_certificate",
    "summatory_log_multiplier",
    "summatory_multiplier",
    "strict_summatory_multiplier",
    "weighted_lemma83_multiplier",
]
