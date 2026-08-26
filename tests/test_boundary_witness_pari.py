from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from source.boundary_witness import BoundaryWitnessError
from source.boundary_witness_pari import (
    discover_boundary_candidates,
    parse_boundary_candidate_payload,
    run_single_block_actual,
)
from source.pari_certificate import CERT_BEGIN, CERT_END, PariInvocation
from source.provenance import ApprovalRequiredError


class BoundaryWitnessPariTests(unittest.TestCase):
    def test_candidate_payload_requires_exact_integer_rows(self) -> None:
        p, q, factors = parse_boundary_candidate_payload(
            "[113,127,[[114,2],[115,5],[116,2],[117,3],[118,2],[119,7]]]"
        )
        self.assertEqual((p, q), (113, 127))
        self.assertEqual(tuple(item.value for item in factors), tuple(range(114, 120)))
        self.assertTrue(all(item.value % item.factor == 0 for item in factors))

    def test_malformed_payload_is_rejected(self) -> None:
        for payload in ("{}", "[113,127]", "[113,127,[[114,true]]]", "not-json"):
            with self.subTest(payload=payload):
                with self.assertRaises(BoundaryWitnessError):
                    parse_boundary_candidate_payload(payload)

    def test_candidate_discovery_requires_contiguous_factor_rows(self) -> None:
        def fake_runner(program: str, timeout_seconds: int) -> PariInvocation:
            self.assertIn("precprime", program)
            self.assertEqual(timeout_seconds, 30)
            return PariInvocation(
                command=("fake-gp",),
                returncode=0,
                stdout=(
                    f"{CERT_BEGIN}\n"
                    "[113,127,[[114,2],[115,5],[116,2],[117,3],[118,2],[119,7]]]\n"
                    f"{CERT_END}\n"
                ),
                stderr="",
                elapsed_seconds=0.01,
                maximum_resident_set_kib=123,
            )

        p, q, factors, invocation = discover_boundary_candidates(
            120, runner=fake_runner, timeout_seconds=30
        )
        self.assertEqual((p, q), (113, 127))
        self.assertEqual(len(factors), 6)
        self.assertEqual(invocation.maximum_resident_set_kib, 123)

    def test_actual_run_refuses_before_prerequisite_reads(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "actual"
            with self.assertRaises(ApprovalRequiredError):
                run_single_block_actual(
                    root / "missing_bounds.csv",
                    root / "missing_adapter.json",
                    root / "missing_replay.json",
                    output,
                    approval_token=None,
                )
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
