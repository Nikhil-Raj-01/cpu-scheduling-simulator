"""
export_utils.py
===============
Utilities to export scheduling results to CSV and TXT formats.
"""

import csv
import io
import datetime


def results_to_csv(result, algo_name="Algorithm"):
    """
    Convert a single algorithm result to CSV bytes.

    Returns
    -------
    bytes  — UTF-8 encoded CSV content
    """
    output = io.StringIO()
    writer = csv.writer(output)

    # Header metadata
    writer.writerow([f"CPU Scheduling Simulator — {algo_name}"])
    writer.writerow([f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
    writer.writerow([])

    # Column headers
    writer.writerow([
        "Process ID", "Arrival Time", "Burst Time", "Priority",
        "Completion Time", "Turnaround Time", "Waiting Time", "Response Time"
    ])

    for p in result["processes"]:
        writer.writerow([
            p["pid"], p["arrival"], p["burst"], p.get("priority", "N/A"),
            p["completion"], p["tat"], p["wt"], p["rt"]
        ])

    writer.writerow([])
    writer.writerow(["Average Waiting Time",    "", "", "", "", "", f"{result['avg_wt']:.2f}"])
    writer.writerow(["Average Turnaround Time", "", "", "", "", "", "", f"{result['avg_tat']:.2f}"])

    return output.getvalue().encode("utf-8")


def comparison_to_csv(comparison_df):
    """
    Convert comparison DataFrame to CSV bytes.
    """
    return comparison_df.to_csv(index=False).encode("utf-8")


def results_to_txt(result, algo_name="Algorithm"):
    """
    Human-readable text report for a single algorithm result.

    Returns
    -------
    str
    """
    lines = []
    sep   = "=" * 65

    lines.append(sep)
    lines.append(f"  CPU SCHEDULING SIMULATOR — {algo_name.upper()}")
    lines.append(f"  Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(sep)
    lines.append("")

    # Table header
    header = (
        f"{'PID':<6} {'Arrival':>8} {'Burst':>7} {'Priority':>9} "
        f"{'CT':>6} {'TAT':>6} {'WT':>6} {'RT':>6}"
    )
    lines.append(header)
    lines.append("-" * 65)

    for p in result["processes"]:
        lines.append(
            f"{p['pid']:<6} {p['arrival']:>8} {p['burst']:>7} "
            f"{str(p.get('priority','N/A')):>9} "
            f"{p['completion']:>6} {p['tat']:>6} {p['wt']:>6} {p['rt']:>6}"
        )

    lines.append("-" * 65)
    lines.append(f"{'Average Waiting Time':50} {result['avg_wt']:.2f}")
    lines.append(f"{'Average Turnaround Time':50} {result['avg_tat']:.2f}")
    lines.append(sep)

    # Gantt chart (ASCII representation)
    lines.append("")
    lines.append("GANTT CHART")
    lines.append("-" * 65)

    gantt_line = ""
    time_line  = ""
    for pid, start, end in result.get("gantt", []):
        width     = max(len(pid) + 2, end - start, 4)
        gantt_line += f"| {pid.center(width - 2)} "
        time_line  += str(start).ljust(width)
    gantt_line += "|"

    if result.get("gantt"):
        last = result["gantt"][-1]
        time_line += str(last[2])

    lines.append(gantt_line)
    lines.append(time_line)
    lines.append("")

    return "\n".join(lines)
