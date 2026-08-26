from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from source.pari_certificate import (
    CERT_BEGIN,
    CERT_END,
    VALID_BEGIN,
    VALID_END,
    PariCertificateError,
    PariInvocation,
    canonical_certificate_json,
    certificate_subject,
    generate_certificate_bundle,
    parse_certificate_json,
    probe_gp_version,
    require_adapter_completion,
    run_adapter_validation,
    verify_saved_adapter_validation,
    verify_certificate_payload,
)
from source.provenance import sha256_file


TEST_TEMP_ROOT = Path(__file__).resolve().parents[1] / "tmp"
INTERMEDIATE = 1_000_000_000_000_000_000_000_000_000_057
INTERMEDIATE_CERT = [
    [
        INTERMEDIATE,
        1_941_308_218_874_090,
        1_603_111_594_224,
        0,
        [519_335_238_006_017_621_936_447_751_736, 51_315_546_389_334_118_416_664_791_836],
    ]
]


def fake_runner(program: str, timeout_seconds: int) -> PariInvocation:
    del timeout_seconds
    if "primecertisvalid" in program:
        stdout = f"{VALID_BEGIN}\n1\n{VALID_END}\n"
    elif "primecert(101)" in program:
        stdout = f"{CERT_BEGIN}\n101\n{CERT_END}\n"
    elif f"primecert({INTERMEDIATE})" in program:
        stdout = (
            f"{CERT_BEGIN}\n{canonical_certificate_json(INTERMEDIATE_CERT)}\n"
            f"{CERT_END}\n"
        )
    else:
        raise AssertionError(f"unexpected fake GP program: {program}")
    return PariInvocation(
        command=("fake-gp",),
        returncode=0,
        stdout=stdout,
        stderr="Maximum resident set size (kbytes): 1234\n",
        elapsed_seconds=0.01,
        maximum_resident_set_kib=1234,
    )


class PariCertificateTests(unittest.TestCase):
    def test_version_probe_accepts_pari_banner_from_stderr(self) -> None:
        from unittest.mock import patch

        completed = type(
            "Completed",
            (),
            {
                "returncode": 0,
                "stdout": "",
                "stderr": "GP/PARI CALCULATOR Version 2.15.4 (released)\n",
            },
        )()
        with patch("source.pari_certificate.subprocess.run", return_value=completed):
            self.assertEqual(
                probe_gp_version(),
                "GP/PARI CALCULATOR Version 2.15.4 (released)",
            )

    def test_small_integer_and_ecpp_subjects_are_bound(self) -> None:
        self.assertEqual(certificate_subject(101), 101)
        self.assertEqual(certificate_subject(INTERMEDIATE_CERT), INTERMEDIATE)
        self.assertEqual(
            parse_certificate_json(canonical_certificate_json(INTERMEDIATE_CERT)),
            INTERMEDIATE_CERT,
        )

    def test_malformed_shapes_and_boolean_are_rejected(self) -> None:
        for bad in (True, [], [[101, 1, 2, 3]], [[101, 1, 2, 3, [4]]]):
            with self.subTest(bad=bad):
                with self.assertRaises(PariCertificateError):
                    certificate_subject(bad)

    def test_wrong_subject_fails_before_gp_verification(self) -> None:
        called = False

        def refusing_runner(program: str, timeout_seconds: int) -> PariInvocation:
            nonlocal called
            called = True
            return fake_runner(program, timeout_seconds)

        report = verify_certificate_payload(
            INTERMEDIATE_CERT, INTERMEDIATE + 2, runner=refusing_runner
        )
        self.assertEqual(report.status, "FAIL")
        self.assertFalse(called)
        self.assertTrue(any("subject mismatch" in issue for issue in report.issues))

    def test_bundle_is_non_overwriting_and_hash_bound(self) -> None:
        TEST_TEMP_ROOT.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=TEST_TEMP_ROOT) as temporary:
            output = Path(temporary) / "bundle"
            manifest = generate_certificate_bundle(
                INTERMEDIATE,
                output,
                runner=fake_runner,
                gp_version="GP/PARI CALCULATOR Version test",
            )
            self.assertEqual(manifest["status"], "PASS")
            self.assertEqual(manifest["subject"], str(INTERMEDIATE))
            saved = json.loads((output / "certificate.json").read_text("ascii"))
            self.assertEqual(certificate_subject(saved), INTERMEDIATE)
            with self.assertRaises(FileExistsError):
                generate_certificate_bundle(
                    INTERMEDIATE,
                    output,
                    runner=fake_runner,
                    gp_version="GP/PARI CALCULATOR Version test",
                )

    def test_full_adapter_validation_has_negative_control(self) -> None:
        TEST_TEMP_ROOT.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=TEST_TEMP_ROOT) as temporary:
            output = Path(temporary) / "validation"
            summary = run_adapter_validation(
                output,
                runner=fake_runner,
                gp_version="GP/PARI CALCULATOR Version test",
            )
            self.assertEqual(summary["status"], "PASS")
            self.assertTrue(summary["wrong_subject_rejected"])
            self.assertFalse(summary["actual_1e20_experiment_executed"])
            manifest = json.loads(
                (output / "manifest.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["saved_artifact_verification"], "PASS")
            verified = verify_saved_adapter_validation(
                output,
                runner=fake_runner,
                gp_version="GP/PARI CALCULATOR Version test",
            )
            self.assertEqual(verified["status"], "PASS")
            self.assertEqual(verified["verified_subject_count"], 2)
            self.assertEqual(
                verified["manifest_sha256"], sha256_file(output / "manifest.json")
            )
            (output / "saved_verification_report.json").write_text(
                json.dumps(verified), encoding="utf-8"
            )
            accepted = require_adapter_completion(output / "manifest.json")
            self.assertEqual(accepted["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
