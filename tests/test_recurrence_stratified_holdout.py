from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np

from source.plateau_recurrence import RecordReference
from source.provenance import ApprovalRequiredError
from source.recurrence_stratified_holdout import (
    EXPECTED_COMPLETE_RECORD_INDICES,
    _derive_plateau_counts,
    iter_prime_chunks_range,
    run_holdout,
    select_complete_holdout_plateaus,
    validate_inputs,
)
from source.recurrence_stratified_null import (
    BIN_SCHEMES,
    accumulate_bin_counts,
    build_components,
)


ROOT = Path(__file__).resolve().parents[1]
RECORDS = (
    ROOT
    / "datas"
    / "validated"
    / "prime-gap-list-project"
    / "1a112a1387052d9ad360686313f501c01fe46b68"
    / "maximal_gap_records.csv"
)
CONTRACT = ROOT / "test_plan" / "P012_statistical_contract_v1.json"


def _reference(index: int, start: int, gap: int, coverage: int = 1_000) -> RecordReference:
    return RecordReference(
        record_index=index,
        start_prime=start,
        gap=gap,
        end_prime=start + gap,
        source_commit="toy",
        verified_exhaustive_limit=coverage,
    )


class RecurrenceStratifiedHoldoutTests(unittest.TestCase):
    def test_range_sieve_includes_one_right_boundary_prime(self) -> None:
        chunks = list(iter_prime_chunks_range(100, 200, segment_span=23))
        observed = np.concatenate(chunks).tolist()
        expected_inside = [
            value
            for value in range(100, 200)
            if value >= 2
            and all(value % divisor for divisor in range(2, int(value**0.5) + 1))
        ]
        self.assertEqual(observed[:-1], expected_inside)
        self.assertEqual(observed[-1], 211)
        self.assertGreaterEqual(observed[-1], 200)

    def test_complete_plateau_selection_excludes_both_censored_edges(self) -> None:
        references = [
            _reference(0, 89, 8),
            _reference(1, 101, 2),
            _reference(2, 103, 4),
            _reference(3, 109, 18),
            _reference(4, 211, 20),
        ]
        selected = select_complete_holdout_plateaus(
            references,
            lower_inclusive=100,
            upper_exclusive=200,
        )
        self.assertEqual([row["record_index"] for row in selected], [1, 2])
        self.assertEqual(selected[0]["right_exclusive"], 103)
        self.assertEqual(selected[1]["right_exclusive"], 109)

    def test_toy_counts_remove_one_forced_record_per_plateau(self) -> None:
        references = [
            _reference(0, 89, 8),
            _reference(1, 101, 2),
            _reference(2, 103, 4),
            _reference(3, 109, 18),
            _reference(4, 211, 20),
        ]
        provisional = select_complete_holdout_plateaus(
            references,
            lower_inclusive=100,
            upper_exclusive=200,
        )
        prime_chunks = list(iter_prime_chunks_range(100, 200, segment_span=23))
        accumulated = accumulate_bin_counts(prime_chunks, provisional)
        plateaus = _derive_plateau_counts(provisional, accumulated)
        components = build_components(plateaus, accumulated)
        self.assertEqual([(row["N"], row["M"], row["C"]) for row in plateaus], [(1, 1, 0), (2, 1, 0)])
        for scheme in BIN_SCHEMES:
            for plateau in plateaus:
                selected = [
                    row
                    for row in components
                    if row["scheme"] == scheme.name
                    and row["record_index"] == plateau["record_index"]
                ]
                self.assertEqual(
                    sum(int(row["forced_record_removed"]) for row in selected), 1
                )
                self.assertEqual(
                    sum(int(row["plateau_exposure_after_removal"]) for row in selected),
                    plateau["N"] - 1,
                )

    def test_preflight_reads_only_pinned_contract_and_record_metadata(self) -> None:
        report = validate_inputs(RECORDS, CONTRACT, segment_span=50_000_000)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(
            tuple(report["selected_record_indices"]), EXPECTED_COMPLETE_RECORD_INDICES
        )
        self.assertFalse(report["holdout_prime_stream_read"])
        self.assertFalse(report["actual_experiment_executed"])

    def test_actual_run_refuses_before_input_read_or_output_write(self) -> None:
        with tempfile.TemporaryDirectory(
            dir=ROOT / "tmp", prefix="p012b-approval-test-"
        ) as directory:
            output = Path(directory) / "result"
            with self.assertRaises(ApprovalRequiredError):
                run_holdout(
                    Path(directory) / "missing-records.csv",
                    Path(directory) / "missing-contract.json",
                    output,
                    approval_token=None,
                )
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
