from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from source.recurrence_artifact_synthesis import (
    PRIMARY_COHORT,
    PRIMARY_SCHEME,
    SynthesisError,
    build_synthesis_data,
    create_figures,
    figure_artifact_qa,
    load_contract,
)


def _statistics(
    record_index: int,
    gap: int,
    observed: int,
    expected: float,
    variance: float,
) -> dict[str, object]:
    return {
        "scheme": PRIMARY_SCHEME,
        "record_index": str(record_index),
        "start_prime": str(1_000 + record_index),
        "gap": str(gap),
        "observed_recurrences": str(observed),
        "expected_recurrences": str(expected),
        "variance": str(variance),
        "cohorts": f"all_eligible;{PRIMARY_COHORT}",
        "information_flag": "LOW_INFORMATION",
    }


def _modeled_payload(
    rows: list[dict[str, object]], observed: int, expected: float, count: int, lower: int, upper: int, kind: str
) -> dict[str, object]:
    range_key = "holdout_range" if kind == "p012b" else "gap_start_range"
    count_key = "holdout_gap_start_count" if kind == "p012b" else "gap_start_count"
    return {
        "summary": {
            range_key: {"lower_inclusive": str(lower), "upper_exclusive": str(upper)},
            count_key: count,
        },
        "cohorts": {
            "cohorts": [
                {
                    "scheme": PRIMARY_SCHEME,
                    "cohort": PRIMARY_COHORT,
                    "observed_total_recurrences": observed,
                    "expected_total_recurrences": expected,
                }
            ]
        },
        "statistics": rows,
    }


def _toy_payloads() -> tuple[dict[str, dict[str, object]], dict[str, object]]:
    p006_rows = [
        {
            "record_index": "1",
            "start_prime": "2",
            "gap": "2",
            "N": "3",
            "M": "2",
            "C": "1",
            "Q_M_over_N": "0.6666666666666666",
            "R_C_over_N_minus_1": "0.5",
        },
        {
            "record_index": "2",
            "start_prime": "11",
            "gap": "4",
            "N": "5",
            "M": "1",
            "C": "0",
            "Q_M_over_N": "0.2",
            "R_C_over_N_minus_1": "0.0",
        },
    ]
    p012a_rows = [_statistics(10, 10, 1, 0.4, 0.2), _statistics(11, 12, 0, 0.0, 0.0)]
    p012b_rows = [_statistics(20, 20, 1, 0.5, 0.25)]
    p013a_rows = [_statistics(30, 30, 0, 0.1, 0.09)]
    p013b_rows = [_statistics(40, 40, 0, 0.05, 0.0475)]
    p018_gate_a = {
        "primary_plateau_rows": 2,
        "primary_expected_recurrences_total": 0.0,
        "primary_positive_variance_rows": 0,
        "primary_low_information_rows": 2,
        "primary_low_information_fraction": 1.0,
        "hypothesis_test_performed": False,
        "recommendation": "HOLD_PREFIX_INFORMATION",
    }
    p018_gate_p0 = dict(p018_gate_a)
    p018_gate_p0.update(
        {
            "primary_plateau_rows": 1,
            "primary_low_information_rows": 1,
            "recommendation": "CALIBRATION_ONLY_NO_GATE",
        }
    )
    components = [
        {
            "scheme": PRIMARY_SCHEME,
            "record_index": 51,
            "gap": 582,
            "forced_record_removed": 1,
            "conditioned_gap_count_after_removal": 0,
            "population_after_removal": 49,
            "plateau_exposure_after_removal": 19,
            "control_exposure": 30,
            "expected_component": 0.0,
            "variance_component": 0.0,
            "information_flag": "LOW_INFORMATION",
        },
        {
            "scheme": PRIMARY_SCHEME,
            "record_index": 52,
            "gap": 588,
            "forced_record_removed": 1,
            "conditioned_gap_count_after_removal": 0,
            "population_after_removal": 49,
            "plateau_exposure_after_removal": 29,
            "control_exposure": 20,
            "expected_component": 0.0,
            "variance_component": 0.0,
            "information_flag": "LOW_INFORMATION",
        },
    ]
    payloads: dict[str, dict[str, object]] = {
        "p006_full": {"summary": {"gap_count": 10, "analysis_limit": 100}, "plateaus": p006_rows},
        "p011": {
            "analysis": {},
            "statistics": [
                {
                    "record_index": "10",
                    "observed_recurrences": "1",
                    "expected_recurrences": "4.0",
                },
                {
                    "record_index": "11",
                    "observed_recurrences": "0",
                    "expected_recurrences": "2.0",
                },
            ],
        },
        "p012a_r2": {
            "summary": {},
            "statistics": p012a_rows,
            "cohorts": {
                "cohorts": [
                    {
                        "scheme": PRIMARY_SCHEME,
                        "cohort": PRIMARY_COHORT,
                        "observed_total_recurrences": 1,
                        "expected_total_recurrences": 0.4,
                    }
                ]
            },
        },
        "p012b": _modeled_payload(p012b_rows, 1, 0.5, 20, 100, 200, "p012b"),
        "p013a_r2": _modeled_payload(p013a_rows, 0, 0.1, 30, 200, 300, "p013a"),
        "p013b": _modeled_payload(p013b_rows, 0, 0.05, 40, 300, 400, "p013b"),
        "p018p0": {
            "summary": {
                "range": {"lower_inclusive": "410", "upper_exclusive": "420"},
                "exact_gap_start_count": 5,
            },
            "plateaus": [{"record_index": 51}],
            "margin": {},
            "components": [components[0]],
            "gate": p018_gate_p0,
        },
        "p018a": {
            "summary": {
                "range": {"lower_inclusive": "400", "upper_exclusive": "500"},
                "exact_gap_start_count": 50,
            },
            "plateaus": [{"record_index": 51}, {"record_index": 52}],
            "margin": {},
            "components": components,
            "gate": p018_gate_a,
        },
    }
    contract = {
        "unique_processing_accounting": {"expected_gap_start_total": 150},
    }
    return payloads, contract


class RecurrenceArtifactSynthesisTests(unittest.TestCase):
    def test_toy_tables_preserve_roles_and_exact_accounting(self) -> None:
        payloads, contract = _toy_payloads()
        data = build_synthesis_data(payloads, contract)
        self.assertEqual(data.summary["unique_reported_gap_start_accounting"], 150)
        self.assertEqual(data.summary["development_null_correction"]["observed_total"], 1)
        self.assertAlmostEqual(
            data.summary["development_null_correction"]["p012_stratified_expected_total"],
            0.4,
        )
        self.assertEqual(len(data.tables["coverage_ranges"]), 8)
        self.assertEqual(len(data.tables["p018_forced_record_funnel"]), 2)
        for row in data.tables["p018_forced_record_funnel"]:
            self.assertNotIn("observed_recurrence", row)
            self.assertEqual(row["conditioned_gap_count_after_removal"], 0)

    def test_contract_rejects_wrong_primary_scheme(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "contract.json"
            path.write_text(
                json.dumps(
                    {
                        "contract_version": "p020-recurrence-artifact-synthesis-contract-v1",
                        "primary_scheme": "wrong",
                        "primary_cohort": PRIMARY_COHORT,
                        "input_runs": {str(i): {} for i in range(8)},
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaises(SynthesisError):
                load_contract(path)

    def test_toy_figures_decode_and_do_not_overwrite(self) -> None:
        payloads, contract = _toy_payloads()
        data = build_synthesis_data(payloads, contract)
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "figures"
            created = create_figures(data.tables, output)
            self.assertEqual(len(created), 12)
            report = figure_artifact_qa(output)
            self.assertEqual(report["status"], "PASS", report["issues"])
            with self.assertRaises(FileExistsError):
                create_figures(data.tables, output)

    def test_unique_accounting_mismatch_stops_before_plotting(self) -> None:
        payloads, contract = _toy_payloads()
        contract["unique_processing_accounting"]["expected_gap_start_total"] = 151
        with self.assertRaises(SynthesisError):
            build_synthesis_data(payloads, contract)


if __name__ == "__main__":
    unittest.main()
