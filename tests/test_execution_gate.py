"""Ensure actual acquisition cannot begin without an explicit approval marker."""

import tempfile
import unittest
from pathlib import Path

from source.pipeline import analyze_validated_records, validate_raw_dataset
from source.provenance import (
    ApprovalRequiredError,
    SCHEMA_FILE_NAME,
    acquire_dataset,
    pinned_raw_url,
)


class ExecutionApprovalGateTests(unittest.TestCase):
    def test_acquisition_refuses_before_network_or_directory_creation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ApprovalRequiredError):
                acquire_dataset(root, approval_token=None)
            self.assertEqual(list(root.iterdir()), [])

    def test_commit_pinned_urls_cover_data_and_schema(self) -> None:
        commit = "a" * 40
        self.assertTrue(pinned_raw_url(commit).endswith(f"/{commit}/allgaps.sql"))
        self.assertTrue(
            pinned_raw_url(commit, SCHEMA_FILE_NAME).endswith(
                f"/{commit}/schema.sql"
            )
        )

    def test_unlisted_upstream_file_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            pinned_raw_url("a" * 40, "README.md")

    def test_validation_refuses_before_read_or_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "validated"
            with self.assertRaises(ApprovalRequiredError):
                validate_raw_dataset(
                    root / "missing.sql",
                    root / "missing.json",
                    output,
                    approval_token=None,
                )
            self.assertFalse(output.exists())

    def test_analysis_refuses_before_read_or_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "result"
            with self.assertRaises(ApprovalRequiredError):
                analyze_validated_records(
                    root / "missing.csv",
                    output,
                    approval_token=None,
                    analysis_limit=10**20,
                )
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
