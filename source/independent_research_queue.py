"""Orchestration-only 47-hour queue for independent P013/P014 user runs."""

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
MAX_WALL_SECONDS = 169_200
MAX_DISK_BYTES = 50 * GB


@dataclass(frozen=True)
class QueueStep:
    name: str
    script: Path
    arguments: tuple[str, ...]
    timeout_seconds: int


def build_steps(project_root: Path) -> tuple[QueueStep, ...]:
    return (
        QueueStep(
            "P013A_RECURRENCE_EXTENSION_1E11_R2",
            project_root / "scripts/experiments/p013/run_p013a_recurrence_extension_1e11_r2.ps1",
            ("-ConfirmP013A",),
            14_400,
        ),
        QueueStep(
            "P013B_RECURRENCE_EXTENSION_1E12",
            project_root / "scripts/experiments/p013/run_p013b_recurrence_extension_1e12.ps1",
            ("-ConfirmP013B",),
            72_000,
        ),
        QueueStep(
            "P014_MOD510510_STAGED_CERTIFICATE",
            project_root / "scripts/experiments/p014/run_p014_mod510510_staged_certificate.ps1",
            ("-ConfirmP014",),
            79_200,
        ),
    )


def _tree_bytes(path: Path) -> int:
    total = 0
    if not path.exists():
        return 0

    def fail(error: OSError) -> None:
        raise error

    for root, _, files in os.walk(path, onerror=fail):
        base = Path(root)
        for name in files:
            try:
                total += (base / name).stat().st_size
            except FileNotFoundError:
                continue
    return total


def _artifact_bytes(project_root: Path) -> int:
    return _tree_bytes(project_root / "test_result") + _tree_bytes(project_root / "tmp")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _terminate_process_tree(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    subprocess.run(
        ["taskkill.exe", "/PID", str(process.pid), "/T", "/F"],
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


def _budget_reason(
    project_root: Path,
    *,
    baseline_bytes: int,
    max_disk_bytes: int,
    deadline: float,
) -> str | None:
    if time.monotonic() >= deadline:
        return "global_wall_budget_exceeded"
    try:
        if _artifact_bytes(project_root) - baseline_bytes > max_disk_bytes:
            return "aggregate_disk_budget_exceeded"
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
        report = json.loads((root / "saved_verification_report.json").read_text(encoding="utf-8"))
        if manifest.get("status") != "PASS" or report.get("status") != "PASS":
            raise ValueError("child manifest or saved report is not PASS")
        if report.get("manifest_sha256") != _sha256(root / "manifest.json"):
            raise ValueError("child saved report is not bound to manifest")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result["status"] = "FAIL"
        result["postcheck_error"] = str(exc)


def _run_step(
    step: QueueStep,
    *,
    project_root: Path,
    baseline_bytes: int,
    max_disk_bytes: int,
    deadline: float,
) -> dict[str, object]:
    print(f"[QUEUE] step={step.name} status=START", flush=True)
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
    elapsed = time.monotonic() - started
    status = "PASS" if exit_code == 0 and reason is None else "FAIL"
    result: dict[str, object] = {
        "name": step.name,
        "status": status,
        "exit_code": exit_code,
        "elapsed_seconds": elapsed,
        "timeout_seconds": step.timeout_seconds,
        "termination_reason": reason,
        "result_directory": _extract_marker(lines, "[RUN] result_directory="),
        "log": _extract_marker(lines, "[RUN] log="),
    }
    _postcheck_child(result)
    print(
        f"[QUEUE] step={step.name} status={result['status']} "
        f"exit_code={exit_code} elapsed_seconds={elapsed:.3f}",
        flush=True,
    )
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
        raise FileExistsError(f"refusing to overwrite P015 queue: {output_directory}")
    if not 1 <= max_wall_seconds <= MAX_WALL_SECONDS:
        raise ValueError("queue wall cap must be in [1,47 hours]")
    if not 1 <= max_disk_bytes <= MAX_DISK_BYTES:
        raise ValueError("queue disk cap exceeds decimal 50 GB")
    steps = build_steps(project_root)
    for step in steps:
        if not step.script.is_file():
            raise FileNotFoundError(step.script)
    baseline_bytes = _artifact_bytes(project_root)
    output_directory.mkdir(parents=True)
    events_path = output_directory / "queue_events.jsonl"
    started_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    started = time.monotonic()
    deadline = started + max_wall_seconds
    results: list[dict[str, object]] = []

    def record(payload: dict[str, object]) -> None:
        results.append(payload)
        with events_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")

    stage_a = _run_step(
        steps[0],
        project_root=project_root,
        baseline_bytes=baseline_bytes,
        max_disk_bytes=max_disk_bytes,
        deadline=deadline,
    )
    record(stage_a)
    if stage_a["status"] == "PASS":
        blocked = _budget_reason(
            project_root,
            baseline_bytes=baseline_bytes,
            max_disk_bytes=max_disk_bytes,
            deadline=deadline,
        )
        if blocked is None:
            record(
                _run_step(
                    steps[1],
                    project_root=project_root,
                    baseline_bytes=baseline_bytes,
                    max_disk_bytes=max_disk_bytes,
                    deadline=deadline,
                )
            )
        else:
            record({"name": steps[1].name, "status": "BLOCKED", "reason": blocked})
    else:
        record(
            {
                "name": steps[1].name,
                "status": "BLOCKED",
                "reason": "shared_P013_implementation_failed_in_stage_A",
            }
        )

    p014_block = _budget_reason(
        project_root,
        baseline_bytes=baseline_bytes,
        max_disk_bytes=max_disk_bytes,
        deadline=deadline,
    )
    if p014_block is None:
        record(
            _run_step(
                steps[2],
                project_root=project_root,
                baseline_bytes=baseline_bytes,
                max_disk_bytes=max_disk_bytes,
                deadline=deadline,
            )
        )
    else:
        record({"name": steps[2].name, "status": "BLOCKED", "reason": p014_block})

    try:
        used_bytes: int | None = _artifact_bytes(project_root) - baseline_bytes
    except OSError as exc:
        used_bytes = None
        record({"name": "QUEUE_RESOURCE_ACCOUNTING", "status": "FAIL", "reason": str(exc)})
    failures = [row for row in results if row["status"] in {"FAIL", "BLOCKED"}]
    summary = {
        "status": "PASS" if not failures else "FAIL",
        "experiment": "P015_48H_INDEPENDENT_RESEARCH_QUEUE",
        "started_utc": started_utc,
        "elapsed_seconds": time.monotonic() - started,
        "max_wall_seconds": max_wall_seconds,
        "max_disk_bytes": max_disk_bytes,
        "observed_artifact_delta_bytes": used_bytes,
        "cpu_only": True,
        "gpu_used": False,
        "queue_is_orchestration_only": True,
        "steps": results,
        "failure_count": len(failures),
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
        manifest = json.loads((output_directory / "manifest.json").read_text(encoding="utf-8"))
        summary = json.loads((output_directory / "summary.json").read_text(encoding="utf-8"))
        for name, expected in dict(manifest.get("artifacts_sha256", {})).items():
            path = output_directory / name
            if not path.is_file() or _sha256(path) != expected:
                issues.append(f"queue artifact missing/hash mismatch: {name}")
        if manifest.get("status") != summary.get("status"):
            issues.append("queue manifest/summary status mismatch")
        if manifest.get("queue_is_orchestration_only") is not True:
            issues.append("queue incorrectly claims analytical work")
    except Exception as exc:
        issues.append(f"queue verification failed: {type(exc).__name__}: {exc}")
    return {"status": "PASS" if not issues else "FAIL", "issues": issues}


__all__ = [
    "GB",
    "MAX_DISK_BYTES",
    "MAX_WALL_SECONDS",
    "QueueStep",
    "build_steps",
    "run_queue",
    "verify_saved_queue",
]
