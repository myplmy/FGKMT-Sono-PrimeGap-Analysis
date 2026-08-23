"""Exact finite-range residue-state certificates for thresholded prime gaps.

The rigorous output of this module is an integer upper bound for the number of
consecutive-prime gaps whose *start prime* lies in ``[A, B)`` and whose length
is at least ``H``.  It is deliberately separate from the canonical end-bounded
``G(x)`` used by the FGKMT/Sono envelope analysis.

Floating-point linear programming is used only to discover a candidate dual
certificate.  Every accepted certificate is checked again with integer and
``Fraction`` arithmetic.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Iterator, Sequence

import mpmath as mp
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

from source.provenance import require_experiment_approval, sha256_file


DEFAULT_A = 10**20
DEFAULT_B = 10**21
DEFAULT_H = 1856
DEFAULT_MODULUS = 2310
DEFAULT_DENOMINATOR = 10**15
PI_1E20 = 2_220_819_602_560_918_840
PI_1E21 = 21_127_269_486_018_731_928
SUPPLIED_CERTIFICATE_SHA256 = (
    "44c6a9e51b5f99ef2f49f89c89cfc40604e83ce8fe20e802f21733109b1e92fb"
)
DEFAULT_SOLVE_CONSTRAINT_CAP = 1_000_000


class CertificateError(ValueError):
    """Raised when a claimed exact certificate does not verify."""


class ResourceGuardError(RuntimeError):
    """Raised before an LP that exceeds the configured safety limit."""


@dataclass(frozen=True)
class RationalCertificate:
    modulus: int
    threshold: int
    denominator: int
    lambda_num: int
    mu_num: int
    t_num: int
    phi_num: tuple[int, ...]
    internal_bound: int
    total_bound: int


def _ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def squarefree_even_prime_factors(modulus: int) -> tuple[int, ...]:
    """Return factors and reject moduli outside the proved model contract."""

    if modulus < 2 or modulus % 2:
        raise ValueError("modulus must be an even squarefree integer")
    remaining = modulus
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= remaining:
        exponent = 0
        while remaining % divisor == 0:
            remaining //= divisor
            exponent += 1
        if exponent > 1:
            raise ValueError("modulus must be squarefree")
        if exponent == 1:
            factors.append(divisor)
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        factors.append(remaining)
    if math.prod(factors) != modulus or factors[0] != 2:
        raise ValueError("modulus factorization failed the even-squarefree contract")
    return tuple(factors)


def unit_residues(modulus: int) -> tuple[int, ...]:
    squarefree_even_prime_factors(modulus)
    return tuple(r for r in range(modulus) if math.gcd(r, modulus) == 1)


def state_count(modulus: int) -> int:
    return math.prod(p - 1 for p in squarefree_even_prime_factors(modulus))


def count_small_transition_edges(modulus: int, threshold: int) -> int:
    """Count minimal representatives ``0 < d < threshold`` without O(phi(M)^2)."""

    if threshold < 2:
        raise ValueError("threshold must be at least 2")
    factors = squarefree_even_prime_factors(modulus)
    upper = min(threshold - 1, modulus - 1)
    count = 0
    for difference in range(2, upper + 1, 2):
        count += math.prod(
            p - 1 if difference % p == 0 else p - 2 for p in factors
        )
    if modulus < threshold:
        count += state_count(modulus)  # residue self-transition, d0 = modulus
    return count


def transition_resource_estimate(
    modulus: int,
    threshold: int,
    *,
    solve_constraint_cap: int = DEFAULT_SOLVE_CONSTRAINT_CAP,
) -> dict[str, object]:
    states = state_count(modulus)
    small_edges = count_small_transition_edges(modulus, threshold)
    large_edges = states * states
    constraints = small_edges + large_edges
    nonzeros_upper = 4 * constraints + 4 * states
    # COO construction alone needs row, column, and value arrays.  Solver
    # presolve/basis storage is implementation-dependent and can be much larger.
    coo_lower_bytes = nonzeros_upper * 24 + constraints * 8
    conservative_working_bytes = coo_lower_bytes * 6
    return {
        "modulus": modulus,
        "threshold": threshold,
        "states": states,
        "small_transition_constraints": small_edges,
        "large_transition_constraints": large_edges,
        "total_transition_constraints": constraints,
        "lp_variables": states + 3,
        "coo_construction_lower_bound_gib": coo_lower_bytes / (1024**3),
        "conservative_working_estimate_gib": conservative_working_bytes
        / (1024**3),
        "solve_constraint_cap": solve_constraint_cap,
        "solve_allowed_by_guard": constraints <= solve_constraint_cap,
        "estimate_is_not_a_memory_guarantee": True,
    }


def _least_large_representative(d0: int, modulus: int, threshold: int) -> int:
    if d0 >= threshold:
        return d0
    steps = (threshold - d0 + modulus - 1) // modulus
    return d0 + steps * modulus


def iter_transition_edges_pairwise(
    modulus: int, threshold: int
) -> Iterator[tuple[int, int, int, int]]:
    """Enumerate proof constraints by ordered residue pairs."""

    residues = unit_residues(modulus)
    for i, source in enumerate(residues):
        for j, target in enumerate(residues):
            difference = (target - source) % modulus
            d0 = difference if difference else modulus
            if d0 < threshold:
                yield i, j, d0, 0
            yield i, j, _least_large_representative(
                d0, modulus, threshold
            ), 1


def iter_transition_edges_by_offsets(
    modulus: int, threshold: int
) -> Iterator[tuple[int, int, int, int]]:
    """Alternative edge construction used to cross-check the pairwise builder."""

    residues = unit_residues(modulus)
    index = {residue: i for i, residue in enumerate(residues)}
    for i, source in enumerate(residues):
        for d0 in range(2, modulus + 1, 2):
            target = (source + d0) % modulus
            j = index.get(target)
            if j is None:
                continue
            if d0 < threshold:
                yield i, j, d0, 0
            yield i, j, _least_large_representative(
                d0, modulus, threshold
            ), 1


def parse_certificate_text(
    text: str,
    *,
    default_modulus: int = DEFAULT_MODULUS,
    default_threshold: int = DEFAULT_H,
) -> RationalCertificate:
    values: dict[str, object] = {}
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        if "=" not in line:
            raise CertificateError(f"certificate line {line_number} lacks '='")
        key, raw_value = line.split("=", 1)
        if key in values:
            raise CertificateError(f"duplicate certificate key: {key}")
        if key == "phi_num":
            try:
                values[key] = tuple(int(item) for item in raw_value.split(","))
            except ValueError as exc:
                raise CertificateError("phi_num contains a non-integer") from exc
        else:
            try:
                values[key] = int(raw_value)
            except ValueError as exc:
                raise CertificateError(f"certificate key {key} is not an integer") from exc

    required = {
        "D",
        "lambda_num",
        "mu_num",
        "t_num",
        "phi_num",
        "internal_bound",
        "total_bound",
    }
    missing = sorted(required.difference(values))
    if missing:
        raise CertificateError(f"certificate keys are missing: {missing}")
    allowed = required | {"modulus", "threshold"}
    unknown = sorted(set(values).difference(allowed))
    if unknown:
        raise CertificateError(f"unknown certificate keys: {unknown}")

    return RationalCertificate(
        modulus=int(values.get("modulus", default_modulus)),
        threshold=int(values.get("threshold", default_threshold)),
        denominator=int(values["D"]),
        lambda_num=int(values["lambda_num"]),
        mu_num=int(values["mu_num"]),
        t_num=int(values["t_num"]),
        phi_num=tuple(values["phi_num"]),  # type: ignore[arg-type]
        internal_bound=int(values["internal_bound"]),
        total_bound=int(values["total_bound"]),
    )


def read_certificate(
    path: Path,
    *,
    default_modulus: int = DEFAULT_MODULUS,
    default_threshold: int = DEFAULT_H,
) -> RationalCertificate:
    return parse_certificate_text(
        path.read_text(encoding="utf-8"),
        default_modulus=default_modulus,
        default_threshold=default_threshold,
    )


def certificate_text(certificate: RationalCertificate) -> str:
    return "\n".join(
        [
            f"modulus={certificate.modulus}",
            f"threshold={certificate.threshold}",
            f"D={certificate.denominator}",
            f"lambda_num={certificate.lambda_num}",
            f"mu_num={certificate.mu_num}",
            f"t_num={certificate.t_num}",
            "phi_num=" + ",".join(map(str, certificate.phi_num)),
            f"internal_bound={certificate.internal_bound}",
            f"total_bound={certificate.total_bound}",
            "",
        ]
    )


def heuristic_normalization_scale(
    a: int = DEFAULT_A, b: int = DEFAULT_B, threshold: int = DEFAULT_H
) -> mp.mpf:
    """Return the memo's heuristic scale; this is not part of the proof."""

    mp.mp.dps = 60
    b_mp = mp.mpf(b)
    span = mp.mpf(b - a)
    h_mp = mp.mpf(threshold)
    return span / mp.log(b_mp) * mp.exp(-h_mp / mp.log(b_mp))


def verify_certificate(
    certificate: RationalCertificate,
    *,
    a: int = DEFAULT_A,
    b: int = DEFAULT_B,
    pi_a: int = PI_1E20,
    pi_b: int = PI_1E21,
    edge_method: str = "pairwise",
) -> dict[str, object]:
    """Verify every dual inequality and recompute the finite-range bound."""

    if not (0 < a < b):
        raise CertificateError("range must satisfy 0 < A < B")
    if certificate.threshold < 2:
        raise CertificateError("threshold must be at least 2")
    if certificate.denominator <= 0:
        raise CertificateError("certificate denominator must be positive")
    if certificate.lambda_num < 0:
        raise CertificateError("lambda must be nonnegative for representative reduction")
    if not (0 <= pi_a < pi_b):
        raise CertificateError("prime counts must satisfy 0 <= pi(A) < pi(B)")

    residues = unit_residues(certificate.modulus)
    if len(certificate.phi_num) != len(residues):
        raise CertificateError(
            f"phi length {len(certificate.phi_num)} != state count {len(residues)}"
        )
    max_phi = max(abs(value) for value in certificate.phi_num)
    if max_phi > certificate.t_num:
        raise CertificateError("t_num does not bound every potential")

    if edge_method == "pairwise":
        edges = iter_transition_edges_pairwise(
            certificate.modulus, certificate.threshold
        )
    elif edge_method == "offsets":
        edges = iter_transition_edges_by_offsets(
            certificate.modulus, certificate.threshold
        )
    else:
        raise ValueError(f"unknown edge method: {edge_method}")

    constraint_count = 0
    minimum_slack: int | None = None
    for i, j, gap, weight in edges:
        slack = (
            certificate.lambda_num * gap
            + certificate.mu_num
            + certificate.phi_num[i]
            - certificate.phi_num[j]
            - weight * certificate.denominator
        )
        if slack < 0:
            raise CertificateError(
                "negative dual slack on "
                f"edge {i}->{j}, gap={gap}, weight={weight}, slack={slack}"
            )
        minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
        constraint_count += 1

    estimate = transition_resource_estimate(
        certificate.modulus, certificate.threshold
    )
    if constraint_count != estimate["total_transition_constraints"]:
        raise CertificateError("enumerated constraint count disagrees with exact estimate")

    internal_gap_count = pi_b - pi_a - 1
    if internal_gap_count <= 0:
        raise CertificateError("the fixed finite range must contain at least two primes")
    span = b - a
    bound_fraction = Fraction(
        certificate.lambda_num * span
        + certificate.mu_num * internal_gap_count
        + 2 * certificate.t_num,
        certificate.denominator,
    )
    internal_bound = _ceil_fraction(bound_fraction)
    # N_{>=H}(A,B) is start-bounded.  At most one final start prime below B
    # can have its next prime at or beyond B.
    total_bound = internal_bound + 1
    if internal_bound != certificate.internal_bound:
        raise CertificateError(
            f"internal bound mismatch: {internal_bound} != {certificate.internal_bound}"
        )
    if total_bound != certificate.total_bound:
        raise CertificateError(
            f"total bound mismatch: {total_bound} != {certificate.total_bound}"
        )

    packing_internal = span // certificate.threshold
    packing_total = packing_internal + 1
    improvement = Fraction(packing_total - total_bound, packing_total)
    normalization = heuristic_normalization_scale(a, b, certificate.threshold)
    c_normalized = mp.mpf(total_bound) / normalization
    return {
        "status": "PASS",
        "theorem_scope": "start-bounded thresholded consecutive-prime-gap count",
        "range": {"A_inclusive": str(a), "B_exclusive": str(b)},
        "threshold": certificate.threshold,
        "modulus": certificate.modulus,
        "states": len(residues),
        "edge_constraints": constraint_count,
        "minimum_integer_slack": minimum_slack,
        "pi_A": str(pi_a),
        "pi_B": str(pi_b),
        "internal_gap_count": str(internal_gap_count),
        "internal_bound": str(internal_bound),
        "right_boundary_crossing_allowance": 1,
        "total_start_bounded_upper_bound": str(total_bound),
        "corrected_packing_total_bound": str(packing_total),
        "improvement_fraction": f"{improvement.numerator}/{improvement.denominator}",
        "improvement_percent": float(improvement * 100),
        "heuristic_normalization_formula": "(B-A)/ln(B)*exp(-H/ln(B))",
        "heuristic_normalization_scale": mp.nstr(normalization, 40),
        "C_normalized_upper_bound_heuristic": mp.nstr(c_normalized, 40),
        "C_is_not_the_rigorous_claim": True,
        "direct_search_acceleration_proved": False,
    }


def _build_sparse_dual_problem(
    edges: Sequence[tuple[int, int, int, int]],
    states: int,
    *,
    span: int,
    internal_gap_count: int,
) -> tuple[np.ndarray, coo_matrix, np.ndarray, list[tuple[float | None, float | None]]]:
    variables = states + 3  # lambda, mu, phi[states], t
    rows: list[int] = []
    columns: list[int] = []
    data: list[float] = []
    rhs: list[float] = []
    for row, (i, j, gap, weight) in enumerate(edges):
        rows.extend((row, row, row, row))
        columns.extend((0, 1, 2 + i, 2 + j))
        data.extend((-float(gap), -1.0, -1.0, 1.0))
        rhs.append(-float(weight))

    base = len(edges)
    t_index = variables - 1
    for i in range(states):
        row = base + 2 * i
        rows.extend((row, row))
        columns.extend((2 + i, t_index))
        data.extend((1.0, -1.0))
        rhs.append(0.0)
        row += 1
        rows.extend((row, row))
        columns.extend((2 + i, t_index))
        data.extend((-1.0, -1.0))
        rhs.append(0.0)

    matrix = coo_matrix(
        (data, (rows, columns)),
        shape=(len(edges) + 2 * states, variables),
    ).tocsr()
    objective = np.zeros(variables)
    objective[0] = span / internal_gap_count
    objective[1] = 1.0
    objective[-1] = 2.0 / internal_gap_count
    bounds: list[tuple[float | None, float | None]] = (
        [(0.0, None), (None, None)]
        + [(None, None)] * states
        + [(0.0, None)]
    )
    return objective, matrix, np.asarray(rhs, dtype=float), bounds


def discover_certificate(
    modulus: int,
    *,
    threshold: int = DEFAULT_H,
    a: int = DEFAULT_A,
    b: int = DEFAULT_B,
    pi_a: int = PI_1E20,
    pi_b: int = PI_1E21,
    denominator: int = DEFAULT_DENOMINATOR,
    solve_constraint_cap: int = DEFAULT_SOLVE_CONSTRAINT_CAP,
) -> tuple[RationalCertificate, dict[str, object]]:
    """Find a floating candidate, repair it, then exact-verify it."""

    estimate = transition_resource_estimate(
        modulus, threshold, solve_constraint_cap=solve_constraint_cap
    )
    constraints = int(estimate["total_transition_constraints"])
    if constraints > solve_constraint_cap:
        raise ResourceGuardError(
            f"modulus {modulus} requires {constraints} transition constraints; "
            f"configured cap is {solve_constraint_cap}"
        )
    if denominator <= 0:
        raise ValueError("denominator must be positive")

    internal_gap_count = pi_b - pi_a - 1
    span = b - a
    residues = unit_residues(modulus)
    edges = list(iter_transition_edges_pairwise(modulus, threshold))
    if len(edges) != constraints:
        raise CertificateError("edge materialization disagrees with resource estimate")

    objective, matrix, rhs, bounds = _build_sparse_dual_problem(
        edges,
        len(residues),
        span=span,
        internal_gap_count=internal_gap_count,
    )
    started = time.perf_counter()
    result = linprog(
        objective,
        A_ub=matrix,
        b_ub=rhs,
        bounds=bounds,
        method="highs",
    )
    elapsed = time.perf_counter() - started
    if not result.success:
        raise RuntimeError(f"LP candidate discovery failed: {result.message}")

    lambda_num = max(0, int(round(float(result.x[0]) * denominator)))
    mu_num = int(round(float(result.x[1]) * denominator))
    potentials = [
        int(round(float(value) * denominator))
        for value in result.x[2 : 2 + len(residues)]
    ]
    # Potentials are translation-invariant.  Centering weakly reduces t.
    shift = (max(potentials) + min(potentials)) // 2
    potentials = [value - shift for value in potentials]
    t_num = max(abs(value) for value in potentials)

    minimum_slack = min(
        lambda_num * gap
        + mu_num
        + potentials[i]
        - potentials[j]
        - weight * denominator
        for i, j, gap, weight in edges
    )
    repair = max(0, -minimum_slack)
    mu_num += repair
    exact_bound = Fraction(
        lambda_num * span + mu_num * internal_gap_count + 2 * t_num,
        denominator,
    )
    internal_bound = _ceil_fraction(exact_bound)
    certificate = RationalCertificate(
        modulus=modulus,
        threshold=threshold,
        denominator=denominator,
        lambda_num=lambda_num,
        mu_num=mu_num,
        t_num=t_num,
        phi_num=tuple(potentials),
        internal_bound=internal_bound,
        total_bound=internal_bound + 1,
    )
    verification = verify_certificate(
        certificate, a=a, b=b, pi_a=pi_a, pi_b=pi_b
    )
    discovery = {
        "modulus": modulus,
        "floating_solver": "scipy.optimize.linprog(method=highs)",
        "floating_solver_success": True,
        "floating_objective": float(result.fun),
        "discovery_elapsed_seconds": elapsed,
        "rational_denominator": denominator,
        "mu_integer_repair": repair,
        "resource_estimate": estimate,
        "exact_verification": verification,
    }
    return certificate, discovery


def _write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_manifest(output_directory: Path, mode: str, artifact_names: Iterable[str]) -> None:
    artifacts = {
        name: sha256_file(output_directory / name) for name in sorted(artifact_names)
    }
    _write_json(
        output_directory / "manifest.json",
        {
            "status": "PASS",
            "mode": mode,
            "artifacts_sha256": artifacts,
            "gpu_used": False,
            "direct_prime_search_executed": False,
        },
    )


def run_supplied_certificate_audit(
    certificate_path: Path,
    output_directory: Path,
    *,
    approval_token: str | None,
) -> dict[str, object]:
    """Approval-gated P007 pilot; no prime enumeration is performed."""

    require_experiment_approval(approval_token)
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite result: {output_directory}")
    payload = certificate_path.read_bytes()
    certificate_hash = _sha256_bytes(payload)
    certificate = parse_certificate_text(payload.decode("utf-8"))
    report = verify_certificate(certificate)
    report.update(
        {
            "mode": "supplied-certificate-audit",
            "input_certificate_path": str(certificate_path.resolve()),
            "input_certificate_sha256": certificate_hash,
            "expected_supplied_certificate_sha256": SUPPLIED_CERTIFICATE_SHA256,
            "input_hash_matches_pinned": certificate_hash
            == SUPPLIED_CERTIFICATE_SHA256,
            "actual_prime_search_executed": False,
        }
    )
    if not report["input_hash_matches_pinned"]:
        raise CertificateError("supplied certificate hash differs from the reviewed input")

    output_directory.mkdir(parents=True)
    (output_directory / "input_certificate.txt").write_bytes(payload)
    _write_json(output_directory / "verification_report.json", report)
    _write_manifest(
        output_directory,
        "supplied-certificate-audit",
        ["input_certificate.txt", "verification_report.json"],
    )
    return report


def run_discovery_comparison(
    moduli: Sequence[int],
    output_directory: Path,
    *,
    approval_token: str | None,
    solve_constraint_cap: int = DEFAULT_SOLVE_CONSTRAINT_CAP,
) -> dict[str, object]:
    """Approval-gated P007 phase-A comparison for safe small moduli."""

    require_experiment_approval(approval_token)
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite result: {output_directory}")
    if not moduli:
        raise ValueError("at least one modulus is required")
    if tuple(sorted(set(moduli))) != tuple(moduli):
        raise ValueError("moduli must be unique and strictly increasing")
    for earlier, later in zip(moduli, moduli[1:]):
        if later % earlier:
            raise ValueError("moduli must form a divisibility chain")

    certificate_payloads: dict[str, str] = {}
    discoveries: list[dict[str, object]] = []
    for modulus in moduli:
        certificate, discovery = discover_certificate(
            modulus, solve_constraint_cap=solve_constraint_cap
        )
        name = f"certificate_mod{modulus}.txt"
        certificate_payloads[name] = certificate_text(certificate)
        discoveries.append(discovery)

    upper_bounds = [
        int(item["exact_verification"]["total_start_bounded_upper_bound"])
        for item in discoveries
    ]
    comparison = {
        "status": "PASS",
        "mode": "small-modulus-certificate-discovery-comparison",
        "moduli": list(moduli),
        "discoveries": discoveries,
        "observed_bounds_nonincreasing": all(
            later <= earlier for earlier, later in zip(upper_bounds, upper_bounds[1:])
        ),
        "mod30030_estimate_only": transition_resource_estimate(
            30030,
            DEFAULT_H,
            solve_constraint_cap=solve_constraint_cap,
        ),
        "mod30030_solve_executed": False,
        "actual_prime_search_executed": False,
        "direct_search_acceleration_proved": False,
    }

    output_directory.mkdir(parents=True)
    artifact_names: list[str] = []
    for name, text in certificate_payloads.items():
        (output_directory / name).write_text(
            text, encoding="utf-8", newline="\n"
        )
        artifact_names.append(name)
    _write_json(output_directory / "comparison_report.json", comparison)
    artifact_names.append("comparison_report.json")
    _write_manifest(output_directory, comparison["mode"], artifact_names)
    return comparison


def verify_saved_result(result_directory: Path) -> dict[str, object]:
    manifest_path = result_directory / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    issues: list[str] = []
    artifacts = manifest.get("artifacts_sha256")
    if not isinstance(artifacts, dict):
        issues.append("manifest lacks artifacts_sha256")
        artifacts = {}
    for name, expected_hash in artifacts.items():
        path = result_directory / name
        if not path.is_file():
            issues.append(f"missing artifact: {name}")
        elif sha256_file(path) != expected_hash:
            issues.append(f"artifact hash mismatch: {name}")

    mode = manifest.get("mode")
    recomputed: list[dict[str, object]] = []
    try:
        if mode == "supplied-certificate-audit":
            certificate = read_certificate(result_directory / "input_certificate.txt")
            recomputed.append(verify_certificate(certificate))
        elif mode == "small-modulus-certificate-discovery-comparison":
            report = json.loads(
                (result_directory / "comparison_report.json").read_text(encoding="utf-8")
            )
            for modulus in report["moduli"]:
                certificate = read_certificate(
                    result_directory / f"certificate_mod{modulus}.txt"
                )
                recomputed.append(verify_certificate(certificate))
        else:
            issues.append(f"unknown manifest mode: {mode}")
    except Exception as exc:  # report exact saved-artifact failure, do not mask it
        issues.append(f"exact recomputation failed: {type(exc).__name__}: {exc}")

    return {
        "status": "PASS" if not issues else "FAIL",
        "mode": mode,
        "issues": issues,
        "recomputed_certificate_count": len(recomputed),
        "actual_prime_search_executed": False,
    }


__all__ = [
    "CertificateError",
    "DEFAULT_A",
    "DEFAULT_B",
    "DEFAULT_H",
    "DEFAULT_MODULUS",
    "DEFAULT_SOLVE_CONSTRAINT_CAP",
    "PI_1E20",
    "PI_1E21",
    "RationalCertificate",
    "ResourceGuardError",
    "SUPPLIED_CERTIFICATE_SHA256",
    "certificate_text",
    "count_small_transition_edges",
    "discover_certificate",
    "iter_transition_edges_by_offsets",
    "iter_transition_edges_pairwise",
    "parse_certificate_text",
    "read_certificate",
    "run_discovery_comparison",
    "run_supplied_certificate_audit",
    "state_count",
    "transition_resource_estimate",
    "unit_residues",
    "verify_certificate",
    "verify_saved_result",
]
