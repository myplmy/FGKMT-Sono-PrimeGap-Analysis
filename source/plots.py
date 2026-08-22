"""Publication-oriented plots for the end-bounded FGKMT analysis."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from source.models import IntervalMetric, JumpMetric


def _save_figure_exclusive(figure: plt.Figure, base_path: Path) -> list[Path]:
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


def _provenance_footer(figure: plt.Figure, provenance_label: str) -> None:
    figure.text(0.01, 0.01, provenance_label, fontsize=7, color="0.35")


def plot_all(
    intervals: Sequence[IntervalMetric],
    jumps: Sequence[JumpMetric],
    output_directory: Path,
    *,
    provenance_label: str,
) -> list[Path]:
    """Generate five core plots and the optional jump plot as PNG and PDF."""

    if not intervals:
        raise ValueError("at least one interval is required for plotting")

    x_left = np.array([float(item.x_left) for item in intervals])
    x_right = np.array([float(item.x_right) for item in intervals])
    log10_right = np.log10(x_right)
    h_left = np.array([float(item.h_left) for item in intervals])
    h_min = np.array([float(item.h_interval_min) for item in intervals])
    running = np.array([float(item.running_min) for item in intervals])
    sono_ratio = np.array([float(item.sono_ratio_min) for item in intervals])
    cramer_ratio = np.array([float(item.cramer_ratio_min) for item in intervals])
    created: list[Path] = []

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for left, right, left_h, right_h in zip(
        x_left, x_right, h_left, h_min, strict=True
    ):
        ax.plot([left, right], [left_h, right_h], color="#1f77b4", linewidth=1.0)
    ax.scatter(x_right, h_min, s=13, color="#d62728", label="interval minimum")
    ax.axhline(1.0, color="#2ca02c", linestyle="--", label="Wolf empirical reference H=1")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("x (log scale)")
    ax.set_ylabel("H(x) = G(x) / F(x)")
    ax.set_title("End-bounded maximal-gap normalization")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8)
    _provenance_footer(fig, provenance_label)
    created.extend(_save_figure_exclusive(fig, output_directory / "h_interval_trajectory"))

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(log10_right, np.log10(h_min), marker="o", markersize=3, linewidth=1)
    ax.set_xlabel("log10(x) at interval right endpoint")
    ax.set_ylabel("log10(interval minimum H)")
    ax.set_title("FGKMT-normalized interval minima")
    ax.grid(True, alpha=0.3)
    _provenance_footer(fig, provenance_label)
    created.extend(_save_figure_exclusive(fig, output_directory / "log_h_interval_min"))

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.step(x_right, running, where="post", color="#d62728")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("x (log scale)")
    ax.set_ylabel("running minimum M(x)")
    ax.set_title("Empirical global lower envelope (monotone non-increasing)")
    ax.grid(True, which="both", alpha=0.25)
    _provenance_footer(fig, provenance_label)
    created.extend(_save_figure_exclusive(fig, output_directory / "running_minimum"))

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(x_right, sono_ratio, marker="o", markersize=3, linewidth=1)
    ax.axhline(1.0, color="#9467bd", linestyle=":", label="Sono ratio = 1")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("x (log scale)")
    ax.set_ylabel("interval minimum H / (2e-17)")
    ax.set_title("Distance from Sono's explicit constant")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8)
    _provenance_footer(fig, provenance_label)
    created.extend(_save_figure_exclusive(fig, output_directory / "sono_ratio"))

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(x_right, cramer_ratio, marker="o", markersize=3, linewidth=1)
    ax.set_xscale("log")
    ax.set_xlabel("x (log scale)")
    ax.set_ylabel("gap / ln(x)^2 at interval right endpoint")
    ax.set_title("Auxiliary Cramer-scale normalization")
    ax.grid(True, which="both", alpha=0.25)
    _provenance_footer(fig, provenance_label)
    created.extend(_save_figure_exclusive(fig, output_directory / "cramer_ratio"))

    if jumps:
        jump_x = np.array([float(item.jump_x) for item in jumps])
        before = np.array([float(item.h_before_jump) for item in jumps])
        after = np.array([float(item.h_after_jump) for item in jumps])
        fig, ax = plt.subplots(figsize=(9, 5.5))
        for x_value, before_h, after_h in zip(jump_x, before, after, strict=True):
            ax.plot([x_value, x_value], [before_h, after_h], color="0.65", linewidth=0.8)
        ax.scatter(jump_x, before, s=15, label="immediately before record", color="#d62728")
        ax.scatter(jump_x, after, s=15, label="at new record", color="#1f77b4")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("record jump x (log scale)")
        ax.set_ylabel("H(x)")
        ax.set_title("Decline and recovery at maximal-gap records")
        ax.grid(True, which="both", alpha=0.25)
        ax.legend(fontsize=8)
        _provenance_footer(fig, provenance_label)
        created.extend(_save_figure_exclusive(fig, output_directory / "record_jump_recovery"))

    return created


__all__ = ["plot_all"]
