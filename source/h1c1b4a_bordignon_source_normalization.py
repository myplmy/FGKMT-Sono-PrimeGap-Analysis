"""Fail-closed source normalization for Bordignon's Theorem 1.2 constant.

The final NYJM paper and arXiv v1 use incompatible notation for the first
term defining ``C(alpha1, alpha2, Y0)`` and both mix the threshold variables
``X0`` and ``Y0=log(log(X0))``.  This module records only the algebra that can
be recovered directly from the displayed Theorem 3.4 remainder and the exact
target in Theorem 1.2.

It deliberately does not manufacture a numerical upper bound for ``C`` and
does not close Maynard Hypothesis 1(2), Proposition 9.2, or ``X_cert``.
"""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp


FINAL_EQ33_FIRST_TERM = "R_star(x,T,q)*log(log(x))/log(x)^2"
ARXIV_V1_EQC_FIRST_TERM = "R_star(x,T,q)*T/(x*log(x)^2)"
PROJECT_DIRECT_FIRST_TERM = (
    "q*R_star(x,T,q)*log(x)^alpha2/x"
)
PROJECT_Q_ENVELOPE_FIRST_TERM = (
    "R_star(x,T,q)*log(x)^(alpha1+alpha2)/x"
)


class UnresolvedBordignonConstantError(RuntimeError):
    """Raised when code tries to use the malformed source formula numerically."""


def _finite_mpf(value: object, name: str, *, positive: bool = False) -> mp.mpf:
    result = mp.mpf(value)
    if not mp.isfinite(result):
        raise ValueError(f"{name} must be finite")
    if positive and result <= 0:
        raise ValueError(f"{name} must be positive")
    return result


def log_x0_from_y0(y0: object) -> mp.mpf:
    """Return ``log(X0)=exp(Y0)`` without constructing double-exponential X0."""

    y0_mpf = _finite_mpf(y0, "y0")
    return mp.exp(y0_mpf)


def y0_from_log_x0(log_x0: object) -> mp.mpf:
    """Return ``Y0=log(log(X0))`` from the safer input ``log(X0)``."""

    log_x0_mpf = _finite_mpf(log_x0, "log_x0", positive=True)
    return mp.log(log_x0_mpf)


def direct_remainder_coefficient_log(
    log_x: object,
    alpha1: object,
    alpha2: object,
    log_rstar_over_x: object,
    *,
    q: int | None = None,
) -> mp.mpf:
    r"""Return the log of the explicit-formula remainder contribution to C.

    Theorem 1.2 asks for an upper bound after multiplication by
    ``log(x)^alpha2``.  If Theorem 3.4 contributes at most ``R_star`` for
    each of at most ``q`` characters, the exact contribution is

    ``q * (R_star/x) * log(x)^alpha2``.

    If ``q`` is omitted, the theorem envelope ``q<=log(x)^alpha1`` is used,
    giving ``(R_star/x)*log(x)^(alpha1+alpha2)``.  All computations remain on
    logarithmic scale.  A supplied q is checked against the envelope.
    """

    log_x_mpf = _finite_mpf(log_x, "log_x", positive=True)
    if log_x_mpf <= 1:
        raise ValueError("log_x must exceed 1")
    alpha1_mpf = _finite_mpf(alpha1, "alpha1", positive=True)
    alpha2_mpf = _finite_mpf(alpha2, "alpha2", positive=True)
    log_ratio = _finite_mpf(log_rstar_over_x, "log_rstar_over_x")
    log_log_x = mp.log(log_x_mpf)

    if q is None:
        return log_ratio + (alpha1_mpf + alpha2_mpf) * log_log_x
    if isinstance(q, bool) or not isinstance(q, int):
        raise TypeError("q must be an integer")
    if q < 1:
        raise ValueError("q must be positive")
    log_q = mp.log(q)
    if log_q > alpha1_mpf * log_log_x:
        raise ValueError("q exceeds the stated log(x)^alpha1 envelope")
    return log_ratio + log_q + alpha2_mpf * log_log_x


def q_envelope_height_identity_log(
    log_x: object,
    alpha1: object,
    alpha2: object,
    log_rstar_over_x: object,
) -> tuple[mp.mpf, mp.mpf]:
    r"""Return two equal log forms of the recovered q-envelope contribution.

    Bordignon chooses ``T=log(x)^(alpha1+alpha2+3)``.  Hence

    ``(R_star/x)*log(x)^(alpha1+alpha2)``
    ``= (R_star/x)*T/log(x)^3``.

    The returned pair lets tests guard against losing ``x`` or one of the
    three powers of ``log(x)``.
    """

    direct = direct_remainder_coefficient_log(
        log_x,
        alpha1,
        alpha2,
        log_rstar_over_x,
    )
    log_x_mpf = _finite_mpf(log_x, "log_x", positive=True)
    alpha1_mpf = _finite_mpf(alpha1, "alpha1", positive=True)
    alpha2_mpf = _finite_mpf(alpha2, "alpha2", positive=True)
    log_ratio = _finite_mpf(log_rstar_over_x, "log_rstar_over_x")
    log_log_x = mp.log(log_x_mpf)
    via_height = (
        log_ratio
        + (alpha1_mpf + alpha2_mpf + 3) * log_log_x
        - 3 * log_log_x
    )
    return direct, via_height


def numerical_theorem12_constant_from_printed_source(*_: object, **__: object) -> mp.mpf:
    """Always fail: neither printed first-term formula is adopted silently."""

    raise UnresolvedBordignonConstantError(
        "Bordignon's printed C formula is not a valid numerical input for the "
        "growing-A application; rederive and bound every Theorem 3.4 term first"
    )


@dataclass(frozen=True)
class H1c1b4aSourceNormalizationCertificate:
    x0_y0_type_mapping_closed: bool
    final_eq33_first_term_dimensionally_valid: bool
    arxiv_v1_first_term_adopted_as_final: bool
    direct_theorem34_to_theorem12_remainder_algebra_closed: bool
    final_table_covers_actual_growing_a: bool
    numerical_theorem12_constant_upper_closed: bool
    bordignon_constant_normalization_resolved: bool
    represented_prime_density_lower_bound_closed: bool
    full_remainder_absorption_closed: bool
    hypothesis1_clause2_closed: bool
    proposition92_closed: bool
    siv_08_closed: bool
    x_cert_ready: bool
    actual_prime_experiment_performed: bool


def structural_certificate() -> H1c1b4aSourceNormalizationCertificate:
    """Return the narrow source-audit result without theorem over-promotion."""

    return H1c1b4aSourceNormalizationCertificate(
        x0_y0_type_mapping_closed=True,
        final_eq33_first_term_dimensionally_valid=False,
        arxiv_v1_first_term_adopted_as_final=False,
        direct_theorem34_to_theorem12_remainder_algebra_closed=True,
        final_table_covers_actual_growing_a=False,
        numerical_theorem12_constant_upper_closed=False,
        bordignon_constant_normalization_resolved=False,
        represented_prime_density_lower_bound_closed=False,
        full_remainder_absorption_closed=False,
        hypothesis1_clause2_closed=False,
        proposition92_closed=False,
        siv_08_closed=False,
        x_cert_ready=False,
        actual_prime_experiment_performed=False,
    )
