"""Exact finite checks for the DEP-R09 weighted survivor-moment audit.

The helper evaluates complex-weighted Bernoulli survivor sums with rational
Gaussian coefficients, verifies the sharp one/two-point upper interface, and
constructs an exchangeable common-shock fixture exhibiting the beta*M loss.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
from typing import Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    REPO_ROOT
    / "docs"
    / "method"
    / "theory"
    / "data"
    / "Sono_FMT_DEPR09_weighted_survivor_moment_audit_v1.json"
)


def _fraction(value: object, name: str, *, probability: bool = False) -> Fraction:
    if not isinstance(value, Fraction):
        raise TypeError(f"{name} must be fractions.Fraction")
    if probability and not 0 <= value <= 1:
        raise ValueError(f"{name} must lie in [0,1]")
    return value


@dataclass(frozen=True)
class GaussianRational:
    real: Fraction
    imag: Fraction = Fraction(0)

    def __post_init__(self) -> None:
        if not isinstance(self.real, Fraction) or not isinstance(
            self.imag, Fraction
        ):
            raise TypeError("coordinates must be Fraction")

    def __add__(self, other: object) -> "GaussianRational":
        if not isinstance(other, GaussianRational):
            return NotImplemented
        return GaussianRational(self.real + other.real, self.imag + other.imag)

    def __mul__(self, other: object) -> "GaussianRational":
        if isinstance(other, Fraction):
            return GaussianRational(self.real * other, self.imag * other)
        if not isinstance(other, GaussianRational):
            return NotImplemented
        return GaussianRational(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real,
        )

    def conjugate(self) -> "GaussianRational":
        return GaussianRational(self.real, -self.imag)

    def norm_square(self) -> Fraction:
        return self.real**2 + self.imag**2


ZERO = GaussianRational(Fraction(0))


def weighted_second_moment(
    weights: Sequence[GaussianRational],
    single_survival: Sequence[Fraction],
    pair_survival: Mapping[tuple[int, int], Fraction],
) -> Fraction:
    """Return E|sum_i b_i X_i|^2 from exact one/two-point data."""

    weights = tuple(weights)
    singles = tuple(single_survival)
    if not weights or len(weights) != len(singles):
        raise ValueError("weights and single probabilities need equal nonzero length")
    count = len(weights)
    for index, probability in enumerate(singles):
        _fraction(probability, f"single[{index}]", probability=True)
    expected_pairs = {
        (i, j) for i in range(count) for j in range(i + 1, count)
    }
    if set(pair_survival) != expected_pairs:
        raise ValueError("pair map must contain each unordered pair exactly once")

    total = sum(
        (
            singles[index] * weight.norm_square()
            for index, weight in enumerate(weights)
        ),
        Fraction(0),
    )
    for (i, j), probability in pair_survival.items():
        probability = _fraction(
            probability, f"pair[{i},{j}]", probability=True
        )
        product = weights[i] * weights[j].conjugate()
        total += 2 * probability * product.real
    if total < 0:
        raise AssertionError("second moment must be nonnegative")
    return total


def weighted_pair_error_upper(
    weights: Sequence[GaussianRational],
    rho: Fraction,
    alpha: Fraction,
    beta: Fraction,
) -> Fraction:
    """Return the sharp entrywise one/two-point certificate.

    It verifies
      rho^2 |sum b|^2
      + ((1+alpha)rho-rho^2+beta*rho^2*(M-1)) sum |b|^2.
    """

    weights = tuple(weights)
    if not weights:
        raise ValueError("weights must be nonempty")
    rho = _fraction(rho, "rho", probability=True)
    alpha = _fraction(alpha, "alpha")
    beta = _fraction(beta, "beta")
    if alpha < 0 or beta < 0:
        raise ValueError("alpha and beta must be nonnegative")
    sum_weight = ZERO
    l2 = Fraction(0)
    for weight in weights:
        if not isinstance(weight, GaussianRational):
            raise TypeError("weights must be GaussianRational")
        sum_weight = sum_weight + weight
        l2 += weight.norm_square()
    count = len(weights)
    coefficient = (
        (1 + alpha) * rho
        - rho**2
        + beta * rho**2 * (count - 1)
    )
    return rho**2 * sum_weight.norm_square() + coefficient * l2


def common_shock_probabilities(
    count: int,
    low_probability: Fraction,
    high_probability: Fraction,
) -> dict[str, object]:
    """Return exact exchangeable one/two-point probabilities.

    A fair latent coin selects one of two Bernoulli product laws.
    """

    if isinstance(count, bool) or not isinstance(count, int) or count < 2:
        raise ValueError("count must be an integer at least two")
    low = _fraction(low_probability, "low_probability", probability=True)
    high = _fraction(high_probability, "high_probability", probability=True)
    rho = (low + high) / 2
    pair = (low**2 + high**2) / 2
    if rho == 0:
        raise ValueError("mean survival must be positive")
    beta = pair / rho**2 - 1
    singles = tuple(rho for _ in range(count))
    pairs = {
        (i, j): pair
        for i in range(count)
        for j in range(i + 1, count)
    }
    return {
        "rho": rho,
        "pair": pair,
        "beta": beta,
        "singles": singles,
        "pairs": pairs,
    }


def enumerate_common_shock_second_moment(
    weights: Sequence[GaussianRational],
    low_probability: Fraction,
    high_probability: Fraction,
) -> Fraction:
    """Exhaust the latent coin and all Bernoulli outcomes exactly."""

    weights = tuple(weights)
    if not 1 <= len(weights) <= 10:
        raise ValueError("bounded fixture requires 1..10 weights")
    low = _fraction(low_probability, "low_probability", probability=True)
    high = _fraction(high_probability, "high_probability", probability=True)
    total = Fraction(0)
    for theta in (low, high):
        for bits in itertools.product((False, True), repeat=len(weights)):
            mass = Fraction(1, 2)
            value = ZERO
            for bit, weight in zip(bits, weights):
                mass *= theta if bit else 1 - theta
                if bit:
                    value = value + weight
            total += mass * value.norm_square()
    return total


def pair_error_spectral_factor_lower(
    beta: Fraction,
    survivor_count: Fraction,
) -> Fraction:
    beta = _fraction(beta, "beta")
    survivor_count = _fraction(survivor_count, "survivor_count")
    if beta < 0 or survivor_count < 0:
        raise ValueError("inputs must be nonnegative")
    return beta * survivor_count


@dataclass(frozen=True)
class WeightedSurvivorMomentDiagnostic:
    arbitrary_complex_weight_second_moment_exact: bool
    entrywise_pair_error_upper_exact: bool
    beta_times_support_loss_is_unavoidable_from_entrywise_data: bool
    toy_count: int
    toy_rho: str
    toy_pair_probability: str
    toy_relative_pair_error: str
    toy_observed_second_moment: str
    toy_certificate_upper: str
    toy_pair_covariance_excess: str
    project_beta_times_vertex_count_exceeds_one: bool
    project_beta_rho_vertex_count_exceeds_one: bool
    gould_kelly_primary_pdf_verified: bool
    gould_kelly_uniform_nearly_regular_matching_theorem: bool
    gould_kelly_handles_current_indexed_variable_edge_covering_law: bool
    gould_kelly_weights_are_nonnegative_preselected: bool
    gould_kelly_supplies_numerical_constants_and_failure_rate: bool
    applicable_weighted_nibble_drop_in_identified: bool
    blind_weighted_moment_closed: bool
    pap_11_closed: bool
    dep_r09_closed: bool
    numerical_x_cert_ready: bool
    bounded_x_cert_range_obtained: bool
    threshold_calculator_ready: bool
    actual_prime_computation_run: bool
    source_theorem_local_axiom_used: bool
    proof_escape_used: bool


def build_diagnostic() -> WeightedSurvivorMomentDiagnostic:
    weights = tuple(GaussianRational(Fraction(1)) for _ in range(4))
    model = common_shock_probabilities(
        4, Fraction(1, 8), Fraction(3, 8)
    )
    observed = enumerate_common_shock_second_moment(
        weights, Fraction(1, 8), Fraction(3, 8)
    )
    direct = weighted_second_moment(
        weights, model["singles"], model["pairs"]
    )
    upper = weighted_pair_error_upper(
        weights, model["rho"], Fraction(0), model["beta"]
    )
    independent_baseline = (
        model["rho"] ** 2 * 16
        + (model["rho"] - model["rho"] ** 2) * 4
    )
    return WeightedSurvivorMomentDiagnostic(
        arbitrary_complex_weight_second_moment_exact=(observed == direct),
        entrywise_pair_error_upper_exact=(observed == upper),
        beta_times_support_loss_is_unavoidable_from_entrywise_data=True,
        toy_count=4,
        toy_rho=str(model["rho"]),
        toy_pair_probability=str(model["pair"]),
        toy_relative_pair_error=str(model["beta"]),
        toy_observed_second_moment=str(observed),
        toy_certificate_upper=str(upper),
        toy_pair_covariance_excess=str(observed - independent_baseline),
        project_beta_times_vertex_count_exceeds_one=True,
        project_beta_rho_vertex_count_exceeds_one=True,
        gould_kelly_primary_pdf_verified=True,
        gould_kelly_uniform_nearly_regular_matching_theorem=True,
        gould_kelly_handles_current_indexed_variable_edge_covering_law=False,
        gould_kelly_weights_are_nonnegative_preselected=True,
        gould_kelly_supplies_numerical_constants_and_failure_rate=False,
        applicable_weighted_nibble_drop_in_identified=False,
        blind_weighted_moment_closed=False,
        pap_11_closed=False,
        dep_r09_closed=False,
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
    issues: list[str] = []
    if document.get("schema_version") != "1.0.0":
        issues.append("schema_version mismatch")
    if document.get("gate") != (
        "DEP-R09 complex-weighted survivor moment and weighted nibble audit"
    ):
        issues.append("gate mismatch")
    if document.get("outcome") != (
        "EXACT_WEIGHTED_SECOND_MOMENT_INTERFACE_BUT_ENTRYWISE_PAIR_ERROR_"
        "HAS_SHARP_BETA_M_LOSS_AND_NO_WEIGHTED_NIBBLE_DROP_IN"
    ):
        issues.append("outcome mismatch")
    if document.get("exact_finite_diagnostic") != asdict(build_diagnostic()):
        issues.append("diagnostic mismatch")
    if document.get("next_gate") != (
        "Obtain a numerical covariance-operator or direct event-energy "
        "correlation theorem for the actual nonuniform indexed covering law; "
        "fixed one/two-point entrywise errors and current weighted matching "
        "theorems do not supply the required blind complex moment."
    ):
        issues.append("next_gate mismatch")

    sources = document.get("source_registry")
    if not isinstance(sources, list) or len(sources) != 6:
        issues.append("source_registry mismatch")
        return issues
    expected_keys = {
        "GOULD_KELLY2025", "FGKMT", "THEORY53", "THEORY54",
        "THEORY89", "THEORY90",
    }
    keys = {
        item.get("key") for item in sources if isinstance(item, dict)
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
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                issues.append(f"{key} hash mismatch")
    return issues


__all__ = [
    "GaussianRational",
    "LEDGER_PATH",
    "build_diagnostic",
    "common_shock_probabilities",
    "enumerate_common_shock_second_moment",
    "load_ledger",
    "pair_error_spectral_factor_lower",
    "validate_ledger",
    "weighted_pair_error_upper",
    "weighted_second_moment",
]
