"""
visualizations.py
=================
All matplotlib-based chart generation for the CPU Scheduler.

Public API
----------
plot_gantt(gantt_data, title)   → matplotlib Figure
plot_comparison(comparison_df)  → matplotlib Figure
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import MaxNLocator
import numpy as np
import hashlib


# ─────────────────────────────────────────────────────────────────────────────
# Color palette — deterministic per PID so colors stay consistent
# ─────────────────────────────────────────────────────────────────────────────

_PALETTE = [
    "#4FC3F7", "#81C784", "#FFB74D", "#F06292",
    "#CE93D8", "#80DEEA", "#FFCC80", "#A5D6A7",
    "#EF9A9A", "#90CAF9", "#FFF176", "#BCAAA4",
]

def _pid_color(pid: str) -> str:
    """Assign a stable color to a PID string."""
    idx = int(hashlib.md5(pid.encode()).hexdigest(), 16) % len(_PALETTE)
    return _PALETTE[idx]


# ─────────────────────────────────────────────────────────────────────────────
# Gantt Chart
# ─────────────────────────────────────────────────────────────────────────────

def plot_gantt(gantt_data, title="Gantt Chart"):
    """
    Parameters
    ----------
    gantt_data : list of (pid, start, end) tuples
    title      : chart title string

    Returns
    -------
    matplotlib.figure.Figure
    """
    if not gantt_data:
        fig, ax = plt.subplots(figsize=(8, 2))
        ax.text(0.5, 0.5, "No data to display", ha="center", va="center",
                transform=ax.transAxes, fontsize=12, color="gray")
        ax.axis("off")
        return fig

    fig, ax = plt.subplots(figsize=(max(10, len(gantt_data) * 1.2), 3.2))
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#1E293B")

    seen_pids = {}   # pid → patch (for legend)

    for pid, start, end in gantt_data:
        color = _pid_color(pid)
        bar = ax.barh(
            y=0, width=end - start, left=start, height=0.5,
            color=color, edgecolor="#0F172A", linewidth=1.2, alpha=0.92
        )
        # Label inside bar if wide enough
        if (end - start) >= 1:
            ax.text(
                (start + end) / 2, 0,
                pid,
                ha="center", va="center",
                fontsize=9, fontweight="bold",
                color="#0F172A"
            )
        if pid not in seen_pids:
            seen_pids[pid] = mpatches.Patch(color=color, label=pid)

    # Draw time ticks below the bar
    all_times = sorted(set(t for _, s, e in gantt_data for t in (s, e)))
    for t in all_times:
        ax.axvline(x=t, color="#475569", linewidth=0.6, linestyle="--", alpha=0.6)
        ax.text(t, -0.38, str(t), ha="center", va="top",
                fontsize=7.5, color="#94A3B8")

    # Axes styling
    ax.set_xlim(left=min(s for _, s, _ in gantt_data) - 0.2,
                right=max(e for _, _, e in gantt_data) + 0.2)
    ax.set_ylim(-0.6, 0.6)
    ax.set_yticks([])
    ax.set_xlabel("Time →", color="#CBD5E1", fontsize=10, labelpad=6)
    ax.tick_params(axis="x", colors="#64748B", labelsize=0)  # hide default x-ticks
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#334155")

    # Title
    ax.set_title(title, color="#F1F5F9", fontsize=13, fontweight="bold", pad=10)

    # Legend
    legend = ax.legend(
        handles=list(seen_pids.values()),
        loc="upper right", fontsize=8,
        framealpha=0.2, labelcolor="#CBD5E1",
        facecolor="#1E293B", edgecolor="#334155"
    )

    fig.tight_layout(pad=1.2)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Algorithm Comparison Bar Chart
# ─────────────────────────────────────────────────────────────────────────────

def plot_comparison(comparison_df):
    """
    Parameters
    ----------
    comparison_df : pandas DataFrame with columns
                    ["Algorithm", "Avg WT", "Avg TAT"]

    Returns
    -------
    matplotlib.figure.Figure
    """
    if comparison_df is None or comparison_df.empty:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "Run comparison first", ha="center", va="center")
        return fig

    algorithms = comparison_df["Algorithm"].tolist()
    avg_wt  = comparison_df["Avg WT"].tolist()
    avg_tat = comparison_df["Avg TAT"].tolist()

    x      = np.arange(len(algorithms))
    width  = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#1E293B")

    bars1 = ax.bar(x - width/2, avg_wt,  width, label="Avg Waiting Time",
                   color="#4FC3F7", edgecolor="#0F172A", linewidth=0.8, alpha=0.9)
    bars2 = ax.bar(x + width/2, avg_tat, width, label="Avg Turnaround Time",
                   color="#81C784", edgecolor="#0F172A", linewidth=0.8, alpha=0.9)

    # Value labels on top of each bar
    for bar in bars1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.15,
                f"{h:.2f}", ha="center", va="bottom",
                fontsize=8, color="#4FC3F7", fontweight="bold")
    for bar in bars2:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.15,
                f"{h:.2f}", ha="center", va="bottom",
                fontsize=8, color="#81C784", fontweight="bold")

    # Highlight best algorithm (lowest Avg WT)
    best_idx = avg_wt.index(min(avg_wt))
    ax.axvspan(best_idx - 0.5, best_idx + 0.5,
               alpha=0.08, color="#F59E0B", zorder=0)
    ax.text(best_idx, max(max(avg_wt), max(avg_tat)) * 1.05,
            "★ Best", ha="center", va="bottom",
            color="#F59E0B", fontsize=9, fontweight="bold")

    # Axes styling
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms, color="#CBD5E1", fontsize=9,
                       rotation=15, ha="right")
    ax.set_ylabel("Time Units", color="#CBD5E1", fontsize=10)
    ax.set_title("Algorithm Comparison — Avg Waiting & Turnaround Time",
                 color="#F1F5F9", fontsize=13, fontweight="bold", pad=10)
    ax.tick_params(axis="y", colors="#64748B")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#334155")
    ax.spines["bottom"].set_color("#334155")
    ax.yaxis.grid(True, color="#334155", linewidth=0.5, alpha=0.7)
    ax.set_axisbelow(True)

    legend = ax.legend(
        fontsize=9, framealpha=0.2, labelcolor="#CBD5E1",
        facecolor="#1E293B", edgecolor="#334155"
    )

    fig.tight_layout(pad=1.5)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Per-Process Metrics Bar Chart (optional detailed view)
# ─────────────────────────────────────────────────────────────────────────────

def plot_process_metrics(result, title="Process Metrics"):
    """
    Horizontal grouped bar chart showing WT and TAT per process for one algorithm.
    """
    procs = result["processes"]
    if not procs:
        fig, ax = plt.subplots()
        return fig

    pids = [p["pid"] for p in procs]
    wts  = [p["wt"]  for p in procs]
    tats = [p["tat"] for p in procs]

    y     = np.arange(len(pids))
    height = 0.35

    fig, ax = plt.subplots(figsize=(8, max(3, len(pids) * 0.7 + 1.5)))
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#1E293B")

    ax.barh(y + height/2, wts,  height, label="Waiting Time",     color="#4FC3F7", alpha=0.88)
    ax.barh(y - height/2, tats, height, label="Turnaround Time",  color="#F06292", alpha=0.88)

    ax.set_yticks(y)
    ax.set_yticklabels(pids, color="#CBD5E1", fontsize=10)
    ax.set_xlabel("Time Units", color="#CBD5E1", fontsize=10)
    ax.set_title(title, color="#F1F5F9", fontsize=12, fontweight="bold", pad=8)
    ax.tick_params(axis="x", colors="#64748B")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#334155")
    ax.spines["bottom"].set_color("#334155")
    ax.xaxis.grid(True, color="#334155", linewidth=0.5, alpha=0.6)
    ax.set_axisbelow(True)

    ax.legend(fontsize=9, framealpha=0.2, labelcolor="#CBD5E1",
              facecolor="#1E293B", edgecolor="#334155")

    fig.tight_layout(pad=1.2)
    return fig
