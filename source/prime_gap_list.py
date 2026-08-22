"""Parse and validate the Prime Gap List Project SQL source.

The upstream file is a SQL text dump, but this module deliberately parses only
``INSERT INTO gaps VALUES (...)`` rows instead of executing downloaded SQL.
That keeps the accepted input surface small and makes every source row
traceable by its original line number.
"""

from __future__ import annotations

import csv
import re
from dataclasses import asdict
from pathlib import Path
from typing import Iterable, Iterator

import gmpy2

from source.models import MaximalGapRecord, PrimeGapSourceRow, ValidationIssue


SOURCE_ID = "prime-gap-list-project/prime-gap-list:allgaps.sql"
DEFAULT_EXHAUSTIVE_LIMIT = 10**20
EXHAUSTIVE_LIMIT_SOURCE_URL = (
    "https://primegap-list-project.github.io/fully-analyzed/"
)
EXHAUSTIVE_LIMIT_AS_OF = "2026-05-08"
EXPECTED_SCHEMA_COLUMNS = (
    "gapsize",
    "ismax",
    "primecat",
    "isfirst",
    "gapcert",
    "discoverer",
    "year",
    "merit",
    "primedigits",
    "startprime",
)

_INSERT_RE = re.compile(r"^INSERT\s+INTO\s+gaps\s+VALUES\s*\((.*)\);\s*$")
_SCHEMA_RE = re.compile(
    r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?gaps\s*\((.*?)\)\s*;",
    flags=re.IGNORECASE | re.DOTALL,
)
_NUMBER_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"^(\d+)\*\(?(\d+)#\)?/(\d+)([+-]\d+)$"), "m_primorial_div"),
    (re.compile(r"^\(?(\d+)#\)?/(\d+)([+-]\d+)$"), "primorial_div"),
    (
        re.compile(r"^(\d+)\*(\d+)#/\((\d+)#\*(\d+)\)([+-]\d+)$"),
        "m_primorial_div_primorial_times",
    ),
    (
        re.compile(r"^(\d+)\*(\d+)#/\((\d+)\*(\d+)\)([+-]\d+)$"),
        "m_primorial_div_product",
    ),
    (re.compile(r"^(\d+)\*(\d+)#/(\d+)#([+-]\d+)$"), "m_primorial_div_primorial"),
    (re.compile(r"^(\d+)\^(\d+)([+-]\d+)$"), "power"),
)


class GapSourceFormatError(ValueError):
    """Raised when the upstream SQL row does not match its published schema."""


def validate_upstream_schema(schema_path: Path) -> tuple[str, ...]:
    """Validate the ordered columns expected by the restricted row parser."""

    text = schema_path.read_text(encoding="utf-8-sig")
    match = _SCHEMA_RE.search(text)
    if match is None:
        raise GapSourceFormatError("schema.sql does not define CREATE TABLE gaps")

    columns: list[str] = []
    for definition in match.group(1).split(","):
        fields = definition.strip().split()
        if not fields:
            raise GapSourceFormatError("schema.sql contains an empty column definition")
        columns.append(fields[0].strip('\"[]').lower())
    parsed = tuple(columns)
    if parsed != EXPECTED_SCHEMA_COLUMNS:
        raise GapSourceFormatError(
            "schema.sql columns changed: "
            f"expected {EXPECTED_SCHEMA_COLUMNS!r}, found {parsed!r}"
        )
    return parsed


def _parse_bool(token: str, *, line_number: int) -> bool:
    if token == "0":
        return False
    if token == "1":
        return True
    raise GapSourceFormatError(f"line {line_number}: ismax must be 0 or 1, got {token!r}")


def parse_insert_line(line: str, line_number: int) -> PrimeGapSourceRow | None:
    """Parse one upstream SQL insert, or return ``None`` for a non-data line."""

    match = _INSERT_RE.match(line.strip())
    if match is None:
        return None

    try:
        fields = next(
            csv.reader(
                [match.group(1)],
                delimiter=",",
                quotechar="'",
                doublequote=True,
                skipinitialspace=True,
            )
        )
    except csv.Error as exc:
        raise GapSourceFormatError(f"line {line_number}: invalid SQL values list") from exc

    if len(fields) != 10:
        raise GapSourceFormatError(
            f"line {line_number}: expected 10 gaps columns, found {len(fields)}"
        )

    fields = [field.strip() for field in fields]
    try:
        gap = int(fields[0])
        year = int(fields[6])
        prime_digits = int(fields[8])
    except ValueError as exc:
        raise GapSourceFormatError(f"line {line_number}: invalid integer field") from exc

    if gap <= 0 or prime_digits <= 0:
        raise GapSourceFormatError(f"line {line_number}: gap and prime_digits must be positive")

    return PrimeGapSourceRow(
        line_number=line_number,
        gap=gap,
        is_max=_parse_bool(fields[1], line_number=line_number),
        prime_category=fields[2],
        first_occurrence_status=fields[3],
        gap_certificate_status=fields[4],
        discoverer=fields[5],
        year=year,
        merit_text=fields[7],
        prime_digits=prime_digits,
        start_prime_expression=fields[9],
    )


def iter_source_rows(path: Path) -> Iterator[PrimeGapSourceRow]:
    """Yield all parsed gap rows with stable line-number provenance."""

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            row = parse_insert_line(line, line_number)
            if row is None and re.match(
                r"^\s*INSERT\s+INTO\s+gaps\b",
                line,
                flags=re.IGNORECASE,
            ):
                raise GapSourceFormatError(
                    f"line {line_number}: malformed gaps INSERT was not accepted"
                )
            if row is not None:
                yield row


def _exact_division(numerator: int, denominator: int, expression: str) -> int:
    if denominator <= 0 or numerator % denominator:
        raise GapSourceFormatError(f"non-integral source expression: {expression!r}")
    return numerator // denominator


def parse_start_prime_expression(expression: str) -> int:
    """Expand a decimal or upstream primorial/power start-prime expression.

    The supported grammar mirrors the six expression forms in the upstream
    project's ``check.py``. ``#`` denotes a primorial, never a comment.
    """

    compact = expression.replace(" ", "")
    if compact.isdigit():
        return int(compact)

    for pattern, kind in _NUMBER_PATTERNS:
        match = pattern.fullmatch(compact)
        if match is None:
            continue
        values = tuple(map(int, match.groups()))

        if kind == "m_primorial_div":
            multiplier, prime, denominator, offset = values
            numerator = multiplier * int(gmpy2.primorial(prime))
            return _exact_division(numerator, denominator, expression) + offset

        if kind == "primorial_div":
            prime, denominator, offset = values
            numerator = int(gmpy2.primorial(prime))
            return _exact_division(numerator, denominator, expression) + offset

        if kind == "m_primorial_div_primorial_times":
            multiplier, prime, divisor_prime, divisor, offset = values
            numerator = multiplier * int(gmpy2.primorial(prime))
            denominator = int(gmpy2.primorial(divisor_prime)) * divisor
            return _exact_division(numerator, denominator, expression) + offset

        if kind == "m_primorial_div_product":
            multiplier, prime, divisor_1, divisor_2, offset = values
            numerator = multiplier * int(gmpy2.primorial(prime))
            return _exact_division(numerator, divisor_1 * divisor_2, expression) + offset

        if kind == "m_primorial_div_primorial":
            multiplier, prime, divisor_prime, offset = values
            numerator = multiplier * int(gmpy2.primorial(prime))
            denominator = int(gmpy2.primorial(divisor_prime))
            return _exact_division(numerator, denominator, expression) + offset

        if kind == "power":
            base, exponent, offset = values
            return base**exponent + offset

    raise GapSourceFormatError(f"unsupported start-prime expression: {expression!r}")


def _derive_high_watermarks(
    rows: Iterable[tuple[PrimeGapSourceRow, int]],
) -> list[tuple[PrimeGapSourceRow, int]]:
    running_gap = -1
    records: list[tuple[PrimeGapSourceRow, int]] = []
    for row, start_prime in sorted(rows, key=lambda item: (item[1], item[0].gap)):
        if row.gap > running_gap:
            records.append((row, start_prime))
            running_gap = row.gap
    return records


def select_verified_maximal_records(
    rows: Iterable[PrimeGapSourceRow],
    *,
    source_commit: str,
    exhaustive_limit: int = DEFAULT_EXHAUSTIVE_LIMIT,
    check_consecutive_primes: bool = True,
) -> tuple[list[MaximalGapRecord], dict[str, object]]:
    """Select end-bounded records inside a documented exhaustive range.

    Rows must be confirmed (``primecat == 'C'``), marked as first occurrences
    (``isfirst == 'F'``), and have ``end_prime <= exhaustive_limit``. The
    upstream ``ismax`` flag is checked against high watermarks independently
    derived from all eligible first-occurrence rows.
    """

    if exhaustive_limit < 2:
        raise ValueError("exhaustive_limit must be at least 2")
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ValueError("source_commit must be a lowercase 40-character Git SHA")

    issues: list[ValidationIssue] = []
    counts: dict[str, int] = {
        "source_rows": 0,
        "rows_above_exhaustive_limit": 0,
        "rows_unconfirmed": 0,
        "rows_not_first_occurrence": 0,
        "eligible_first_occurrence_rows": 0,
        "flagged_maximal_rows": 0,
    }
    eligible: list[tuple[PrimeGapSourceRow, int]] = []
    max_digits = len(str(exhaustive_limit))

    for row in rows:
        counts["source_rows"] += 1

        # Avoid expanding enormous primorials that cannot possibly fall in the
        # approved range. Equal digit counts still require exact comparison.
        if row.prime_digits > max_digits:
            counts["rows_above_exhaustive_limit"] += 1
            continue

        source_row_id = f"allgaps.sql:{row.line_number}"
        try:
            start_prime = parse_start_prime_expression(row.start_prime_expression)
        except GapSourceFormatError as exc:
            issues.append(ValidationIssue("error", "start_expression", str(exc), source_row_id))
            continue

        end_prime = start_prime + row.gap
        if end_prime > exhaustive_limit:
            counts["rows_above_exhaustive_limit"] += 1
            continue
        if len(str(start_prime)) != row.prime_digits:
            issues.append(
                ValidationIssue(
                    "error",
                    "prime_digits",
                    f"declared {row.prime_digits}, calculated {len(str(start_prime))}",
                    source_row_id,
                )
            )
            continue
        if row.prime_category != "C":
            counts["rows_unconfirmed"] += 1
            continue
        if row.first_occurrence_status != "F":
            counts["rows_not_first_occurrence"] += 1
            continue

        eligible.append((row, start_prime))

    counts["eligible_first_occurrence_rows"] = len(eligible)
    derived = _derive_high_watermarks(eligible)
    flagged = sorted(
        ((row, start_prime) for row, start_prime in eligible if row.is_max),
        key=lambda item: item[1],
    )
    counts["flagged_maximal_rows"] = len(flagged)

    derived_keys = [(start, row.gap) for row, start in derived]
    flagged_keys = sorted((start, row.gap) for row, start in flagged)
    if derived_keys != flagged_keys:
        issues.append(
            ValidationIssue(
                "error",
                "ismax_mismatch",
                "upstream ismax rows do not match independently derived high watermarks",
            )
        )

    records: list[MaximalGapRecord] = []
    previous_start = -1
    previous_end = -1
    previous_gap = -1
    for record_index, (row, start_prime) in enumerate(flagged, start=1):
        source_row_id = f"allgaps.sql:{row.line_number}"
        end_prime = start_prime + row.gap

        if start_prime <= previous_start or end_prime <= previous_end:
            issues.append(
                ValidationIssue(
                    "error",
                    "record_order",
                    "record start/end primes are not strictly increasing",
                    source_row_id,
                )
            )
        if row.gap <= previous_gap:
            issues.append(
                ValidationIssue(
                    "error",
                    "gap_order",
                    "record gaps are not strictly increasing",
                    source_row_id,
                )
            )

        if check_consecutive_primes:
            if int(gmpy2.next_prime(start_prime)) != end_prime:
                issues.append(
                    ValidationIssue(
                        "error",
                        "not_consecutive_primes",
                        "end_prime is not the next prime after start_prime",
                        source_row_id,
                    )
                )

        records.append(
            MaximalGapRecord(
                record_index=record_index,
                start_prime=start_prime,
                gap=row.gap,
                end_prime=end_prime,
                source_id=SOURCE_ID,
                source_row_id=source_row_id,
                source_commit=source_commit,
                verified_exhaustive_limit=exhaustive_limit,
            )
        )
        previous_start = start_prime
        previous_end = end_prime
        previous_gap = row.gap

    if not records:
        issues.append(ValidationIssue("error", "no_records", "no eligible maximal records found"))

    report: dict[str, object] = {
        "status": "FAIL" if any(issue.severity == "error" for issue in issues) else "PASS",
        "source_id": SOURCE_ID,
        "source_commit": source_commit,
        "boundary_mode": "end",
        "verified_exhaustive_limit": str(exhaustive_limit),
        "exhaustive_limit_source_url": EXHAUSTIVE_LIMIT_SOURCE_URL,
        "exhaustive_limit_source_as_of": EXHAUSTIVE_LIMIT_AS_OF,
        "counts": counts | {"selected_records": len(records)},
        "issues": [asdict(issue) for issue in issues],
        "validation_scope": {
            "source_flags": ["ismax=1", "primecat=C", "isfirst=F"],
            "arithmetic": "end_prime = start_prime + gap",
            "sequence": "start, end, and gap strictly increase",
            "consecutive_prime_check": check_consecutive_primes,
            "completeness_basis": "external exhaustive-range provenance; not inferred from primality checks",
        },
    }
    return records, report


def load_and_select_records(
    raw_path: Path,
    *,
    source_commit: str,
    exhaustive_limit: int = DEFAULT_EXHAUSTIVE_LIMIT,
    check_consecutive_primes: bool = True,
) -> tuple[list[MaximalGapRecord], dict[str, object]]:
    """Convenience wrapper around streaming parse and record selection."""

    return select_verified_maximal_records(
        iter_source_rows(raw_path),
        source_commit=source_commit,
        exhaustive_limit=exhaustive_limit,
        check_consecutive_primes=check_consecutive_primes,
    )


__all__ = [
    "DEFAULT_EXHAUSTIVE_LIMIT",
    "EXPECTED_SCHEMA_COLUMNS",
    "EXHAUSTIVE_LIMIT_AS_OF",
    "EXHAUSTIVE_LIMIT_SOURCE_URL",
    "GapSourceFormatError",
    "SOURCE_ID",
    "iter_source_rows",
    "load_and_select_records",
    "parse_insert_line",
    "parse_start_prime_expression",
    "select_verified_maximal_records",
    "validate_upstream_schema",
]
