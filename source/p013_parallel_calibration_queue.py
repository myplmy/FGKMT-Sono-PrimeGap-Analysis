"""Orchestration-only 16-hour queue for the two approved P017 calibrations."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path

from source.provenance import require_experiment_approval


GB = 1_000_000_000
MAX_WALL_SECONDS = 57_600
MAX_DISK_BYTES = 5 * GB


@dataclass(frozen=True)
class CalibrationStep:
    name: str
    script: Path
    arguments: tuple[str, ...]
    timeout_seconds: int


def build_steps(project_root: Path) -> tuple[CalibrationStep, ...]:
    return (
        CalibrationStep(
            "P017A_P013A_PARALLEL_FULL_CALIBRATION",
            project_root
            / "scripts/experiments/p017/run_p017a_p013a_parallel_full_calibration.ps1",
            ("-ConfirmAfterP013B",),
            14_400,
        ),
        CalibrationStep(
            "P017B_P013B_PARALLEL_MIDRANGE_CALIBRATION",
            project_root
            / "scripts/experiments/p017/run_p017b_p013b_parallel_midrange_calibration.ps1",
            ("-ConfirmAfterP013B",),
            39_600,
        ),
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _tree_bytes(path: Path) -> int:
    total = 0
    if not path.exists():
        return 0
    for root, _, files in os.walk(path):
        base = Path(root)
        for name in files:
            try:
                total += (base / name).stat().st_size
            except FileNotFoundError:
                continue
    return total


def _artifact_bytes(project_root: Path) -> int:
    return _tree_bytes(project_root / "test_result") + _tree_bytes(
        project_root / "tmp"
    )


def _terminate_process_tree(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    subprocess.run(
        ("taskkill.exe", "/PID", str(process.pid), "/T", "/F"),
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _extract_marker(lines: list[str], marker: str) -> str | None:
    for line in reversed(lines):
        stripped = line.strip()
        if stripped.startswith(marker):
            return stripped[len(marker) :]
    return None


def _append_live(path: Path, message: str) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(message if message.endswith("\n") else message + "\n")
        handle.flush()


def _budget_reason(
    project_root: Path,
    *,
    baseline_bytes: int,
    max_disk_bytes: int,
    deadline: float,
) -> str | None:
    if time.monotonic() >= deadline:
        return "global_16h_wall_budget_exceeded"
    try:
        if _artifact_bytes(project_root) - baseline_bytes > max_disk_bytes:
            return "aggregate_5gb_disk_budget_exceeded"
    except OSError:
        return "disk_accounting_failed"
    return None


def _postcheck_child(result: dict[str, object]) -> None:
    if result.get("status") != "PASS":
        return
    raw = result.get("result_directory")
    if not raw:
        result["status"] = "FAIL"
        result["postcheck_error"] = "terminal success lacked result_directory marker"
        return
    try:
        root = Path(str(raw))
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        report = json.loads(
            (root / "saved_verification_report.json").read_text(encoding="utf-8")
        )
        if manifest.get("status") != "PASS" or report.get("status") != "PASS":
            raise ValueError("child manifest or saved report is not PASS")
        if report.get("manifest_sha256") != _sha256(root / "manifest.json"):
            raise ValueError("child saved report is not bound to manifest")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result["status"] = "FAIL"
        result["postcheck_error"] = str(exc)


def _run_step(
    step: CalibrationStep,
    *,
    project_root: Path,
    baseline_bytes: int,
    max_disk_bytes: int,
    deadline: float,
    live_log_path: Path,
) -> dict[str, object]:
    start_line = f"[QUEUE] step={step.name} status=START"
    print(start_line, flush=True)
    _append_live(live_log_path, start_line)
    command = (
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(step.script),
        *step.arguments,
    )
    started = time.monotonic()
    process = subprocess.Popen(
        command,
        cwd=project_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    lines: list[str] = []

    def collect() -> None:
        assert process.stdout is not None
        for line in process.stdout:
            lines.append(line)
            print(line, end="", flush=True)
            _append_live(live_log_path, line)

    reader = threading.Thread(target=collect, daemon=True)
    reader.start()
    reason: str | None = None
    while process.poll() is None:
        if time.monotonic() - started >= step.timeout_seconds:
            reason = "step_timeout_exceeded"
        else:
            reason = _budget_reason(
                project_root,
                baseline_bytes=baseline_bytes,
                max_disk_bytes=max_disk_bytes,
                deadline=deadline,
            )
        if reason is not None:
            _terminate_process_tree(process)
            break
        time.sleep(5)
    try:
        exit_code = process.wait(timeout=30)
    except subprocess.TimeoutExpired:
        _terminate_process_tree(process)
        exit_code = -1
        reason = reason or "process_tree_did_not_exit"
    reader.join(timeout=30)
    result: dict[str, object] = {
        "name": step.name,
        "status": "PASS" if exit_code == 0 and reason is None else "FAIL",
        "exit_code": exit_code,
        "elapsed_seconds": time.monotonic() - started,
        "timeout_seconds": step.timeout_seconds,
        "termination_reason": reason,
        "result_directory": _extract_marker(lines, "[RUN] result_directory="),
        "log": _extract_marker(lines, "[RUN] log="),
        "live_progress_file": _extract_marker(lines, "[RUN] live_progress_file="),
    }
    _postcheck_child(result)
    completion_line = (
        f"[QUEUE] step={step.name} status={result['status']} "
        f"exit_code={exit_code} elapsed_seconds={result['elapsed_seconds']:.3f}"
    )
    print(completion_line, flush=True)
    _append_live(live_log_path, completion_line)
    return result


def run_queue(
    project_root: Path,
    output_directory: Path,
    *,
    approval_token: str | None,
    max_wall_seconds: int = MAX_WALL_SECONDS,
    max_disk_bytes: int = MAX_DISK_BYTES,
) -> dict[str, object]:
    require_experiment_approval(approval_token)
    project_root = project_root.resolve()
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite P017 queue: {output_directory}")
    if not 1 <= max_wall_seconds <= MAX_WALL_SECONDS:
        raise ValueError("P017 queue wall cap must be in [1,16 hours]")
    if not 1 <= max_disk_bytes <= MAX_DISK_BYTES:
        raise ValueError("P017 queue disk cap exceeds decimal 5 GB")
    steps = build_steps(project_root)
    if sum(step.timeout_seconds for step in steps) > 15 * 3600:
        raise ValueError("P017 child timeout sum exceeds 15 hours")
    for step in steps:
        if not step.script.is_file():
            raise FileNotFoundError(step.script)
    baseline_bytes = _artifact_bytes(project_root)
    output_directory.mkdir(parents=True)
    events_path = output_directory / "queue_events.jsonl"
    live_log_path = output_directory / "live_console.log"
    live_log_path.write_text("", encoding="utf-8", newline="\n")
    started = time.monotonic()
    deadline = started + max_wall_seconds
    results: list[dict[str, object]] = []
    for step in steps:
        blocked = _budget_reason(
            project_root,
            baseline_bytes=baseline_bytes,
            max_disk_bytes=max_disk_bytes,
            deadline=deadline,
        )
        result = (
            {"name": step.name, "status": "BLOCKED", "reason": blocked}
            if blocked is not None
            else _run_step(
                step,
                project_root=project_root,
                baseline_bytes=baseline_bytes,
                max_disk_bytes=max_disk_bytes,
                deadline=deadline,
                live_log_path=live_log_path,
            )
        )
        if result["status"] == "BLOCKED":
            _append_live(
                live_log_path,
                "[QUEUE] step=" + step.name + " status=BLOCKED reason=" + str(result["reason"]),
            )
        results.append(result)
        with events_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(result, ensure_ascii=False, sort_keys=True) + "\n")
    try:
        used_bytes: int | None = _artifact_bytes(project_root) - baseline_bytes
    except OSError:
        used_bytes = None
    failures = [row for row in results if row["status"] != "PASS"]
    summary = {
        "status": "PASS" if not failures else "FAIL",
        "experiment": "P017_16H_P013_PARALLEL_CALIBRATION_QUEUE",
        "elapsed_seconds": time.monotonic() - started,
        "max_wall_seconds": max_wall_seconds,
        "child_timeout_sum_seconds": sum(step.timeout_seconds for step in steps),
        "max_disk_bytes": max_disk_bytes,
        "observed_artifact_delta_bytes": used_bytes,
        "steps": results,
        "failure_count": len(failures),
        "continue_after_child_failure": True,
        "queue_is_orchestration_only": True,
        "live_console_log": str(live_log_path),
        "cpu_only": True,
        "gpu_used": False,
    }
    summary_path = output_directory / "summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    manifest = {
        "status": summary["status"],
        "experiment": summary["experiment"],
        "artifacts_sha256": {
            "queue_events.jsonl": _sha256(events_path),
            "live_console.log": _sha256(live_log_path),
            "summary.json": _sha256(summary_path),
        },
        "queue_is_orchestration_only": True,
        "gpu_used": False,
    }
    (output_directory / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return summary


def verify_saved_queue(output_directory: Path) -> dict[str, object]:
    issues: list[str] = []
    try:
        manifest = json.loads(
            (output_directory / "manifest.json").read_text(encoding="utf-8")
        )
        summary = json.loads(
            (output_directory / "summary.json").read_text(encoding="utf-8")
        )
        for name, expected in dict(manifest.get("artifacts_sha256", {})).items():
            path = output_directory / name
            if not path.is_file() or _sha256(path) != expected:
                issues.append(f"queue artifact missing/hash mismatch: {name}")
        if manifest.get("status") != summary.get("status"):
            issues.append("queue manifest/summary status mismatch")
        if summary.get("max_wall_seconds") > MAX_WALL_SECONDS:
            issues.append("queue summary exceeds 16-hour cap")
        if summary.get("child_timeout_sum_seconds") > 15 * 3600:
            issues.append("queue child timeout sum exceeds 15 hours")
        if manifest.get("queue_is_orchestration_only") is not True:
            issues.append("queue incorrectly claims analytical work")
    except Exception as exc:
        issues.append(f"queue verification failed: {type(exc).__name__}: {exc}")
    return {"status": "PASS" if not issues else "FAIL", "issues": issues}


__all__ = [
    "GB",
    "MAX_DISK_BYTES",
    "MAX_WALL_SECONDS",
    "CalibrationStep",
    "build_steps",
    "run_queue",
    "verify_saved_queue",
]
