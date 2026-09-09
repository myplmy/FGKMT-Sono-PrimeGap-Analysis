"""Exact endpoint correction for the actual FGKMT Hypothesis 1 call.

Maynard's original Definition (2.1) uses ``[T,2T)``.  FGKMT explicitly
replace that convention by ``[T,2T]`` in their Definition 2, while the
prime set occurring in the Section 8 application is ``(T,2T]``.  The
Bordignon/Abel source interval therefore already matches the latter and
needs only the lower endpoint atom to match the former.

This module is a correction layer over the historical H1c-1b.3 bridge.
It does not claim that the downstream weighted endpoint term in FGKMT
equation (6.5), all of Hypothesis 1, Theorem 6, or ``X_cert`` is closed.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import mpmath as mp

from source.h1c1b3_endpoint_count_transfer import (
    PRIME_POWER_CUMULATIVE_CONSTANT,
    _validated_integer,
    _validated_mpf,
)


SOURCE_PRIME_INTERVAL = "(T,2T]"
FGKMT_HYPOTHESIS_INTERVAL = "[T,2T]"
FGKMT_OUTER_PRIME_INTERVAL = "(T,2T]"


def centered_lower_endpoint_atom(residue_hit: int, phi_q: int) -> Fraction:
    """Return the exact centered correction made by adding the prime ``T``.

    ``residue_hit`` is one precisely when the lower endpoint is a prime in
    the selected reduced residue class.  If the lower endpoint is prime but
    lies in another class, it is zero.  The total count always gains one.
    Hence the correction is ``residue_hit - 1/phi(q)`` and has absolute
    value at most one.
    """

    residue_hit = _validated_integer(residue_hit, "residue_hit")
    if residue_hit not in (0, 1):
        raise ValueError("residue_hit must be 0 or 1")
    phi_q = _validated_integer(phi_q, "phi_q", minimum=1)
    correction = Fraction(residue_hit, 1) - Fraction(1, phi_q)
    if abs(correction) > 1:
        raise AssertionError("centered lower-endpoint correction exceeded one")
    return correction


@dataclass(frozen=True)
class ClosedCountTransferUpperComponents:
    """Upper-bound components for the FGKMT closed interval ``[T,2T]``."""

    partial_summation: mp.mpf
    prime_power_removal: mp.mpf
    lower_endpoint_addition: mp.mpf

    @property
    def total(self) -> mp.mpf:
        return mp.fsum(
            (
                self.partial_summation,
                self.prime_power_removal,
                self.lower_endpoint_addition,
            )
        )


def closed_count_transfer_upper_from_components(
    t: object,
    *,
    remainder_at_t_upper: object,
    remainder_at_2t_upper: object,
    abel_integral_upper: object,
    modulus_count: int,
    reciprocal_totient_sum: object,
) -> ClosedCountTransferUpperComponents:
    r"""Compose the corrected parameterized bound for ``[T,2T]``.

    The first two components are the same Abel and prime-power terms as in
    H1c-1b.3.  The last term is ``M``, because converting ``(T,2T]`` to
    ``[T,2T]`` only adds the lower endpoint ``T``.  No upper endpoint is
    removed.
    """

    t_mpf = _validated_mpf(t, "t", strictly_positive=True)
    if t_mpf < 4:
        raise ValueError("t must be at least 4")
    r_t = _validated_mpf(remainder_at_t_upper, "remainder_at_t_upper")
    r_2t = _validated_mpf(remainder_at_2t_upper, "remainder_at_2t_upper")
    integral = _validated_mpf(abel_integral_upper, "abel_integral_upper")
    modulus_count = _validated_integer(modulus_count, "modulus_count")
    phi_sum = _validated_mpf(reciprocal_totient_sum, "reciprocal_totient_sum")

    partial = r_2t / mp.log(2 * t_mpf) + r_t / mp.log(t_mpf) + integral
    prime_powers = (
        PRIME_POWER_CUMULATIVE_CONSTANT
        * mp.sqrt(2 * t_mpf)
        * (modulus_count + phi_sum)
    )
    return ClosedCountTransferUpperComponents(
        partial_summation=partial,
        prime_power_removal=prime_powers,
        lower_endpoint_addition=mp.mpf(modulus_count),
    )


def crude_normalized_closed_count_transfer_upper(
    log_t: object,
    relative_remainder_supremum: object,
) -> ClosedCountTransferUpperComponents:
    r"""Return the safe normalized envelope for the corrected interval.

    The numerical formula is deliberately identical to the historical
    half-open envelope: both endpoint conversions cost at most one centered
    atom per modulus.  Its semantics are different: the final term now adds
    ``T`` and never removes ``2T``.
    """

    log_t_mpf = _validated_mpf(log_t, "log_t", strictly_positive=True)
    if log_t_mpf <= mp.log(2):
        raise ValueError("log_t must correspond to t > 2")
    rho = _validated_mpf(
        relative_remainder_supremum,
        "relative_remainder_supremum",
    )
    partial = rho * (
        1 / log_t_mpf
        + 2 / (log_t_mpf + mp.log(2))
        + 1 / log_t_mpf**2
    )
    prime_powers = 4 * mp.sqrt(2) * mp.exp(-log_t_mpf / 6)
    lower_endpoint = mp.exp(-2 * log_t_mpf / 3)
    return ClosedCountTransferUpperComponents(
        partial_summation=partial,
        prime_power_removal=prime_powers,
        lower_endpoint_addition=lower_endpoint,
    )


@dataclass(frozen=True)
class FgkmtEndpointCorrectionCertificate:
    source_interval: str
    fgkmt_hypothesis_interval: str
    fgkmt_outer_prime_interval: str
    maynard_original_interval: str
    lower_endpoint_only: bool
    upper_endpoint_removed: bool
    per_modulus_centered_cost_at_most_one: bool
    historical_numeric_envelope_remains_safe: bool
    historical_actual_target_label_correct: bool
    fgkmt_hypothesis_endpoint_bridge_closed: bool
    downstream_weighted_endpoint_closed: bool
    siv_08_closed: bool
    x_cert_ready: bool


def endpoint_correction_certificate() -> FgkmtEndpointCorrectionCertificate:
    """Return the fail-closed source-to-application endpoint certificate."""

    return FgkmtEndpointCorrectionCertificate(
        source_interval=SOURCE_PRIME_INTERVAL,
        fgkmt_hypothesis_interval=FGKMT_HYPOTHESIS_INTERVAL,
        fgkmt_outer_prime_interval=FGKMT_OUTER_PRIME_INTERVAL,
        maynard_original_interval="[T,2T)",
        lower_endpoint_only=True,
        upper_endpoint_removed=False,
        per_modulus_centered_cost_at_most_one=True,
        historical_numeric_envelope_remains_safe=True,
        historical_actual_target_label_correct=False,
        fgkmt_hypothesis_endpoint_bridge_closed=True,
        downstream_weighted_endpoint_closed=False,
        siv_08_closed=False,
        x_cert_ready=False,
    )
