"""Exact Euler normalization for the H1b-2a.1 Proposition 9.4 audit.

Maynard's displayed equations (9.61)--(9.66) replace the denominator

    g_*(p,m) = (p-m)^2 / (p+m-2)

by ``p+O(k)``.  This module keeps the exact rational local factors and
certifies uniform tail bounds.  It closes only the final Euler-normalization
child of Proposition 9.4; the distribution error and the parent proposition
remain open.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp


H1B2A1_MINIMUM_K = 36


@dataclass(frozen=True)
class LocalEulerCertificate:
    """One exact prime-local identity and its uniform rational majorant."""

    k: int
    prime: int
    omega: int
    omega_star: int
    exact_factor: Fraction
    comparison_factor: Fraction
    exact_excess: Fraction
    excess_upper_bound: Fraction
    identity_verified: bool
    upper_bound_verified: bool


@dataclass(frozen=True)
class EulerTailCertificate:
    """Uniform products over primes larger than an integer cutoff."""

    k: int
    cutoff: int
    pre_y_log_tail_upper: Fraction
    sharp_r0_log_tail_upper: Fraction
    canonical_ratio_log_tail_upper: Fraction
    final_two_products_log_tail_upper: Fraction
    full_line_966_log_tail_upper: Fraction
    final_two_products_multiplier_upper: mp.mpf
    full_line_966_multiplier_upper: mp.mpf
    exact_local_factors_recovered: bool
    final_euler_products_closed: bool
    distribution_error_closed: bool
    proposition_94_closed: bool
    siv_07_closed: bool
    x_cert_ready: bool


def _validate_k(k: int) -> None:
    if isinstance(k, bool) or not isinstance(k, int) or k < H1B2A1_MINIMUM_K:
        raise ValueError(f"k must be an integer at least {H1B2A1_MINIMUM_K}")


def _validate_local_inputs(k: int, prime: int, omega: int) -> None:
    _validate_k(k)
    if isinstance(prime, bool) or not isinstance(prime, int):
        raise ValueError("prime must be an integer")
    if prime <= 2 * k * k:
        raise ValueError("a nonexcluded source prime must exceed 2*k^2")
    if isinstance(omega, bool) or not isinstance(omega, int) or not 0 <= omega <= k:
        raise ValueError("omega must be an integer in [0,k]")


def _fraction_to_mpf(value: Fraction) -> mp.mpf:
    return mp.mpf(value.numerator) / value.denominator


def exact_star_denominator(prime: int, omega_star: int) -> Fraction:
    """Return ``(p-omega*)^2/(p+omega*-2)`` exactly.

    The caller is responsible for the Maynard support restrictions.  This
    helper merely checks positivity, so it is also useful in algebra tests.
    """

    if isinstance(prime, bool) or not isinstance(prime, int) or prime < 3:
        raise ValueError("prime must be an integer at least 3")
    if (
        isinstance(omega_star, bool)
        or not isinstance(omega_star, int)
        or not 0 <= omega_star < prime
    ):
        raise ValueError("omega_star must be an integer in [0,prime)")
    denominator = prime + omega_star - 2
    if denominator <= 0:
        raise ValueError("the exact local denominator must be positive")
    return Fraction((prime - omega_star) ** 2, denominator)


def pre_y_local_certificate(k: int, prime: int, omega: int) -> LocalEulerCertificate:
    """Certify the exact product at source (9.64), before (9.65).

    For ``p not dividing WB`` its local factor is

    ``1 + omega/((p-1)(p-omega))``.
    """

    _validate_local_inputs(k, prime, omega)
    factor = Fraction(1) + Fraction(omega, (prime - 1) * (prime - omega))
    excess = factor - 1
    upper = Fraction(4 * k, prime * prime)
    return LocalEulerCertificate(
        k=k,
        prime=prime,
        omega=omega,
        omega_star=omega,
        exact_factor=factor,
        comparison_factor=Fraction(1),
        exact_excess=excess,
        excess_upper_bound=upper,
        identity_verified=True,
        upper_bound_verified=excess <= upper,
    )


def sharp_r0_local_certificate(
    k: int,
    prime: int,
    omega: int,
    *,
    prime_divides_b: bool = False,
) -> LocalEulerCertificate:
    """Certify the first exact Euler product in source equation (9.66).

    If ``p`` divides ``B``, Maynard defines ``omega(p)=0`` and
    ``omega*(p)=1``; the factor is exactly one.  Otherwise ``p`` is outside
    ``W_0``, hence outside ``Delta_L``, and ``omega*=omega+1``.  In that case

    ``(1+1/g_*)(1-1/p)``

    equals

    ``1 + omega(3p-omega-3)/(p(p-omega-1)^2)``.
    """

    _validate_local_inputs(k, prime, omega)
    if not isinstance(prime_divides_b, bool):
        raise ValueError("prime_divides_b must be boolean")
    if prime_divides_b and omega != 0:
        raise ValueError("Maynard defines omega(p)=0 when p divides B")

    omega_star = 1 if prime_divides_b else omega + 1
    g_star = exact_star_denominator(prime, omega_star)
    factor = (Fraction(1) + 1 / g_star) * Fraction(prime - 1, prime)
    if prime_divides_b:
        comparison = Fraction(1)
    else:
        comparison = Fraction(1) + Fraction(
            omega * (3 * prime - omega - 3),
            prime * (prime - omega - 1) ** 2,
        )
    excess = factor - 1
    upper = Fraction(4 * k, prime * prime)
    return LocalEulerCertificate(
        k=k,
        prime=prime,
        omega=omega,
        omega_star=omega_star,
        exact_factor=factor,
        comparison_factor=comparison,
        exact_excess=excess,
        excess_upper_bound=upper,
        identity_verified=factor == comparison,
        upper_bound_verified=Fraction(0) <= excess <= upper,
    )


def canonical_ratio_local_certificate(
    k: int,
    prime: int,
    omega: int,
    *,
    collides_with_extra_form: bool,
) -> LocalEulerCertificate:
    """Compare the second product in (9.66) primewise to ``S_WB^-1``.

    ``collides_with_extra_form`` means ``p`` divides ``Delta_L``.  Then
    ``omega*=omega``; otherwise ``omega*=omega+1``.  The common factor
    ``(1-1/p)^k`` cancels in the ratio.
    """

    _validate_local_inputs(k, prime, omega)
    if not isinstance(collides_with_extra_form, bool):
        raise ValueError("collides_with_extra_form must be boolean")

    omega_star = omega if collides_with_extra_form else omega + 1
    g_star = exact_star_denominator(prime, omega_star)
    exact_numerator = Fraction(1) + Fraction(omega, 1) / g_star
    singular_inverse_numerator = Fraction(1) + Fraction(
        omega,
        prime - omega,
    )
    ratio = exact_numerator / singular_inverse_numerator

    if collides_with_extra_form:
        comparison = Fraction(1) + Fraction(
            2 * omega * (omega - 1),
            prime * (prime - omega),
        )
    else:
        comparison = Fraction(1) + Fraction(
            omega * ((2 * omega + 1) * (prime - omega) - 1),
            prime * (prime - omega - 1) ** 2,
        )
    excess = ratio - 1
    upper = Fraction(4 * k * k, prime * prime)
    return LocalEulerCertificate(
        k=k,
        prime=prime,
        omega=omega,
        omega_star=omega_star,
        exact_factor=ratio,
        comparison_factor=comparison,
        exact_excess=excess,
        excess_upper_bound=upper,
        identity_verified=ratio == comparison,
        upper_bound_verified=Fraction(0) <= excess <= upper,
    )


def euler_tail_certificate(k: int, cutoff: int | None = None) -> EulerTailCertificate:
    """Return analytic product bounds beyond ``cutoff``.

    For every integer cutoff ``Y >= 2*k^2``, comparison with all integers
    gives ``sum_{p>Y} 1/p^2 <= 1/Y``.  Consequently the source-(9.64)
    product and the sharp ``r0`` product each have log tail at most ``4k/Y``;
    the canonical/singular-series ratio has log tail at most ``4k^2/Y``.

    At the natural cutoff ``Y=2*k^2`` the final two products in (9.66) are
    at most ``exp(2+2/k) * S_WB(L)^(-1)``.  Including the squared (9.64)
    factor gives ``exp(2+6/k) * S_WB(L)^(-1)``.
    """

    _validate_k(k)
    if cutoff is None:
        cutoff = 2 * k * k
    if isinstance(cutoff, bool) or not isinstance(cutoff, int):
        raise ValueError("cutoff must be an integer")
    if cutoff < 2 * k * k:
        raise ValueError("cutoff must be at least 2*k^2")

    pre_y = Fraction(4 * k, cutoff)
    sharp_r0 = Fraction(4 * k, cutoff)
    canonical = Fraction(4 * k * k, cutoff)
    final_two = sharp_r0 + canonical
    full_line_966 = 2 * pre_y + final_two
    return EulerTailCertificate(
        k=k,
        cutoff=cutoff,
        pre_y_log_tail_upper=pre_y,
        sharp_r0_log_tail_upper=sharp_r0,
        canonical_ratio_log_tail_upper=canonical,
        final_two_products_log_tail_upper=final_two,
        full_line_966_log_tail_upper=full_line_966,
        final_two_products_multiplier_upper=mp.exp(_fraction_to_mpf(final_two)),
        full_line_966_multiplier_upper=mp.exp(_fraction_to_mpf(full_line_966)),
        exact_local_factors_recovered=True,
        final_euler_products_closed=True,
        distribution_error_closed=False,
        proposition_94_closed=False,
        siv_07_closed=False,
        x_cert_ready=False,
    )


__all__ = [
    "EulerTailCertificate",
    "H1B2A1_MINIMUM_K",
    "LocalEulerCertificate",
    "canonical_ratio_local_certificate",
    "euler_tail_certificate",
    "exact_star_denominator",
    "pre_y_local_certificate",
    "sharp_r0_local_certificate",
]
