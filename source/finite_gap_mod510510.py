"""P014 memory-safe staged exact/cutting-plane certificate experiment.

The experiment lifts the exact P010A modulus-30030 certificate to modulus
510510, checks every target inequality with integer arithmetic, and only then
attempts a bounded working-set optimization when the calibration gate permits.
It studies a finite count upper bound and does not prove search acceleration.
"""

from __future__ import annotations

import json
import math
import shutil
import time
from pathlib import Path
from typing import Callable

import numpy as np

from source.finite_gap_certificate import (
    DEFAULT_DENOMINATOR,
    DEFAULT_H,
    RationalCertificate,
    certificate_text,
    read_certificate,
    state_count,
    transition_resource_estimate,
)
from source.finite_gap_cutting_plane import (
    _candidate_from_certificate,
    _candidate_from_vector,
    _certificate_objective_numerator,
    _edge_from_payload,
    _solve_working_set,
    rationalize_and_repair_candidate,
    verify_saved_cutting_plane,
)
from source.finite_gap_replay import lift_certificate_exact_to_modulus
from source.finite_gap_separation import (
    scan_exact_certificate_constraints,
    scan_smallest_transition_slacks,
    scan_transition_violations,
    separation_memory_estimate,
)
from source.provenance import require_experiment_approval, sha256_file


EXPERIMENT = "P014_MOD510510_STAGED_CERTIFICATE"
SCHEMA_VERSION = "p014-mod510510-staged-certificate-v1"
SOURCE_MODULUS = 30_030
TARGET_MODULUS = 510_510
TARGET_STATES = 92_160
TARGET_CONSTRAINTS = 8_524_288_932
BASELINE_TOTAL_BOUND = 436_001_550_591_586_306
G4_MANIFEST_SHA256 = (
    "6f68c8f4c5356f29b23aa48025699e02887b1d396645f04e6eee96aa535080e9"
)
G4_CERTIFICATE_SHA256 = (
    "22e345c0cae727fe60105d30a4cf99e2672c69bbf93815f02c5084c8d5805b65"
)
G4_SAVED_REPORT_SHA256 = (
    "e10a758a93343d6af8b3c82e3b86d6aa46ba2f609cd69f36dddfb32dc7f44ca7"
)
DEFAULT_CHUNK_ROWS = 64
DEFAULT_STAGE_A_GATE_SECONDS = 14_400
MAX_WALL_SECONDS = 54_000
MAX_DISK_BYTES = 10_000_000_000
MAX_WORKING_CONSTRAINTS = 100_000

Edge = tuple[int, int, int, int]


class Mod510510Error(RuntimeError):
    """Raised when a P014 provenance, proof, or resource contract fails."""


def _write_json_exclusive(path: Path, payload: object) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def _directory_bytes(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def _overflow_guard_upper_bound(certificate: RationalCertificate) -> int:
    max_phi = max(abs(value) for value in certificate.phi_num)
    max_representative = certificate.threshold + certificate.modulus - 1
    return (
        abs(certificate.lambda_num) * max_representative
        + abs(certificate.mu_num)
        + 2 * max_phi
        + certificate.denominator
    )


def require_g4_prerequisite(result_directory: Path) -> RationalCertificate:
    manifest_path = result_directory / "manifest.json"
    report_path = result_directory / "saved_verification_report.json"
    certificate_path = result_directory / "best_certificate_mod30030.txt"
    if (
        sha256_file(manifest_path) != G4_MANIFEST_SHA256
        or sha256_file(report_path) != G4_SAVED_REPORT_SHA256
        or sha256_file(certificate_path) != G4_CERTIFICATE_SHA256
    ):
        raise Mod510510Error("P010A G4 prerequisite hash mismatch")
    verification = verify_saved_cutting_plane(result_directory)
    if verification.get("status") != "PASS" or not verification.get("exact_recomputed"):
        raise Mod510510Error("P010A G4 exact saved verification did not PASS")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report = json.loads(report_path.read_text(encoding="utf-8"))
    certificate = read_certificate(certificate_path)
    if (
        manifest.get("status") != "PASS"
        or report.get("status") != "PASS"
        or report.get("manifest_sha256") != G4_MANIFEST_SHA256
        or certificate.modulus != SOURCE_MODULUS
        or certificate.threshold != DEFAULT_H
        or certificate.lambda_num < 0
        or certificate.total_bound != BASELINE_TOTAL_BOUND
    ):
        raise Mod510510Error("P010A G4 prerequisite contract changed")
    return certificate


def preflight(result_directory: Path, *, chunk_rows: int = DEFAULT_CHUNK_ROWS) -> dict[str, object]:
    source = require_g4_prerequisite(result_directory)
    lifted = lift_certificate_exact_to_modulus(source, TARGET_MODULUS)
    resource = transition_resource_estimate(TARGET_MODULUS, DEFAULT_H)
    memory = separation_memory_estimate(TARGET_MODULUS, chunk_rows=chunk_rows, top_k=5_000)
    overflow = _overflow_guard_upper_bound(lifted)
    checks = (
        state_count(TARGET_MODULUS) == TARGET_STATES,
        int(resource["total_transition_constraints"]) == TARGET_CONSTRAINTS,
        bool(memory["under_1_gib"]),
        overflow <= int(np.iinfo(np.int64).max),
        lifted.total_bound == BASELINE_TOTAL_BOUND,
    )
    if not all(checks):
        raise Mod510510Error("P014 static resource or lift contract failed")
    return {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "source_modulus": SOURCE_MODULUS,
        "target_modulus": TARGET_MODULUS,
        "target_states": TARGET_STATES,
        "target_constraints": TARGET_CONSTRAINTS,
        "baseline_total_upper_bound": str(BASELINE_TOTAL_BOUND),
        "chunk_rows": chunk_rows,
        "conservative_scan_memory_mib": memory["conservative_working_mib"],
        "full_matrix_lower_bound_gib": resource["coo_construction_lower_bound_gib"],
        "signed_int64_guard_upper_bound": str(overflow),
        "signed_int64_limit": str(int(np.iinfo(np.int64).max)),
        "full_constraint_matrix_materialized": False,
        "actual_experiment_executed": False,
        "direct_search_acceleration_proved": False,
    }


def run_staged_experiment(
    g4_result_directory: Path,
    output_directory: Path,
    *,
    approval_token: str | None,
    max_wall_seconds: int = MAX_WALL_SECONDS,
    stage_a_gate_seconds: int = DEFAULT_STAGE_A_GATE_SECONDS,
    per_solve_time_limit_seconds: int = 1_800,
    max_iterations: int = 12,
    seed_constraint_count: int = 5_000,
    add_per_iteration: int = 5_000,
    max_working_constraints: int = MAX_WORKING_CONSTRAINTS,
    max_disk_bytes: int = MAX_DISK_BYTES,
    chunk_rows: int = DEFAULT_CHUNK_ROWS,
    runtime_resource_policy: dict[str, object] | None = None,
    progress_callback: Callable[[dict[str, object]], None] | None = None,
) -> dict[str, object]:
    require_experiment_approval(approval_token)
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite P014 result: {output_directory}")
    if not 1 <= max_wall_seconds <= MAX_WALL_SECONDS:
        raise Mod510510Error("P014 max wall must be in [1,54000] seconds")
    if not 1 <= stage_a_gate_seconds <= max_wall_seconds:
        raise Mod510510Error("stage-A gate must not exceed total wall")
    if not 1 <= per_solve_time_limit_seconds <= max_wall_seconds:
        raise Mod510510Error("per-solve limit is outside total wall")
    if not 1 <= max_iterations <= 12:
        raise Mod510510Error("P014 iteration cap must be in [1,12]")
    if seed_constraint_count < 1 or add_per_iteration < 1:
        raise Mod510510Error("seed/add counts must be positive")
    if not seed_constraint_count <= max_working_constraints <= MAX_WORKING_CONSTRAINTS:
        raise Mod510510Error("working-set cap exceeds reviewed limit")
    if not 1 <= max_disk_bytes <= MAX_DISK_BYTES:
        raise Mod510510Error("P014 disk cap exceeds decimal 10 GB")

    source = require_g4_prerequisite(g4_result_directory)
    lifted = lift_certificate_exact_to_modulus(source, TARGET_MODULUS)
    static = preflight(g4_result_directory, chunk_rows=chunk_rows)
    started = time.perf_counter()
    output_directory.mkdir(parents=True)
    input_files = {
        "input_g4_manifest.json": g4_result_directory / "manifest.json",
        "input_g4_saved_verification_report.json": g4_result_directory / "saved_verification_report.json",
        "input_g4_best_certificate_mod30030.txt": g4_result_directory / "best_certificate_mod30030.txt",
    }
    for name, source_path in input_files.items():
        shutil.copyfile(source_path, output_directory / name)
    _write_json_exclusive(output_directory / "resource_preflight.json", static)
    with (output_directory / "lifted_baseline_mod510510.txt").open("x", encoding="ascii", newline="\n") as handle:
        handle.write(certificate_text(lifted))

    if progress_callback:
        progress_callback(
            {
                "stage": "exact_lift",
                "status": "STARTED",
                "constraints": TARGET_CONSTRAINTS,
            }
        )
    stage_a_started = time.perf_counter()
    stage_a = scan_exact_certificate_constraints(
        lifted,
        chunk_rows=chunk_rows,
        top_k=100,
        allow_large_state_scan=True,
    )
    stage_a_elapsed = time.perf_counter() - stage_a_started
    if (
        stage_a.get("status") != "PASS"
        or int(stage_a["violation_count"]) != 0
        or int(stage_a["scanned_constraints"]) != TARGET_CONSTRAINTS
    ):
        raise Mod510510Error("stage-A lifted certificate exact scan failed")
    stage_a["elapsed_seconds"] = stage_a_elapsed
    _write_json_exclusive(output_directory / "stage_a_exact_report.json", stage_a)
    if progress_callback:
        progress_callback(
            {
                "stage": "exact_lift",
                "status": "PASS",
                "elapsed_seconds": stage_a_elapsed,
                "constraints": TARGET_CONSTRAINTS,
            }
        )

    best = lifted
    history: list[dict[str, object]] = []
    optimizer_run = False
    outcome = "CALIBRATION_ONLY_TIME_GATE"
    solver_runs = 0
    working: set[Edge] = set()
    best_floating_vector: np.ndarray | None = None
    best_floating_objective = math.inf

    if stage_a_elapsed <= stage_a_gate_seconds and time.perf_counter() - started < max_wall_seconds:
        optimizer_run = True
        baseline_candidate = _candidate_from_certificate(lifted)
        if progress_callback:
            progress_callback({"stage": "seed_scan", "status": "STARTED"})
        seed = scan_smallest_transition_slacks(
            TARGET_MODULUS,
            DEFAULT_H,
            baseline_candidate,
            chunk_rows=chunk_rows,
            top_k=seed_constraint_count,
            allow_large_state_scan=True,
        )
        _write_json_exclusive(output_directory / "seed_scan_report.json", seed)
        if progress_callback:
            progress_callback(
                {
                    "stage": "seed_scan",
                    "status": "PASS",
                    "constraints": int(seed["scanned_constraints"]),
                }
            )
        working = {_edge_from_payload(item) for item in seed["smallest_constraints"]}
        outcome = "MAX_ITERATIONS"
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
                states=TARGET_STATES,
                solver_time_limit_seconds=solve_limit,
            )
            solver_runs += 1
            vector = getattr(result, "x", None)
            row: dict[str, object] = {
                "iteration": iteration,
                "working_constraints_before_solve": len(working),
                "solver_status": int(getattr(result, "status", -1)),
                "solver_success": bool(getattr(result, "success", False)),
                "solver_message": str(getattr(result, "message", "")),
                "solver_elapsed_seconds": time.perf_counter() - solve_started,
                "floating_objective": None if getattr(result, "fun", None) is None else float(result.fun),
            }
            if vector is None:
                row["stop_reason"] = "solver_returned_no_candidate"
                history.append(row)
                outcome = "SOLVER_NO_CANDIDATE"
                break
            vector_array = np.asarray(vector, dtype=float)
            candidate = _candidate_from_vector(vector_array, TARGET_STATES)
            objective = float(getattr(result, "fun", math.inf))
            if math.isfinite(objective) and objective < best_floating_objective:
                best_floating_objective = objective
                best_floating_vector = vector_array.copy()
            separation = scan_transition_violations(
                TARGET_MODULUS,
                DEFAULT_H,
                candidate,
                chunk_rows=chunk_rows,
                top_k=add_per_iteration,
                violation_tolerance=1e-8,
                allow_large_state_scan=True,
            )
            violations = [_edge_from_payload(item) for item in separation["top_violations"]]
            new_edges = [edge for edge in violations if edge not in working]
            row.update(
                {
                    "scanned_constraints": int(separation["scanned_constraints"]),
                    "floating_violation_count": int(separation["violation_count"]),
                    "floating_minimum_slack": float(separation["minimum_slack"]),
                    "new_constraints_added": len(new_edges),
                    "elapsed_seconds": time.perf_counter() - started,
                }
            )
            history.append(row)
            if progress_callback:
                progress_callback({"stage": "iteration", **row})
            if _directory_bytes(output_directory) > max_disk_bytes:
                raise Mod510510Error("P014 output exceeded disk cap")
            if int(separation["violation_count"]) == 0:
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
        if best_floating_vector is not None and time.perf_counter() - started < max_wall_seconds:
            try:
                candidate = _candidate_from_vector(best_floating_vector, TARGET_STATES)
                repaired, repair = rationalize_and_repair_candidate(
                    candidate,
                    modulus=TARGET_MODULUS,
                    threshold=DEFAULT_H,
                    denominator=DEFAULT_DENOMINATOR,
                    chunk_rows=chunk_rows,
                    allow_large_state_scan=True,
                )
                _write_json_exclusive(output_directory / "candidate_repair_report.json", repair)
                if _certificate_objective_numerator(repaired) < _certificate_objective_numerator(best):
                    best = repaired
            except Exception as exc:
                _write_json_exclusive(
                    output_directory / "candidate_repair_report.json",
                    {"status": "FAIL", "error": f"{type(exc).__name__}: {exc}", "baseline_retained": True},
                )
                outcome = "CANDIDATE_REPAIR_FAILED"

    _write_json_exclusive(output_directory / "iteration_history.json", history)
    with (output_directory / "best_certificate_mod510510.txt").open("x", encoding="ascii", newline="\n") as handle:
        handle.write(certificate_text(best))
    if progress_callback:
        progress_callback({"stage": "final_exact", "status": "STARTED"})
    final_exact = scan_exact_certificate_constraints(
        best,
        chunk_rows=chunk_rows,
        top_k=100,
        allow_large_state_scan=True,
    )
    if final_exact.get("status") != "PASS" or int(final_exact["violation_count"]) != 0:
        raise Mod510510Error("P014 final certificate exact verification failed")
    if progress_callback:
        progress_callback(
            {
                "stage": "final_exact",
                "status": "PASS",
                "constraints": int(final_exact["scanned_constraints"]),
            }
        )
    _write_json_exclusive(output_directory / "exact_best_report.json", final_exact)
    strict = best.total_bound < BASELINE_TOTAL_BOUND
    scientific_outcome = (
        "STRICT_BOUND_IMPROVEMENT"
        if strict
        else ("NO_IMPROVEMENT" if optimizer_run else "CALIBRATION_ONLY_TIME_GATE")
    )
    summary = {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "source_modulus": SOURCE_MODULUS,
        "target_modulus": TARGET_MODULUS,
        "states": TARGET_STATES,
        "exact_constraint_count": TARGET_CONSTRAINTS,
        "stage_a_elapsed_seconds": stage_a_elapsed,
        "stage_a_gate_seconds": stage_a_gate_seconds,
        "stage_a_exact_verified": True,
        "optimizer_run": optimizer_run,
        "optimizer_outcome": outcome,
        "scientific_outcome": scientific_outcome,
        "solver_runs": solver_runs,
        "iterations_recorded": len(history),
        "working_constraints_final": len(working),
        "baseline_total_upper_bound": str(BASELINE_TOTAL_BOUND),
        "best_total_upper_bound": str(best.total_bound),
        "strict_bound_improvement": strict,
        "elapsed_seconds": time.perf_counter() - started,
        "max_wall_seconds": max_wall_seconds,
        "max_disk_bytes": max_disk_bytes,
        "full_constraint_matrix_materialized": False,
        "direct_prime_search_executed": False,
        "direct_search_acceleration_proved": False,
        "gpu_used": False,
        "runtime_resource_policy": runtime_resource_policy,
    }
    _write_json_exclusive(output_directory / "summary.json", summary)
    artifacts = sorted(path for path in output_directory.rglob("*") if path.is_file())
    manifest = {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "schema_version": SCHEMA_VERSION,
        "input_sha256": {
            "g4_manifest": G4_MANIFEST_SHA256,
            "g4_saved_report": G4_SAVED_REPORT_SHA256,
            "g4_certificate": G4_CERTIFICATE_SHA256,
        },
        "analysis_source_sha256": sha256_file(Path(__file__)),
        "artifacts_sha256": {
            path.relative_to(output_directory).as_posix(): sha256_file(path)
            for path in artifacts
        },
        "strict_bound_improvement": strict,
        "direct_search_acceleration_proved": False,
        "gpu_used": False,
        "runtime_resource_policy": runtime_resource_policy,
    }
    _write_json_exclusive(output_directory / "manifest.json", manifest)
    return summary


def verify_saved_experiment(
    output_directory: Path,
    *,
    chunk_rows: int = DEFAULT_CHUNK_ROWS,
    progress_callback: Callable[[dict[str, object]], None] | None = None,
) -> dict[str, object]:
    issues: list[str] = []
    try:
        manifest_path = output_directory / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        summary = json.loads((output_directory / "summary.json").read_text(encoding="utf-8"))
        artifacts = manifest.get("artifacts_sha256")
        if not isinstance(artifacts, dict):
            raise Mod510510Error("manifest artifact hashes missing")
        for relative, expected in artifacts.items():
            path = output_directory / str(relative)
            if not path.is_file() or sha256_file(path) != str(expected):
                issues.append(f"artifact missing/hash mismatch: {relative}")
        if manifest.get("analysis_source_sha256") != sha256_file(Path(__file__)):
            issues.append("current P014 source hash differs from manifest")
        if sha256_file(output_directory / "input_g4_manifest.json") != G4_MANIFEST_SHA256:
            issues.append("copied G4 manifest hash mismatch")
        if sha256_file(output_directory / "input_g4_saved_verification_report.json") != G4_SAVED_REPORT_SHA256:
            issues.append("copied G4 saved report hash mismatch")
        if sha256_file(output_directory / "input_g4_best_certificate_mod30030.txt") != G4_CERTIFICATE_SHA256:
            issues.append("copied G4 certificate hash mismatch")
        certificate = read_certificate(output_directory / "best_certificate_mod510510.txt")
        if progress_callback:
            progress_callback({"stage": "saved_exact", "status": "STARTED"})
        exact = scan_exact_certificate_constraints(
            certificate,
            chunk_rows=chunk_rows,
            top_k=100,
            allow_large_state_scan=True,
        )
        if (
            exact.get("status") != "PASS"
            or int(exact["violation_count"]) != 0
            or int(exact["scanned_constraints"]) != TARGET_CONSTRAINTS
        ):
            issues.append("saved P014 certificate exact recomputation failed")
        if progress_callback:
            progress_callback(
                {
                    "stage": "saved_exact",
                    "status": "PASS" if not issues else "FAIL",
                    "constraints": int(exact["scanned_constraints"]),
                }
            )
        if str(certificate.total_bound) != str(summary.get("best_total_upper_bound")):
            issues.append("saved P014 bound differs from summary")
        strict = certificate.total_bound < BASELINE_TOTAL_BOUND
        if bool(summary.get("strict_bound_improvement")) != strict:
            issues.append("summary strict-improvement flag mismatch")
        if summary.get("direct_search_acceleration_proved") is not False:
            issues.append("P014 must not claim search acceleration")
    except Exception as exc:
        issues.append(f"saved P014 verification failed: {type(exc).__name__}: {exc}")
    manifest_path = output_directory / "manifest.json"
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "exact_recomputed": not issues,
        "manifest_sha256": sha256_file(manifest_path) if manifest_path.is_file() else None,
        "direct_search_acceleration_proved": False,
    }


__all__ = [
    "BASELINE_TOTAL_BOUND",
    "EXPERIMENT",
    "Mod510510Error",
    "TARGET_CONSTRAINTS",
    "TARGET_MODULUS",
    "TARGET_STATES",
    "preflight",
    "require_g4_prerequisite",
    "run_staged_experiment",
    "verify_saved_experiment",
]
