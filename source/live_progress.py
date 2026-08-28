"""Durable Python-side progress events for long approval-gated experiments."""

from __future__ import annotations

import json
import os
import threading
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Mapping


class LiveProgressError(RuntimeError):
    """Raised when a live progress channel cannot be opened safely."""


class LiveProgressReporter:
    """Write fsync-backed JSONL events and optional Windows console updates."""

    def __init__(
        self,
        path: Path,
        *,
        experiment: str,
        stage: str,
        heartbeat_seconds: float = 300.0,
        live_console: bool = False,
    ) -> None:
        if not experiment or not stage:
            raise ValueError("experiment and stage must be nonempty")
        if not 0.01 <= heartbeat_seconds <= 86_400:
            raise ValueError("heartbeat_seconds must be in [0.01,86400]")
        self.path = path
        self.experiment = experiment
        self.stage = stage
        self.heartbeat_seconds = float(heartbeat_seconds)
        self.live_console = bool(live_console)
        self._lock = threading.RLock()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._handle = None
        self._console = None
        self._started = 0.0
        self._last_progress: dict[str, object] | None = None

    @staticmethod
    def _utc_now() -> str:
        return datetime.now(UTC).isoformat().replace("+00:00", "Z")

    def _write_locked(self, payload: dict[str, object]) -> None:
        if self._handle is None:
            raise LiveProgressError("progress reporter is not open")
        line = json.dumps(payload, ensure_ascii=True, sort_keys=True) + "\n"
        self._handle.write(line)
        self._handle.flush()
        os.fsync(self._handle.fileno())
        if self._console is not None:
            self._console.write("[LIVE] " + line)
            self._console.flush()

    def _base_event(self, event: str) -> dict[str, object]:
        return {
            "elapsed_seconds": round(time.monotonic() - self._started, 3),
            "event": event,
            "experiment": self.experiment,
            "pid": os.getpid(),
            "stage": self.stage,
            "utc": self._utc_now(),
        }

    def __enter__(self) -> "LiveProgressReporter":
        if self.path.exists():
            raise FileExistsError(f"refusing to overwrite progress log: {self.path}")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._handle = self.path.open("x", encoding="utf-8", buffering=1, newline="\n")
        if self.live_console and os.name == "nt":
            try:
                self._console = open(  # noqa: PTH123 - Windows console device
                    "CONOUT$", "w", encoding="utf-8", buffering=1, newline="\n"
                )
            except OSError:
                self._console = None
        self._started = time.monotonic()
        with self._lock:
            self._write_locked(self._base_event("START"))
        self._thread = threading.Thread(
            target=self._heartbeat_loop,
            name=f"live-progress-{self.stage}",
            daemon=True,
        )
        self._thread.start()
        return self

    def emit(self, payload: Mapping[str, object]) -> None:
        snapshot = dict(payload)
        with self._lock:
            self._last_progress = snapshot
            event = self._base_event("PROGRESS")
            event["progress"] = snapshot
            self._write_locked(event)

    def _heartbeat_loop(self) -> None:
        while not self._stop.wait(self.heartbeat_seconds):
            with self._lock:
                event = self._base_event("HEARTBEAT")
                event["last_progress"] = self._last_progress
                self._write_locked(event)

    def close(
        self,
        *,
        status: str,
        error: str | None = None,
    ) -> None:
        if self._handle is None:
            return
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=5.0)
        with self._lock:
            event = self._base_event("END")
            event["status"] = status
            if error is not None:
                event["error"] = error
            self._write_locked(event)
            if self._console is not None:
                self._console.close()
                self._console = None
            self._handle.close()
            self._handle = None

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        if exc_type is None:
            self.close(status="PASS")
        else:
            self.close(
                status="FAIL",
                error=f"{exc_type.__name__}: {exc_value}",
            )
        return False


__all__ = ["LiveProgressError", "LiveProgressReporter"]
