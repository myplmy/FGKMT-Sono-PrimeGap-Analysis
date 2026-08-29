"""Approval-gated exact calibration for the P013 process-parallel sieve.

P017 does not replace the serial P013 pipeline.  Stage A recomputes the full
P013-A sufficient statistics in parallel and compares them with the completed
serial oracle.  Stage B-mid computes a frozen first-half-decade range once by
the serial oracle and once by the parallel engine.  No scientific P013-B result
is claimed from the intermediate range.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Callable, Iterable, Sequence

import numpy as np

from source.parallel_segment_statistics import (
    exact_statistics_core,
    parallel_accumulate_bin_counts,
)
from source.plateau_recurrence import load_record_references
from source.provenance import require_experiment_approval, sha256_file
from source.recurrence_sequential_extension import (
    P013_CONTRACT_SHA256,
    STAGES,
    StageConfig,
    _derive_plateau_counts,
    _payload_sha256,
    _sufficient_statistics_payload,
    _validate_sufficient_statistics,
    compute_extension_analysis,
    select_complete_plateaus,
    validate_inputs,
)
from source.recurrence_stratified_holdout import iter_prime_chunks_range
from source.recurrence_stratified_null import (
    accumulate_bin_counts,
    analyze_components,
    build_components,
)


EXPERIMENT = "P017_P013_PARALLEL_ACTUAL_CALIBRATION"
MODES = ("A_FULL", "B_MID")
SCHEMA_VERSION = "P017-P013-PARALLEL-CALIBRATION-1"
EXPECTED_RECORDS_SHA256 = (
    "62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297"
)
EXPECTED_A_CHECKPOINT_SHA256 = (
    "cd6a85ef2cb766bc04a9ddc3bf98a2fc8f12c5f19efbcaaa740318622edf4502"
)
EXPECTED_A_ANALYSIS_SHA256 = (
    "70c8897af813ec072e1510bcc6e40e6535d3bce95b782801fe4f6bf9a9060b7b"
)
EXPECTED_P017_CONTRACT_SHA256 = (
    "27eebe4873bf24e0b63e6e667deede9314c22207f2fd3dfc11c727218ff7932f"
)


class ParallelCalibrationError(RuntimeError):
    """Raised when a frozen P017 input or exact-equivalence gate fails."""


def _write_json_exclusive(path: Path, payload: object) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def _load_json_object(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ParallelCalibrationError(f"JSON root is not an object: {path}")
    return payload


def _load_contract(path: Path) -> dict[str, object]:
    if sha256_file(path) != EXPECTED_P017_CONTRACT_SHA256:
        raise ParallelCalibrationError("P017 calibration contract hash changed")
    payload = _load_json_object(path)
    if (
        payload.get("contract_id") != "P017_P013_PARALLEL_CALIBRATION_V1"
        or payload.get("status") != "FROZEN_BEFORE_USER_RUN"
        or payload.get("validated_records_sha256") != EXPECTED_RECORDS_SHA256
        or payload.get("p013_contract_sha256") != P013_CONTRACT_SHA256
        or payload.get("theorem_claimed") is not False
    ):
        raise ParallelCalibrationError("P017 calibration contract changed")
    return payload


def _mode_payload(contract: dict[str, object], mode: str) -> dict[str, object]:
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES!r}")
    key = "p013a_full" if mode == "A_FULL" else "p013b_midrange"
    payload = contract.get(key)
    if not isinstance(payload, dict):
        raise ParallelCalibrationError(f"contract section is missing: {key}")
    return payload


def _parallel_payload(contract: dict[str, object]) -> dict[str, object]:
    payload = contract.get("parallel")
    if not isinstance(payload, dict):
        raise ParallelCalibrationError("contract parallel section is missing")
    expected = {
        "worker_count": 8,
        "p013a_segment_count": 32,
        "p013b_midrange_segment_count": 64,
        "sieve_segment_span": 50_000_000,
        "worker_native_thread_ceiling": 1,
        "physical_cores": 4,
        "logical_processors": 8,
    }
    if payload != expected:
        raise ParallelCalibrationError("P017 parallel resource contract changed")
    return payload


def _calibration_config(contract: dict[str, object], mode: str) -> StageConfig:
    frozen = _mode_payload(contract, mode)
    indices = tuple(int(value) for value in frozen["expected_complete_record_indices"])
    return StageConfig(
        mode,
        int(frozen["lower_inclusive"]),
        int(frozen["upper_exclusive"]),
        int(frozen.get("expected_gap_start_count", 0)),
        indices,
        int(frozen["seed"]),
    )


def validate_calibration_inputs(
    records_path: Path,
    p012_contract_path: Path,
    p013_contract_path: Path,
    p012b_manifest_path: Path,
    p012b_saved_report_path: Path,
    calibration_contract_path: Path,
    oracle_root: Path,
    *,
    mode: str,
) -> dict[str, object]:
    contract = _load_contract(calibration_contract_path)
    resources = _parallel_payload(contract)
    stage = "A" if mode == "A_FULL" else "B"
    prerequisite = validate_inputs(
        records_path,
        p012_contract_path,
        p013_contract_path,
        p012b_manifest_path,
        p012b_saved_report_path,
        stage=stage,
        segment_span=int(resources["sieve_segment_span"]),
    )
    if sha256_file(records_path) != EXPECTED_RECORDS_SHA256:
        raise ParallelCalibrationError("validated records hash changed")
    config = _calibration_config(contract, mode)
    selected = select_complete_plateaus(load_record_references(records_path), config)
    if mode == "A_FULL":
        checkpoint = oracle_root / "sufficient_statistics_checkpoint.json"
        analysis = oracle_root / "analysis.json"
        if sha256_file(checkpoint) != EXPECTED_A_CHECKPOINT_SHA256:
            raise ParallelCalibrationError("P013-A serial checkpoint hash changed")
        if sha256_file(analysis) != EXPECTED_A_ANALYSIS_SHA256:
            raise ParallelCalibrationError("P013-A serial analysis hash changed")
    return {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "mode": mode,
        "range": {
            "lower_inclusive": str(config.lower_inclusive),
            "upper_exclusive": str(config.upper_exclusive),
        },
        "selected_record_indices": [row["record_index"] for row in selected],
        "parallel": resources,
        "p013_prerequisite": prerequisite,
        "actual_prime_range_read": False,
        "actual_experiment_executed": False,
        "current_p013b_artifacts_read": False,
    }


def _statistics_payload(accumulated: dict[str, object]) -> dict[str, object]:
    payload: dict[str, object] = {
        "prime_count": int(accumulated["prime_count"]),
        "gap_count": int(accumulated["gap_count"]),
    }
    for field in (
        "populations",
        "gap_counts",
        "exposure_counts",
        "exposure_equal_counts",
    ):
        schemes = accumulated[field]
        if not isinstance(schemes, dict):
            raise ParallelCalibrationError(f"invalid statistics field: {field}")
        encoded_schemes: dict[str, list[list[object]]] = {}
        for scheme, counts in sorted(schemes.items()):
            if not isinstance(counts, dict):
                raise ParallelCalibrationError(f"invalid count map: {field}/{scheme}")
            entries: list[list[object]] = []
            for key, value in sorted(
                counts.items(),
                key=lambda item: item[0]
                if isinstance(item[0], tuple)
                else (item[0],),
            ):
                parts = list(key) if isinstance(key, tuple) else [key]
                entries.append([*[int(part) for part in parts], int(value)])
            encoded_schemes[str(scheme)] = entries
        payload[field] = encoded_schemes
    return payload


def _statistics_sha256(accumulated: dict[str, object]) -> str:
    encoded = json.dumps(
        _statistics_payload(accumulated),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _serial_accumulate(
    config: StageConfig,
    plateaus: Sequence[dict[str, int]],
    *,
    segment_span: int,
    progress_callback: Callable[[dict[str, object]], None] | None,
) -> dict[str, object]:
    chunks = iter_prime_chunks_range(
        config.lower_inclusive,
        config.upper_exclusive,
        segment_span=segment_span,
    )

    def monitored() -> Iterable[Sequence[int] | np.ndarray]:
        emitted = 0
        for index, raw in enumerate(chunks, start=1):
            values = np.asarray(raw, dtype=np.int64)
            emitted += int(values.size)
            if progress_callback is not None and (index == 1 or index % 100 == 0):
                progress_callback(
                    {
                        "event": "serial_sieve_progress",
                        "mode": config.name,
                        "sieve_chunks_completed": index,
                        "primes_emitted_including_possible_boundary": emitted,
                        "last_prime": str(int(values[-1])),
                    }
                )
            yield values

    return accumulate_bin_counts(monitored(), plateaus)


def _derive_compact(
    config: StageConfig,
    provisional: Sequence[dict[str, int]],
    accumulated: dict[str, object],
    *,
    seed: int,
    replications: int,
) -> tuple[dict[str, object], dict[str, object]]:
    plateaus = _derive_plateau_counts(provisional, accumulated)
    components = build_components(plateaus, accumulated)
    inference = analyze_components(
        plateaus,
        components,
        {},
        replications=replications,
        seed=seed,
    )
    checkpoint = {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "mode": config.name,
        "range": {
            "lower_inclusive": str(config.lower_inclusive),
            "upper_exclusive": str(config.upper_exclusive),
        },
        "prime_count_including_boundary": int(accumulated["prime_count"]),
        "gap_count": int(accumulated["gap_count"]),
        "statistics_sha256": _statistics_sha256(accumulated),
        "selected_record_indices": [row["record_index"] for row in plateaus],
        "plateaus": plateaus,
        "components": components,
    }
    return checkpoint, inference


def _run_a_full(
    paths: dict[str, Path],
    output_directory: Path,
    contract: dict[str, object],
    *,
    progress_callback: Callable[[dict[str, object]], None],
) -> dict[str, object]:
    config = STAGES["A"]
    resources = _parallel_payload(contract)
    provisional = select_complete_plateaus(
        load_record_references(paths["records"]), config
    )
    accumulated = parallel_accumulate_bin_counts(
        config.lower_inclusive,
        config.upper_exclusive,
        provisional,
        worker_count=int(resources["worker_count"]),
        segment_count=int(resources["p013a_segment_count"]),
        sieve_segment_span=int(resources["sieve_segment_span"]),
        progress_callback=progress_callback,
    )
    if int(accumulated["gap_count"]) != config.expected_gap_start_count:
        raise ParallelCalibrationError("P013-A parallel gap-start count changed")
    plateaus = _derive_plateau_counts(provisional, accumulated)
    components = build_components(plateaus, accumulated)
    checkpoint = _sufficient_statistics_payload(
        config,
        prime_count=int(accumulated["prime_count"]),
        gap_count=int(accumulated["gap_count"]),
        plateaus=plateaus,
        components=components,
    )
    _validate_sufficient_statistics(checkpoint, config, provisional)
    oracle_checkpoint_path = paths["oracle_root"] / "sufficient_statistics_checkpoint.json"
    oracle_checkpoint = _load_json_object(oracle_checkpoint_path)
    checkpoint_equal = checkpoint == oracle_checkpoint
    if not checkpoint_equal:
        raise ParallelCalibrationError("P013-A parallel checkpoint differs from serial oracle")
    checkpoint_path = output_directory / "parallel_sufficient_statistics_checkpoint.json"
    _write_json_exclusive(checkpoint_path, checkpoint)
    analysis = compute_extension_analysis(
        paths["records"],
        paths["p012_contract"],
        paths["p013_contract"],
        paths["p012b_manifest"],
        paths["p012b_saved_report"],
        stage="A",
        segment_span=int(resources["sieve_segment_span"]),
        checkpoint_path=checkpoint_path,
    )
    oracle_analysis = _load_json_object(paths["oracle_root"] / "analysis.json")
    analysis_equal = analysis == oracle_analysis
    if not analysis_equal:
        raise ParallelCalibrationError("P013-A analysis differs from serial oracle")
    _write_json_exclusive(output_directory / "parallel_analysis.json", analysis)
    parallel_metadata = accumulated["parallel_execution"]
    if not isinstance(parallel_metadata, dict):
        raise ParallelCalibrationError("parallel execution metadata is missing")
    return {
        "status": "PASS",
        "mode": "A_FULL",
        "range": analysis["gap_start_range"],
        "gap_start_count": config.expected_gap_start_count,
        "selected_record_indices": list(config.expected_record_indices),
        "serial_checkpoint_file_sha256": sha256_file(oracle_checkpoint_path),
        "parallel_checkpoint_canonical_sha256": _payload_sha256(checkpoint),
        "serial_checkpoint_canonical_sha256": _payload_sha256(oracle_checkpoint),
        "checkpoint_payload_exact_equal": checkpoint_equal,
        "serial_analysis_file_sha256": sha256_file(
            paths["oracle_root"] / "analysis.json"
        ),
        "analysis_exact_equal": analysis_equal,
        "parallel_execution": parallel_metadata,
        "scientific_result_changed": False,
    }


def _run_b_mid(
    paths: dict[str, Path],
    output_directory: Path,
    contract: dict[str, object],
    *,
    progress_callback: Callable[[dict[str, object]], None],
) -> dict[str, object]:
    frozen = _mode_payload(contract, "B_MID")
    config = _calibration_config(contract, "B_MID")
    resources = _parallel_payload(contract)
    provisional = select_complete_plateaus(
        load_record_references(paths["records"]), config
    )
    progress_callback({"event": "serial_oracle_started", "mode": "B_MID"})
    serial = _serial_accumulate(
        config,
        provisional,
        segment_span=int(resources["sieve_segment_span"]),
        progress_callback=progress_callback,
    )
    progress_callback(
        {
            "event": "serial_oracle_completed",
            "mode": "B_MID",
            "gap_count": int(serial["gap_count"]),
        }
    )
    parallel = parallel_accumulate_bin_counts(
        config.lower_inclusive,
        config.upper_exclusive,
        provisional,
        worker_count=int(resources["worker_count"]),
        segment_count=int(resources["p013b_midrange_segment_count"]),
        sieve_segment_span=int(resources["sieve_segment_span"]),
        progress_callback=progress_callback,
    )
    exact_core_equal = exact_statistics_core(serial) == exact_statistics_core(parallel)
    if not exact_core_equal:
        raise ParallelCalibrationError("P013-B midrange exact statistics differ")
    if int(serial["prime_count"]) != int(serial["gap_count"]) + 1:
        raise ParallelCalibrationError("P013-B serial boundary-prime invariant failed")
    serial_checkpoint, serial_inference = _derive_compact(
        config,
        provisional,
        serial,
        seed=int(frozen["seed"]),
        replications=int(frozen["replications"]),
    )
    parallel_checkpoint, parallel_inference = _derive_compact(
        config,
        provisional,
        parallel,
        seed=int(frozen["seed"]),
        replications=int(frozen["replications"]),
    )
    checkpoint_equal = serial_checkpoint == parallel_checkpoint
    inference_equal = serial_inference == parallel_inference
    if not checkpoint_equal or not inference_equal:
        raise ParallelCalibrationError("P013-B midrange derived results differ")
    _write_json_exclusive(output_directory / "serial_compact_checkpoint.json", serial_checkpoint)
    _write_json_exclusive(output_directory / "parallel_compact_checkpoint.json", parallel_checkpoint)
    _write_json_exclusive(output_directory / "serial_inference.json", serial_inference)
    _write_json_exclusive(output_directory / "parallel_inference.json", parallel_inference)
    parallel_metadata = parallel["parallel_execution"]
    if not isinstance(parallel_metadata, dict):
        raise ParallelCalibrationError("parallel execution metadata is missing")
    return {
        "status": "PASS",
        "mode": "B_MID",
        "range": serial_checkpoint["range"],
        "gap_start_count": int(serial["gap_count"]),
        "selected_record_indices": serial_checkpoint["selected_record_indices"],
        "serial_statistics_sha256": serial_checkpoint["statistics_sha256"],
        "parallel_statistics_sha256": parallel_checkpoint["statistics_sha256"],
        "exact_statistics_core_equal": exact_core_equal,
        "checkpoint_exact_equal": checkpoint_equal,
        "fixed_seed_inference_exact_equal": inference_equal,
        "parallel_execution": parallel_metadata,
        "scientific_p013b_result_claimed": False,
    }


def run_calibration(
    records_path: Path,
    p012_contract_path: Path,
    p013_contract_path: Path,
    p012b_manifest_path: Path,
    p012b_saved_report_path: Path,
    calibration_contract_path: Path,
    oracle_root: Path,
    output_directory: Path,
    *,
    mode: str,
    approval_token: str | None,
    runtime_resource_policy: dict[str, object] | None = None,
) -> dict[str, object]:
    require_experiment_approval(approval_token)
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite P017 result: {output_directory}")
    preflight = validate_calibration_inputs(
        records_path,
        p012_contract_path,
        p013_contract_path,
        p012b_manifest_path,
        p012b_saved_report_path,
        calibration_contract_path,
        oracle_root,
        mode=mode,
    )
    output_directory.mkdir(parents=True)
    progress_path = output_directory / "progress.jsonl"
    progress_path.touch(exist_ok=False)
    started = time.perf_counter()

    def progress(payload: dict[str, object]) -> None:
        enriched = {"elapsed_seconds": time.perf_counter() - started, **payload}
        line = json.dumps(enriched, ensure_ascii=False, sort_keys=True)
        with progress_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(line + "\n")
            handle.flush()
        print("[P017] " + line, flush=True)

    contract = _load_contract(calibration_contract_path)
    paths = {
        "records": records_path,
        "p012_contract": p012_contract_path,
        "p013_contract": p013_contract_path,
        "p012b_manifest": p012b_manifest_path,
        "p012b_saved_report": p012b_saved_report_path,
        "calibration_contract": calibration_contract_path,
        "oracle_root": oracle_root,
    }
    progress({"event": "calibration_started", "mode": mode})
    comparison = (
        _run_a_full(paths, output_directory, contract, progress_callback=progress)
        if mode == "A_FULL"
        else _run_b_mid(paths, output_directory, contract, progress_callback=progress)
    )
    progress({"event": "calibration_exact_comparison_passed", "mode": mode})
    _write_json_exclusive(output_directory / "comparison.json", comparison)
    summary = {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "schema_version": SCHEMA_VERSION,
        "mode": mode,
        "range": comparison["range"],
        "gap_start_count": comparison["gap_start_count"],
        "selected_record_indices": comparison["selected_record_indices"],
        "exact_equivalence": "PASS",
        "elapsed_seconds": time.perf_counter() - started,
        "runtime_resource_policy": runtime_resource_policy,
        "current_p013b_artifacts_read": False,
        "current_p013b_process_modified": False,
        "precision_reduced": False,
        "work_items_omitted": False,
        "theorem_claimed": False,
        "gpu_used": False,
    }
    _write_json_exclusive(output_directory / "summary.json", summary)
    artifacts = sorted(path for path in output_directory.iterdir() if path.is_file())
    manifest = {
        "status": "PASS",
        "experiment": EXPERIMENT,
        "schema_version": SCHEMA_VERSION,
        "mode": mode,
        "input_sha256": {
            "validated_records": sha256_file(records_path),
            "p012_contract": sha256_file(p012_contract_path),
            "p013_contract": sha256_file(p013_contract_path),
            "p012b_manifest": sha256_file(p012b_manifest_path),
            "p012b_saved_report": sha256_file(p012b_saved_report_path),
            "p017_contract": sha256_file(calibration_contract_path),
        },
        "source_sha256": {
            "calibration": sha256_file(Path(__file__)),
            "parallel_segment_statistics": sha256_file(
                Path(__file__).with_name("parallel_segment_statistics.py")
            ),
            "serial_oracle": sha256_file(
                Path(__file__).with_name("recurrence_sequential_extension.py")
            ),
        },
        "artifacts_sha256": {
            path.name: sha256_file(path) for path in artifacts
        },
        "preflight": preflight,
        "precision_reduced": False,
        "work_items_omitted": False,
        "theorem_claimed": False,
        "gpu_used": False,
    }
    _write_json_exclusive(output_directory / "manifest.json", manifest)
    return summary


def verify_saved_calibration(output_directory: Path) -> dict[str, object]:
    issues: list[str] = []
    manifest_path = output_directory / "manifest.json"
    try:
        manifest = _load_json_object(manifest_path)
        summary = _load_json_object(output_directory / "summary.json")
        comparison = _load_json_object(output_directory / "comparison.json")
        artifacts = manifest.get("artifacts_sha256")
        if not isinstance(artifacts, dict):
            raise ParallelCalibrationError("manifest artifact hash table is missing")
        for name, expected in artifacts.items():
            path = output_directory / str(name)
            if not path.is_file() or sha256_file(path) != str(expected):
                issues.append(f"artifact missing/hash mismatch: {name}")
        if summary.get("status") != "PASS" or comparison.get("status") != "PASS":
            issues.append("summary or comparison is not PASS")
        if summary.get("exact_equivalence") != "PASS":
            issues.append("summary exact-equivalence gate is not PASS")
        if manifest.get("precision_reduced") is not False:
            issues.append("manifest does not preserve full precision")
        if manifest.get("work_items_omitted") is not False:
            issues.append("manifest reports omitted work")
        sources = manifest.get("source_sha256")
        if not isinstance(sources, dict):
            raise ParallelCalibrationError("manifest source hash table is missing")
        current = {
            "calibration": sha256_file(Path(__file__)),
            "parallel_segment_statistics": sha256_file(
                Path(__file__).with_name("parallel_segment_statistics.py")
            ),
            "serial_oracle": sha256_file(
                Path(__file__).with_name("recurrence_sequential_extension.py")
            ),
        }
        if sources != current:
            issues.append("current source hashes differ from calibration manifest")
    except Exception as exc:
        issues.append(f"saved P017 verification failed: {type(exc).__name__}: {exc}")
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "saved_artifact_verification": "PASS" if not issues else "FAIL",
        "manifest_sha256": sha256_file(manifest_path) if manifest_path.is_file() else None,
        "heavy_recomputation_performed": False,
        "theorem_claimed": False,
    }


__all__ = [
    "EXPERIMENT",
    "MODES",
    "ParallelCalibrationError",
    "run_calibration",
    "validate_calibration_inputs",
    "verify_saved_calibration",
]
