from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from source.finite_gap_certificate import RationalCertificate, state_count
from source.finite_gap_mod510510 import (
    TARGET_CONSTRAINTS,
    TARGET_MODULUS,
    TARGET_STATES,
    _overflow_guard_upper_bound,
    _scan_certificate_exact,
    Mod510510Error,
    run_staged_experiment,
)
from source.finite_gap_replay import lift_certificate_exact_to_modulus
from source.finite_gap_separation import scan_exact_certificate_constraints
from source.provenance import ApprovalRequiredError


class FiniteGapMod510510Tests(unittest.TestCase):
    @staticmethod
    def _small_certificate() -> RationalCertificate:
        return RationalCertificate(
            modulus=30,
            threshold=12,
            denominator=100,
            lambda_num=0,
            mu_num=100,
            t_num=0,
            phi_num=tuple(0 for _ in range(state_count(30))),
            internal_bound=1,
            total_bound=2,
        )

    def test_static_target_contract(self) -> None:
        self.assertEqual(state_count(TARGET_MODULUS), TARGET_STATES)
        self.assertEqual(TARGET_CONSTRAINTS, 8_524_288_932)

    def test_small_exact_lift_remains_feasible(self) -> None:
        source = self._small_certificate()
        lifted = lift_certificate_exact_to_modulus(source, 210)
        report = scan_exact_certificate_constraints(lifted)
        self.assertEqual(report["status"], "PASS")
        self.assertLess(_overflow_guard_upper_bound(lifted), np.iinfo(np.int64).max)

    def test_parallel_backend_is_explicit_and_receives_resource_contract(self) -> None:
        sentinel = {"status": "PASS", "scanned_constraints": 1, "violation_count": 0}
        with patch(
            "source.finite_gap_mod510510.parallel_scan_exact_certificate_constraints",
            return_value=sentinel,
        ) as scanner:
            actual = _scan_certificate_exact(
                self._small_certificate(),
                exact_scan_backend="parallel",
                exact_scan_workers=8,
                chunk_rows=64,
                top_k=100,
            )
        self.assertIs(actual, sentinel)
        self.assertEqual(scanner.call_args.kwargs["worker_count"], 8)
        self.assertEqual(scanner.call_args.kwargs["row_block_rows"], 64)
        self.assertTrue(scanner.call_args.kwargs["allow_large_state_scan"])

    def test_serial_backend_refuses_parallel_worker_count(self) -> None:
        with self.assertRaises(Mod510510Error):
            _scan_certificate_exact(
                self._small_certificate(),
                exact_scan_backend="serial",
                exact_scan_workers=8,
                chunk_rows=64,
                top_k=100,
            )

    def test_actual_refuses_before_prerequisite_or_output_access(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "result"
            with self.assertRaises(ApprovalRequiredError):
                run_staged_experiment(
                    root / "missing-g4",
                    output,
                    approval_token=None,
                )
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
