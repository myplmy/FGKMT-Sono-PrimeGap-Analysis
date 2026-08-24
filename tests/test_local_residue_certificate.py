from __future__ import annotations

import tempfile
import unittest
import hashlib
from pathlib import Path

from source.finite_gap_certificate import read_certificate
from source.local_residue_certificate import (
    COUNT_FIELDS,
    P008_FULL_COUNT_PROVENANCE,
    P008_FULL_LENGTHS,
    P008_FULL_X,
    LocalBlockInput,
    LocalCertificateError,
    evaluate_local_block,
    read_block_inputs,
    run_local_experiment,
    toy_block_inputs,
    write_block_inputs,
    verify_coverage_ledger,
    verify_saved_result,
)
from source.provenance import APPROVAL_TOKEN


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE_PATH = (
    ROOT
    / "ai_dev_tool"
    / "temp_prime_gap_count_algorithm"
    / "source"
    / "C2310_certificate.txt"
)


class LocalResidueCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.certificate = read_certificate(CERTIFICATE_PATH)

    def test_unknown_right_boundary_never_produces_zero_for_nonempty_block(self) -> None:
        resolved = toy_block_inputs(self.certificate.threshold)[0]
        unknown = LocalBlockInput(
            block_id="unknown",
            a=resolved.a,
            b=resolved.b,
            pi_a_minus_1=resolved.pi_a_minus_1,
            pi_b_minus_1=resolved.pi_b_minus_1,
            count_provenance="toy_counts_without_boundary",
        )
        report = evaluate_local_block(unknown, self.certificate)
        self.assertGreater(int(report["start_prime_count"]), 0)
        self.assertEqual(report["right_boundary_status"], "UNRESOLVED")
        self.assertGreaterEqual(int(report["total_start_bounded_upper_bound"]), 1)
        self.assertFalse(report["certified_zero"])

    def test_resolved_small_crossing_can_certify_zero(self) -> None:
        block = toy_block_inputs(self.certificate.threshold)[0]
        report = evaluate_local_block(block, self.certificate)
        self.assertEqual(report["right_boundary_status"], "CERTIFIED_SMALL")
        self.assertEqual(report["actual_large_gap_count"], "0")
        self.assertEqual(report["total_start_bounded_upper_bound"], "0")
        self.assertTrue(report["certified_zero"])

    def test_floor_is_tighter_than_historic_conservative_ceil(self) -> None:
        block = toy_block_inputs(self.certificate.threshold)[-1]
        report = evaluate_local_block(block, self.certificate)
        floor_value = int(report["raw_internal_floor"])
        ceil_value = int(report["historic_conservative_ceil"])
        self.assertIn(ceil_value - floor_value, (0, 1))
        self.assertLessEqual(
            int(report["internal_integer_upper_bound"]),
            floor_value,
        )

    def test_coverage_ledger_requires_contiguity_and_evidence(self) -> None:
        valid = [
            {
                "a": 100,
                "b": 200,
                "status": "CERTIFIED_ZERO",
                "certificate_sha256": "abc",
            },
            {
                "a": 200,
                "b": 300,
                "status": "EXACT_SEARCHED",
                "artifact_sha256": "def",
            },
        ]
        self.assertEqual(
            verify_coverage_ledger(valid, a=100, b=300)["status"], "PASS"
        )
        invalid = [dict(valid[0]), {**valid[1], "a": 201}]
        self.assertEqual(
            verify_coverage_ledger(invalid, a=100, b=300)["status"], "FAIL"
        )

    def test_pilot_is_approval_gated_and_saved_result_reverifies(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = Path(temporary) / "result"
            with self.assertRaises(PermissionError):
                run_local_experiment(
                    CERTIFICATE_PATH,
                    result,
                    mode="pilot",
                    approval_token=None,
                )
            summary = run_local_experiment(
                CERTIFICATE_PATH,
                result,
                mode="pilot",
                approval_token=APPROVAL_TOKEN,
            )
            self.assertEqual(summary["status"], "PASS")
            self.assertEqual(verify_saved_result(result)["status"], "PASS")
            with self.assertRaises(FileExistsError):
                run_local_experiment(
                    CERTIFICATE_PATH,
                    result,
                    mode="pilot",
                    approval_token=APPROVAL_TOKEN,
                )

    def test_count_csv_schema_is_exact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "bad.csv"
            path.write_text(
                ",".join(COUNT_FIELDS[:-1]) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(LocalCertificateError):
                read_block_inputs(path)

    def test_full_mode_rejects_metadata_hash_mismatch_before_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            counts = root / "counts.csv"
            metadata = root / "metadata.txt"
            result = root / "result"
            phase_a_rows = [
                LocalBlockInput(
                    block_id=f"x1e20_L{length}",
                    a=P008_FULL_X,
                    b=P008_FULL_X + length,
                    pi_a_minus_1=2_220_819_602_560_918_840,
                    pi_b_minus_1=(
                        2_220_819_602_560_918_840 + max(1, length // 46)
                    ),
                    count_provenance=P008_FULL_COUNT_PROVENANCE,
                )
                for length in P008_FULL_LENGTHS
            ]
            write_block_inputs(counts, phase_a_rows)
            metadata.write_text(
                "\n".join(
                    (
                        "status=PRIMECOUNTS_READY",
                        "primecount_version=primecount 7.10",
                        "algorithms=gourdon,deleglise-rivat",
                        "algorithm_outputs_must_match=true",
                        "threads=8",
                        "virtual_memory_limit_kib=31457280",
                        "gpu_used=false",
                        "actual_prime_gap_search=false",
                        "bound_calculator=Windows_FGKMT_Python_in_separate_step",
                        f"counts_sha256={'0' * 64}",
                    )
                )
                + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(LocalCertificateError):
                run_local_experiment(
                    CERTIFICATE_PATH,
                    result,
                    mode="full",
                    approval_token=APPROVAL_TOKEN,
                    counts_path=counts,
                    count_metadata_path=metadata,
                )
            self.assertFalse(result.exists())

            counts_hash = hashlib.sha256(counts.read_bytes()).hexdigest()
            text = metadata.read_text(encoding="utf-8").replace("0" * 64, counts_hash)
            metadata.write_text(text, encoding="utf-8")
            summary = run_local_experiment(
                CERTIFICATE_PATH,
                result,
                mode="full",
                approval_token=APPROVAL_TOKEN,
                counts_path=counts,
                count_metadata_path=metadata,
            )
            self.assertEqual(summary["status"], "PASS")
            self.assertEqual(verify_saved_result(result)["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
