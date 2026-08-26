"""Memory-bounded modulus-30030 cutting-plane experiment for P010A G4.

The full 35,224,647-row transition matrix is never materialized.  A sparse
working set is solved with HiGHS, every floating candidate is separated by a
full streaming scan, and every candidate considered for the final result is
rounded, repaired, and checked with exact integer arithmetic.
"""

from __future__ import annotations

import json
import shutil
import time
from dataclasses import asdict
from fractions import Fraction
from pathlib import Path
from typing import Callable, Iterable

import numpy as np
from scipy.optimize import linprog

from source.finite_gap_certificate import (
    DEFAULT_A,
    DEFAULT_B,
    DEFAULT_DENOMINATOR,
    DEFAULT_H,
    PI_1E20,
    PI_1E21,
    RationalCertificate,
    _build_sparse_dual_problem,
    _ceil_fraction,
    certificate_text,
    read_certificate,
    state_count,
)
from source.finite_gap_replay import verify_saved_mod30030_exact_lift
from source.finite_gap_separation import (
    SeparationCandidate,
    scan_exact_certificate_constraints,
    scan_smallest_transition_slacks,
    scan_transition_violations,
)
from source.provenance import require_experiment_approval, sha256_file


P010A_G4_EXPERIMENT = "P010A_MOD30030_CUTTING_PLANE"
TARGET_MODULUS = 30_030
BASELINE_TOTAL_BOUND = 439_161_464_927_854_179
MAX_ALLOWED_WALL_SECONDS = 43_200
MAX_ALLOWED_DISK_BYTES = 50_000_000_000
MAX_ALLOWED_WORKING_CONSTRAINTS = 500_000

Edge = tuple[int, int, int, int]


class CuttingPlaneError(RuntimeError):
    """Raised when a P010A G4 contract or resource gate fails."""


def _write_json_exclusive(path: Path, payload: object) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def _directory_bytes(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def _candidate_from_vector(vector: np.ndarray, states: int) -> SeparationCandidate:
    if vector.ndim != 1 or vector.size < states + 2 or not np.isfinite(vector).all():
        raise CuttingPlaneError("solver candidate vector is incomplete or non-finite")
    return SeparationCandidate(
        lambda_value=max(0.0, float(vector[0])),
        mu_value=float(vector[1]),
        potentials=tuple(float(value) for value in vector[2 : 2 + states]),
    )


def _candidate_from_certificate(certificate: RationalCertificate) -> SeparationCandidate:
    scale = certificate.denominator
    return SeparationCandidate(
        lambda_value=certificate.lambda_num / scale,
        mu_value=certificate.mu_num / scale,
        potentials=tuple(value / scale for value in certificate.phi_num),
    )


def _edge_from_payload(payload: dict[str, object]) -> Edge:
    return (
        int(payload["source_index"]),
        int(payload["target_index"]),
        int(payload["gap"]),
        int(payload["weight"]),
    )


def _certificate_objective_numerator(certificate: RationalCertificate) -> int:
    span = DEFAULT_B - DEFAULT_A
    internal_gap_count = PI_1E21 - PI_1E20 - 1
    return (
        certificate.lambda_num * span
        + certificate.mu_num * internal_gap_count
        + 2 * certificate.t_num
    )


def rationalize_and_repair_candidate(
    candidate: SeparationCandidate,
    *,
    modulus: int,
    threshold: int,
    denominator: int = DEFAULT_DENOMINATOR,
    chunk_rows: int = 64,
    allow_large_state_scan: bool = False,
) -> tuple[RationalCertificate, dict[str, object]]:
    """Round a floating candidate and exactly repair its common mu slack."""

    if denominator <= 0:
        raise ValueError("denominator must be positive")
    states = state_count(modulus)
    if len(candidate.potentials) != states:
        raise ValueError("candidate potential count differs from state count")
    lambda_num = max(0, int(round(candidate.lambda_value * denominator)))
    mu_num = int(round(candidate.mu_value * denominator))
    potentials = [int(round(value * denominator)) for value in candidate.potentials]
    shift = (max(potentials) + min(potentials)) // 2
    potentials = [value - shift for value in potentials]
    t_num = max(abs(value) for value in potentials)
    provisional = RationalCertificate(
        modulus=modulus,
        threshold=threshold,
        denominator=denominator,
        lambda_num=lambda_num,
        mu_num=mu_num,
        t_num=t_num,
        phi_num=tuple(potentials),
        internal_bound=0,
        total_bound=0,
    )
    before = scan_exact_certificate_constraints(
        provisional,
        chunk_rows=chunk_rows,
        top_k=100,
        allow_large_state_scan=allow_large_state_scan,
    )
    minimum = int(before["minimum_integer_slack"])
    repair = max(0, -minimum)
    repaired_mu = mu_num + repair
    numerator = (
        lambda_num * (DEFAULT_B - DEFAULT_A)
        + repaired_mu * (PI_1E21 - PI_1E20 - 1)
        + 2 * t_num
    )
    exact_bound = Fraction(numerator, denominator)
    internal = _ceil_fraction(exact_bound)
    certificate = RationalCertificate(
        modulus=modulus,
        threshold=threshold,
        denominator=denominator,
        lambda_num=lambda_num,
        mu_num=repaired_mu,
        t_num=t_num,
        phi_num=tuple(potentials),
        internal_bound=internal,
        total_bound=internal + 1,
    )
    return certificate, {
        "minimum_integer_slack_before_repair": minimum,
        "mu_integer_repair": repair,
        "exact_violation_count_before_repair": int(before["violation_count"]),
        "repaired_minimum_integer_slack": minimum + repair,
        "internal_upper_bound": str(internal),
        "total_upper_bound": str(internal + 1),
        "objective_numerator": str(numerator),
        "denominator": denominator,
    }


def require_exact_lift_completion(manifest_path: Path) -> RationalCertificate:
    if not manifest_path.is_file():
        raise CuttingPlaneError("P010A exact-lift manifest is missing")
    result_directory = manifest_path.parent
    verification = verify_saved_mod30030_exact_lift(result_directory)
    if verification.get("status") != "PASS" or not verification.get("exact_recomputed"):
        raise CuttingPlaneError(
            "P010A exact-lift saved verification did not independently PASS"
        )
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        saved = json.loads(
            (result_directory / "saved_verification_report.json").read_text(
                encoding="utf-8"
            )
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise CuttingPlaneError(f"P010A exact-lift prerequisite cannot be read: {exc}") from exc
    if manifest.get("status") != "PASS":
        raise CuttingPlaneError("P010A exact-lift manifest is not PASS")
    if saved.get("status") != "PASS" or saved.get("manifest_sha256") != sha256_file(
        manifest_path
    ):
        raise CuttingPlaneError("P010A exact-lift saved report binding mismatch")
    certificate = read_certificate(result_directory / "certificate_mod30030_exact_lift.txt")
    if (
        certificate.modulus != TARGET_MODULUS
        or certificate.threshold != DEFAULT_H
        or certificate.total_bound != BASELINE_TOTAL_BOUND
    ):
        raise CuttingPlaneError("P010A exact-lift certificate contract changed")
    return certificate


def cutting_plane_preflight(manifest_path: Path) -> dict[str, object]:
    certificate = require_exact_lift_completion(manifest_path)
    return {
        "status": "PASS",
        "experiment": P010A_G4_EXPERIMENT,
        "modulus": certificate.modulus,
        "states": len(certificate.phi_num),
        "threshold": certificate.threshold,
        "baseline_total_bound": str(certificate.total_bound),
        "full_constraint_matrix_materialized": False,
        "actual_cutting_plane_executed": False,
        "direct_search_acceleration_proved": False,
    }


def _solve_working_set(
    edges: Iterable[Edge],
    *,
    states: int,
    solver_time_limit_seconds: float,
) -> object:
    edge_list = sorted(set(edges))
    objective, matrix, rhs, bounds = _build_sparse_dual_problem(
        edge_list,
        states,
        span=DEFAULT_B - DEFAULT_A,
        internal_gap_count=PI_1E21 - PI_1E20 - 1,
    )
    return linprog(
        objective,
        A_ub=matrix,
        b_ub=rhs,
        bounds=bounds,
        method="highs",
        options={
            "time_limit": max(1.0, solver_time_limit_seconds),
            "presolve": True,
            "primal_feasibility_tolerance": 1e-8,
            "dual_feasibility_tolerance": 1e-8,
        },
    )


def run_cutting_plane_experiment(
    exact_lift_manifest_path: Path,
    output_directory: Path,
    *,
    approval_token: str | None,
    max_wall_seconds: int = 39_600,
    per_solve_time_limit_seconds: int = 3_600,
    max_iterations: int = 100,
    seed_constraint_count: int = 20_000,
    add_per_iteration: int = 10_000,
    max_working_constraints: int = 250_000,
    max_disk_bytes: int = MAX_ALLOWED_DISK_BYTES,
    chunk_rows: int = 64,
    progress_callback: Callable[[dict[str, object]], None] | None = None,
) -> dict[str, object]:
    """Run the approval-gated P010A G4 working-set solve."""

    require_experiment_approval(approval_token)
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite cutting-plane result: {output_directory}")
    if not (1 <= max_wall_seconds <= MAX_ALLOWED_WALL_SECONDS):
        raise CuttingPlaneError("max wall time must be in [1, 43200] seconds")
    if not (1 <= per_solve_time_limit_seconds <= max_wall_seconds):
        raise CuttingPlaneError("per-solve time limit must not exceed total wall time")
    if not (1 <= max_iterations <= 200):
        raise CuttingPlaneError("max iterations must be in [1, 200]")
    if seed_constraint_count < 1 or add_per_iteration < 1:
        raise CuttingPlaneError("seed and add counts must be positive")
    if not (
        seed_constraint_count <= max_working_constraints <= MAX_ALLOWED_WORKING_CONSTRAINTS
    ):
        raise CuttingPlaneError("working-set constraint cap is outside the safe range")
    if not (1 <= max_disk_bytes <= MAX_ALLOWED_DISK_BYTES):
        raise CuttingPlaneError("disk cap exceeds the approved decimal 50 GB")

    baseline = require_exact_lift_completion(exact_lift_manifest_path)
    states = len(baseline.phi_num)
    started = time.perf_counter()
    output_directory.mkdir(parents=True)
    checkpoints = output_directory / "checkpoints"
    checkpoints.mkdir()
    shutil.copyfile(
        exact_lift_manifest_path,
        output_directory / "input_exact_lift_manifest.json",
    )
    shutil.copyfile(
        exact_lift_manifest_path.with_name("saved_verification_report.json"),
        output_directory / "input_exact_lift_saved_verification_report.json",
    )
    source_certificate_path = exact_lift_manifest_path.with_name(
        "certificate_mod30030_exact_lift.txt"
    )
    shutil.copyfile(
        source_certificate_path,
        output_directory / "input_certificate_mod30030_exact_lift.txt",
    )

    baseline_candidate = _candidate_from_certificate(baseline)
    seed_report = scan_smallest_transition_slacks(
        TARGET_MODULUS,
        DEFAULT_H,
        baseline_candidate,
        chunk_rows=chunk_rows,
        top_k=seed_constraint_count,
        allow_large_state_scan=True,
    )
    _write_json_exclusive(output_directory / "seed_scan_report.json", seed_report)
    if progress_callback is not None:
        progress_callback(
            {
                "stage": "seed_scan",
                "seed_constraints": len(seed_report["smallest_constraints"]),
                "scanned_constraints": int(seed_report["scanned_constraints"]),
                "elapsed_seconds": time.perf_counter() - started,
            }
        )
    working: set[Edge] = {
        _edge_from_payload(item)
        for item in seed_report["smallest_constraints"]  # type: ignore[index]
    }
    best = baseline
    best_numerator = _certificate_objective_numerator(baseline)
    best_iteration = 0
    history: list[dict[str, object]] = []
    outcome = "MAX_ITERATIONS"
    full_floating_convergence = False
    solver_runs = 0

    for iteration in range(1, max_iterations + 1):
        elapsed = time.perf_counter() - started
        remaining = max_wall_seconds - elapsed
        if remaining <= 2:
            outcome = "TIME_LIMIT"
            break
        if len(working) > max_working_constraints:
            outcome = "WORKING_SET_CAP"
            break
        solve_limit = min(float(per_solve_time_limit_seconds), max(1.0, remaining - 1))
        solve_started = time.perf_counter()
        result = _solve_working_set(
            working,
            states=states,
            solver_time_limit_seconds=solve_limit,
        )
        solver_runs += 1
        solve_elapsed = time.perf_counter() - solve_started
        vector = getattr(result, "x", None)
        record: dict[str, object] = {
            "iteration": iteration,
            "working_constraints_before_solve": len(working),
            "solver_status": int(getattr(result, "status", -1)),
            "solver_success": bool(getattr(result, "success", False)),
            "solver_message": str(getattr(result, "message", "")),
            "solver_elapsed_seconds": solve_elapsed,
            "solver_iterations": int(getattr(result, "nit", 0) or 0),
            "floating_objective": (
                None if getattr(result, "fun", None) is None else float(result.fun)
            ),
        }
        if vector is None:
            record["stop_reason"] = "solver_returned_no_candidate"
            history.append(record)
            _write_json_exclusive(
                checkpoints / f"iteration_{iteration:04d}.json", record
            )
            outcome = "SOLVER_NO_CANDIDATE"
            break

        candidate = _candidate_from_vector(np.asarray(vector, dtype=float), states)
        separation = scan_transition_violations(
            TARGET_MODULUS,
            DEFAULT_H,
            candidate,
            chunk_rows=chunk_rows,
            top_k=add_per_iteration,
            violation_tolerance=1e-8,
            allow_large_state_scan=True,
        )
        try:
            repaired, exact_candidate = rationalize_and_repair_candidate(
                candidate,
                modulus=TARGET_MODULUS,
                threshold=DEFAULT_H,
                denominator=DEFAULT_DENOMINATOR,
                chunk_rows=chunk_rows,
                allow_large_state_scan=True,
            )
            numerator = _certificate_objective_numerator(repaired)
            if numerator < best_numerator:
                best = repaired
                best_numerator = numerator
                best_iteration = iteration
            record.update(exact_candidate)
            record["candidate_strict_total_bound_improvement"] = (
                repaired.total_bound < BASELINE_TOTAL_BOUND
            )
            record["best_total_upper_bound"] = str(best.total_bound)
            record["best_iteration"] = best_iteration
        except Exception as exc:
            record["exact_candidate_error"] = f"{type(exc).__name__}: {exc}"

        violations = [
            _edge_from_payload(item)
            for item in separation["top_violations"]  # type: ignore[index]
        ]
        new_edges = [edge for edge in violations if edge not in working]
        record.update(
            {
                "scanned_constraints": int(separation["scanned_constraints"]),
                "floating_violation_count": int(separation["violation_count"]),
                "floating_minimum_slack": float(separation["minimum_slack"]),
                "new_constraints_added": len(new_edges),
                "elapsed_seconds": time.perf_counter() - started,
            }
        )
        history.append(record)
        _write_json_exclusive(checkpoints / f"iteration_{iteration:04d}.json", record)
        if progress_callback is not None:
            progress_callback({"stage": "iteration", **record})
        if _directory_bytes(output_directory) > max_disk_bytes:
            raise CuttingPlaneError("cutting-plane output exceeded disk cap")

        if int(separation["violation_count"]) == 0:
            full_floating_convergence = True
            outcome = "FULL_FLOATING_CONVERGENCE"
            break
        if not new_edges:
            outcome = "NO_NEW_VIOLATED_CONSTRAINTS"
            break
        available = max_working_constraints - len(working)
        if available <= 0:
            outcome = "WORKING_SET_CAP"
            break
        working.update(new_edges[:available])
        if len(new_edges) > available:
            outcome = "WORKING_SET_CAP"
            break
        if time.perf_counter() - started >= max_wall_seconds:
            outcome = "TIME_LIMIT"
            break

    best_path = output_directory / "best_certificate_mod30030.txt"
    with best_path.open("x", encoding="ascii", newline="\n") as handle:
        handle.write(certificate_text(best))
    exact_best = scan_exact_certificate_constraints(
        best,
        chunk_rows=chunk_rows,
        top_k=100,
        allow_large_state_scan=True,
    )
    if exact_best.get("status") != "PASS" or int(exact_best["violation_count"]) != 0:
        raise CuttingPlaneError("final best certificate failed exact verification")
    _write_json_exclusive(output_directory / "exact_best_report.json", exact_best)
    _write_json_exclusive(output_directory / "iteration_history.json", history)
    elapsed = time.perf_counter() - started
    summary = {
        "status": "PASS",
        "experiment": P010A_G4_EXPERIMENT,
        "outcome": outcome,
        "modulus": TARGET_MODULUS,
        "states": states,
        "threshold": DEFAULT_H,
        "baseline_total_upper_bound": str(BASELINE_TOTAL_BOUND),
        "best_total_upper_bound": str(best.total_bound),
        "strict_bound_improvement": best.total_bound < BASELINE_TOTAL_BOUND,
        "best_iteration": best_iteration,
        "solver_runs": solver_runs,
        "iterations_recorded": len(history),
        "working_constraints_final": len(working),
        "full_floating_convergence": full_floating_convergence,
        "exact_final_verified": True,
        "elapsed_seconds": elapsed,
        "max_wall_seconds": max_wall_seconds,
        "max_disk_bytes": max_disk_bytes,
        "artifact_bytes_before_manifest": _directory_bytes(output_directory),
        "full_constraint_matrix_materialized": False,
        "direct_search_acceleration_proved": False,
        "gpu_used": False,
    }
    _write_json_exclusive(output_directory / "summary.json", summary)
    artifact_names = (
        "input_exact_lift_manifest.json",
        "input_exact_lift_saved_verification_report.json",
        "input_certificate_mod30030_exact_lift.txt",
        "seed_scan_report.json",
        "iteration_history.json",
        "best_certificate_mod30030.txt",
        "exact_best_report.json",
        "summary.json",
    )
    manifest = {
        "status": "PASS",
        "experiment": P010A_G4_EXPERIMENT,
        "input_exact_lift_manifest_sha256": sha256_file(exact_lift_manifest_path),
        "artifacts_sha256": {
            name: sha256_file(output_directory / name) for name in artifact_names
        },
        "checkpoint_count": len(list(checkpoints.glob("iteration_*.json"))),
        "strict_bound_improvement": summary["strict_bound_improvement"],
        "direct_search_acceleration_proved": False,
        "gpu_used": False,
    }
    _write_json_exclusive(output_directory / "manifest.json", manifest)
    return summary


def verify_saved_cutting_plane(output_directory: Path) -> dict[str, object]:
    issues: list[str] = []
    try:
        manifest = json.loads(
            (output_directory / "manifest.json").read_text(encoding="utf-8")
        )
        summary = json.loads(
            (output_directory / "summary.json").read_text(encoding="utf-8")
        )
        if manifest.get("experiment") != P010A_G4_EXPERIMENT:
            issues.append("unexpected cutting-plane experiment label")
        artifacts = manifest.get("artifacts_sha256")
        if not isinstance(artifacts, dict):
            issues.append("manifest lacks artifact hashes")
            artifacts = {}
        for name, expected in artifacts.items():
            path = output_directory / str(name)
            if not path.is_file() or sha256_file(path) != str(expected):
                issues.append(f"artifact missing/hash mismatch: {name}")
        input_manifest = output_directory / "input_exact_lift_manifest.json"
        if sha256_file(input_manifest) != manifest.get(
            "input_exact_lift_manifest_sha256"
        ):
            issues.append("input exact-lift manifest binding mismatch")
        input_manifest_payload = json.loads(input_manifest.read_text(encoding="utf-8"))
        input_saved = json.loads(
            (
                output_directory
                / "input_exact_lift_saved_verification_report.json"
            ).read_text(encoding="utf-8")
        )
        if (
            input_saved.get("status") != "PASS"
            or input_saved.get("manifest_sha256") != sha256_file(input_manifest)
        ):
            issues.append("input exact-lift saved report binding mismatch")
        input_certificate = output_directory / "input_certificate_mod30030_exact_lift.txt"
        expected_input_certificate_hash = dict(
            input_manifest_payload.get("artifacts_sha256", {})
        ).get("certificate_mod30030_exact_lift.txt")
        if (
            not expected_input_certificate_hash
            or sha256_file(input_certificate) != expected_input_certificate_hash
        ):
            issues.append("input exact-lift certificate binding mismatch")
        certificate = read_certificate(
            output_directory / "best_certificate_mod30030.txt"
        )
        exact = scan_exact_certificate_constraints(
            certificate,
            chunk_rows=64,
            top_k=100,
            allow_large_state_scan=True,
        )
        if exact.get("status") != "PASS" or int(exact["violation_count"]) != 0:
            issues.append("saved best certificate exact recomputation failed")
        if str(certificate.total_bound) != str(summary.get("best_total_upper_bound")):
            issues.append("saved best bound disagrees with summary")
        strict = certificate.total_bound < BASELINE_TOTAL_BOUND
        if bool(summary.get("strict_bound_improvement")) != strict:
            issues.append("summary strict-improvement flag mismatch")
        if bool(manifest.get("strict_bound_improvement")) != strict:
            issues.append("manifest strict-improvement flag mismatch")
        if summary.get("direct_search_acceleration_proved") is not False:
            issues.append("cutting-plane result must not claim search acceleration")
    except Exception as exc:
        issues.append(f"saved cutting-plane verification failed: {type(exc).__name__}: {exc}")
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "exact_recomputed": not issues,
        "manifest_sha256": (
            sha256_file(output_directory / "manifest.json")
            if (output_directory / "manifest.json").is_file()
            else None
        ),
        "direct_search_acceleration_proved": False,
    }


__all__ = [
    "BASELINE_TOTAL_BOUND",
    "CuttingPlaneError",
    "P010A_G4_EXPERIMENT",
    "cutting_plane_preflight",
    "rationalize_and_repair_candidate",
    "require_exact_lift_completion",
    "run_cutting_plane_experiment",
    "verify_saved_cutting_plane",
]
