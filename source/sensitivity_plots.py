"""Plots for the P004 finite-boundary and envelope sensitivity run."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from source.models import IntervalMetric, RollingEnvelopeMetric
from source.sensitivity import BoundaryPairMetric, ShiftedLogBinMetric, XWidthEnvelopeMetric


def _save(figure: plt.Figure, base_path: Path) -> list[Path]:
    paths = [base_path.with_suffix(".png"), base_path.with_suffix(".pdf")]
    for path in paths:
        if path.exists():
            plt.close(figure)
            raise FileExistsError(f"refusing to overwrite figure: {path}")
    base_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(paths[0], dpi=180, bbox_inches="tight")
    figure.savefig(paths[1], bbox_inches="tight")
    plt.close(figure)
    return paths


def _footer(figure: plt.Figure, label: str) -> None:
    figure.text(0.01, 0.01, label, fontsize=7, color="0.35")


def _trajectory(
    intervals: Sequence[IntervalMetric],
    output_directory: Path,
    *,
    provenance_label: str,
    skip_first: bool,
    y_max: float,
    filename: str,
) -> list[Path]:
    selected = list(intervals[1:] if skip_first else intervals)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    for item in selected:
        ax.plot(
            [float(item.x_left), float(item.x_right)],
            [float(item.h_left), float(item.h_interval_min)],
            color="#1f77b4",
            linewidth=1.0,
        )
    ax.scatter(
        [float(item.x_right) for item in selected],
        [float(item.h_interval_min) for item in selected],
        s=13,
        color="#d62728",
        label="interval minimum",
    )
    ax.axhline(1.0, color="#2ca02c", linestyle="--", label="H=1 reference")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(top=y_max)
    ax.set_xlabel("x (log scale)")
    ax.set_ylabel("H_end(x) = G_end(x) / F(x)")
    omission = "; first interval omitted" if skip_first else ""
    ax.set_title(f"End-bounded trajectory; y <= {y_max:g}{omission}")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8)
    _footer(fig, provenance_label)
    return _save(fig, output_directory / filename)


def plot_sensitivity_all(
    end_intervals: Sequence[IntervalMetric],
    start_intervals: Sequence[IntervalMetric],
    pairs: Sequence[BoundaryPairMetric],
    shifted_by_offset: Mapping[str, Sequence[ShiftedLogBinMetric]],
    rolling_by_window: Mapping[int, Sequence[RollingEnvelopeMetric]],
    x_width_by_decades: Mapping[str, Sequence[XWidthEnvelopeMetric]],
    output_directory: Path,
    *,
    provenance_label: str,
) -> list[Path]:
    if not end_intervals or not start_intervals or not pairs:
        raise ValueError("sensitivity plots require non-empty interval pairs")
    created: list[Path] = []
    created.extend(
        _trajectory(
            end_intervals,
            output_directory,
            provenance_label=provenance_label,
            skip_first=False,
            y_max=1e4,
            filename="h_interval_trajectory_ymax_1e4",
        )
    )
    created.extend(
        _trajectory(
            end_intervals,
            output_directory,
            provenance_label=provenance_label,
            skip_first=True,
            y_max=1e3,
            filename="h_interval_trajectory_skip_first_ymax_1e3",
        )
    )

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(
        [float(item.x_right) for item in end_intervals],
        [float(item.h_interval_min) for item in end_intervals],
        marker="o",
        markersize=2.5,
        linewidth=1,
        label="end-bounded (Sono G1)",
    )
    ax.plot(
        [float(item.x_right) for item in start_intervals],
        [float(item.h_interval_min) for item in start_intervals],
        marker=".",
        markersize=2.5,
        linewidth=1,
        label="start-bounded (FGKMT finite G)",
    )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("integer interval right endpoint x")
    ax.set_ylabel("interval minimum H")
    ax.set_title("Start/end finite-boundary comparison")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8)
    _footer(fig, provenance_label)
    created.extend(_save(fig, output_directory / "start_end_paired_interval_minima"))

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for shift, series in sorted(shifted_by_offset.items(), key=lambda item: float(item[0])):
        ax.plot(
            [float(item.minimum_x) for item in series],
            [float(item.h_bin_min) for item in series],
            marker="o",
            markersize=3,
            linewidth=1,
            label=f"shift={shift} decade",
        )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("x attaining shifted-bin minimum")
    ax.set_ylabel("shifted log-bin minimum H_end")
    ax.set_title("Shifted log10-bin sensitivity")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8)
    _footer(fig, provenance_label)
    created.extend(_save(fig, output_directory / "shifted_log10_bin_minima"))

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for window, series in sorted(rolling_by_window.items()):
        ax.plot(
            [float(item.window_x_right) for item in series],
            [float(item.h_rolling_min) for item in series],
            marker="o",
            markersize=2.2,
            linewidth=1,
            label=f"w={window} records",
        )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("trailing record-window right endpoint x")
    ax.set_ylabel("rolling local minimum H_end")
    ax.set_title("Additional record-window sensitivity")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8)
    _footer(fig, provenance_label)
    created.extend(_save(fig, output_directory / "additional_rolling_windows"))

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for width, series in sorted(x_width_by_decades.items(), key=lambda item: float(item[0])):
        full = [item for item in series if item.full_window]
        ax.plot(
            [float(item.window_x_right) for item in full],
            [float(item.h_x_width_min) for item in full],
            marker="o",
            markersize=2.2,
            linewidth=1,
            label=f"width={width} decade",
        )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("trailing x-window right endpoint")
    ax.set_ylabel("x-width local minimum H_end")
    ax.set_title("Fixed log10(x)-width trailing envelopes")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8)
    _footer(fig, provenance_label)
    created.extend(_save(fig, output_directory / "x_width_local_envelopes"))
    return created


__all__ = ["plot_sensitivity_all"]

