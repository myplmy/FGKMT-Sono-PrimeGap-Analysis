"""Finite constants for the DEP-R09 Jutila Lemma 8 actual replacement.

The analytic inputs are McCurley (1984), equations (5), (13), and Lemmas
1--4.  This module checks only the finite real-algebra and geometry used after
those published inputs.  It does not numerically locate Dirichlet L-function
zeros and does not claim to prove the source analytic identities.
"""

from __future__ import annotations

from fractions import Fraction

import mpmath as mp


MAX_RADIUS = Fraction(1, 21)
GAMMA_REMAINDER = Fraction(1959, 5000)  # McCurley Lemma 2: 0.3918.
KAPPA_RATIONAL_UPPER = Fraction(3, 10)
KERNEL_NORMALIZED_LOWER = Fraction(3, 8)


def kappa() -> mp.mpf:
    """Return McCurley's exact kappa=(5-sqrt(5))/10."""

    return (mp.mpf(5) - mp.sqrt(5)) / 10


def sigma_one(sigma: mp.mpf | str | int) -> mp.mpf:
    """Return sigma_1=(1+sqrt(1+4 sigma^2))/2."""

    sigma = mp.mpf(sigma)
    return (1 + mp.sqrt(1 + 4 * sigma**2)) / 2


def _real_reciprocal_component(x: mp.mpf, y: mp.mpf) -> mp.mpf:
    return x / (x**2 + y**2)


def stechkin_kernel(
    radius: mp.mpf | str,
    beta: mp.mpf | str,
    ordinate_offset: mp.mpf | str,
) -> mp.mpf:
    """Evaluate the local Stechkin kernel used in the direct source proof.

    ``ordinate_offset`` is ``t_0-gamma``.  Valid proof inputs satisfy
    ``0<radius<=1/21``, ``1-radius<=beta<=1`` and
    ``abs(ordinate_offset)<=radius/2``.
    """

    radius = mp.mpf(radius)
    beta = mp.mpf(beta)
    ordinate_offset = mp.mpf(ordinate_offset)
    if not (0 < radius <= mp.mpf(1) / 21):
        raise ValueError("require 0 < radius <= 1/21")
    if not (1 - radius <= beta <= 1):
        raise ValueError("require 1-radius <= beta <= 1")
    if abs(ordinate_offset) > radius / 2:
        raise ValueError("require |t0-gamma| <= radius/2")

    sigma = 1 + radius
    sigma1 = sigma_one(sigma)
    first = _real_reciprocal_component(sigma - beta, ordinate_offset)
    first += _real_reciprocal_component(sigma - 1 + beta, ordinate_offset)
    shifted = _real_reciprocal_component(sigma1 - beta, ordinate_offset)
    shifted += _real_reciprocal_component(sigma1 - 1 + beta, ordinate_offset)
    return first - shifted / mp.sqrt(5)


def local_zero_count_envelope(
    radius: mp.mpf | str,
    modulus: int,
    center_height: mp.mpf | str,
) -> mp.mpf:
    """Return the proved actual square envelope ``3+r log(q(1+|t|))``."""

    radius = mp.mpf(radius)
    center_height = mp.mpf(center_height)
    if not (0 < radius <= mp.mpf(1) / 21):
        raise ValueError("require 0 < radius <= 1/21")
    if modulus < 3:
        raise ValueError("require modulus >= 3 for a nonprincipal conductor")
    return 3 + radius * mp.log(modulus * (1 + abs(center_height)))


def actual_strip_radius(
    alpha_defect: mp.mpf | str,
    log_d: mp.mpf | str,
) -> mp.mpf:
    """Return max(1-alpha, 1/log(D)) for Jutila's strip covering."""

    alpha_defect = mp.mpf(alpha_defect)
    log_d = mp.mpf(log_d)
    if alpha_defect <= 0:
        raise ValueError("require 1-alpha > 0")
    if log_d <= 0:
        raise ValueError("require log(D) > 0")
    return max(alpha_defect, 1 / log_d)


def exact_slacks() -> dict[str, Fraction]:
    """Return the exact positive rational slacks in the coarse proof."""

    # 8/17 is the normalized first-pole contribution.  The shifted F term
    # costs at most (3/2)r, maximized at r=1/21.
    kernel_slack = Fraction(8, 17) - Fraction(3, 2 * 21) - Fraction(3, 8)

    # After multiplying the explicit-formula upper bound by 8r/3, the
    # radius-independent part must stay below 3.  The 0.3918 term is largest
    # at r=1/21.
    constant_slack = (
        Fraction(3)
        - Fraction(8, 3)
        - Fraction(8, 3) * GAMMA_REMAINDER * MAX_RADIUS
    )
    log_coefficient_slack = Fraction(1) - Fraction(8, 3) * KAPPA_RATIONAL_UPPER
    return {
        "kernel_slack": kernel_slack,
        "constant_slack": constant_slack,
        "log_coefficient_slack": log_coefficient_slack,
    }


def strip_to_selected_system_envelope(
    local_envelope: mp.mpf | str,
    selected_system_size: int,
) -> mp.mpf:
    """Apply the even/odd strip split: total zeros <= 2*B*J."""

    local_envelope = mp.mpf(local_envelope)
    if local_envelope < 0:
        raise ValueError("local envelope must be nonnegative")
    if selected_system_size < 0:
        raise ValueError("selected system size must be nonnegative")
    return 2 * local_envelope * selected_system_size


def diagnostic(radius: str = "0.01", modulus: int = 10**6, height: str = "1e9") -> dict:
    """Return a high-precision diagnostic; not a directed certificate."""

    radius_mp = mp.mpf(radius)
    envelope = local_zero_count_envelope(radius_mp, modulus, height)
    slacks = exact_slacks()
    return {
        "radius": mp.nstr(radius_mp, 30),
        "modulus": modulus,
        "height": mp.nstr(mp.mpf(height), 30),
        "kappa": mp.nstr(kappa(), 50),
        "local_zero_count_envelope": mp.nstr(envelope, 50),
        "normalized_kernel_lower": str(KERNEL_NORMALIZED_LOWER),
        "exact_slacks": {key: str(value) for key, value in slacks.items()},
        "directed_certificate": False,
    }


if __name__ == "__main__":
    import json

    mp.mp.dps = 100
    print(json.dumps(diagnostic(), ensure_ascii=True, indent=2, sort_keys=True))
