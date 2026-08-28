"""Exact finite-population hypergeometric sampling beyond NumPy's size limit.

NumPy's ``Generator.hypergeometric`` requires both category counts to be
strictly below 1e9.  P013 can exceed that implementation limit even though
all mathematical parameters remain ordinary signed 64-bit integers.

For large parameters this module uses a symmetry of the hypergeometric law
and sequential sampling without replacement.  If

    X ~ Hypergeometric(N, K, n),

then one may instead expose whichever is smallest among the K marked items,
the N-K unmarked items, the n sampled positions, or the N-n omitted positions.
The corresponding sequential Bernoulli probabilities are conditional exact
probabilities for sampling without replacement.  This preserves the target
finite-population distribution; it is not a binomial approximation.

Reference: V. Kachitvichyanukul and B. W. Schmeiser, "Computer Generation
of Hypergeometric Random Variates", Journal of Statistical Computation and
Simulation 22 (1985), 127-145, DOI 10.1080/00949658508810839.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np


NUMPY_CATEGORY_LIMIT = 1_000_000_000
MAX_SEQUENTIAL_DRAWS = 2_000_000


class HypergeometricSamplingError(ValueError):
    """Raised when a requested exact sampler configuration is invalid."""


@dataclass(frozen=True, slots=True)
class HypergeometricSamplingPlan:
    backend: str
    symmetry: str
    population: int
    marked: int
    sequential_draws: int
    output_transform: str

    def as_dict(self) -> dict[str, int | str]:
        return asdict(self)


def _validate_parameters(ngood: int, nbad: int, nsample: int, size: int) -> None:
    if any(isinstance(value, bool) for value in (ngood, nbad, nsample, size)):
        raise HypergeometricSamplingError("boolean hypergeometric parameters are invalid")
    if ngood < 0 or nbad < 0 or nsample < 0 or size < 0:
        raise HypergeometricSamplingError("hypergeometric parameters must be nonnegative")
    if nsample > ngood + nbad:
        raise HypergeometricSamplingError("sample size exceeds the population")
    if ngood + nbad > np.iinfo(np.int64).max:
        raise HypergeometricSamplingError("population exceeds signed-int64 range")


def hypergeometric_sampling_plan(
    ngood: int,
    nbad: int,
    nsample: int,
    *,
    force_sequential: bool = False,
) -> HypergeometricSamplingPlan:
    """Select a deterministic exact backend and the cheapest symmetry."""

    ngood = int(ngood)
    nbad = int(nbad)
    nsample = int(nsample)
    _validate_parameters(ngood, nbad, nsample, 0)
    population = ngood + nbad
    if not force_sequential and ngood < NUMPY_CATEGORY_LIMIT and nbad < NUMPY_CATEGORY_LIMIT:
        return HypergeometricSamplingPlan(
            "numpy_hypergeometric",
            "native",
            population,
            ngood,
            nsample,
            "identity",
        )

    candidates = (
        # Expose all marked population items and count how many lie in the
        # fixed sample.  This is usually cheapest for rare prime-gap sizes.
        (ngood, 0, "marked_items", nsample, "identity"),
        # Expose all unmarked items; marked-in-sample = n - unmarked-in-sample.
        (nbad, 1, "unmarked_items", nsample, "sample_minus_draw"),
        # Draw the sample directly and count marked items.
        (nsample, 2, "sampled_positions", ngood, "identity"),
        # Draw the omitted positions; marked-in-sample = K - marked-omitted.
        (population - nsample, 3, "omitted_positions", ngood, "good_minus_draw"),
    )
    draws, _, symmetry, marked, transform = min(candidates)
    if draws > MAX_SEQUENTIAL_DRAWS:
        raise HypergeometricSamplingError(
            "exact sequential hypergeometric plan exceeds the reviewed draw cap: "
            f"{draws} > {MAX_SEQUENTIAL_DRAWS}"
        )
    return HypergeometricSamplingPlan(
        "exact_sequential_symmetry",
        symmetry,
        population,
        marked,
        draws,
        transform,
    )


def _sequential_marked_count(
    rng: np.random.Generator,
    *,
    population: int,
    marked: int,
    draws: int,
    size: int,
) -> np.ndarray:
    """Draw exact marked-item counts by conditional sampling without replacement."""

    result = np.zeros(size, dtype=np.int64)
    if size == 0 or draws == 0 or marked == 0:
        return result
    if marked == population:
        result.fill(draws)
        return result
    for offset in range(draws):
        remaining_population = population - offset
        remaining_marked = marked - result
        probabilities = remaining_marked.astype(np.float64) / remaining_population
        result += rng.random(size) < probabilities
    return result


def sample_hypergeometric(
    rng: np.random.Generator,
    ngood: int,
    nbad: int,
    nsample: int,
    *,
    size: int,
    force_sequential: bool = False,
) -> tuple[np.ndarray, HypergeometricSamplingPlan]:
    """Sample the exact finite-population law and return its audited plan."""

    ngood = int(ngood)
    nbad = int(nbad)
    nsample = int(nsample)
    size = int(size)
    _validate_parameters(ngood, nbad, nsample, size)
    plan = hypergeometric_sampling_plan(
        ngood,
        nbad,
        nsample,
        force_sequential=force_sequential,
    )
    if plan.backend == "numpy_hypergeometric":
        values = rng.hypergeometric(ngood, nbad, nsample, size=size)
        return np.asarray(values, dtype=np.int64), plan

    exposed = _sequential_marked_count(
        rng,
        population=plan.population,
        marked=plan.marked,
        draws=plan.sequential_draws,
        size=size,
    )
    if plan.output_transform == "identity":
        values = exposed
    elif plan.output_transform == "sample_minus_draw":
        values = nsample - exposed
    elif plan.output_transform == "good_minus_draw":
        values = ngood - exposed
    else:  # pragma: no cover - protected by the frozen plan constructor
        raise HypergeometricSamplingError("unknown hypergeometric output transform")

    lower = max(0, nsample - nbad)
    upper = min(ngood, nsample)
    if values.size and (int(values.min()) < lower or int(values.max()) > upper):
        raise HypergeometricSamplingError("sample fell outside hypergeometric support")
    return np.asarray(values, dtype=np.int64), plan


__all__ = [
    "HypergeometricSamplingError",
    "HypergeometricSamplingPlan",
    "MAX_SEQUENTIAL_DRAWS",
    "NUMPY_CATEGORY_LIMIT",
    "hypergeometric_sampling_plan",
    "sample_hypergeometric",
]
