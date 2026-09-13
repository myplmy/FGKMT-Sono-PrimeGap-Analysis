"""Finite envelopes for Jutila's printed-p.53 principal residue.

The residue left after shifting the Mellin contour contains two exact
structures: Jutila Lemma 3 forces ``r = r_prime``, and the selected zeros
belonging to one Dirichlet character are ``Delta``-well-spaced, where
``Delta = 1 / log(D)``.  This module evaluates the resulting finite objects
and records the conservative calculator-safe bound

    residue < 52 * J * (phi(q) / q)^2 * x^(2-2*alpha) * log(D)^2

for the actual range ``0 < theta <= 1/21`` and ``log(D) >= theta^(-2)``.

It is not a proof of Jutila's terminal density theorem, the averaged
primitive-character replay, PAP-11, DEP-R09, the fixed Sono coefficient, or
a numerical X_cert.  Those downstream flags stay false deliberately.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
from math import gcd
from typing import Iterable

import mpmath as mp

from source.dep_r09_jutila_jl7_lemma3 import (
    eligible_r_values,
    euler_totient,
)


THETA_MAX = Fraction(1, 21)
GAMMA_ENVELOPE = Fraction(3, 1)
DIAGONAL_MASS_COEFFICIENT = Fraction(7, 1)
OFF_DIAGONAL_KERNEL_COEFFICIENT = Fraction(7, 1)
SPACING_ROW_COEFFICIENT = Fraction(10, 3)
RESIDUE_ROW_COEFFICIENT = Fraction(91, 1)
DIAGONAL_R_SUM_COEFFICIENT = Fraction(12, 1)
RESIDUE_MULTIPLIER = Fraction(52, 1)


def _mp(value: object) -> mp.mpf:
    if isinstance(value, Fraction):
        return mp.mpf(value.numerator) / value.denominator
    return mp.mpf(value)


def _validated_parameters(theta: object, log_d: object) -> tuple[mp.mpf, mp.mpf]:
    theta_mp = _mp(theta)
    log_d_mp = _mp(log_d)
    if not mp.isfinite(theta_mp) or theta_mp <= 0 or theta_mp > _mp(THETA_MAX):
        raise ValueError("theta must satisfy 0 < theta <= 1/21")
    required_log_d = 1 / (theta_mp * theta_mp)
    if not mp.isfinite(log_d_mp) or (
        log_d_mp < required_log_d and not mp.almosteq(log_d_mp, required_log_d)
    ):
        raise ValueError("log_d must satisfy log_d >= theta^(-2)")
    return theta_mp, log_d_mp


def phi_over_q(modulus_q: int) -> Fraction:
    """Return ``phi(q)/q`` exactly."""

    if isinstance(modulus_q, bool) or not isinstance(modulus_q, int) or modulus_q < 1:
        raise ValueError("modulus_q must be a positive integer")
    return Fraction(euler_totient(modulus_q), modulus_q)


def residue_intervals(theta: object, log_d: object) -> tuple[mp.mpf, ...]:
    """Return ``a,b,c,d`` for the two integrations on printed p.53."""

    theta_mp, log_d_mp = _validated_parameters(theta, log_d)
    log_z1 = (mp.mpf("0.5") + 7 * theta_mp) * log_d_mp
    log_x = (1 + 12 * theta_mp) * log_d_mp + 2 * mp.log(log_d_mp)
    return (
        (1 - theta_mp) * log_z1,
        log_z1,
        log_x,
        (1 + theta_mp) * log_x,
    )


def interval_lengths(theta: object, log_d: object) -> tuple[mp.mpf, mp.mpf]:
    """Return the xi- and eta-interval lengths ``A`` and ``B``."""

    a, b, c, d = residue_intervals(theta, log_d)
    return b - a, d - c


def ladder_mass_at_zero(theta: object, log_d: object) -> mp.mpf:
    """Return the removable ``z=0`` value of the integrated ladder kernel."""

    a, b, c, d = residue_intervals(theta, log_d)
    length_a = b - a
    length_b = d - c
    return length_a * length_b * ((c + d - a - b) / 2)


def ladder_kernel(z: object, theta: object, log_d: object) -> mp.mpc:
    r"""Evaluate the integrated exponential ladder kernel stably.

    For ``z != 0`` this is

    ``[B(e^(-az)-e^(-bz))-A(e^(-cz)-e^(-dz))]/z^2``.

    At zero the analytic continuation is the positive triple-integral mass.
    """

    z_mp = mp.mpc(z)
    a, b, c, d = residue_intervals(theta, log_d)
    length_a = b - a
    length_b = d - c
    if z_mp == 0:
        return mp.mpc(ladder_mass_at_zero(theta, log_d))
    first_difference = -mp.exp(-a * z_mp) * mp.expm1(-length_a * z_mp)
    second_difference = -mp.exp(-c * z_mp) * mp.expm1(-length_b * z_mp)
    return (length_b * first_difference - length_a * second_difference) / (z_mp * z_mp)


def ladder_kernel_by_quadrature(z: object, theta: object, log_d: object) -> mp.mpc:
    """Independent one-dimensional quadrature used only as a test oracle.

    Fubini reduces the triple integral to two unrelated numerical integrals;
    unlike :func:`ladder_kernel`, this path does not use the exponential
    endpoint closed form.
    """

    z_mp = mp.mpc(z)
    a, b, c, d = residue_intervals(theta, log_d)

    if z_mp == 0:
        return mp.mpc(ladder_mass_at_zero(theta, log_d))
    length_a = b - a
    length_b = d - c
    xi_integral = mp.quad(lambda xi: mp.exp(-xi * z_mp), [a, b])
    eta_integral = mp.quad(lambda eta: mp.exp(-eta * z_mp), [c, d])
    return (length_b * xi_integral - length_a * eta_integral) / z_mp


def cancelled_residue_pair(z: object, theta: object, log_d: object) -> mp.mpc:
    """Return the pole-cancelled pair kernel ``-Gamma(1-z) K(z)``."""

    z_mp = mp.mpc(z)
    return -mp.gamma(1 - z_mp) * ladder_kernel(z_mp, theta, log_d)


def selected_height_inverse_square_row(
    heights: Iterable[object],
    row_index: int,
    log_d: object,
) -> mp.mpf:
    """Return one same-character off-diagonal height row exactly.

    Heights must be strictly increasing and adjacent heights must differ by
    at least ``Delta=1/log(D)``.  This is the property supplied by one of
    Jutila's even/odd selected systems.
    """

    log_d_mp = _mp(log_d)
    if not mp.isfinite(log_d_mp) or log_d_mp <= 0:
        raise ValueError("log_d must be positive")
    values = tuple(_mp(value) for value in heights)
    if not values or isinstance(row_index, bool) or not isinstance(row_index, int):
        raise ValueError("heights must be nonempty and row_index must be an integer")
    if row_index < 0 or row_index >= len(values):
        raise ValueError("row_index is outside heights")
    delta = 1 / log_d_mp
    for left, right in zip(values, values[1:]):
        spacing = right - left
        if not (
            right > left
            and (spacing >= delta or mp.almosteq(spacing, delta))
        ):
            raise ValueError("heights must be strictly increasing and Delta-well-spaced")
    center = values[row_index]
    return mp.fsum(
        1 / ((height - center) ** 2)
        for index, height in enumerate(values)
        if index != row_index
    )


def spacing_row_envelope(log_d: object) -> mp.mpf:
    """Return ``(10/3) log(D)^2`` for one same-character row."""

    log_d_mp = _mp(log_d)
    if not mp.isfinite(log_d_mp) or log_d_mp <= 0:
        raise ValueError("log_d must be positive")
    return _mp(SPACING_ROW_COEFFICIENT) * log_d_mp**2


def diagonal_r_sum(endpoint_k: int, modulus_q: int) -> Fraction:
    """Return ``sum'_(r<=K) phi(r)/r^2`` exactly."""

    return sum(
        (Fraction(euler_totient(r), r * r) for r in eligible_r_values(endpoint_k, modulus_q)),
        Fraction(0, 1),
    )


def local_excluded_prime_ratio(prime: int, lambda_value: object) -> mp.mpf:
    """Return ``(1-p^(-1-lambda))/(1-p^(-1))``."""

    if isinstance(prime, bool) or not isinstance(prime, int) or prime < 2:
        raise ValueError("prime must be an integer at least 2")
    lambda_mp = _mp(lambda_value)
    if not mp.isfinite(lambda_mp) or lambda_mp <= 0:
        raise ValueError("lambda_value must be positive")
    return (1 - mp.power(prime, -1 - lambda_mp)) / (1 - mp.mpf(1) / prime)


def excluded_prime_ratio_product(modulus_q: int, log_d: object) -> mp.mpf:
    """Return the finite excluded-prime product in the Rankin comparison."""

    if isinstance(modulus_q, bool) or not isinstance(modulus_q, int) or modulus_q < 1:
        raise ValueError("modulus_q must be a positive integer")
    log_d_mp = _mp(log_d)
    if not mp.isfinite(log_d_mp) or log_d_mp <= 0:
        raise ValueError("log_d must be positive")
    remaining = modulus_q
    prime = 2
    result = mp.mpf(1)
    while prime * prime <= remaining:
        if remaining % prime == 0:
            result *= local_excluded_prime_ratio(prime, 1 / log_d_mp)
            while remaining % prime == 0:
                remaining //= prime
        prime = 3 if prime == 2 else prime + 2
    if remaining > 1:
        result *= local_excluded_prime_ratio(remaining, 1 / log_d_mp)
    return result


def diagonal_r_sum_envelope(modulus_q: int, log_d: object) -> mp.mpf:
    """Return the rational safe envelope ``12*(phi(q)/q)*log(D)``."""

    log_d_mp = _mp(log_d)
    if not mp.isfinite(log_d_mp) or log_d_mp <= 0:
        raise ValueError("log_d must be positive")
    return _mp(DIAGONAL_R_SUM_COEFFICIENT * phi_over_q(modulus_q)) * log_d_mp


def residue_coefficient_at_theta(theta: object) -> mp.mpf:
    """Return the pre-endpoint coefficient ``12*91*theta``."""

    theta_mp = _mp(theta)
    if not mp.isfinite(theta_mp) or theta_mp <= 0 or theta_mp > _mp(THETA_MAX):
        raise ValueError("theta must satisfy 0 < theta <= 1/21")
    return _mp(DIAGONAL_R_SUM_COEFFICIENT * RESIDUE_ROW_COEFFICIENT) * theta_mp


@dataclass(frozen=True)
class JutilaJL7ResidueDiagnostic:
    theta: str
    log_d: str
    modulus_q: int
    endpoint_k: int
    xi_length_over_theta_log_d: str
    eta_length_over_theta_log_d: str
    maximum_span_over_log_d: str
    zero_mass_over_theta_squared_log_d_cubed: str
    finite_diagonal_r_sum: str
    diagonal_r_sum_envelope: str
    excluded_prime_ratio_product: str
    residue_coefficient_at_theta: str
    residue_multiplier: int
    interval_geometry_verified: bool
    diagonal_r_sum_verified: bool
    excluded_prime_product_verified: bool
    residue_well_spacing_multiplier_explicit: bool
    terminal_density_closed: bool
    averaged_primitive_density_closed: bool
    pap_11_closed: bool
    numerical_x_cert_ready: bool


def build_diagnostic(
    endpoint_k: int = 100,
    modulus_q: int = 30,
    theta: object = THETA_MAX,
    log_d: object = 441,
) -> JutilaJL7ResidueDiagnostic:
    """Build a small finite diagnostic without running any prime experiment."""

    theta_mp, log_d_mp = _validated_parameters(theta, log_d)
    a, b, c, d = residue_intervals(theta_mp, log_d_mp)
    length_a, length_b = b - a, d - c
    mass = ladder_mass_at_zero(theta_mp, log_d_mp)
    finite_r_sum = diagonal_r_sum(endpoint_k, modulus_q)
    r_envelope = diagonal_r_sum_envelope(modulus_q, log_d_mp)
    excluded_product = excluded_prime_ratio_product(modulus_q, log_d_mp)
    geometry_verified = (
        length_a <= _mp(Fraction(5, 6)) * theta_mp * log_d_mp
        and length_b <= _mp(Fraction(18, 7)) * theta_mp * log_d_mp
        and d - a < 3 * log_d_mp
        and mass < 7 * theta_mp**2 * log_d_mp**3
    )
    return JutilaJL7ResidueDiagnostic(
        theta=mp.nstr(theta_mp, 30),
        log_d=mp.nstr(log_d_mp, 30),
        modulus_q=modulus_q,
        endpoint_k=endpoint_k,
        xi_length_over_theta_log_d=mp.nstr(length_a / (theta_mp * log_d_mp), 30),
        eta_length_over_theta_log_d=mp.nstr(length_b / (theta_mp * log_d_mp), 30),
        maximum_span_over_log_d=mp.nstr((d - a) / log_d_mp, 30),
        zero_mass_over_theta_squared_log_d_cubed=mp.nstr(
            mass / (theta_mp**2 * log_d_mp**3), 30
        ),
        finite_diagonal_r_sum=str(finite_r_sum),
        diagonal_r_sum_envelope=mp.nstr(r_envelope, 30),
        excluded_prime_ratio_product=mp.nstr(excluded_product, 30),
        residue_coefficient_at_theta=mp.nstr(residue_coefficient_at_theta(theta_mp), 30),
        residue_multiplier=RESIDUE_MULTIPLIER.numerator,
        interval_geometry_verified=bool(geometry_verified),
        diagonal_r_sum_verified=(mp.mpf(finite_r_sum.numerator) / finite_r_sum.denominator < r_envelope),
        excluded_prime_product_verified=(excluded_product <= mp.e),
        residue_well_spacing_multiplier_explicit=True,
        terminal_density_closed=False,
        averaged_primitive_density_closed=False,
        pap_11_closed=False,
        numerical_x_cert_ready=False,
    )


def diagnostic_as_dict(**kwargs: object) -> dict[str, object]:
    """Return a JSON-serializable diagnostic mapping."""

    return asdict(build_diagnostic(**kwargs))
