"""Data-independent checks for the independent result verifier."""

import tempfile
import unittest
from pathlib import Path

import mpmath as mp

from source.provenance import ApprovalRequiredError
from source.result_verification import _direct_f, verify_result_artifacts


class ResultVerificationTests(unittest.TestCase):
    def test_direct_formula_is_explicitly_nested_natural_logarithms(self) -> None:
        x = mp.mpf("1e20")
        log_1 = mp.log(x)
        log_2 = mp.log(log_1)
        log_3 = mp.log(log_2)
        log_4 = mp.log(log_3)
        expected = log_1 * log_2 * log_4 / log_3
        self.assertTrue(mp.almosteq(_direct_f(int(x)), expected))

    def test_verifier_refuses_before_read_or_write_without_approval(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ApprovalRequiredError):
                verify_result_artifacts(
                    root / "missing.csv",
                    root / "missing-result",
                    approval_token=None,
                )
            self.assertEqual(list(root.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
