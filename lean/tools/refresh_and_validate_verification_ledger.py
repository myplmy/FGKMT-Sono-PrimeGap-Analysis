"""Refresh the generated Lean formula ledger, then validate it fail-closed."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


TOOLS_DIR = Path(__file__).resolve().parent
LEAN_ROOT = TOOLS_DIR.parent


def _run(script_name: str) -> int:
    script_path = TOOLS_DIR / script_name
    completed = subprocess.run(
        [sys.executable, "-X", "utf8", str(script_path)],
        cwd=LEAN_ROOT,
        check=False,
    )
    return completed.returncode


def main() -> int:
    generator_exit = _run("generate_verification_ledger.py")
    if generator_exit != 0:
        print(
            json.dumps(
                {
                    "failed_stage": "generate_verification_ledger",
                    "generator_exit_code": generator_exit,
                    "status": "FAIL",
                    "validator_ran": False,
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return generator_exit

    validator_exit = _run("validate_verification_ledger.py")
    if validator_exit != 0:
        print(
            json.dumps(
                {
                    "failed_stage": "validate_verification_ledger",
                    "generator_exit_code": generator_exit,
                    "status": "FAIL",
                    "validator_exit_code": validator_exit,
                    "validator_ran": True,
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return validator_exit

    print(
        json.dumps(
            {
                "generator_exit_code": generator_exit,
                "sequence": "generate_then_validate",
                "status": "PASS",
                "validator_exit_code": validator_exit,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
