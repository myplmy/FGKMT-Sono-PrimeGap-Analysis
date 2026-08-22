"""Tests for the upstream SQL parser and verified-record selector."""

import unittest
import tempfile
from pathlib import Path

from source.models import PrimeGapSourceRow
from source.prime_gap_list import (
    GapSourceFormatError,
    iter_source_rows,
    parse_insert_line,
    parse_start_prime_expression,
    select_verified_maximal_records,
    validate_upstream_schema,
)


def source_row(
    line_number: int,
    start_prime: int,
    gap: int,
    *,
    is_max: bool,
) -> PrimeGapSourceRow:
    return PrimeGapSourceRow(
        line_number=line_number,
        gap=gap,
        is_max=is_max,
        prime_category="C",
        first_occurrence_status="F",
        gap_certificate_status="C",
        discoverer="test",
        year=2026,
        merit_text="1.0000",
        prime_digits=len(str(start_prime)),
        start_prime_expression=str(start_prime),
    )


class PrimeGapListParsingTests(unittest.TestCase):
    def test_parse_insert_line_uses_published_ten_column_schema(self) -> None:
        line = "INSERT INTO gaps VALUES(14,1,'C','F','C','abc',2026,1.2345,3,'113');"
        row = parse_insert_line(line, 42)
        self.assertIsNotNone(row)
        assert row is not None
        self.assertEqual(row.line_number, 42)
        self.assertEqual(row.gap, 14)
        self.assertTrue(row.is_max)
        self.assertEqual(row.start_prime_expression, "113")

    def test_non_insert_line_is_ignored(self) -> None:
        self.assertIsNone(parse_insert_line("BEGIN TRANSACTION;", 1))

    def test_malformed_gaps_insert_is_not_silently_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "allgaps.sql"
            path.write_text("INSERT INTO gaps VALUES(not-valid)\n", encoding="utf-8")
            with self.assertRaises(GapSourceFormatError):
                list(iter_source_rows(path))

    def test_published_schema_column_order_is_validated(self) -> None:
        schema = """CREATE TABLE IF NOT EXISTS gaps(
            gapsize INTEGER,
            ismax BOOLEAN,
            primecat TEXT,
            isfirst TEXT,
            gapcert TEXT,
            discoverer TEXT,
            year INTEGER,
            merit REAL,
            primedigits INTEGER,
            startprime BLOB
        );"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schema.sql"
            path.write_text(schema, encoding="utf-8")
            columns = validate_upstream_schema(path)
        self.assertEqual(columns[0], "gapsize")
        self.assertEqual(columns[-1], "startprime")

    def test_changed_schema_column_order_is_rejected(self) -> None:
        schema = "CREATE TABLE gaps(ismax BOOLEAN, gapsize INTEGER);"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schema.sql"
            path.write_text(schema, encoding="utf-8")
            with self.assertRaises(GapSourceFormatError):
                validate_upstream_schema(path)

    def test_upstream_start_prime_expression_forms(self) -> None:
        cases = {
            "123": 123,
            "2*(5#)/3+1": 21,
            "5#/3+1": 11,
            "2*7#/(3#*5)+1": 15,
            "2*7#/(3*5)+1": 29,
            "2*7#/5#+1": 15,
            "2^5-1": 31,
        }
        for expression, expected in cases.items():
            with self.subTest(expression=expression):
                self.assertEqual(parse_start_prime_expression(expression), expected)

    def test_non_integral_or_unknown_expression_is_rejected(self) -> None:
        with self.assertRaises(GapSourceFormatError):
            parse_start_prime_expression("5#/4+1")
        with self.assertRaises(GapSourceFormatError):
            parse_start_prime_expression("not-a-prime")

    def test_flagged_records_match_independently_derived_high_watermarks(self) -> None:
        rows = [
            source_row(1, 2, 1, is_max=True),
            source_row(2, 3, 2, is_max=True),
            source_row(3, 7, 4, is_max=True),
            source_row(4, 23, 6, is_max=True),
            source_row(5, 89, 8, is_max=True),
            source_row(6, 113, 14, is_max=True),
            source_row(7, 139, 10, is_max=False),
        ]
        records, report = select_verified_maximal_records(
            rows,
            source_commit="a" * 40,
            exhaustive_limit=1_000,
            check_consecutive_primes=True,
        )
        self.assertEqual(report["status"], "PASS")
        self.assertEqual([record.gap for record in records], [1, 2, 4, 6, 8, 14])
        self.assertEqual(records[-1].end_prime, 127)
        self.assertEqual(report["boundary_mode"], "end")

    def test_incorrect_upstream_maximum_flag_fails_validation(self) -> None:
        rows = [
            source_row(1, 2, 1, is_max=True),
            source_row(2, 3, 2, is_max=False),
        ]
        _records, report = select_verified_maximal_records(
            rows,
            source_commit="b" * 40,
            exhaustive_limit=100,
            check_consecutive_primes=False,
        )
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("ismax_mismatch", {item["code"] for item in report["issues"]})

    def test_source_row_order_does_not_change_high_watermark_selection(self) -> None:
        rows = [
            source_row(1, 113, 14, is_max=True),
            source_row(2, 2, 1, is_max=True),
            source_row(3, 23, 6, is_max=True),
            source_row(4, 3, 2, is_max=True),
            source_row(5, 89, 8, is_max=True),
            source_row(6, 7, 4, is_max=True),
        ]
        records, report = select_verified_maximal_records(
            rows,
            source_commit="f" * 40,
            exhaustive_limit=1_000,
            check_consecutive_primes=True,
        )
        self.assertEqual(report["status"], "PASS")
        self.assertEqual([record.gap for record in records], [1, 2, 4, 6, 8, 14])


if __name__ == "__main__":
    unittest.main()
