"""Exact finite composition for Jutila's Lemma 3 in the JL7 call.

Jutila, *On Linnik's constant* (1977), printed pp. 48--49 defines
``h(d; r, r')`` by a finite Euler product and states two conclusions for
``f(n) = mu(n) * phi(n)``.  The actual off-diagonal call on printed p. 53
uses

    sum_{r,r' <= R}' (r*r')^(-1) * sum_d |h(d; r, r')|,

where the prime denotes positive square-free integers coprime to ``q``.

This module expands the finite local factors exactly and verifies the safe
calculator envelope

    H_q(R) < 3 * R^2.

For an integer endpoint ``K = floor(R)``, the proof first bounds the outer
one-variable sum by ``(5/3) * K`` using a reciprocal-square partial sum;
squaring gives ``25/9 * K^2 < 3 * K^2 <= 3 * R^2``.

The code is a finite exact-arithmetic checker.  It does not prove Jutila's
analytic density theorem, the principal residue term, terminal absorption,
PAP-11, DEP-R09, the fixed Sono coefficient, or a numerical X_cert.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
from math import gcd


LEMMA3_OUTER_COEFFICIENT = Fraction(5, 3)
LEMMA3_PAIR_COEFFICIENT = Fraction(3, 1)


def _positive_integer(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def factorization(n: int) -> dict[int, int]:
    """Return the prime factorization of a positive integer."""

    n = _positive_integer(n, "n")
    remaining = n
    factors: dict[int, int] = {}
    prime = 2
    while prime * prime <= remaining:
        while remaining % prime == 0:
            factors[prime] = factors.get(prime, 0) + 1
            remaining //= prime
        prime = 3 if prime == 2 else prime + 2
    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1
    return factors


def is_squarefree(n: int) -> bool:
    """Return whether ``n`` is square-free; 1 is square-free."""

    return all(exponent == 1 for exponent in factorization(n).values())


def positive_divisors(n: int) -> tuple[int, ...]:
    """Return all positive divisors of ``n`` in increasing order."""

    factors = factorization(n)
    divisors = [1]
    for prime, exponent in factors.items():
        powers = [prime**power for power in range(exponent + 1)]
        divisors = [divisor * power for divisor in divisors for power in powers]
    return tuple(sorted(divisors))


def euler_totient(n: int) -> int:
    """Return Euler's totient using the exact prime factorization."""

    n = _positive_integer(n, "n")
    result = n
    for prime in factorization(n):
        result = result // prime * (prime - 1)
    return result


def eligible_r_values(endpoint_k: int, modulus_q: int) -> tuple[int, ...]:
    """Return Jutila's primed ``r <= K`` family."""

    endpoint_k = _positive_integer(endpoint_k, "endpoint_k")
    modulus_q = _positive_integer(modulus_q, "modulus_q")
    return tuple(
        r
        for r in range(1, endpoint_k + 1)
        if is_squarefree(r) and gcd(r, modulus_q) == 1
    )


def h_coefficients(r: int, r_prime: int) -> dict[int, int]:
    """Expand the exact finite Euler product defining ``h(d; r, r')``.

    For ``f(p) = mu(p) * phi(p) = -(p-1)``, a prime dividing exactly one
    of ``r`` and ``r'`` contributes ``1 - p*p^(-s)``.  A prime dividing
    both contributes ``1 + p*(p-2)*p^(-s)``.  Both inputs must be
    square-free, as in Jutila's primed sums.
    """

    r = _positive_integer(r, "r")
    r_prime = _positive_integer(r_prime, "r_prime")
    if not is_squarefree(r) or not is_squarefree(r_prime):
        raise ValueError("r and r_prime must be square-free")

    r_factors = set(factorization(r))
    r_prime_factors = set(factorization(r_prime))
    coefficients = {1: 1}
    for prime in sorted(r_factors | r_prime_factors):
        local_coefficient = (
            prime * (prime - 2)
            if prime in r_factors and prime in r_prime_factors
            else -prime
        )
        previous = tuple(coefficients.items())
        if local_coefficient != 0:
            for divisor, coefficient in previous:
                coefficients[divisor * prime] = coefficient * local_coefficient
    return dict(sorted(coefficients.items()))


def absolute_h_sum(r: int, r_prime: int) -> int:
    """Return ``sum_d |h(d; r, r')|`` exactly."""

    return sum(abs(coefficient) for coefficient in h_coefficients(r, r_prime).values())


def absolute_h_sum_local_product(r: int, r_prime: int) -> int:
    """Return the exact local-product formula for the absolute h-sum."""

    r = _positive_integer(r, "r")
    r_prime = _positive_integer(r_prime, "r_prime")
    if not is_squarefree(r) or not is_squarefree(r_prime):
        raise ValueError("r and r_prime must be square-free")
    r_factors = set(factorization(r))
    r_prime_factors = set(factorization(r_prime))
    result = 1
    for prime in r_factors ^ r_prime_factors:
        result *= prime + 1
    for prime in r_factors & r_prime_factors:
        result *= (prime - 1) ** 2
    return result


def lemma3_source_product_bound(r: int, r_prime: int) -> int:
    """Return Jutila Lemma 3's printed product upper bound."""

    r = _positive_integer(r, "r")
    r_prime = _positive_integer(r_prime, "r_prime")
    if not is_squarefree(r) or not is_squarefree(r_prime):
        raise ValueError("r and r_prime must be square-free")
    result = 1
    for prime in factorization(r):
        result *= prime + 1
    for prime in factorization(r_prime):
        result *= prime + 1
    return result


def reciprocal_h_identity(r: int, r_prime: int) -> Fraction:
    """Return ``sum_d h(d; r, r') / d`` exactly."""

    return sum(
        (Fraction(coefficient, divisor) for divisor, coefficient in h_coefficients(r, r_prime).items()),
        start=Fraction(0, 1),
    )


def expected_reciprocal_h_identity(r: int, r_prime: int) -> Fraction:
    """Return ``delta_(r,r') * phi(r)`` from Jutila Lemma 3."""

    r = _positive_integer(r, "r")
    r_prime = _positive_integer(r_prime, "r_prime")
    return Fraction(euler_totient(r), 1) if r == r_prime else Fraction(0, 1)


def normalized_pair_absolute_sum(r: int, r_prime: int) -> Fraction:
    """Return the exact normalized pair contribution."""

    return Fraction(absolute_h_sum(r, r_prime), r * r_prime)


def outer_lemma3_weight(r: int) -> Fraction:
    """Return ``prod_(p|r)(p+1)/r`` for square-free ``r``."""

    r = _positive_integer(r, "r")
    if not is_squarefree(r):
        raise ValueError("r must be square-free")
    numerator = 1
    for prime in factorization(r):
        numerator *= prime + 1
    return Fraction(numerator, r)


def reciprocal_divisor_weight(r: int) -> Fraction:
    """Return ``sum_(d|r) 1/d``; equal to the outer weight when r is square-free."""

    return sum((Fraction(1, divisor) for divisor in positive_divisors(r)), Fraction(0, 1))


def outer_weight_sum(endpoint_k: int, modulus_q: int) -> Fraction:
    """Return the actual one-variable primed outer sum."""

    return sum(
        (outer_lemma3_weight(r) for r in eligible_r_values(endpoint_k, modulus_q)),
        Fraction(0, 1),
    )


def all_integer_divisor_envelope(endpoint_k: int) -> Fraction:
    """Return ``sum_(d<=K) floor(K/d)/d`` after finite double counting."""

    endpoint_k = _positive_integer(endpoint_k, "endpoint_k")
    return sum(
        (Fraction(endpoint_k // divisor, divisor) for divisor in range(1, endpoint_k + 1)),
        Fraction(0, 1),
    )


def reciprocal_square_partial_sum(endpoint_k: int) -> Fraction:
    """Return the exact finite Basel partial sum through ``K``."""

    endpoint_k = _positive_integer(endpoint_k, "endpoint_k")
    return sum(
        (Fraction(1, divisor * divisor) for divisor in range(1, endpoint_k + 1)),
        Fraction(0, 1),
    )


def actual_absolute_composition(endpoint_k: int, modulus_q: int) -> Fraction:
    """Return the exact finite JL7 Lemma 3 absolute composition."""

    family = eligible_r_values(endpoint_k, modulus_q)
    return sum(
        (normalized_pair_absolute_sum(r, r_prime) for r in family for r_prime in family),
        Fraction(0, 1),
    )


def source_product_composition_bound(endpoint_k: int, modulus_q: int) -> Fraction:
    """Return the square of the actual outer source-product sum."""

    outer = outer_weight_sum(endpoint_k, modulus_q)
    return outer * outer


def outer_rational_bound(endpoint_k: int) -> Fraction:
    """Return ``(5/3)K``, the rational outer-sum envelope."""

    endpoint_k = _positive_integer(endpoint_k, "endpoint_k")
    return LEMMA3_OUTER_COEFFICIENT * endpoint_k


def pair_rational_bound(endpoint_k: int) -> Fraction:
    """Return ``3K^2``, the calculator-safe pair envelope."""

    endpoint_k = _positive_integer(endpoint_k, "endpoint_k")
    return LEMMA3_PAIR_COEFFICIENT * endpoint_k * endpoint_k


@dataclass(frozen=True)
class JutilaJL7Lemma3Diagnostic:
    endpoint_k: int
    modulus_q: int
    eligible_r_count: int
    outer_weight_sum: str
    all_integer_divisor_envelope: str
    k_times_reciprocal_square_partial_sum: str
    five_thirds_k_bound: str
    actual_absolute_composition: str
    source_product_composition_bound: str
    three_k_squared_bound: str
    reciprocal_identity_verified: bool
    local_absolute_product_verified: bool
    printed_source_product_bound_verified: bool
    outer_double_count_verified: bool
    reciprocal_square_bound_verified_numerically: bool
    pair_composition_verified: bool
    lemma3_actual_inputs_parameterized_explicit: bool
    residue_multiplier_explicit: bool
    terminal_density_closed: bool
    pap_11_closed: bool
    numerical_x_cert_ready: bool


def build_diagnostic(endpoint_k: int, modulus_q: int) -> JutilaJL7Lemma3Diagnostic:
    """Build an exact finite diagnostic for a small or moderate endpoint."""

    endpoint_k = _positive_integer(endpoint_k, "endpoint_k")
    modulus_q = _positive_integer(modulus_q, "modulus_q")
    family = eligible_r_values(endpoint_k, modulus_q)
    reciprocal_identity_verified = all(
        reciprocal_h_identity(r, r_prime) == expected_reciprocal_h_identity(r, r_prime)
        for r in family
        for r_prime in family
    )
    local_absolute_product_verified = all(
        absolute_h_sum(r, r_prime) == absolute_h_sum_local_product(r, r_prime)
        for r in family
        for r_prime in family
    )
    printed_source_product_bound_verified = all(
        absolute_h_sum(r, r_prime) <= lemma3_source_product_bound(r, r_prime)
        for r in family
        for r_prime in family
    )
    outer = outer_weight_sum(endpoint_k, modulus_q)
    divisor_envelope = all_integer_divisor_envelope(endpoint_k)
    reciprocal_square_scaled = endpoint_k * reciprocal_square_partial_sum(endpoint_k)
    outer_bound = outer_rational_bound(endpoint_k)
    actual = actual_absolute_composition(endpoint_k, modulus_q)
    source_bound = source_product_composition_bound(endpoint_k, modulus_q)
    pair_bound = pair_rational_bound(endpoint_k)
    return JutilaJL7Lemma3Diagnostic(
        endpoint_k=endpoint_k,
        modulus_q=modulus_q,
        eligible_r_count=len(family),
        outer_weight_sum=str(outer),
        all_integer_divisor_envelope=str(divisor_envelope),
        k_times_reciprocal_square_partial_sum=str(reciprocal_square_scaled),
        five_thirds_k_bound=str(outer_bound),
        actual_absolute_composition=str(actual),
        source_product_composition_bound=str(source_bound),
        three_k_squared_bound=str(pair_bound),
        reciprocal_identity_verified=reciprocal_identity_verified,
        local_absolute_product_verified=local_absolute_product_verified,
        printed_source_product_bound_verified=printed_source_product_bound_verified,
        outer_double_count_verified=(outer <= divisor_envelope <= reciprocal_square_scaled),
        reciprocal_square_bound_verified_numerically=(reciprocal_square_scaled < outer_bound),
        pair_composition_verified=(actual <= source_bound < pair_bound),
        lemma3_actual_inputs_parameterized_explicit=True,
        residue_multiplier_explicit=False,
        terminal_density_closed=False,
        pap_11_closed=False,
        numerical_x_cert_ready=False,
    )


def diagnostic_as_dict(endpoint_k: int, modulus_q: int) -> dict[str, object]:
    """Return a JSON-serializable diagnostic mapping."""

    return asdict(build_diagnostic(endpoint_k, modulus_q))
