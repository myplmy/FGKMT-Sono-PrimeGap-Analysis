"""Finite diagnostics for the DEP-R09 fixed-primorial variance source audit.

The module distinguishes three statements that must not be conflated:

* the Theory-82 character-energy gate that would be sufficient;
* the numerical right-hand side supplied by a direct classical large-sieve
  certificate after the primitive-conductor reduction;
* the unknown actual value of the prime-error character energy.

It proves no lower bound for the actual character energy.  It only verifies
that the direct large-sieve upper certificate is too coarse to imply the
strict Theory-82 gate, even after granting the most favourable possible
shift atom cap.  No PAP theorem, Sono coefficient, or numerical ``X_cert``
is certified here.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from typing import Mapping

import mpmath as mp


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_fixed_primorial_variance_large_sieve_barrier_v1.json"
)

D_MIN = 21
D_MAX = 186
Q_MIN = 3
DUSART_THETA_COEFFICIENT = "1.2323"
ROSSER_SCHOENFELD_EXCEPTION_COEFFICIENT = "2.50637"


def _integer(value: object, name: str, *, minimum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def euler_phi(value: int) -> int:
    """Return Euler's phi by exact trial division for diagnostic moduli."""

    value = _integer(value, "value", minimum=1)
    result = value
    remainder = value
    prime = 2
    while prime * prime <= remainder:
        if remainder % prime == 0:
            result -= result // prime
            while remainder % prime == 0:
                remainder //= prime
        prime = 3 if prime == 2 else prime + 2
    if remainder > 1:
        result -= result // remainder
    return result


def _power_regime(q: int, d: int) -> tuple[int, int]:
    q = _integer(q, "q", minimum=Q_MIN)
    d = _integer(d, "d", minimum=D_MIN)
    return q, d


def log_scales(q: int, d: int) -> tuple[mp.mpf, mp.mpf]:
    """Return ``(log q, log Y)`` for ``Y=q**d`` without forming ``Y``."""

    q, d = _power_regime(q, d)
    with mp.workdps(max(mp.mp.dps, 100)):
        log_q = mp.log(q)
        return +log_q, +(d * log_q)


def dusart_coefficient_from_log_y(log_y: object) -> mp.mpf:
    """Return the half-interval theta coefficient as a function of log(Y)."""

    with mp.workdps(max(mp.mp.dps, 100)):
        value = mp.mpf(log_y)
        log_two = mp.log(2)
        if not mp.isfinite(value) or value <= log_two:
            raise ValueError("log_y must be finite and greater than log(2)")
        return +(
            mp.mpf("0.5")
            - mp.mpf(DUSART_THETA_COEFFICIENT) / value
            - mp.mpf(DUSART_THETA_COEFFICIENT) / (2 * (value - log_two))
        )


def dusart_half_interval_coefficient(q: int, d: int) -> mp.mpf:
    """Return the explicit coefficient in theta(Y)-theta(Y/2)>cY.

    Dusart's ``abs(theta(x)-x)<1.2323*x/log(x)`` gives

    ``c = 1/2-a/log(Y)-a/(2*(log(Y)-log(2)))``.
    """

    _, log_y = log_scales(q, d)
    return dusart_coefficient_from_log_y(log_y)


def lambda_square_sum_lower_over_y(q: int, d: int) -> mp.mpf:
    """Return a strict source-derived lower bound for S2(Y)/Y.

    Here ``S2(Y)=sum_(n<=Y) Lambda(n)^2`` and ``Y=q**d``.  Primes in
    ``(Y/2,Y]`` alone give

    ``S2(Y)/Y > c*(log(Y)-log(2))``.
    """

    _, log_y = log_scales(q, d)
    with mp.workdps(max(mp.mp.dps, 100)):
        return +(
            dusart_half_interval_coefficient(q, d)
            * (log_y - mp.log(2))
        )


def coarse_large_sieve_rhs_lower_over_y2(q: int, d: int) -> mp.mpf:
    """Return ``(log(Y)-log(2))/4``, a strict lower bound for B_LS/Y^2.

    The direct Montgomery--Vaughan certificate has published right-hand
    side ``B_LS=(Y+q^2) S2(Y)``.  The returned quantity is deliberately
    smaller: ``B_LS/Y^2 > S2(Y)/Y > (log(Y)-log(2))/4``.
    """

    _, log_y = log_scales(q, d)
    with mp.workdps(max(mp.mp.dps, 100)):
        return +((log_y - mp.log(2)) / 4)


def best_possible_entropy_gate_upper_over_y2(q: int) -> mp.mpf:
    """Return ``exp(-4)*q/phi(q)``.

    This grants ``tau<=exp(-2)``, success mass at most one, survivor ratio
    at most one, and a perfectly uniform final shift over all q residues.
    Every actual Theory-82 atom-cap gate is no larger than this envelope.
    """

    q = _integer(q, "q", minimum=Q_MIN)
    with mp.workdps(max(mp.mp.dps, 100)):
        return +(mp.exp(-4) * mp.mpf(q) / euler_phi(q))


def rosser_schoenfeld_q_over_phi_upper(q: int) -> mp.mpf:
    """Return a valid all-q>=3 Rosser--Schoenfeld envelope for q/phi(q)."""

    q = _integer(q, "q", minimum=Q_MIN)
    with mp.workdps(max(mp.mp.dps, 100)):
        log_q = mp.log(q)
        log_log_q = mp.log(log_q)
        if log_log_q <= 0:
            raise ValueError("log(log(q)) must be positive")
        return +(
            mp.exp(mp.euler) * log_log_q
            + mp.mpf(ROSSER_SCHOENFELD_EXCEPTION_COEFFICIENT) / log_log_q
        )


def rosser_entropy_gate_upper_over_y2(q: int) -> mp.mpf:
    """Return the source-certified upper envelope for the best atom gate."""

    with mp.workdps(max(mp.mp.dps, 100)):
        return +(mp.exp(-4) * rosser_schoenfeld_q_over_phi_upper(q))


def direct_large_sieve_barrier_margin(q: int, d: int) -> mp.mpf:
    """Return conservative ``B_LS/Y^2 - gate/Y^2`` margin.

    A positive result means only that the numerical right-hand side of the
    direct certificate lies above the largest possible sufficient gate.
    It is not a lower bound for the unknown actual character energy.
    """

    with mp.workdps(max(mp.mp.dps, 100)):
        return +(
            coarse_large_sieve_rhs_lower_over_y2(q, d)
            - rosser_entropy_gate_upper_over_y2(q)
        )


def upper_certificate_implies_strict_gate(
    certificate_upper: object,
    strict_gate: object,
) -> bool:
    """Return whether ``V<=certificate_upper`` alone proves ``V<strict_gate``.

    Equality is deliberately rejected.  If the certificate upper is at or
    above the gate, choosing the abstract value ``V=strict_gate`` is a
    countermodel to the desired logical implication.
    """

    with mp.workdps(max(mp.mp.dps, 100)):
        upper = mp.mpf(certificate_upper)
        gate = mp.mpf(strict_gate)
        if not mp.isfinite(upper) or upper < 0:
            raise ValueError("certificate_upper must be finite and nonnegative")
        if not mp.isfinite(gate) or gate <= 0:
            raise ValueError("strict_gate must be finite and positive")
        return upper < gate


@dataclass(frozen=True)
class FixedPrimorialVarianceBarrierDiagnostic:
    endpoint_q: int
    endpoint_d: int
    dusart_log8_coefficient: str
    dusart_log8_coefficient_exceeds_one_quarter: bool
    dusart_half_interval_coefficient: str
    dusart_coefficient_exceeds_one_quarter: bool
    large_sieve_rhs_lower_over_y2: str
    exact_best_entropy_gate_upper_over_y2: str
    rosser_entropy_gate_upper_over_y2: str
    conservative_barrier_margin: str
    sample_primorial_margins_all_positive: bool
    montgomery_vaughan_primary_constant_crosschecked: bool
    direct_large_sieve_rhs_can_certify_theory82_gate: bool
    actual_character_energy_lower_bound_claimed: bool
    fixed_primorial_natural_variance_theorem_identified: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool
    bounded_x_cert_range_obtained: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> FixedPrimorialVarianceBarrierDiagnostic:
    """Build the deterministic fail-closed Theory-83 diagnostic."""

    q = Q_MIN
    d = D_MIN
    sample_moduli = (3, 30, 210, 2310, 30030, 510510)
    with mp.workdps(max(mp.mp.dps, 120)):
        theta_coefficient = dusart_half_interval_coefficient(q, d)
        log8_coefficient = dusart_coefficient_from_log_y(8)
        large_sieve_lower = coarse_large_sieve_rhs_lower_over_y2(q, d)
        exact_gate = best_possible_entropy_gate_upper_over_y2(q)
        rosser_gate = rosser_entropy_gate_upper_over_y2(q)
        margin = direct_large_sieve_barrier_margin(q, d)
        sample_positive = all(
            direct_large_sieve_barrier_margin(modulus, D_MIN) > 0
            for modulus in sample_moduli
        )
        return FixedPrimorialVarianceBarrierDiagnostic(
            endpoint_q=q,
            endpoint_d=d,
            dusart_log8_coefficient=mp.nstr(log8_coefficient, 80),
            dusart_log8_coefficient_exceeds_one_quarter=(
                log8_coefficient > mp.mpf(1) / 4
            ),
            dusart_half_interval_coefficient=mp.nstr(theta_coefficient, 80),
            dusart_coefficient_exceeds_one_quarter=(
                theta_coefficient > mp.mpf(1) / 4
            ),
            large_sieve_rhs_lower_over_y2=mp.nstr(large_sieve_lower, 80),
            exact_best_entropy_gate_upper_over_y2=mp.nstr(exact_gate, 80),
            rosser_entropy_gate_upper_over_y2=mp.nstr(rosser_gate, 80),
            conservative_barrier_margin=mp.nstr(margin, 80),
            sample_primorial_margins_all_positive=sample_positive,
            montgomery_vaughan_primary_constant_crosschecked=True,
            direct_large_sieve_rhs_can_certify_theory82_gate=False,
            actual_character_energy_lower_bound_claimed=False,
            fixed_primorial_natural_variance_theorem_identified=False,
            pap_11_closed=False,
            dep_r09_closed=False,
            fixed_2e_minus_17_independently_certified=False,
            numerical_x_cert_ready=False,
            bounded_x_cert_range_obtained=False,
            threshold_calculator_ready=False,
            actual_prime_computation_run=False,
            source_theorem_local_axiom_used=False,
            proof_escape_used=False,
        )


def load_ledger() -> dict[str, object]:
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def validate_ledger(
    document: Mapping[str, object],
    *,
    check_hashes: bool = True,
) -> list[str]:
    """Validate scientific status and every locally pinned source."""

    issues: list[str] = []
    if document.get("schema_version") != "1.0.0":
        issues.append("schema_version mismatch")
    if document.get("gate") != (
        "DEP-R09 fixed-primorial variance source and direct large-sieve barrier audit"
    ):
        issues.append("gate mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Find or prove a prime-specific or sparse-divisor fixed-primorial bound, "
        "or a direct same-law weighted-correlation theorem, that is strictly "
        "smaller than the Theory-82 gate; the raw classical large-sieve RHS "
        "and shift entropy alone cannot certify it."
    ):
        issues.append("next_gate mismatch")

    sources = document.get("source_registry")
    if not isinstance(sources, list):
        issues.append("source_registry mismatch")
        return issues
    pinned = {
        item.get("key")
        for item in sources
        if isinstance(item, dict) and "locator" in item
    }
    expected_pinned = {
        "MONTGOMERY_VAUGHAN1973",
        "FIORILLI2013",
        "FIORILLI_MARTIN2023",
        "ROSSER_SCHOENFELD1962",
        "DUSART2010",
        "THEORY82",
    }
    if pinned != expected_pinned:
        issues.append("pinned source keys mismatch")

    if check_hashes:
        for source in sources:
            if not isinstance(source, dict) or "locator" not in source:
                continue
            key = source.get("key", "unknown")
            locator = source.get("locator")
            digest = source.get("sha256")
            if not isinstance(locator, str) or not isinstance(digest, str):
                issues.append(f"{key} missing pin")
                continue
            path = (REPO_ROOT / locator).resolve()
            try:
                path.relative_to(REPO_ROOT.resolve())
            except ValueError:
                issues.append(f"{key} path escape")
                continue
            if not path.is_file():
                issues.append(f"{key} missing source")
                continue
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                issues.append(f"{key} hash mismatch")
    return issues


__all__ = [
    "D_MAX",
    "D_MIN",
    "LEDGER_PATH",
    "Q_MIN",
    "best_possible_entropy_gate_upper_over_y2",
    "build_diagnostic",
    "coarse_large_sieve_rhs_lower_over_y2",
    "direct_large_sieve_barrier_margin",
    "dusart_coefficient_from_log_y",
    "dusart_half_interval_coefficient",
    "euler_phi",
    "lambda_square_sum_lower_over_y",
    "load_ledger",
    "log_scales",
    "rosser_entropy_gate_upper_over_y2",
    "rosser_schoenfeld_q_over_phi_upper",
    "upper_certificate_implies_strict_gate",
    "validate_ledger",
]
