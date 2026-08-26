from __future__ import annotations

import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from source.boundary_witness import (
    CompositeEvidence,
    PrimeEvidence,
    build_toy_witness,
    run_toy_witness,
    verify_boundary_witness,
    verify_saved_toy_result,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_TEMP_ROOT = PROJECT_ROOT / "tmp"


class BoundaryWitnessTests(unittest.TestCase):
    def test_toy_witness_closes_crossing_exactly(self) -> None:
        witness = build_toy_witness()
        report = verify_boundary_witness(witness)
        self.assertEqual(report["status"], "PASS")
        self.assertTrue(report["crossing_certified_small"])
        self.assertTrue(report["certified_zero"])
        self.assertEqual(report["last_prime"], "113")
        self.assertEqual(report["right_prime"], "127")

    def test_missing_integer_is_a_coverage_failure(self) -> None:
        witness = build_toy_witness()
        broken = replace(witness, composite_evidence=witness.composite_evidence[:-1])
        report = verify_boundary_witness(broken)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("coverage holes" in issue for issue in report["issues"]))

    def test_bad_factor_is_rejected(self) -> None:
        witness = build_toy_witness()
        evidence = list(witness.composite_evidence)
        evidence[0] = CompositeEvidence(evidence[0].value, 5)
        report = verify_boundary_witness(
            replace(witness, composite_evidence=tuple(evidence))
        )
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("does not divide" in issue for issue in report["issues"]))

    def test_threshold_equality_is_not_accepted(self) -> None:
        witness = build_toy_witness()
        report = verify_boundary_witness(replace(witness, threshold=14))
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("q-p < threshold" in issue for issue in report["issues"]))

    def test_probable_prime_label_is_rejected(self) -> None:
        witness = build_toy_witness()
        probable = replace(
            witness,
            right_prime=PrimeEvidence(127, "miller_rabin_probable"),
        )
        report = verify_boundary_witness(probable)
        self.assertEqual(report["status"], "FAIL")
        self.assertFalse(report["probable_prime_accepted"])

    def test_internal_nonzero_closes_crossing_but_not_whole_block(self) -> None:
        witness = build_toy_witness(internal_start_bounded_upper_bound=1)
        report = verify_boundary_witness(witness)
        self.assertEqual(report["status"], "PASS")
        self.assertTrue(report["crossing_certified_small"])
        self.assertFalse(report["certified_zero"])

    def test_saved_artifacts_reverify_and_do_not_overwrite(self) -> None:
        TEST_TEMP_ROOT.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=TEST_TEMP_ROOT) as temporary:
            output = Path(temporary) / "toy"
            run_toy_witness(output)
            self.assertEqual(verify_saved_toy_result(output)["status"], "PASS")
            with self.assertRaises(FileExistsError):
                run_toy_witness(output)

    def test_saved_verifier_cross_checks_composite_csv(self) -> None:
        TEST_TEMP_ROOT.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=TEST_TEMP_ROOT) as temporary:
            output = Path(temporary) / "toy"
            run_toy_witness(output)
            csv_path = output / "composite_evidence.csv"
            text = csv_path.read_text(encoding="utf-8")
            csv_path.write_text(text.replace("114,2", "114,3"), encoding="utf-8")
            report = verify_saved_toy_result(output)
            self.assertEqual(report["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
