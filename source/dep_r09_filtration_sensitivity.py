"""Exact finite checks for the DEP-R09 filtration/survivor-floor audit.

This module proves only elementary finite statements:

* the final sieve-good mass and denominator normalization algebra;
* a one-prime residue-change bound for survivor *counts*;
* an exact counterexample showing that this count bound does not transfer to
  a nonprincipal Dirichlet-character coefficient;
* fail-closed status/provenance checks for the project machine ledger.

It does not prove a martingale increment bound, a conditional variance bound,
an FMT/FGKMT analytic theorem, PAP-11, DEP-R09, or a numerical ``X_cert``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_filtration_sensitivity_survivor_floor_v1.json"
)


def _integer(value: int, name: str, *, minimum: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def _fraction(value: Fraction, name: str, *, positive: bool = False) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, Fraction):
        raise TypeError(f"{name} must be fractions.Fraction")
    if positive and value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def _failure_probability(value: Fraction, name: str) -> Fraction:
    value = _fraction(value, name)
    if value < 0 or value >= 1:
        raise ValueError(f"{name} must lie in [0,1)")
    return value


def is_prime(value: int) -> bool:
    value = _integer(value, "value", minimum=0)
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def is_squarefree(value: int) -> bool:
    value = _integer(value, "value", minimum=1)
    divisor = 2
    remaining = value
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            remaining //= divisor
            if remaining % divisor == 0:
                return False
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    return True


def ceil_div(numerator: int, denominator: int) -> int:
    numerator = _integer(numerator, "numerator", minimum=0)
    denominator = _integer(denominator, "denominator", minimum=1)
    return (numerator + denominator - 1) // denominator


def one_residue_membership_bound(interval_length: int, prime: int) -> int:
    """Return ``2*ceil(interval_length/prime)``.

    When two CRT shifts agree modulo ``P/prime`` and differ modulo ``prime``,
    their survivor symmetric difference is contained in two residue classes
    modulo ``prime``.
    """

    interval_length = _integer(interval_length, "interval_length", minimum=0)
    prime = _integer(prime, "prime", minimum=2)
    if not is_prime(prime):
        raise ValueError("prime must be prime")
    return 2 * ceil_div(interval_length, prime)


def survivor_offsets(
    modulus: int,
    shift: int,
    interval_start: int,
    interval_length: int,
) -> frozenset[int]:
    modulus = _integer(modulus, "modulus", minimum=2)
    shift = _integer(shift, "shift")
    interval_start = _integer(interval_start, "interval_start")
    interval_length = _integer(interval_length, "interval_length", minimum=0)
    return frozenset(
        offset
        for offset in range(interval_start, interval_start + interval_length)
        if math.gcd(shift + offset, modulus) == 1
    )


@dataclass(frozen=True)
class OneResidueCountDiagnostic:
    modulus: int
    changed_prime: int
    interval_length: int
    old_survivors: int
    new_survivors: int
    symmetric_difference: int
    symmetric_difference_bound: int
    count_difference: int
    exact_bound_pass: bool


def one_residue_count_diagnostic(
    modulus: int,
    changed_prime: int,
    old_shift: int,
    new_shift: int,
    interval_start: int,
    interval_length: int,
) -> OneResidueCountDiagnostic:
    """Check the exact survivor-count sensitivity for one CRT coordinate."""

    modulus = _integer(modulus, "modulus", minimum=2)
    changed_prime = _integer(changed_prime, "changed_prime", minimum=2)
    old_shift = _integer(old_shift, "old_shift")
    new_shift = _integer(new_shift, "new_shift")
    interval_start = _integer(interval_start, "interval_start")
    interval_length = _integer(interval_length, "interval_length", minimum=0)
    if not is_squarefree(modulus):
        raise ValueError("modulus must be squarefree")
    if not is_prime(changed_prime) or modulus % changed_prime != 0:
        raise ValueError("changed_prime must be a prime divisor of modulus")
    unchanged_part = modulus // changed_prime
    if (old_shift - new_shift) % unchanged_part != 0:
        raise ValueError("shifts must agree modulo modulus/changed_prime")
    if (old_shift - new_shift) % changed_prime == 0:
        raise ValueError("shifts must differ modulo changed_prime")

    old = survivor_offsets(modulus, old_shift, interval_start, interval_length)
    new = survivor_offsets(modulus, new_shift, interval_start, interval_length)
    symmetric_difference = len(old ^ new)
    count_difference = abs(len(old) - len(new))
    bound = one_residue_membership_bound(interval_length, changed_prime)
    return OneResidueCountDiagnostic(
        modulus=modulus,
        changed_prime=changed_prime,
        interval_length=interval_length,
        old_survivors=len(old),
        new_survivors=len(new),
        symmetric_difference=symmetric_difference,
        symmetric_difference_bound=bound,
        count_difference=count_difference,
        exact_bound_pass=(count_difference <= symmetric_difference <= bound),
    )


def legendre_symbol(value: int, odd_prime: int) -> int:
    value = _integer(value, "value")
    odd_prime = _integer(odd_prime, "odd_prime", minimum=3)
    if odd_prime % 2 == 0 or not is_prime(odd_prime):
        raise ValueError("odd_prime must be an odd prime")
    residue = value % odd_prime
    if residue == 0:
        return 0
    symbol = pow(residue, (odd_prime - 1) // 2, odd_prime)
    if symbol == 1:
        return 1
    if symbol == odd_prime - 1:
        return -1
    raise ArithmeticError("Euler criterion returned an impossible value")


def quadratic_times_principal_character(value: int, p: int, q: int) -> int:
    """Quadratic character mod ``p`` times the principal character mod ``q``."""

    value = _integer(value, "value")
    p = _integer(p, "p", minimum=3)
    q = _integer(q, "q", minimum=2)
    if not is_prime(q) or p == q:
        raise ValueError("p and q must be distinct primes")
    if math.gcd(value, q) != 1:
        return 0
    return legendre_symbol(value, p)


def character_interval_sum(
    shift: int,
    interval_start: int,
    interval_length: int,
    p: int,
    q: int,
) -> int:
    shift = _integer(shift, "shift")
    interval_start = _integer(interval_start, "interval_start")
    interval_length = _integer(interval_length, "interval_length", minimum=0)
    return sum(
        quadratic_times_principal_character(shift + offset, p, q)
        for offset in range(interval_start, interval_start + interval_length)
    )


@dataclass(frozen=True)
class CharacterPhaseCounterexample:
    modulus: int
    changed_prime: int
    unchanged_prime: int
    interval_start: int
    interval_length: int
    old_shift: int
    new_shift: int
    old_character_sum: int
    new_character_sum: int
    character_sum_difference: int
    membership_symmetric_difference: int
    membership_bound: int
    exceeds_membership_bound: bool


def character_phase_counterexample() -> CharacterPhaseCounterexample:
    """Return the exact ``P=65`` witness rejecting count-to-phase transfer.

    Take ``p=5``, ``q=13``, shifts 0 and 13, and offsets ``{1,2,3}``.
    The shifts agree modulo 13 and differ modulo 5.  The survivor symmetric
    difference has size 1 and its general bound is 2, but the nonprincipal
    character sums are -1 and 2, hence differ by 3.
    """

    p, q = 5, 13
    modulus = p * q
    start, length = 1, 3
    old_shift, new_shift = 0, q
    count = one_residue_count_diagnostic(
        modulus,
        p,
        old_shift,
        new_shift,
        start,
        length,
    )
    old_sum = character_interval_sum(old_shift, start, length, p, q)
    new_sum = character_interval_sum(new_shift, start, length, p, q)
    difference = abs(new_sum - old_sum)
    return CharacterPhaseCounterexample(
        modulus=modulus,
        changed_prime=p,
        unchanged_prime=q,
        interval_start=start,
        interval_length=length,
        old_shift=old_shift,
        new_shift=new_shift,
        old_character_sum=old_sum,
        new_character_sum=new_sum,
        character_sum_difference=difference,
        membership_symmetric_difference=count.symmetric_difference,
        membership_bound=count.symmetric_difference_bound,
        exceeds_membership_bound=difference > count.symmetric_difference_bound,
    )


def trivial_character_sum_change_bound(interval_length: int) -> int:
    """Return the unconditional ``2N`` bound for two length-``N`` sums."""

    interval_length = _integer(interval_length, "interval_length", minimum=0)
    return 2 * interval_length


def weighted_l1_change_bound(
    interval_length: int,
    coefficient_weight_l1: Fraction,
) -> Fraction:
    """Return the trivial ``2N * sum |Z_chi|`` weighted-error bound."""

    interval_length = _integer(interval_length, "interval_length", minimum=0)
    weight = _fraction(coefficient_weight_l1, "coefficient_weight_l1")
    if weight < 0:
        raise ValueError("coefficient_weight_l1 must be nonnegative")
    return trivial_character_sum_change_bound(interval_length) * weight


def sieve_good_mass_lower(
    outer_failure_upper: Fraction,
    inner_failure_upper: Fraction,
) -> Fraction:
    f_out = _failure_probability(outer_failure_upper, "outer_failure_upper")
    f_in = _failure_probability(inner_failure_upper, "inner_failure_upper")
    return (1 - f_out) * (1 - f_in)


def survivor_floor(
    scale_a: Fraction,
    relative_error_eta: Fraction,
    x_over_log_x: Fraction,
) -> Fraction:
    """Return Theory 55's final sieve-good floor ``A(1-eta)X/log X``."""

    scale_a = _fraction(scale_a, "scale_a", positive=True)
    eta = _fraction(relative_error_eta, "relative_error_eta")
    x_scale = _fraction(x_over_log_x, "x_over_log_x", positive=True)
    if eta < 0 or eta >= 1:
        raise ValueError("relative_error_eta must lie in [0,1)")
    return scale_a * (1 - eta) * x_scale


def raw_to_sieve_good_normalized_moment_upper(
    raw_sieve_good_second_moment_upper: Fraction,
    minimum_survivors: Fraction,
    prime_scale: Fraction,
) -> Fraction:
    """Normalize ``E[1_S |R|^2]`` using a pointwise floor on the same event S."""

    raw = _fraction(
        raw_sieve_good_second_moment_upper,
        "raw_sieve_good_second_moment_upper",
    )
    minimum = _fraction(minimum_survivors, "minimum_survivors", positive=True)
    scale = _fraction(prime_scale, "prime_scale", positive=True)
    if raw < 0:
        raise ValueError("raw_sieve_good_second_moment_upper must be nonnegative")
    return raw / (minimum**2 * scale**2)


def sieve_good_markov_success_lower(
    outer_failure_upper: Fraction,
    inner_failure_upper: Fraction,
    sieve_good_normalized_moment_upper: Fraction,
    tau: Fraction,
) -> Fraction:
    """Return ``max(0,P_lower(S)-mu_S/tau^2)`` exactly."""

    mass = sieve_good_mass_lower(outer_failure_upper, inner_failure_upper)
    moment = _fraction(
        sieve_good_normalized_moment_upper,
        "sieve_good_normalized_moment_upper",
    )
    tau = _fraction(tau, "tau", positive=True)
    if moment < 0:
        raise ValueError("sieve_good_normalized_moment_upper must be nonnegative")
    return max(Fraction(0), mass - moment / tau**2)


def sieve_good_strict_gate(
    outer_failure_upper: Fraction,
    inner_failure_upper: Fraction,
    sieve_good_normalized_moment_upper: Fraction,
    tau: Fraction,
) -> bool:
    mass = sieve_good_mass_lower(outer_failure_upper, inner_failure_upper)
    moment = _fraction(
        sieve_good_normalized_moment_upper,
        "sieve_good_normalized_moment_upper",
    )
    tau = _fraction(tau, "tau", positive=True)
    if moment < 0:
        raise ValueError("sieve_good_normalized_moment_upper must be nonnegative")
    return moment < tau**2 * mass


@dataclass(frozen=True)
class FiltrationSensitivityDiagnostic:
    sieve_good_denominator_floor_aligned: bool
    final_law_globally_product_independent: bool
    within_nibble_conditional_independence_source_verified: bool
    one_residue_survivor_count_bound_exact: bool
    count_bound_transfers_to_nonprincipal_character_phase: bool
    character_phase_counterexample_exact: bool
    martingale_increment_bound_available: bool
    martingale_conditional_variance_bound_available: bool
    same_law_analytic_moment_bound_available: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    fixed_2e_minus_17_independently_certified: bool
    numerical_x_cert_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> FiltrationSensitivityDiagnostic:
    return FiltrationSensitivityDiagnostic(
        sieve_good_denominator_floor_aligned=True,
        final_law_globally_product_independent=False,
        within_nibble_conditional_independence_source_verified=True,
        one_residue_survivor_count_bound_exact=True,
        count_bound_transfers_to_nonprincipal_character_phase=False,
        character_phase_counterexample_exact=True,
        martingale_increment_bound_available=False,
        martingale_conditional_variance_bound_available=False,
        same_law_analytic_moment_bound_available=False,
        pap_11_closed=False,
        dep_r09_closed=False,
        fixed_2e_minus_17_independently_certified=False,
        numerical_x_cert_ready=False,
        actual_prime_computation_run=False,
        source_theorem_local_axiom_used=False,
        proof_escape_used=False,
    )


def load_ledger() -> dict[str, object]:
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def validate_ledger(
    document: dict[str, object],
    *,
    check_hashes: bool = True,
) -> list[str]:
    """Validate fixed status fields, the exact witness, and local source pins."""

    issues: list[str] = []
    if document.get("schema_version") != "1.0.0":
        issues.append("schema_version mismatch")
    if document.get("gate") != "DEP-R09 filtration sensitivity and survivor floor":
        issues.append("gate mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("character_phase_counterexample") != asdict(
        character_phase_counterexample()
    ):
        issues.append("character counterexample mismatch")
    if document.get("next_gate") != (
        "Prove a same-law conditional second moment or a filtration martingale "
        "increment plus conditional-variance theorem for the actual FMT output; "
        "do not infer it from survivor-count sensitivity."
    ):
        issues.append("next_gate mismatch")

    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 5:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {"FMT", "FGKMT", "THEORY55", "THEORY79", "THEORY80"}
    keys = {
        item.get("key")
        for item in sources
        if isinstance(item, dict)
    }
    if keys != expected_keys:
        issues.append("source keys mismatch")

    if check_hashes:
        for source in sources:
            if not isinstance(source, dict):
                issues.append("invalid source entry")
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
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != digest:
                issues.append(f"{key} hash mismatch")
    return issues
