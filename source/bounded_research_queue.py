"""Orchestration-only queue for bounded P010B/P010A/P009 user runs."""

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


@dataclass(frozen=True)
class QueueStep:
    name: str
    script: Path
    arguments: tuple[str, ...]
    timeout_seconds: int


def _tree_bytes(path: Path) -> int:
    total = 0
    if not path.exists():
        return 0
    def fail_on_walk_error(error: OSError) -> None:
        raise error

    for root, _, files in os.walk(path, onerror=fail_on_walk_error):
        root_path = Path(root)
        for name in files:
            try:
                total += (root_path / name).stat().st_size
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


def _extract_result_directory(lines: list[str]) -> Path | None:
    prefix = "[RUN] result_directory="
    for line in reversed(lines):
        stripped = line.strip()
        if stripped.startswith(prefix):
            return Path(stripped[len(prefix) :])
    return None


def _run_step(
    step: QueueStep,
    *,
    project_root: Path,
    baseline_bytes: int,
    max_disk_bytes: int,
    global_deadline: float,
) -> dict[str, object]:
    command = (
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(step.script),
        *step.arguments,
    )
    print(f"[QUEUE] step={step.name} status=START", flush=True)
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
    termination_reason: str | None = None
    while process.poll() is None:
        now = time.monotonic()
        if now >= global_deadline:
            termination_reason = "global_wall_budget_exceeded"
        elif now - started >= step.timeout_seconds:
            termination_reason = "step_timeout_exceeded"
        else:
            try:
                if _artifact_bytes(project_root) - baseline_bytes > max_disk_bytes:
                    termination_reason = "aggregate_disk_budget_exceeded"
            except OSError:
                termination_reason = "disk_accounting_failed"
        if termination_reason is not None:
            _terminate_process_tree(process)
            break
        time.sleep(5)
    try:
        exit_code = process.wait(timeout=30)
    except subprocess.TimeoutExpired:
        _terminate_process_tree(process)
        exit_code = -1
        termination_reason = termination_reason or "process_tree_did_not_exit"
    reader.join(timeout=30)
    elapsed = time.monotonic() - started
    result_directory = _extract_result_directory(lines)
    status = "PASS" if exit_code == 0 and termination_reason is None else "FAIL"
    print(
        f"[QUEUE] step={step.name} status={status} exit_code={exit_code} "
        f"elapsed_seconds={elapsed:.3f}",
        flush=True,
    )
    return {
        "name": step.name,
        "status": status,
        "exit_code": exit_code,
        "elapsed_seconds": elapsed,
        "timeout_seconds": step.timeout_seconds,
        "termination_reason": termination_reason,
        "result_directory": str(result_directory) if result_directory else None,
    }


def run_bounded_queue(
    project_root: Path,
    replay_manifest: Path,
    output_directory: Path,
    *,
    approval_token: str | None,
    max_wall_seconds: int = 55_800,
    max_disk_bytes: int = 50 * GB,
) -> dict[str, object]:
    require_experiment_approval(approval_token)
    project_root = project_root.resolve()
    replay_manifest = replay_manifest.resolve()
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite queue result: {output_directory}")
    if max_wall_seconds <= 0 or max_wall_seconds > 16 * 3600:
        raise ValueError("queue wall budget must be in (0, 16 hours]")
    if max_disk_bytes <= 0 or max_disk_bytes > 50 * GB:
        raise ValueError("queue disk budget must be in (0, 50 GB]")
    if not replay_manifest.is_file():
        raise FileNotFoundError(replay_manifest)

    from source.finite_gap_replay import require_mod2310_replay_completion

    require_mod2310_replay_completion(replay_manifest)
    baseline_bytes = _artifact_bytes(project_root)
    output_directory.mkdir(parents=True)
    started_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    global_started = time.monotonic()
    deadline = global_started + max_wall_seconds
    events_path = output_directory / "queue_events.jsonl"
    results: list[dict[str, object]] = []

    def record(payload: dict[str, object]) -> None:
        results.append(payload)
        with events_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")

    p010b = QueueStep(
        "P010B_MOD30030_ONE_CANDIDATE_SCAN",
        project_root / "scripts/experiments/p010b/run_p010b_mod30030_one_candidate_scan.ps1",
        ("-ConfirmP010B", "-P010AReplayManifest", str(replay_manifest)),
        3600,
    )
    p010b_result = _run_step(
        p010b,
        project_root=project_root,
        baseline_bytes=baseline_bytes,
        max_disk_bytes=max_disk_bytes,
        global_deadline=deadline,
    )
    scan_manifest: Path | None = None
    candidate_zero = False
    if p010b_result["status"] == "PASS":
        if not p010b_result["result_directory"]:
            p010b_result["status"] = "FAIL"
            p010b_result["postcheck_error"] = "terminal PASS lacked result_directory marker"
        else:
            try:
                scan_root = Path(str(p010b_result["result_directory"]))
                scan_manifest = scan_root / "manifest.json"
                summary = json.loads((scan_root / "summary.json").read_text(encoding="utf-8"))
                if not scan_manifest.is_file() or summary.get("status") != "PASS":
                    raise ValueError("P010B terminal output lacks PASS manifest/summary")
                candidate_zero = int(summary["violation_count"]) == 0
            except (OSError, ValueError, json.JSONDecodeError, KeyError) as exc:
                p010b_result["status"] = "FAIL"
                p010b_result["postcheck_error"] = str(exc)
                scan_manifest = None
    record(p010b_result)

    def budget_block_reason() -> str | None:
        if time.monotonic() >= deadline:
            return "global_wall_budget_exceeded"
        try:
            if _artifact_bytes(project_root) - baseline_bytes > max_disk_bytes:
                return "aggregate_disk_budget_exceeded"
        except OSError:
            return "disk_accounting_failed"
        return None

    exact_budget_block = budget_block_reason()
    if scan_manifest is not None and candidate_zero and exact_budget_block is None:
        exact_lift = QueueStep(
            "P010A_MOD30030_EXACT_LIFT",
            project_root / "scripts/experiments/p010a/run_p010a_mod30030_exact_lift.ps1",
            (
                "-ConfirmP010AExactLift",
                "-P010AReplayManifest",
                str(replay_manifest),
                "-P010BScanManifest",
                str(scan_manifest),
            ),
            14_400,
        )
        record(
            _run_step(
                exact_lift,
                project_root=project_root,
                baseline_bytes=baseline_bytes,
                max_disk_bytes=max_disk_bytes,
                global_deadline=deadline,
            )
        )
    else:
        reason = exact_budget_block or (
            "scientific_branch_not_applicable_nonzero_violations"
            if p010b_result["status"] == "PASS"
            else "blocked_by_p010b_failure"
        )
        record(
            {
                "name": "P010A_MOD30030_EXACT_LIFT",
                "status": (
                    "NOT_APPLICABLE"
                    if exact_budget_block is None
                    and candidate_zero is False
                    and p010b_result["status"] == "PASS"
                    else "BLOCKED"
                ),
                "reason": reason,
            }
        )

    p009 = QueueStep(
        "P009_SINGLE_BLOCK_BOUNDARY_ACTUAL",
        project_root / "scripts/experiments/p009/run_p009_single_block_actual.ps1",
        ("-ConfirmP009Actual", "-P010AReplayManifest", str(replay_manifest)),
        3600,
    )
    p009_budget_block = budget_block_reason()
    if p009_budget_block is None:
        record(
            _run_step(
                p009,
                project_root=project_root,
                baseline_bytes=baseline_bytes,
                max_disk_bytes=max_disk_bytes,
                global_deadline=deadline,
            )
        )
    else:
        record({"name": p009.name, "status": "BLOCKED", "reason": p009_budget_block})

    try:
        used_bytes: int | None = _artifact_bytes(project_root) - baseline_bytes
    except OSError as exc:
        used_bytes = None
        record(
            {
                "name": "QUEUE_RESOURCE_ACCOUNTING",
                "status": "FAIL",
                "reason": f"disk_accounting_failed: {exc}",
            }
        )
    failures = [row for row in results if row["status"] in {"FAIL", "BLOCKED"}]
    summary = {
        "status": "PASS" if not failures else "FAIL",
        "experiment": "P009_P010_BOUNDED_RESEARCH_QUEUE",
        "started_utc": started_utc,
        "elapsed_seconds": time.monotonic() - global_started,
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
    }
    (output_directory / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return summary


__all__ = ["GB", "QueueStep", "run_bounded_queue"]
