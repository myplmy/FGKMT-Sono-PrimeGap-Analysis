"""End-to-end synthetic fixture test for validation and analysis artifacts."""

import json
import tempfile
import unittest
from pathlib import Path

import gmpy2

from source.definitions import X_SCALE_POSITIVE_MIN
from source.pipeline import analyze_validated_records, validate_raw_dataset
from source.provenance import APPROVAL_TOKEN, sha256_file


SCHEMA = (
    "CREATE TABLE IF NOT EXISTS gaps ("
    "gapsize INTEGER,ismax BOOLEAN,primecat TEXT,isfirst TEXT,"
    "gapcert TEXT,discoverer TEXT,year INTEGER,merit REAL,"
    "primedigits INTEGER,startprime BLOB);\n"
)


def make_toy_record_rows() -> list[tuple[int, int]]:
    records: list[tuple[int, int]] = []
    running_gap = -1
    start = int(gmpy2.next_prime(X_SCALE_POSITIVE_MIN - 500))
    for _ in range(20_000):
        end = int(gmpy2.next_prime(start))
        gap = end - start
        if gap > running_gap:
            records.append((start, gap))
            running_gap = gap
            if len(records) >= 5 and end > X_SCALE_POSITIVE_MIN:
                return records
        start = end
    raise AssertionError("could not build enough synthetic local high-watermarks")


class SyntheticPipelineTests(unittest.TestCase):
    def test_validation_analysis_and_provenance_artifacts(self) -> None:
        toy_records = make_toy_record_rows()
        final_end = toy_records[-1][0] + toy_records[-1][1]
        exhaustive_limit = final_end + 10_000

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw_directory = root / "raw"
            raw_directory.mkdir()
            raw_path = raw_directory / "allgaps.sql"
            schema_path = raw_directory / "schema.sql"
            metadata_path = raw_directory / "metadata.json"
            schema_path.write_text(SCHEMA, encoding="utf-8")

            sql_rows = []
            for start, gap in toy_records:
                sql_rows.append(
                    "INSERT INTO gaps VALUES("
                    f"{gap},1,'C','F','C','toy',2026,1.0000,"
                    f"{len(str(start))},'{start}');"
                )
            raw_path.write_text("\n".join(sql_rows) + "\n", encoding="utf-8")
            commit = "e" * 40
            metadata = {
                "commit": commit,
                "sha256": sha256_file(raw_path),
                "files": {
                    "allgaps.sql": {"sha256": sha256_file(raw_path)},
                    "schema.sql": {"sha256": sha256_file(schema_path)},
                },
            }
            metadata_path.write_text(
                json.dumps(metadata),
                encoding="utf-8",
            )

            validated_directory = root / "validated"
            records_path, report_path, records, report = validate_raw_dataset(
                raw_path,
                metadata_path,
                validated_directory,
                approval_token=APPROVAL_TOKEN,
                exhaustive_limit=exhaustive_limit,
            )
            self.assertEqual(report["status"], "PASS")
            self.assertTrue(records_path.is_file())
            self.assertTrue(report_path.is_file())
            self.assertEqual(len(records), len(toy_records))
            self.assertIn("code_sha256", report["execution"])

            result_directory = root / "result"
            summary = analyze_validated_records(
                records_path,
                result_directory,
                approval_token=APPROVAL_TOKEN,
                analysis_limit=exhaustive_limit,
                summary_additions={"execution_scope": "SYNTHETIC_TEST"},
            )
            self.assertEqual(summary["boundary_mode"], "end")
            self.assertEqual(len(summary["figure_files"]), 14)
            self.assertIn("code_sha256", summary["execution"])
            self.assertEqual(summary["execution_scope"], "SYNTHETIC_TEST")
            self.assertTrue((result_directory / "summary.json").is_file())
            self.assertTrue((result_directory / "tables" / "log10_bin_minima.csv").is_file())
            self.assertIn("local_envelopes", summary)


if __name__ == "__main__":
    unittest.main()
