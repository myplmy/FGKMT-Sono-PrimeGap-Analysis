from __future__ import annotations

import math
import tempfile
import unittest
import json
from pathlib import Path

from source.finite_gap_certificate import RationalCertificate, state_count
from source.finite_gap_replay import (
    P007_MOD2310_CERTIFICATE_SHA256,
    P010A_EXPERIMENT,
    ReplayError,
    candidate_from_certificate,
    lift_candidate_to_modulus,
    require_mod2310_replay_completion,
    run_mod2310_replay,
    run_mod30030_one_candidate_scan,
)
from source.provenance import sha256_file
from source.provenance import ApprovalRequiredError


def toy_certificate(modulus: int = 30) -> RationalCertificate:
    states = state_count(modulus)
    return RationalCertificate(
        modulus=modulus,
        threshold=12,
        denominator=10,
        lambda_num=2,
        mu_num=3,
        t_num=0,
        phi_num=tuple(range(states)),
        internal_bound=0,
        total_bound=0,
    )


class FiniteGapReplayTests(unittest.TestCase):
    def test_candidate_conversion_preserves_scaled_values(self) -> None:
        candidate = candidate_from_certificate(toy_certificate())
        self.assertEqual(candidate.lambda_value, 0.2)
        self.assertEqual(candidate.mu_value, 0.3)
        self.assertEqual(candidate.potentials[3], 0.3)

    def test_lift_maps_each_target_residue_to_source_state(self) -> None:
        certificate = toy_certificate()
        lifted = lift_candidate_to_modulus(certificate, 210)
        source_values = candidate_from_certificate(certificate).potentials
        source_residues = tuple(
            value for value in range(30) if math.gcd(value, 30) == 1
        )
        source_index = {value: index for index, value in enumerate(source_residues)}
        target_residues = tuple(
            value for value in range(210) if math.gcd(value, 210) == 1
        )
        for target_index, residue in enumerate(target_residues):
            expected = source_values[source_index[residue % 30]]
            self.assertEqual(lifted.potentials[target_index], expected)

    def test_lift_rejects_nonmultiple_modulus(self) -> None:
        with self.assertRaises(ReplayError):
            lift_candidate_to_modulus(toy_certificate(), 210 + 2)

    def test_replay_refuses_before_input_read_or_output_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "replay"
            with self.assertRaises(ApprovalRequiredError):
                run_mod2310_replay(
                    root / "missing.txt", output, approval_token=None
                )
            self.assertFalse(output.exists())

    def test_mod30030_scan_refuses_before_prerequisite_reads(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "scan"
            with self.assertRaises(ApprovalRequiredError):
                run_mod30030_one_candidate_scan(
                    root / "missing_certificate.txt",
                    root / "missing_manifest.json",
                    output,
                    approval_token=None,
                )
            self.assertFalse(output.exists())

    def test_replay_completion_requires_hash_bound_saved_verification(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest_path = root / "manifest.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "status": "PASS",
                        "experiment": P010A_EXPERIMENT,
                        "input_certificate_sha256": P007_MOD2310_CERTIFICATE_SHA256,
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaises(ReplayError):
                require_mod2310_replay_completion(manifest_path)
            (root / "saved_verification_report.json").write_text(
                json.dumps(
                    {
                        "status": "PASS",
                        "exact_recomputed": True,
                        "manifest_sha256": sha256_file(manifest_path),
                    }
                ),
                encoding="utf-8",
            )
            accepted = require_mod2310_replay_completion(manifest_path)
            self.assertEqual(accepted["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
