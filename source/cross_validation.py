"""Acquire immutable independent representations and cross-check maximal records."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

from source.provenance import require_experiment_approval, sha256_file


OEIS_STARTS_URL = "https://oeis.org/A002386/b002386.txt"
OEIS_GAPS_URL = "https://oeis.org/A005250/b005250.txt"
OEIS_STARTS_ID = "A002386"
OEIS_GAPS_ID = "A005250"
OLIVEIRA_TABLE_URL = "https://sweet.ua.pt/tos/gaps/t0.txt.gz"
OLIVEIRA_PAGE_URL = "https://sweet.ua.pt/tos/gaps.html"
OLIVEIRA_TEST_LIMIT = 4_000_000_000_000_000_000
OLIVEIRA_DOUBLE_TEST_LIMIT = 400_000_000_000_000_000
_OLIVEIRA_ROW = re.compile(r"^\s*(\d+)(\*)?\s+(\d+)(\*)?\s+(\d+)\s+")


def _download(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "FGKMT-Sono-PrimeGap-Analysis/1.0"},
    )
    with urllib.request.urlopen(request, timeout=90) as response:  # noqa: S310
        payload = response.read()
    if not payload:
        raise RuntimeError(f"independent source returned an empty response: {url}")
    return payload


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _write_bytes_exclusive(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(payload)


def _write_json_exclusive(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(serialized)


def _parse_oeis_bfile(payload: bytes, *, sequence_id: str) -> list[int]:
    try:
        text = payload.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{sequence_id} b-file is not UTF-8 text") from exc
    values: list[int] = []
    expected_index = 1
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split()
        if len(fields) != 2:
            raise ValueError(
                f"{sequence_id} line {line_number}: expected index and value"
            )
        try:
            index, value = map(int, fields)
        except ValueError as exc:
            raise ValueError(
                f"{sequence_id} line {line_number}: invalid integer"
            ) from exc
        if index != expected_index:
            raise ValueError(
                f"{sequence_id} line {line_number}: expected index "
                f"{expected_index}, found {index}"
            )
        if value <= 0:
            raise ValueError(f"{sequence_id} line {line_number}: value must be positive")
        values.append(value)
        expected_index += 1
    if not values:
        raise ValueError(f"{sequence_id} b-file contains no terms")
    return values


def _parse_oliveira_table(
    payload: bytes,
) -> tuple[list[dict[str, int]], dict[str, object]]:
    """Extract gap-record rows marked by ``g*`` from Oliveira e Silva's table."""

    try:
        text = gzip.decompress(payload).decode("utf-8")
    except (gzip.BadGzipFile, EOFError, UnicodeDecodeError) as exc:
        raise ValueError("Oliveira table is not valid UTF-8 gzip text") from exc
    required_headers = {
        "# Test interval ---------- [2,4d18]": OLIVEIRA_TEST_LIMIT,
        "# Double test interval --- [2,4d17]": OLIVEIRA_DOUBLE_TEST_LIMIT,
    }
    for header in required_headers:
        if header not in text:
            raise ValueError(f"Oliveira table is missing coverage header: {header}")

    records: list[dict[str, int]] = []
    data_row_count = 0
    last_update = ""
    for line in text.splitlines():
        if line.startswith("# Last update made on "):
            last_update = line.removeprefix("# Last update made on ").strip()
        match = _OLIVEIRA_ROW.match(line)
        if match is None:
            continue
        data_row_count += 1
        gap = int(match.group(1))
        start_prime = int(match.group(3))
        if match.group(2) != "*":
            continue
        records.append(
            {
                "record_index": len(records) + 1,
                "start_prime": start_prime,
                "gap": gap,
                "end_prime": start_prime + gap,
            }
        )
    if not records:
        raise ValueError("Oliveira table contains no g*-marked maximal-gap records")
    for previous, current in zip(records, records[1:], strict=False):
        if current["gap"] <= previous["gap"]:
            raise ValueError("Oliveira g*-marked gaps are not strictly increasing")
        if current["start_prime"] <= previous["start_prime"]:
            raise ValueError("Oliveira g*-marked start primes are not strictly increasing")
    return records, {
        "data_row_count": data_row_count,
        "record_count": len(records),
        "last_update_text": last_update,
        "test_limit": OLIVEIRA_TEST_LIMIT,
        "double_test_limit": OLIVEIRA_DOUBLE_TEST_LIMIT,
    }


def _load_canonical_records(path: Path) -> list[dict[str, int]]:
    records: list[dict[str, int]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            records.append(
                {
                    "record_index": int(row["record_index"]),
                    "start_prime": int(row["start_prime"]),
                    "gap": int(row["gap"]),
                    "end_prime": int(row["end_prime"]),
                    "verified_exhaustive_limit": int(row["verified_exhaustive_limit"]),
                }
            )
    if not records:
        raise ValueError("canonical records file is empty")
    return records


def cross_validate_oeis(
    records_path: Path,
    raw_directory: Path,
    result_directory: Path,
    *,
    approval_token: str | None,
) -> tuple[Path, dict[str, object]]:
    """Cross-check canonical ``(start, gap, end)`` records against OEIS b-files."""

    require_experiment_approval(approval_token)
    starts_path = raw_directory / "A002386_b.txt"
    gaps_path = raw_directory / "A005250_b.txt"
    metadata_path = raw_directory / "metadata.json"
    report_path = result_directory / "cross_validation" / "oeis_cross_validation.json"
    for path in (starts_path, gaps_path, metadata_path, report_path):
        if path.exists():
            raise FileExistsError(f"refusing to overwrite independent source artifact: {path}")

    retrieved_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    starts_payload = _download(OEIS_STARTS_URL)
    gaps_payload = _download(OEIS_GAPS_URL)
    starts = _parse_oeis_bfile(starts_payload, sequence_id=OEIS_STARTS_ID)
    gaps = _parse_oeis_bfile(gaps_payload, sequence_id=OEIS_GAPS_ID)
    if len(starts) != len(gaps):
        raise RuntimeError(
            f"OEIS paired sequence lengths differ: {len(starts)} starts, {len(gaps)} gaps"
        )

    _write_bytes_exclusive(starts_path, starts_payload)
    _write_bytes_exclusive(gaps_path, gaps_payload)
    metadata: dict[str, object] = {
        "retrieved_at_utc": retrieved_at,
        "raw_immutable": True,
        "source_role": "independent public representation; computational lineage not established",
        "sequence_semantics": {
            OEIS_STARTS_ID: "lower/start primes of record gaps to the next consecutive prime",
            OEIS_GAPS_ID: "successive record prime-gap sizes",
        },
        "boundary_conversion": "end_prime = start_prime + gap",
        "files": {
            starts_path.name: {
                "sequence_id": OEIS_STARTS_ID,
                "url": OEIS_STARTS_URL,
                "byte_count": len(starts_payload),
                "sha256": _sha256_bytes(starts_payload),
                "term_count": len(starts),
            },
            gaps_path.name: {
                "sequence_id": OEIS_GAPS_ID,
                "url": OEIS_GAPS_URL,
                "byte_count": len(gaps_payload),
                "sha256": _sha256_bytes(gaps_payload),
                "term_count": len(gaps),
            },
        },
    }
    _write_json_exclusive(metadata_path, metadata)

    canonical = _load_canonical_records(records_path)
    exhaustive_limit = canonical[0]["verified_exhaustive_limit"]
    mismatches: list[dict[str, str]] = []
    if len(starts) < len(canonical):
        mismatches.append(
            {
                "code": "oeis_shorter_than_canonical",
                "oeis_term_count": str(len(starts)),
                "canonical_record_count": str(len(canonical)),
            }
        )
    comparison_count = min(len(starts), len(canonical))
    for position in range(comparison_count):
        record = canonical[position]
        oeis_start = starts[position]
        oeis_gap = gaps[position]
        oeis_end = oeis_start + oeis_gap
        expected = (
            record["start_prime"],
            record["gap"],
            record["end_prime"],
        )
        actual = (oeis_start, oeis_gap, oeis_end)
        if actual != expected:
            mismatches.append(
                {
                    "code": "record_mismatch",
                    "record_index": str(position + 1),
                    "canonical": ",".join(map(str, expected)),
                    "oeis": ",".join(map(str, actual)),
                }
            )

    extra_terms = []
    for position in range(len(canonical), len(starts)):
        start = starts[position]
        gap = gaps[position]
        extra_terms.append(
            {
                "record_index": str(position + 1),
                "start_prime": str(start),
                "gap": str(gap),
                "end_prime": str(start + gap),
                "end_above_canonical_exhaustive_limit": start + gap > exhaustive_limit,
            }
        )
    if any(not item["end_above_canonical_exhaustive_limit"] for item in extra_terms):
        mismatches.append(
            {
                "code": "oeis_extra_term_within_canonical_limit",
                "exhaustive_limit": str(exhaustive_limit),
            }
        )

    report: dict[str, object] = {
        "status": "PASS" if not mismatches else "FAIL",
        "cross_checked_at_utc": datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "canonical_records_path": str(records_path),
        "canonical_records_sha256": sha256_file(records_path),
        "canonical_record_count": len(canonical),
        "canonical_verified_exhaustive_limit": str(exhaustive_limit),
        "independent_source": "OEIS paired b-files A002386 and A005250",
        "independence_classification": (
            "independent public representation; not claimed as a fully independent "
            "exhaustive computation"
        ),
        "metadata_path": str(metadata_path),
        "metadata_sha256": sha256_file(metadata_path),
        "oeis_term_count": len(starts),
        "overlap_record_count": comparison_count,
        "matched_record_count": comparison_count
        - sum(item.get("code") == "record_mismatch" for item in mismatches),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "extra_terms_beyond_canonical_count": extra_terms,
    }
    _write_json_exclusive(report_path, report)
    if mismatches:
        raise RuntimeError(
            f"OEIS cross-validation failed with {len(mismatches)} mismatch(es); "
            f"report: {report_path}"
        )
    return report_path, report


def cross_validate_oliveira(
    records_path: Path,
    raw_directory: Path,
    result_directory: Path,
    *,
    approval_token: str | None,
) -> tuple[Path, dict[str, object]]:
    """Cross-check the canonical records against a separate exhaustive computation."""

    require_experiment_approval(approval_token)
    table_path = raw_directory / "t0.txt.gz"
    metadata_path = raw_directory / "metadata.json"
    report_path = (
        result_directory / "cross_validation" / "oliveira_cross_validation.json"
    )
    for path in (table_path, metadata_path, report_path):
        if path.exists():
            raise FileExistsError(f"refusing to overwrite independent source artifact: {path}")

    retrieved_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    table_payload = _download(OLIVEIRA_TABLE_URL)
    source_records, table_info = _parse_oliveira_table(table_payload)
    _write_bytes_exclusive(table_path, table_payload)
    metadata: dict[str, object] = {
        "retrieved_at_utc": retrieved_at,
        "raw_immutable": True,
        "source_role": (
            "official table derived from a separate exhaustive prime-gap computation"
        ),
        "source_page_url": OLIVEIRA_PAGE_URL,
        "coverage_semantics": (
            "table header states Test interval [2,4d18] and Double test interval "
            "[2,4d17]; P(g) is the lower/start prime"
        ),
        "record_marker_semantics": (
            "an asterisk immediately after g marks a maximal-gap record holder"
        ),
        "boundary_conversion": "end_prime = P(g) + g",
        "table_info": table_info,
        "files": {
            table_path.name: {
                "url": OLIVEIRA_TABLE_URL,
                "byte_count": len(table_payload),
                "sha256": _sha256_bytes(table_payload),
            }
        },
    }
    _write_json_exclusive(metadata_path, metadata)

    canonical = _load_canonical_records(records_path)
    canonical_exhaustive_limit = canonical[0]["verified_exhaustive_limit"]
    comparison_limit = min(OLIVEIRA_TEST_LIMIT, canonical_exhaustive_limit)
    canonical_overlap = [
        record for record in canonical if record["end_prime"] <= comparison_limit
    ]
    source_overlap = [
        record for record in source_records if record["end_prime"] <= comparison_limit
    ]
    mismatches: list[dict[str, str]] = []
    if len(source_overlap) != len(canonical_overlap):
        mismatches.append(
            {
                "code": "overlap_length_mismatch",
                "source_record_count": str(len(source_overlap)),
                "canonical_record_count": str(len(canonical_overlap)),
            }
        )
    comparison_count = min(len(source_overlap), len(canonical_overlap))
    matched_record_count = 0
    for position in range(comparison_count):
        source_record = source_overlap[position]
        canonical_record = canonical_overlap[position]
        expected = (
            canonical_record["start_prime"],
            canonical_record["gap"],
            canonical_record["end_prime"],
        )
        actual = (
            source_record["start_prime"],
            source_record["gap"],
            source_record["end_prime"],
        )
        if actual == expected:
            matched_record_count += 1
        else:
            mismatches.append(
                {
                    "code": "record_mismatch",
                    "record_index": str(position + 1),
                    "canonical": ",".join(map(str, expected)),
                    "oliveira": ",".join(map(str, actual)),
                }
            )

    report: dict[str, object] = {
        "status": "PASS" if not mismatches else "FAIL",
        "cross_checked_at_utc": datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "canonical_records_path": str(records_path),
        "canonical_records_sha256": sha256_file(records_path),
        "canonical_record_count": len(canonical),
        "canonical_verified_exhaustive_limit": str(canonical_exhaustive_limit),
        "independent_source": "Tomás Oliveira e Silva official t0.txt.gz table",
        "independence_classification": (
            "official table derived from a separate exhaustive computation; "
            "computed through 4e18 and stated as double-tested through 4e17"
        ),
        "source_page_url": OLIVEIRA_PAGE_URL,
        "source_table_url": OLIVEIRA_TABLE_URL,
        "source_test_limit": str(OLIVEIRA_TEST_LIMIT),
        "source_double_test_limit": str(OLIVEIRA_DOUBLE_TEST_LIMIT),
        "comparison_boundary": "end_prime <= min(source_test_limit, canonical_limit)",
        "comparison_limit": str(comparison_limit),
        "metadata_path": str(metadata_path),
        "metadata_sha256": sha256_file(metadata_path),
        "source_record_count": len(source_records),
        "overlap_record_count": comparison_count,
        "matched_record_count": matched_record_count,
        "double_tested_overlap_record_count": sum(
            record["end_prime"] <= OLIVEIRA_DOUBLE_TEST_LIMIT
            for record in source_overlap
        ),
        "canonical_records_above_source_limit": len(canonical)
        - len(canonical_overlap),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "coverage_limit_note": (
            "this independent computation does not cover the nine canonical records "
            "above 4e18; OEIS is used as a separate full-range public representation"
        ),
    }
    _write_json_exclusive(report_path, report)
    if mismatches:
        raise RuntimeError(
            f"Oliveira cross-validation failed with {len(mismatches)} mismatch(es); "
            f"report: {report_path}"
        )
    return report_path, report


__all__ = ["cross_validate_oeis", "cross_validate_oliveira"]
