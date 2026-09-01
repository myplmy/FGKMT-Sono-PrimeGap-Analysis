"""Run one native stage with immediate console display and durable log append.

This helper intentionally uses Python ``subprocess`` instead of PowerShell
``Start-Process``/``System.Diagnostics.Process``.  It keeps stdout and stderr
drained concurrently, mirrors both to the current console immediately, and
records stream changes in the shared runner log.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import json
import queue
import subprocess
import sys
import threading
from pathlib import Path
from typing import BinaryIO, Sequence


class LiveNativeTeeError(RuntimeError):
    """Raised when the broker input is invalid or the child cannot start."""


def _reader(
    pipe: BinaryIO,
    stream_name: str,
    events: "queue.Queue[tuple[str, bytes | None]]",
) -> None:
    try:
        while True:
            data = pipe.readline()
            if not data:
                break
            events.put((stream_name, data))
    finally:
        pipe.close()
        events.put((stream_name, None))


def _write_console(console: BinaryIO, data: bytes) -> None:
    console.write(data)
    console.flush()


def run_live_native_tee(
    command: Sequence[str],
    *,
    log_path: Path,
    stage_name: str,
    console: BinaryIO | None = None,
) -> int:
    """Run *command*, tee both streams live, and return the exact child code."""

    if not command or any(not isinstance(part, str) or not part for part in command):
        raise LiveNativeTeeError("command must contain nonempty string arguments")
    if not stage_name:
        raise LiveNativeTeeError("stage_name must be nonempty")
    if not log_path.is_file():
        raise LiveNativeTeeError(f"initialized runner log does not exist: {log_path}")
    if console is None:
        console = sys.stdout.buffer

    events: "queue.Queue[tuple[str, bytes | None]]" = queue.Queue()
    with log_path.open("a", encoding="utf-8", newline="") as log_handle:
        log_handle.write("[CAPTURE] live_native_tee begin\n")
        log_handle.flush()
        try:
            process = subprocess.Popen(
                list(command),
                stdin=None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=0,
            )
        except OSError as exc:
            message = f"[CAPTURE] launch_error={type(exc).__name__}: {exc}\n"
            log_handle.write(message)
            log_handle.write("[CAPTURE] live_native_tee end child_exit_code=127\n")
            log_handle.flush()
            _write_console(console, message.encode("utf-8", errors="replace"))
            return 127

        assert process.stdout is not None
        assert process.stderr is not None
        threads = [
            threading.Thread(
                target=_reader,
                args=(process.stdout, "stdout", events),
                name=f"live-tee-{stage_name}-stdout",
                daemon=True,
            ),
            threading.Thread(
                target=_reader,
                args=(process.stderr, "stderr", events),
                name=f"live-tee-{stage_name}-stderr",
                daemon=True,
            ),
        ]
        for thread in threads:
            thread.start()

        completed_streams = 0
        current_stream: str | None = None
        log_at_line_start = True
        try:
            while completed_streams < len(threads):
                stream_name, data = events.get()
                if data is None:
                    completed_streams += 1
                    continue
                if stream_name != current_stream:
                    if not log_at_line_start:
                        log_handle.write("\n")
                    log_handle.write(f"[CAPTURE] stream={stream_name} live\n")
                    current_stream = stream_name
                    log_at_line_start = True
                text = data.decode("utf-8", errors="replace")
                log_handle.write(text)
                log_at_line_start = text.endswith(("\n", "\r"))
                log_handle.flush()
                _write_console(console, data)
        except KeyboardInterrupt:
            process.terminate()
            process.wait(timeout=30)
            raise
        finally:
            for thread in threads:
                thread.join(timeout=5)

        exit_code = int(process.wait())
        if not log_at_line_start:
            log_handle.write("\n")
        log_handle.write(
            f"[CAPTURE] live_native_tee end child_exit_code={exit_code}\n"
        )
        log_handle.flush()
        return exit_code


class _BrokerArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise LiveNativeTeeError(f"broker argument error: {message}")


def _parser() -> argparse.ArgumentParser:
    parser = _BrokerArgumentParser(description=__doc__)
    parser.add_argument("--log-path", type=Path, required=True)
    parser.add_argument("--stage-name", required=True)
    parser.add_argument("--executable", required=True)
    transport = parser.add_mutually_exclusive_group(required=True)
    transport.add_argument("--arguments-json")
    transport.add_argument("--arguments-base64")
    return parser


def _decode_arguments(args: argparse.Namespace) -> list[str]:
    if args.arguments_base64 is not None:
        encoded = args.arguments_base64.encode("ascii", errors="strict")
        payload = base64.b64decode(encoded, validate=True).decode("utf-8")
    else:
        payload = args.arguments_json
    arguments = json.loads(payload)
    if not isinstance(arguments, list) or not all(
        isinstance(value, str) for value in arguments
    ):
        raise LiveNativeTeeError("arguments JSON must be an array of strings")
    return arguments


def _append_broker_failure(log_path: Path, message: str) -> None:
    try:
        if log_path.is_file():
            with log_path.open("a", encoding="utf-8", newline="") as handle:
                handle.write(message + "\n")
                handle.flush()
    except OSError:
        # The console diagnostic still survives even if the already-initialized
        # runner log becomes unavailable while handling the broker error.
        pass


def _recover_log_path(argv: Sequence[str]) -> Path | None:
    values = list(argv)
    try:
        index = values.index("--log-path")
        value = values[index + 1]
    except (ValueError, IndexError):
        return None
    return Path(value) if value else None


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    try:
        args = _parser().parse_args(raw_argv)
    except LiveNativeTeeError as exc:
        message = f"[FAIL] live_native_tee={type(exc).__name__}: {exc}"
        recovered_log = _recover_log_path(raw_argv)
        if recovered_log is not None:
            _append_broker_failure(recovered_log, message)
        print(message, file=sys.stderr, flush=True)
        return 2
    try:
        arguments = _decode_arguments(args)
        return run_live_native_tee(
            [args.executable, *arguments],
            log_path=args.log_path,
            stage_name=args.stage_name,
        )
    except (
        UnicodeEncodeError,
        UnicodeDecodeError,
        binascii.Error,
        json.JSONDecodeError,
        LiveNativeTeeError,
    ) as exc:
        message = f"[FAIL] live_native_tee={type(exc).__name__}: {exc}"
        _append_broker_failure(args.log_path, message)
        print(message, file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
