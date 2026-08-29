from __future__ import annotations

import unittest

from source.finite_gap_certificate import RationalCertificate, state_count
from source.finite_gap_parallel_exact_scan import (
    exact_scan_core,
    parallel_scan_exact_certificate_constraints,
)
from source.finite_gap_separation import scan_exact_certificate_constraints


def _certificate(*, feasible: bool) -> RationalCertificate:
    modulus = 210
    states = state_count(modulus)
    denominator = 100
    potentials = tuple((index % 7) - 3 for index in range(states))
    return RationalCertificate(
        modulus=modulus,
        threshold=12,
        denominator=denominator,
        lambda_num=2,
        mu_num=denominator if feasible else 0,
        t_num=3,
        phi_num=potentials,
        internal_bound=0,
        total_bound=0,
    )


class FiniteGapParallelExactScanTests(unittest.TestCase):
    def _assert_worker_invariance(self, certificate: RationalCertificate) -> None:
        serial = scan_exact_certificate_constraints(
            certificate,
            chunk_rows=3,
            top_k=25,
        )
        serial_core = exact_scan_core(serial)
        for workers in (1, 2, 4, 8):
            with self.subTest(workers=workers, feasible=serial["status"] == "PASS"):
                parallel = parallel_scan_exact_certificate_constraints(
                    certificate,
                    worker_count=workers,
                    row_block_rows=3,
                    top_k=25,
                )
                self.assertEqual(exact_scan_core(parallel), serial_core)
                metadata = parallel["parallel_execution"]
                self.assertEqual(metadata["source_rows_covered"], state_count(210))
                self.assertTrue(metadata["exact_integer_reduction"])
                self.assertFalse(metadata["worker_completion_order_affects_result"])
                self.assertEqual(metadata["worker_native_thread_ceiling"], 1)
                self.assertTrue(metadata["all_worker_native_thread_limits_one"])
                self.assertTrue(metadata["worker_static_arrays_initialized_once"])
                self.assertFalse(metadata["certificate_copied_per_row_block"])

    def test_feasible_certificate_matches_serial_for_workers_1_2_4_8(self) -> None:
        self._assert_worker_invariance(_certificate(feasible=True))

    def test_infeasible_certificate_matches_serial_for_workers_1_2_4_8(self) -> None:
        self._assert_worker_invariance(_certificate(feasible=False))

    def test_parallel_repeat_is_deterministic_including_top_k_ties(self) -> None:
        certificate = _certificate(feasible=False)
        first = parallel_scan_exact_certificate_constraints(
            certificate,
            worker_count=8,
            row_block_rows=3,
            top_k=25,
        )
        second = parallel_scan_exact_certificate_constraints(
            certificate,
            worker_count=8,
            row_block_rows=3,
            top_k=25,
        )
        self.assertEqual(exact_scan_core(first), exact_scan_core(second))
        self.assertEqual(len(first["top_exact_violations"]), 25)

    def test_parent_progress_callback_reaches_full_exact_coverage(self) -> None:
        events: list[dict[str, object]] = []
        report = parallel_scan_exact_certificate_constraints(
            _certificate(feasible=True),
            worker_count=1,
            row_block_rows=3,
            top_k=25,
            progress_callback=events.append,
        )
        self.assertEqual(report["status"], "PASS")
        self.assertGreater(len(events), 0)
        self.assertEqual(events[-1]["blocks_completed"], events[-1]["blocks_total"])
        self.assertEqual(events[-1]["source_rows_completed"], state_count(210))
        self.assertEqual(
            events[-1]["scanned_constraints_so_far"], report["scanned_constraints"]
        )


if __name__ == "__main__":
    unittest.main()
