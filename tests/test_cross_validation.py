"""Data-independent parser and approval tests for independent sources."""

import gzip
import tempfile
import unittest
from pathlib import Path

from source.cross_validation import (
    _parse_oeis_bfile,
    _parse_oliveira_table,
    cross_validate_oeis,
    cross_validate_oliveira,
)
from source.provenance import ApprovalRequiredError


class IndependentSourceTests(unittest.TestCase):
    def test_oeis_bfile_parser_requires_sequential_positive_terms(self) -> None:
        payload = b"# comment\n1 2\n2 3\n3 7\n"
        self.assertEqual(
            _parse_oeis_bfile(payload, sequence_id="A002386"),
            [2, 3, 7],
        )
        with self.assertRaises(ValueError):
            _parse_oeis_bfile(b"1 2\n3 7\n", sequence_id="A002386")

    def test_oliveira_parser_uses_star_after_gap_not_star_after_start(self) -> None:
        text = """# Test interval ---------- [2,4d18]
# Double test interval --- [2,4d17]
# Last update made on April 7, 2012
   g                 P(g)              N(g) finder
   1*                   2*                1 other
   2*                   3*                2 other
  10                  139*                3 other
  14*                 113                 4 other
"""
        records, info = _parse_oliveira_table(gzip.compress(text.encode("utf-8")))
        self.assertEqual(
            [(row["start_prime"], row["gap"], row["end_prime"]) for row in records],
            [(2, 1, 3), (3, 2, 5), (113, 14, 127)],
        )
        self.assertEqual(info["data_row_count"], 4)
        self.assertEqual(info["last_update_text"], "April 7, 2012")

    def test_oliveira_parser_rejects_missing_coverage_header(self) -> None:
        payload = gzip.compress(b"1* 2* 1 other\n")
        with self.assertRaises(ValueError):
            _parse_oliveira_table(payload)

    def test_cross_validation_refuses_before_network_or_write_without_approval(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ApprovalRequiredError):
                cross_validate_oeis(
                    root / "missing.csv",
                    root / "raw",
                    root / "result",
                    approval_token=None,
                )
            self.assertEqual(list(root.iterdir()), [])
            with self.assertRaises(ApprovalRequiredError):
                cross_validate_oliveira(
                    root / "missing.csv",
                    root / "raw",
                    root / "result",
                    approval_token=None,
                )
            self.assertEqual(list(root.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
