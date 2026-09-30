"""Finite exact checks for a common-height centered explicit-formula replay.

No primes or zeros are generated. Logarithms, remainders and zero packets in
the fixtures are supplied rational values, not analytic PNT certificates.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Sequence

from source.dep_r09_weighted_survivor_moment_audit import GaussianRational


ZERO = GaussianRational(Fraction(0))
LEDGER = Path("docs/method/theory/data/Sono_FMT_DEPR09_common_height_replay_v1.json")


def centered_mask(phi: int, selected: Sequence[int]) -> tuple[int, ...]:
    if isinstance(phi, bool) or not isinstance(phi, int) or phi < 1:
        raise ValueError("phi must be a positive integer")
    chosen = tuple(selected)
    if any(isinstance(a, bool) or not isinstance(a, int) for a in chosen):
        raise TypeError("selected indices must be integers")
    if len(set(chosen)) != len(chosen) or any(not 0 <= a < phi for a in chosen):
        raise ValueError("selected indices must be distinct and in range")
    count = len(chosen)
    membership = set(chosen)
    return tuple(phi * int(a in membership) - count for a in range(phi))


def mask_mass(phi: int, selected: Sequence[int]) -> dict[str, int]:
    weights = centered_mask(phi, selected)
    count = len(selected)
    return {
        "zero_sum": sum(weights),
        "l1": sum(abs(h) for h in weights),
        "l1_formula": 2 * count * (phi - count),
        "max_abs": max(abs(h) for h in weights),
    }


def remainder_budget(
    phi: int, selected: Sequence[int], upper_error: Fraction, lower_error: Fraction
) -> Fraction:
    if not isinstance(upper_error, Fraction) or not isinstance(lower_error, Fraction):
        raise TypeError("endpoint errors must be Fraction")
    if upper_error < 0 or lower_error < 0:
        raise ValueError("endpoint error envelopes must be nonnegative")
    return mask_mass(phi, selected)["l1"] * (upper_error + lower_error)


def common_height_packet_difference(
    upper_packets: Sequence[GaussianRational],
    lower_packets: Sequence[GaussianRational],
    upper_regularizers: Sequence[GaussianRational],
    lower_regularizers: Sequence[GaussianRational],
) -> tuple[GaussianRational, ...]:
    sequences = tuple(tuple(values) for values in (
        upper_packets, lower_packets, upper_regularizers, lower_regularizers
    ))
    if not sequences[0] or len({len(values) for values in sequences}) != 1:
        raise ValueError("channel vectors need equal nonzero length")
    if any(not isinstance(value, GaussianRational)
           for values in sequences for value in values):
        raise TypeError("channel entries must be GaussianRational")
    if sequences[2] != sequences[3]:
        raise ValueError("common-height replay requires identical regularizers")
    # Subtraction is expressed using the existing Gaussian rational operations.
    return tuple(
        (u + b_u * Fraction(-1)) +
        (x + b_x * Fraction(-1)) * Fraction(-1)
        for u, x, b_u, b_x in zip(*sequences)
    )


def _chi_mod_five(index: int, residue: int) -> GaussianRational:
    if index not in range(4) or residue not in range(1, 5):
        raise ValueError("fixture uses four modulo-five reduced residues")
    exponent = {1: 0, 2: 1, 4: 2, 3: 3}[residue]
    roots = (
        GaussianRational(Fraction(1)),
        GaussianRational(Fraction(0), Fraction(1)),
        GaussianRational(Fraction(-1)),
        GaussianRational(Fraction(0), Fraction(-1)),
    )
    return roots[(index * exponent) % 4]


def synthetic_replay_mod_five(
    selected: Sequence[int],
    upper_packets: Sequence[GaussianRational],
    lower_packets: Sequence[GaussianRational],
    regularizers: Sequence[GaussianRational],
    upper_errors: Sequence[Fraction],
    lower_errors: Sequence[Fraction],
    upper_common_mass: Fraction = Fraction(17),
    lower_common_mass: Fraction = Fraction(3),
) -> dict[str, GaussianRational]:
    """Compare residue projection and character sum with arbitrary packets."""
    if any(len(values) != 4 for values in (
        upper_packets, lower_packets, regularizers, upper_errors, lower_errors
    )):
        raise ValueError("fixture needs four channels and four residue errors")
    if any(not isinstance(value, Fraction)
           for values in (upper_errors, lower_errors) for value in values):
        raise TypeError("residue errors must be Fraction")
    if not all(isinstance(value, Fraction) for value in (
        upper_common_mass, lower_common_mass
    )):
        raise TypeError("common masses must be Fraction")
    packets = common_height_packet_difference(
        upper_packets, lower_packets, regularizers, regularizers
    )
    weights = centered_mask(4, selected)
    residues = (1, 2, 3, 4)
    residue_side = ZERO
    error_side = ZERO
    for a, h, e_u, e_x in zip(residues, weights, upper_errors, lower_errors):
        increment = GaussianRational((upper_common_mass - lower_common_mass) / 4)
        for j in range(4):
            increment = increment + (
                _chi_mod_five(j, a).conjugate() * packets[j] * Fraction(-1, 4)
            )
        error = GaussianRational(e_u - e_x)
        residue_side = residue_side + (increment + error) * Fraction(h)
        error_side = error_side + error * Fraction(h)
    signed_zero = ZERO
    for j in range(1, 4):
        coefficient = ZERO
        for index in selected:
            coefficient = coefficient + _chi_mod_five(j, residues[index]).conjugate()
        signed_zero = signed_zero + coefficient * packets[j]
    replay_side = signed_zero * Fraction(-1) + error_side
    if residue_side != replay_side:
        raise AssertionError("common-height signed replay failed")
    return {
        "residue_side": residue_side,
        "signed_zero": signed_zero,
        "weighted_remainder": error_side,
        "replay_side": replay_side,
    }


def ef_error_shape(
    scale: Fraction, log_scale: Fraction, log_f: Fraction,
    height: Fraction, log_height: Fraction, phi: int,
) -> Fraction:
    """Evaluate the source error shape on supplied rational inputs."""
    values = (scale, log_scale, log_f, height, log_height)
    if any(not isinstance(value, Fraction) for value in values):
        raise TypeError("supplied scale/log inputs must be Fraction")
    if scale <= 0 or height <= 0 or min(log_scale, log_f, log_height) < 0:
        raise ValueError("scales must be positive and logarithms nonnegative")
    centered_mask(phi, ())
    return (
        ((scale * log_scale + height) / height * log_f
         + log_scale + scale * log_scale * log_height / height) / phi
        + log_scale * log_f + scale * log_scale**2 / height
    )


def truncation_coefficient(d_upper: int = 416, height_exponent: Fraction = Fraction(3, 2)) -> Fraction:
    if isinstance(d_upper, bool) or not isinstance(d_upper, int) or d_upper < 1:
        raise ValueError("d_upper must be a positive integer")
    if not isinstance(height_exponent, Fraction) or not 1 < height_exponent <= 21:
        raise ValueError("height exponent must be a Fraction in (1,21]")
    return 4 * (d_upper**2 + (3 + height_exponent) * d_upper + 1)


def density_height_kappa(
    height_exponent: Fraction, window: Fraction = Fraction(1, 21)
) -> Fraction:
    if not isinstance(height_exponent, Fraction) or height_exponent <= 1:
        raise ValueError("height exponent must be a Fraction above one")
    if not isinstance(window, Fraction) or not 0 < window <= Fraction(1, 21):
        raise ValueError("window must be a Fraction in (0,1/21]")
    return 2 * (2 + height_exponent) * (1 + 12 * window)


def audit_ledger(repo_root: Path | None = None) -> dict[str, object]:
    """Verify pinned inputs and rational terminals, not the analytic premises."""
    root = repo_root or Path(__file__).resolve().parents[1]
    document = json.loads((root / LEDGER).read_text(encoding="utf-8"))
    for item in document["source_registry"]:
        observed = hashlib.sha256((root / item["locator"]).read_bytes()).hexdigest()
        if observed != item["sha256"]:
            raise ValueError(f"source hash mismatch: {item['key']}")
    diagnostic = document["exact_finite_diagnostic"]
    expected_terminals = {
        "truncation_coefficient": str(truncation_coefficient()),
        "kappa_s_3_over_2": str(density_height_kappa(Fraction(3, 2))),
        "kappa_s_5": str(density_height_kappa(Fraction(5))),
    }
    for name, expected in expected_terminals.items():
        if diagnostic[name] != expected:
            raise ValueError(f"rational terminal mismatch: {name}")
    open_flags = (
        "numeric_EF_multiplier_recovered", "signed_zero_gate_closed",
        "lower_height_density_transfer_closed", "pap_11_closed",
        "dep_r09_closed", "numerical_x_cert_ready",
        "bounded_x_cert_range_obtained", "threshold_calculator_ready",
        "actual_prime_or_zero_computation_run",
        "source_theorem_local_axiom_used", "proof_escape_used",
    )
    if any(diagnostic[name] is not False for name in open_flags):
        raise ValueError("an unresolved analytic or execution gate was promoted")
    if document["parameterized_correction"]["numeric_EF_multiplier"] is not None:
        raise ValueError("the unresolved EF multiplier must remain null")
    return {
        "status": "FINITE_SOURCE_PIN_AND_RATIONAL_TERMINALS_PASS",
        "source_count": len(document["source_registry"]),
        **expected_terminals,
        **{name: diagnostic[name] for name in open_flags},
    }


if __name__ == "__main__":
    print(json.dumps(audit_ledger(), sort_keys=True))
