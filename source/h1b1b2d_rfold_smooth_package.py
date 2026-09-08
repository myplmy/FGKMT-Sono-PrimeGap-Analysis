"""Fail-closed explicit composition package for Maynard Lemma 8.4.

The analytic proof and the exact scope of this module are recorded in
``docs/method/theory/24_Sono_FMT_H1b1b2d_rfold_smooth_composition.md``.
The module evaluates conservative consequences of that proof.  It does not
claim that every Section 8 application is closed, certify Proposition 6.1,
or compute the theorem threshold ``X_cert``.

The key normalization is support aware.  A profile supported on ``[0, s]``
is summed by applying the one-dimensional estimate with ``z = R**s``.  Thus

    omega_s(G) = sup(|G| + s |G'|) / integral(G)

is the relevant dimensionless norm.  This avoids silently treating the wide
``psi(t/2)`` profile in ``F_2`` as if it were supported on ``[0, 1]``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import reduce
from operator import mul

import mpmath as mp

from source.h1b1b2_local_factor_lower_bound import (
    APPLICATION_L1015_R_W_M,
    APPLICATION_L1096_W0,
    APPLICATION_L1135_CANONICAL_FACTOR,
    APPLICATION_L1135_W0_FACTOR,
    APPLICATION_L1232_CANONICAL,
    APPLICATION_L620_D_W,
    APPLICATION_L737_CANONICAL,
    APPLICATION_L752_CANONICAL,
    APPLICATION_L885_W_PRIME,
    APPLICATION_L905_W_PRIME,
    APPLICATION_L995_A_M_W_B_R,
    MAYNARD_APPLICATION_EXCLUSION_IDS,
    maynard_uniform_application_log_q_upper,
)
from source.h1b1b2b_corrected_wirsing import (
    summatory_multiplier,
    weighted_lemma83_multiplier,
)
from source.h1b1b2c_actual_parameter_package import (
    H1B1B2C_MAYNARD_A1_GAP,
    H1B1B2C_UPPER_DISCREPANCY_A2,
    lower_discrepancy_l,
)
from source.h1b1a_explicit_package import H1B1A_CUTOFF_SLOPE_BOUND


PROFILE_N = "N"
PROFILE_N2 = "N2"
PROFILE_W = "W"
PROFILE_W2 = "W2"
PROFILE_NW = "NW"

APPLICATION_MODE_SMOOTH_COMPOSED = "SMOOTH_COMPOSITION_PARAMETERIZED_EXPLICIT"
APPLICATION_MODE_SHARP_SUMMATORY = "SHARP_CUTOFF_SUMMATORY_PARAMETERIZED_EXPLICIT"
APPLICATION_MODE_H_SQUARE_BYPASS_SCALAR_OPEN = (
    "H_SQUARE_BYPASS_EXPLICIT_SCALAR_MULTIPLIER_OPEN"
)

H1B1B2D_MINIMUM_TARGET_K = 36
H1B1B2D_PLATEAU_NUMERATOR = 9
H1B1B2D_PLATEAU_DENOMINATOR = 10


@dataclass(frozen=True)
class ProfileSpec:
    """One nonnegative one-variable profile occurring after tensor expansion."""

    name: str
    support_scale: mp.mpf
    psi_power: int
    denominator_power: int


@dataclass(frozen=True)
class ProfileNormCertificate:
    """A conservative support-scaled C1 norm certificate."""

    spec: ProfileSpec
    t_k: mp.mpf
    integral_lower_bound: mp.mpf
    scaled_c1_numerator_upper_bound: mp.mpf
    scaled_omega_upper_bound: mp.mpf


@dataclass(frozen=True)
class ApplicationSmoothSpec:
    """Smooth-function status for one source-traced analytic subapplication."""

    application_id: str
    source_locator: str
    mode: str
    tensor_family: str
    dimension: str
    blocker: str | None


@dataclass(frozen=True)
class RfoldErrorCertificate:
    """Error normalized by the nonnegative reference-profile integral.

    With a coupled cutoff such as ``psi(sum(t_i))``, this is not necessarily
    a relative error against that smaller coupled main integral.  It is the
    absolute error coefficient on the product-profile envelope used in
    Maynard's Lemma 8.4.
    """

    application_id: str
    k: int
    log_r: mp.mpf
    log_lambda_star: mp.mpf
    l_plus_one: mp.mpf
    kappa_sum_upper_bound: mp.mpf
    one_step_multiplier: mp.mpf
    delta_sum_upper_bound: mp.mpf
    product_error_upper_bound: mp.mpf
    exponential_error_upper_bound: mp.mpf
    linearized_error_upper_bound: mp.mpf | None
    linearization_gate_passed: bool
    theorem_claimed: bool
    siv_07_closed: bool
    x_cert_ready: bool


@dataclass(frozen=True)
class CommonSmoothGateCertificate:
    """An explicit but deliberately coarse sufficient log(R) cutoff."""

    k: int
    alpha: mp.mpf
    theta: mp.mpf
    kappa_max: mp.mpf
    weighted_multiplier: mp.mpf
    e_coefficient: mp.mpf
    lambda_affine_constant: mp.mpf
    lambda_affine_slope: mp.mpf
    log_r_sufficient: mp.mpf
    direct_gate_right_hand_side: mp.mpf
    gate_verified: bool
    all_actual_calls_closed: bool
    siv_07_closed: bool
    x_cert_ready: bool


MAYNARD_APPLICATION_SMOOTH_SPECS = (
    ApplicationSmoothSpec(
        APPLICATION_L620_D_W,
        "Maynard source lines 620-625",
        APPLICATION_MODE_SMOOTH_COMPOSED,
        "F = psi(sum t_i) product N(t_i)",
        "k",
        None,
    ),
    ApplicationSmoothSpec(
        APPLICATION_L737_CANONICAL,
        "Maynard source lines 723-739",
        APPLICATION_MODE_SMOOTH_COMPOSED,
        "F2^2 expanded into k^2 nonnegative tensor terms",
        "k",
        None,
    ),
    ApplicationSmoothSpec(
        APPLICATION_L752_CANONICAL,
        "Maynard source lines 750-760",
        APPLICATION_MODE_SMOOTH_COMPOSED,
        "F^2 = psi(sum t_i)^2 product N(t_i)^2",
        "k",
        None,
    ),
    ApplicationSmoothSpec(
        APPLICATION_L885_W_PRIME,
        "Maynard source lines 883-892",
        APPLICATION_MODE_SMOOTH_COMPOSED,
        "F2(t_m=0)^2 sliced tensor expansion",
        "k-1",
        None,
    ),
    ApplicationSmoothSpec(
        APPLICATION_L905_W_PRIME,
        "Maynard source lines 903-916",
        APPLICATION_MODE_H_SQUARE_BYPASS_SCALAR_OPEN,
        "square sum bypassed through A^2, A*B and B^2 tensor families",
        "k-1",
        "The functional C1 requirement is bypassed, but source lines 986-999 do not give a numerical scalar pointwise remainder multiplier.",
    ),
    ApplicationSmoothSpec(
        APPLICATION_L995_A_M_W_B_R,
        "Maynard source lines 995-999",
        APPLICATION_MODE_SMOOTH_COMPOSED,
        "one-variable F2 = coefficient*N + coefficient*W",
        "1",
        None,
    ),
    ApplicationSmoothSpec(
        APPLICATION_L1015_R_W_M,
        "Maynard source lines 1015-1026",
        APPLICATION_MODE_SMOOTH_COMPOSED,
        "one-variable F with coupled cutoff psi",
        "1",
        None,
    ),
    ApplicationSmoothSpec(
        APPLICATION_L1096_W0,
        "Maynard source lines 1092-1098",
        APPLICATION_MODE_SHARP_SUMMATORY,
        "indicator r0 < x^xi",
        "1",
        None,
    ),
    ApplicationSmoothSpec(
        APPLICATION_L1135_W0_FACTOR,
        "Maynard source lines 1112-1141, r0 factor",
        APPLICATION_MODE_SHARP_SUMMATORY,
        "indicator r0 < x^xi",
        "1",
        None,
    ),
    ApplicationSmoothSpec(
        APPLICATION_L1135_CANONICAL_FACTOR,
        "Maynard source lines 1112-1141, r-vector factor",
        APPLICATION_MODE_SMOOTH_COMPOSED,
        "F^2 = psi(sum t_i)^2 product N(t_i)^2",
        "k",
        None,
    ),
    ApplicationSmoothSpec(
        APPLICATION_L1232_CANONICAL,
        "Maynard source lines 1228-1237",
        APPLICATION_MODE_SMOOTH_COMPOSED,
        "F2^2 expanded into k^2 nonnegative tensor terms",
        "k",
        None,
    ),
)

# In these F2^2 applications, any tensor term containing the support-[0,2]
# W^2 profile must sum that coordinate first.  The current coordinate never
# enters the excluded integer Q_j, so all remaining coordinates then have
# support at most R and the H1b-1b-2c Lambda_star bound remains valid.
WIDE_SUPPORT_FIRST_APPLICATIONS = frozenset(
    {
        APPLICATION_L737_CANONICAL,
        APPLICATION_L885_W_PRIME,
        APPLICATION_L1232_CANONICAL,
    }
)


def _validate_k(k: int, *, target_range: bool = False) -> None:
    minimum = H1B1B2D_MINIMUM_TARGET_K if target_range else 2
    if isinstance(k, bool) or not isinstance(k, int) or k < minimum:
        raise ValueError(f"k must be an integer at least {minimum}")


def _positive_mpf(value: int | float | str | mp.mpf, name: str) -> mp.mpf:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be finite and positive")
    result = mp.mpf(value)
    if not mp.isfinite(result) or result <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def profile_spec(k: int, profile: str) -> ProfileSpec:
    """Return the exact support and powers for an actual Maynard profile."""

    _validate_k(k)
    u_k = 1 / mp.sqrt(k)
    mapping = {
        PROFILE_N: ProfileSpec(PROFILE_N, u_k, 1, 1),
        PROFILE_N2: ProfileSpec(PROFILE_N2, u_k, 2, 2),
        PROFILE_W: ProfileSpec(PROFILE_W, mp.mpf(2), 1, 1),
        PROFILE_W2: ProfileSpec(PROFILE_W2, mp.mpf(2), 2, 2),
        # On support of psi(t/U_k), t/2 <= 1/2, so psi(t/2)=1.
        PROFILE_NW: ProfileSpec(PROFILE_NW, u_k, 1, 2),
    }
    try:
        return mapping[profile]
    except KeyError as exc:
        raise ValueError(f"unknown profile: {profile}") from exc


def profile_norm_certificate(k: int, profile: str) -> ProfileNormCertificate:
    """Evaluate the proved lower integral and upper scaled-C1 bounds.

    For ``P(t)=psi(t/a)^m/(1+T_k*t)^q`` the project cutoff satisfies
    ``0<=psi<=1``, ``psi=1`` through ``0.9``, and ``|psi'|<=50``.  Hence

    ``integral(P) >= integral_0^(0.9a) (1+T_k*t)^(-q) dt``

    and

    ``sup(P + a*|P'|) <= 1 + 50*m + a*q*T_k``.
    """

    spec = profile_spec(k, profile)
    t_k = mp.mpf(k) * mp.log(k)
    plateau = (
        mp.mpf(H1B1B2D_PLATEAU_NUMERATOR)
        / H1B1B2D_PLATEAU_DENOMINATOR
        * spec.support_scale
    )
    if spec.denominator_power == 1:
        integral_lower = mp.log(1 + plateau * t_k) / t_k
    elif spec.denominator_power == 2:
        integral_lower = plateau / (1 + plateau * t_k)
    else:  # pragma: no cover - all project profiles are registered above
        raise AssertionError("unsupported denominator power")

    slope = mp.mpf(H1B1A_CUTOFF_SLOPE_BOUND.numerator) / mp.mpf(
        H1B1A_CUTOFF_SLOPE_BOUND.denominator
    )
    numerator = (
        1
        + slope * spec.psi_power
        + spec.support_scale * spec.denominator_power * t_k
    )
    return ProfileNormCertificate(
        spec=spec,
        t_k=t_k,
        integral_lower_bound=integral_lower,
        scaled_c1_numerator_upper_bound=numerator,
        scaled_omega_upper_bound=numerator / integral_lower,
    )


def _omega(k: int, profile: str) -> mp.mpf:
    return profile_norm_certificate(k, profile).scaled_omega_upper_bound


def f_kappa_sum(k: int) -> mp.mpf:
    """Return the sum of normalized error coefficients for ``F``."""

    _validate_k(k)
    u_k = 1 / mp.sqrt(k)
    phi_factor = 1 + 50 * u_k
    return k * phi_factor * _omega(k, PROFILE_N)


def f_squared_kappa_sum(k: int) -> mp.mpf:
    """Return the envelope coefficient for ``F^2``."""

    _validate_k(k)
    u_k = 1 / mp.sqrt(k)
    phi_factor = 1 + 100 * u_k
    return k * phi_factor * _omega(k, PROFILE_N2)


def f2_squared_kappa_sum(k: int) -> mp.mpf:
    """Return the worst ordered tensor term coefficient for ``F_2^2``."""

    _validate_k(k)
    diagonal = _omega(k, PROFILE_W2) + (k - 1) * _omega(k, PROFILE_N2)
    cross = 2 * _omega(k, PROFILE_NW) + (k - 2) * _omega(k, PROFILE_N2)
    return max(diagonal, cross)


def f2_squared_slice_kappa_sum(k: int) -> mp.mpf:
    """Return the worst tensor coefficient for ``F_2(t_m=0)^2``."""

    _validate_k(k)
    dimension = k - 1
    candidates = [dimension * _omega(k, PROFILE_N2)]
    if dimension >= 1:
        candidates.extend(
            [
                _omega(k, PROFILE_W2)
                + (dimension - 1) * _omega(k, PROFILE_N2),
                _omega(k, PROFILE_NW)
                + (dimension - 1) * _omega(k, PROFILE_N2),
            ]
        )
    if dimension >= 2:
        candidates.append(
            2 * _omega(k, PROFILE_NW)
            + (dimension - 2) * _omega(k, PROFILE_N2)
        )
    return max(candidates)


def f2_one_variable_kappa(k: int) -> mp.mpf:
    """Return the termwise bound for a one-variable slice of ``F_2``."""

    _validate_k(k)
    return max(_omega(k, PROFILE_N), _omega(k, PROFILE_W))


def f_one_variable_kappa(k: int) -> mp.mpf:
    """Return the support-scaled bound for a one-variable slice of ``F``."""

    _validate_k(k)
    u_k = 1 / mp.sqrt(k)
    return (1 + 50 * u_k) * _omega(k, PROFILE_N)


def application_kappa_term_families(
    k: int,
    application_id: str,
) -> tuple[tuple[mp.mpf, ...], ...]:
    """Return every tensor family needed for an exact product envelope.

    A nonnegative sum of tensor terms has relative error at most the largest
    relative error of its terms.  The wide ``W^2`` coordinate is listed first;
    summing it first is a required ordering that prevents its ``R^2`` support
    from entering a later excluded modulus.  The existing common
    ``Lambda_star`` therefore remains valid.
    """

    _validate_k(k)
    u_k = 1 / mp.sqrt(k)
    omega_n = _omega(k, PROFILE_N)
    omega_n2 = _omega(k, PROFILE_N2)
    omega_w = _omega(k, PROFILE_W)
    omega_w2 = _omega(k, PROFILE_W2)
    omega_nw = _omega(k, PROFILE_NW)

    f_terms = ((1 + 50 * u_k) * omega_n,) * k
    f_squared_terms = ((1 + 100 * u_k) * omega_n2,) * k
    f2_squared_terms = (
        (omega_w2,) + (omega_n2,) * (k - 1),
        (omega_nw, omega_nw) + (omega_n2,) * (k - 2),
    )
    dimension = k - 1
    sliced_terms = [
        (omega_n2,) * dimension,
        (omega_w2,) + (omega_n2,) * (dimension - 1),
        (omega_nw,) + (omega_n2,) * (dimension - 1),
    ]
    if dimension >= 2:
        sliced_terms.append(
            (omega_nw, omega_nw) + (omega_n2,) * (dimension - 2)
        )

    smooth_mapping = {
        APPLICATION_L620_D_W: (f_terms,),
        APPLICATION_L737_CANONICAL: f2_squared_terms,
        APPLICATION_L752_CANONICAL: (f_squared_terms,),
        APPLICATION_L885_W_PRIME: tuple(sliced_terms),
        APPLICATION_L995_A_M_W_B_R: ((omega_n,), (omega_w,)),
        APPLICATION_L1015_R_W_M: (((1 + 50 * u_k) * omega_n,),),
        APPLICATION_L1135_CANONICAL_FACTOR: (f_squared_terms,),
        APPLICATION_L1232_CANONICAL: f2_squared_terms,
    }
    if application_id == APPLICATION_L905_W_PRIME:
        raise ValueError(
            "L905 cannot use a direct H smooth path; use the conditional "
            "square-sum bypass while its scalar source multiplier remains open"
        )
    if application_id in {APPLICATION_L1096_W0, APPLICATION_L1135_W0_FACTOR}:
        raise ValueError("sharp-cutoff applications require the summatory formula")
    try:
        return smooth_mapping[application_id]
    except KeyError as exc:
        raise ValueError(f"unknown application id: {application_id}") from exc


def application_kappa_sum(k: int, application_id: str) -> mp.mpf:
    """Return the worst tensor-family sum for one explicit smooth call."""

    return max(
        mp.fsum(family)
        for family in application_kappa_term_families(k, application_id)
    )


def exact_product_relative_error(deltas: tuple[Fraction, ...]) -> Fraction:
    """Return ``product(1+delta_i)-1`` in exact rational arithmetic."""

    if any(
        isinstance(value, bool) or not isinstance(value, Fraction) or value < 0
        for value in deltas
    ):
        raise ValueError("all deltas must be nonnegative Fractions")
    return reduce(mul, (1 + value for value in deltas), Fraction(1)) - 1


def product_relative_error_upper(
    *,
    multiplier_over_log_r: int | float | str | mp.mpf,
    kappa_families: tuple[tuple[mp.mpf, ...], ...],
) -> mp.mpf:
    """Evaluate the largest exact finite product among tensor families."""

    coefficient = _positive_mpf(multiplier_over_log_r, "multiplier_over_log_r")
    if not kappa_families or any(not family for family in kappa_families):
        raise ValueError("kappa_families must contain nonempty families")
    products = []
    for family in kappa_families:
        if any(not mp.isfinite(value) or value < 0 for value in family):
            raise ValueError("all kappa values must be finite and nonnegative")
        products.append(mp.fprod(1 + coefficient * value for value in family) - 1)
    return max(products)


def rfold_error_certificate(
    *,
    application_id: str,
    k: int,
    alpha: int | float | str | mp.mpf,
    theta: int | float | str | mp.mpf,
    log_r: int | float | str | mp.mpf,
) -> RfoldErrorCertificate:
    """Evaluate the corrected product-envelope error for one smooth call."""

    _validate_k(k, target_range=True)
    log_r_value = _positive_mpf(log_r, "log_r")
    alpha_value = _positive_mpf(alpha, "alpha")
    theta_value = _positive_mpf(theta, "theta")
    if theta_value >= 1:
        raise ValueError("theta must lie in (0,1)")
    lambda_star = maynard_uniform_application_log_q_upper(
        k=k,
        alpha=alpha_value,
        theta=theta_value,
        log_r=log_r_value,
    )
    l_plus_one = lower_discrepancy_l(lambda_star) + 1
    kappa_families = application_kappa_term_families(k, application_id)
    kappa_sum = max(mp.fsum(family) for family in kappa_families)
    multiplier = weighted_lemma83_multiplier(
        H1B1B2C_MAYNARD_A1_GAP,
        H1B1B2C_UPPER_DISCREPANCY_A2,
    )
    coefficient = multiplier * l_plus_one / log_r_value
    delta_sum = coefficient * kappa_sum
    product_error = product_relative_error_upper(
        multiplier_over_log_r=coefficient,
        kappa_families=kappa_families,
    )
    # product(1+delta_i)-1 <= exp(sum delta_i)-1
    exponential_error = mp.expm1(delta_sum)
    gate_passed = delta_sum <= 1
    linear = 2 * delta_sum if gate_passed else None
    return RfoldErrorCertificate(
        application_id=application_id,
        k=k,
        log_r=log_r_value,
        log_lambda_star=mp.log(lambda_star),
        l_plus_one=l_plus_one,
        kappa_sum_upper_bound=kappa_sum,
        one_step_multiplier=multiplier,
        delta_sum_upper_bound=delta_sum,
        product_error_upper_bound=product_error,
        exponential_error_upper_bound=exponential_error,
        linearized_error_upper_bound=linear,
        linearization_gate_passed=gate_passed,
        theorem_claimed=False,
        siv_07_closed=False,
        x_cert_ready=False,
    )


def sharp_cutoff_relative_error(
    *,
    scale_log: int | float | str | mp.mpf,
    log_lambda_star: int | float | str | mp.mpf,
) -> mp.mpf:
    """Return the relative error for the two sharp ``r_0 < x^xi`` calls."""

    scale = _positive_mpf(scale_log, "scale_log")
    lambda_log = _positive_mpf(log_lambda_star, "log_lambda_star")
    l_plus_one = 6 + lambda_log
    base = summatory_multiplier(
        H1B1B2C_MAYNARD_A1_GAP,
        H1B1B2C_UPPER_DISCREPANCY_A2,
    )
    return base * l_plus_one / scale


def common_smooth_gate_certificate(
    *,
    k: int,
    alpha: int | float | str | mp.mpf,
    theta: int | float | str | mp.mpf,
) -> CommonSmoothGateCertificate:
    """Construct a closed-form cutoff shared by the closed smooth profiles.

    Write ``y=log R`` and ``Lambda_star=A+B*y``.  For ``y>=1``,
    ``log(A+B*y) <= log(A+B)+log(y)``.  If

    ``y >= max(4E*log(4E), 2E(6+log(A+B)))``,

    where ``E=C_L83*K_max>1``, then ``E*log(y)`` and
    ``E*(6+log(A+B))`` are each at most ``y/2``.  Consequently

    ``E*(6+log Lambda_star) <= y``

    and the linearization condition ``sum(delta_i)<=1`` is verified for every
    smooth application whose profile has been closed (seven Lemma 8.4 calls
    and the direct one-dimensional call at source line 1015).  This
    deliberately coarse cutoff does not certify the line-905 scalar
    pointwise remainder or repair the sharp-cutoff scale blocker.
    """

    _validate_k(k, target_range=True)
    alpha_value = _positive_mpf(alpha, "alpha")
    theta_value = _positive_mpf(theta, "theta")
    if theta_value >= 1:
        raise ValueError("theta must lie in (0,1)")
    kappa_max = max(
        f_kappa_sum(k),
        f_squared_kappa_sum(k),
        f2_squared_kappa_sum(k),
        f2_squared_slice_kappa_sum(k),
        f2_one_variable_kappa(k),
        f_one_variable_kappa(k),
    )
    multiplier = weighted_lemma83_multiplier(
        H1B1B2C_MAYNARD_A1_GAP,
        H1B1B2C_UPPER_DISCREPANCY_A2,
    )
    e_coefficient = multiplier * kappa_max
    k_mpf = mp.mpf(k)
    affine_constant = 2 * k_mpf**2 * mp.log(2 * k_mpf**2) + k_mpf * (k_mpf - 1) * mp.log(2)
    affine_slope = (
        10 * alpha_value * (2 * k_mpf**2 - k_mpf + 1) / theta_value + k_mpf
    )
    d_constant = 6 + mp.log(affine_constant + affine_slope)
    support_endpoint_gate = mp.sqrt(k_mpf) * mp.log(2)
    if e_coefficient <= 1:
        raise AssertionError("the proved project-range coefficient must exceed one")
    log_r_sufficient = max(
        mp.mpf(1),
        support_endpoint_gate,
        4 * e_coefficient * mp.log(4 * e_coefficient),
        2 * e_coefficient * d_constant,
    )
    lambda_star = affine_constant + affine_slope * log_r_sufficient
    direct_rhs = e_coefficient * (6 + mp.log(lambda_star))
    gate_verified = direct_rhs <= log_r_sufficient
    return CommonSmoothGateCertificate(
        k=k,
        alpha=alpha_value,
        theta=theta_value,
        kappa_max=kappa_max,
        weighted_multiplier=multiplier,
        e_coefficient=e_coefficient,
        lambda_affine_constant=affine_constant,
        lambda_affine_slope=affine_slope,
        log_r_sufficient=log_r_sufficient,
        direct_gate_right_hand_side=direct_rhs,
        gate_verified=gate_verified,
        all_actual_calls_closed=False,
        siv_07_closed=False,
        x_cert_ready=False,
    )


def maximum_tensor_support_exponent(k: int) -> mp.mpf:
    """Return the largest log_R support sum among the explicit tensor terms."""

    _validate_k(k)
    u_k = 1 / mp.sqrt(k)
    return max(k * u_k, 2 + (k - 1) * u_k)


assert {row.application_id for row in MAYNARD_APPLICATION_SMOOTH_SPECS} == (
    MAYNARD_APPLICATION_EXCLUSION_IDS
)


__all__ = [
    "APPLICATION_MODE_H_SQUARE_BYPASS_SCALAR_OPEN",
    "APPLICATION_MODE_SHARP_SUMMATORY",
    "APPLICATION_MODE_SMOOTH_COMPOSED",
    "ApplicationSmoothSpec",
    "CommonSmoothGateCertificate",
    "H1B1B2D_MINIMUM_TARGET_K",
    "MAYNARD_APPLICATION_SMOOTH_SPECS",
    "PROFILE_N",
    "PROFILE_N2",
    "PROFILE_NW",
    "PROFILE_W",
    "PROFILE_W2",
    "ProfileNormCertificate",
    "ProfileSpec",
    "RfoldErrorCertificate",
    "WIDE_SUPPORT_FIRST_APPLICATIONS",
    "application_kappa_sum",
    "application_kappa_term_families",
    "common_smooth_gate_certificate",
    "exact_product_relative_error",
    "f2_one_variable_kappa",
    "f2_squared_kappa_sum",
    "f2_squared_slice_kappa_sum",
    "f_kappa_sum",
    "f_one_variable_kappa",
    "f_squared_kappa_sum",
    "maximum_tensor_support_exponent",
    "profile_norm_certificate",
    "profile_spec",
    "product_relative_error_upper",
    "rfold_error_certificate",
    "sharp_cutoff_relative_error",
]
