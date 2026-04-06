"""
app.py
======
Advanced CPU Scheduling Simulator — Streamlit Frontend
=====================================================
Run with:  streamlit run app.py

Author  : CPU Scheduler Project
Version : 1.0.0
"""

import random
import streamlit as st
import pandas as pd

from algorithms import (
    fcfs, sjf_non_preemptive, sjf_preemptive,
    round_robin, priority_non_preemptive,
    ALGORITHM_REGISTRY,
)
from visualizations import plot_gantt, plot_comparison, plot_process_metrics
from export_utils   import results_to_csv, comparison_to_csv, results_to_txt


# ─────────────────────────────────────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="CPU Scheduling Simulator",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────────────────────────────────────
# Global CSS — dark theme, custom typography, card styling
# ─────────────────────────────────────────────────────────────────────────────

CUSTOM_CSS = """
<style>
/* ── Google Fonts ──────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

/* ── Root token overrides ──────────────────────────────────────────── */
:root {
    --bg-base   : #0B1120;
    --bg-surface: #131D2E;
    --bg-card   : #1A2640;
    --accent-1  : #38BDF8;
    --accent-2  : #34D399;
    --accent-3  : #FBBF24;
    --text-primary  : #F0F6FF;
    --text-secondary: #8BA3C3;
    --border    : #243046;
}

/* ── Global ─────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
}

/* ── Sidebar ─────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0D1B2A 0%, #0F2440 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* ── Headers ─────────────────────────────────────────────────────────── */
h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif !important; }

/* ── Metric cards ─────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 14px 18px !important;
}
[data-testid="stMetricValue"] {
    color: var(--accent-1) !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

/* ── DataFrame table ─────────────────────────────────────────────────── */
[data-testid="stDataFrame"] { border-radius: 10px !important; overflow: hidden; }

/* ── Buttons ─────────────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #1E3A5F 0%, #0E2238 100%) !important;
    color: var(--accent-1) !important;
    border: 1px solid var(--accent-1) !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: var(--accent-1) !important;
    color: #0B1120 !important;
    box-shadow: 0 0 14px rgba(56,189,248,0.4) !important;
}

/* ── Inputs & selects ─────────────────────────────────────────────────── */
input, select, textarea, [data-baseweb="input"] input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ── Tabs ─────────────────────────────────────────────────────────────── */
[data-testid="stTabs"] button {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--accent-1) !important;
    border-bottom-color: var(--accent-1) !important;
}

/* ── Expander ─────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

/* ── Hero banner ─────────────────────────────────────────────────────── */
.hero-banner {
    background: linear-gradient(120deg, #0B1E38 0%, #0F2A50 50%, #0A1E35 100%);
    border: 1px solid #1D3254;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(56,189,248,0.15) 0%, transparent 70%);
}
.hero-banner h1 {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #38BDF8, #34D399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.hero-banner p {
    color: #8BA3C3;
    font-size: 0.95rem;
    margin: 0;
}

/* ── Badge ─────────────────────────────────────────────────────────── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.badge-blue  { background: rgba(56,189,248,0.15); color: #38BDF8; border: 1px solid rgba(56,189,248,0.3); }
.badge-green { background: rgba(52,211,153,0.15); color: #34D399; border: 1px solid rgba(52,211,153,0.3); }
.badge-gold  { background: rgba(251,191,36,0.15);  color: #FBBF24; border: 1px solid rgba(251,191,36,0.3); }

/* ── Section label ─────────────────────────────────────────────────── */
.section-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #38BDF8;
    border-bottom: 1px solid #1D3254;
    padding-bottom: 6px;
    margin-bottom: 14px;
}

/* ── Info callout ─────────────────────────────────────────────────── */
.info-callout {
    background: rgba(56,189,248,0.07);
    border-left: 3px solid #38BDF8;
    border-radius: 0 8px 8px 0;
    padding: 10px 16px;
    font-size: 0.88rem;
    color: #8BA3C3;
    margin: 10px 0;
}

/* ── Best highlight row ─────────────────────────────────────────────── */
.best-row { color: #FBBF24 !important; font-weight: 700 !important; }

/* ── scrollbar ──────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-surface); }
::-webkit-scrollbar-thumb { background: #243046; border-radius: 3px; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Session State Initialisation
# ─────────────────────────────────────────────────────────────────────────────

def _init_state():
    defaults = {
        "processes": [
            {"pid": "P1", "arrival": 0, "burst": 6, "priority": 2},
            {"pid": "P2", "arrival": 2, "burst": 4, "priority": 1},
            {"pid": "P3", "arrival": 4, "burst": 2, "priority": 3},
            {"pid": "P4", "arrival": 6, "burst": 5, "priority": 2},
        ],
        "quantum": 2,
        "last_result": None,
        "last_algo":   None,
        "comparison":  None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _validate_processes(procs):
    """Return (ok: bool, error_message: str)."""
    if not procs:
        return False, "Please add at least one process."
    pids = [p["pid"].strip() for p in procs]
    if len(pids) != len(set(pids)):
        return False, "Duplicate Process IDs found. Each PID must be unique."
    for p in procs:
        if not p["pid"].strip():
            return False, "Process ID cannot be empty."
        if p["arrival"] < 0:
            return False, f"{p['pid']}: Arrival time cannot be negative."
        if p["burst"] <= 0:
            return False, f"{p['pid']}: Burst time must be > 0."
        if p["priority"] < 1:
            return False, f"{p['pid']}: Priority must be ≥ 1."
    return True, ""


def _result_to_df(result):
    rows = []
    for p in result["processes"]:
        rows.append({
            "PID":             p["pid"],
            "Arrival":         p["arrival"],
            "Burst":           p["burst"],
            "Priority":        p.get("priority", "—"),
            "Completion (CT)": p["completion"],
            "TAT":             p["tat"],
            "WT":              p["wt"],
            "RT":              p["rt"],
        })
    return pd.DataFrame(rows)


def _run_algorithm(algo_name, procs, quantum=2):
    fn = ALGORITHM_REGISTRY[algo_name]
    if algo_name == "Round Robin":
        return fn(procs, quantum=quantum)
    return fn(procs)


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar — Process Management
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        '<div class="section-label">⚙️ Process Manager</div>',
        unsafe_allow_html=True
    )

    # ── Add process form ──────────────────────────────────────────────────
    with st.expander("➕  Add New Process", expanded=False):
        c1, c2 = st.columns(2)
        new_pid      = c1.text_input("Process ID", value="", key="np_pid",
                                      placeholder="P5")
        new_arrival  = c1.number_input("Arrival Time", min_value=0, value=0,
                                        key="np_arrival")
        new_burst    = c2.number_input("Burst Time",   min_value=1, value=3,
                                        key="np_burst")
        new_priority = c2.number_input("Priority",     min_value=1, value=1,
                                        key="np_priority")
        if st.button("Add Process", use_container_width=True):
            pid = new_pid.strip().upper()
            if not pid:
                st.error("Process ID is required.")
            elif any(p["pid"] == pid for p in st.session_state.processes):
                st.error(f"'{pid}' already exists.")
            else:
                st.session_state.processes.append({
                    "pid": pid, "arrival": new_arrival,
                    "burst": new_burst, "priority": new_priority
                })
                st.success(f"Process {pid} added!")
                st.rerun()

    # ── Random generation ─────────────────────────────────────────────────
    with st.expander("🎲  Random Generator", expanded=False):
        n_rand = st.slider("Number of Processes", 3, 10, 5, key="n_rand")
        if st.button("Generate Random Processes", use_container_width=True):
            st.session_state.processes = []
            for i in range(1, n_rand + 1):
                st.session_state.processes.append({
                    "pid":      f"P{i}",
                    "arrival":  random.randint(0, 10),
                    "burst":    random.randint(1, 12),
                    "priority": random.randint(1, 5),
                })
            st.success(f"{n_rand} processes generated.")
            st.rerun()

    st.divider()

    # ── Process list (editable) ───────────────────────────────────────────
    st.markdown('<div class="section-label">Current Processes</div>', unsafe_allow_html=True)

    remove_idx = None
    for i, proc in enumerate(st.session_state.processes):
        col_pid, col_at, col_bt, col_pr, col_rm = st.columns([2, 2, 2, 2, 1])
        proc["pid"]      = col_pid.text_input("ID", value=proc["pid"],
                                               key=f"pid_{i}", label_visibility="collapsed")
        proc["arrival"]  = col_at.number_input("AT",  value=proc["arrival"],
                                                min_value=0, key=f"at_{i}",
                                                label_visibility="collapsed")
        proc["burst"]    = col_bt.number_input("BT",  value=proc["burst"],
                                                min_value=1, key=f"bt_{i}",
                                                label_visibility="collapsed")
        proc["priority"] = col_pr.number_input("PR",  value=proc["priority"],
                                                min_value=1, key=f"pr_{i}",
                                                label_visibility="collapsed")
        if col_rm.button("✕", key=f"rm_{i}", help=f"Remove {proc['pid']}"):
            remove_idx = i

    if remove_idx is not None:
        st.session_state.processes.pop(remove_idx)
        st.rerun()

    st.divider()

    # ── Algorithm config ──────────────────────────────────────────────────
    st.markdown('<div class="section-label">⚙️ Algorithm Config</div>', unsafe_allow_html=True)

    selected_algo = st.selectbox(
        "Algorithm",
        list(ALGORITHM_REGISTRY.keys()),
        key="selected_algo"
    )

    if selected_algo == "Round Robin":
        st.session_state.quantum = st.slider(
            "Time Quantum", min_value=1, max_value=10,
            value=st.session_state.quantum
        )

    st.divider()

    if st.button("🗑️  Reset All", use_container_width=True):
        for key in ["processes", "last_result", "last_algo", "comparison", "quantum"]:
            if key in st.session_state:
                del st.session_state[key]
        _init_state()
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# Main Content
# ─────────────────────────────────────────────────────────────────────────────

# Hero banner
st.markdown("""
<div class="hero-banner">
  <h1>⚙️ CPU Scheduling Simulator</h1>
  <p>Visualise & analyse FCFS · SJF · SRTF · Round Robin · Priority scheduling algorithms in real-time.</p>
</div>
""", unsafe_allow_html=True)

# Quick stats strip
procs = st.session_state.processes
q1, q2, q3, q4 = st.columns(4)
q1.metric("Processes Loaded",  len(procs))
q2.metric("Selected Algorithm", st.session_state.get("selected_algo", "—"))
q3.metric("Time Quantum (RR)",  st.session_state.quantum)
q4.metric("Avg Burst Time",
          f"{(sum(p['burst'] for p in procs)/len(procs)):.1f}" if procs else "—")

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_sim, tab_compare, tab_export = st.tabs([
    "🖥️  Simulator",
    "📊  Comparison Mode",
    "📥  Export Results",
])


# ═══════════════════════════════════════════════════════════════════════════
# TAB 1 — SIMULATOR
# ═══════════════════════════════════════════════════════════════════════════

with tab_sim:
    ok, err = _validate_processes(st.session_state.processes)
    if not ok:
        st.error(f"⚠️  {err}")
    else:
        run_col, _ = st.columns([1, 4])
        if run_col.button("▶  Run Simulation", use_container_width=True, type="primary"):
            with st.spinner("Simulating…"):
                result = _run_algorithm(
                    st.session_state.selected_algo,
                    st.session_state.processes,
                    st.session_state.quantum,
                )
                st.session_state.last_result = result
                st.session_state.last_algo   = st.session_state.selected_algo

    result    = st.session_state.last_result
    algo_name = st.session_state.last_algo

    if result:
        st.markdown(
            f'<div class="section-label">Results — {algo_name}</div>',
            unsafe_allow_html=True
        )

        # ── Key metrics ──────────────────────────────────────────────────
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Avg Waiting Time",      f"{result['avg_wt']:.2f}")
        m2.metric("Avg Turnaround Time",   f"{result['avg_tat']:.2f}")
        m3.metric("Processes Completed",   len(result["processes"]))
        total_time = (max(p["completion"] for p in result["processes"])
                      - min(p["arrival"]  for p in result["processes"]))
        m4.metric("Total Span", f"{total_time} units")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Gantt chart ──────────────────────────────────────────────────
        st.markdown(
            '<div class="section-label">Gantt Chart</div>',
            unsafe_allow_html=True
        )
        fig_gantt = plot_gantt(result["gantt"], title=f"Gantt — {algo_name}")
        st.pyplot(fig_gantt, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Results table ─────────────────────────────────────────────────
        st.markdown(
            '<div class="section-label">Process Metrics Table</div>',
            unsafe_allow_html=True
        )
        df = _result_to_df(result)
        st.dataframe(
            df.style
              .highlight_max(subset=["TAT", "WT"], color="#2D1515")
              .highlight_min(subset=["TAT", "WT"], color="#152D1F")
              .format(precision=0),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown(
            '<div class="info-callout">'
            '🟢 Green = best (lowest) value &nbsp;|&nbsp; 🔴 Red = worst (highest) value'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Per-process bar chart ─────────────────────────────────────────
        st.markdown(
            '<div class="section-label">Per-Process WT & TAT</div>',
            unsafe_allow_html=True
        )
        fig_proc = plot_process_metrics(result, title=f"WT & TAT — {algo_name}")
        st.pyplot(fig_proc, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# TAB 2 — COMPARISON MODE
# ═══════════════════════════════════════════════════════════════════════════

with tab_compare:
    ok, err = _validate_processes(st.session_state.processes)
    if not ok:
        st.error(f"⚠️  {err}")
    else:
        cmp_col, _ = st.columns([1, 4])
        if cmp_col.button("🔄  Run All Algorithms", use_container_width=True, type="primary"):
            with st.spinner("Running all algorithms…"):
                rows = []
                for name in ALGORITHM_REGISTRY:
                    res = _run_algorithm(name, st.session_state.processes,
                                         st.session_state.quantum)
                    rows.append({
                        "Algorithm": name,
                        "Avg WT":   round(res["avg_wt"], 3),
                        "Avg TAT":  round(res["avg_tat"], 3),
                    })
                st.session_state.comparison = pd.DataFrame(rows)

    cmp = st.session_state.comparison
    if cmp is not None:
        best_wt  = cmp["Avg WT"].idxmin()
        best_tat = cmp["Avg TAT"].idxmin()

        st.markdown(
            '<div class="section-label">Comparison Table</div>',
            unsafe_allow_html=True
        )

        # Format DF with highlighting
        styled = (
            cmp.style
               .highlight_min(subset=["Avg WT", "Avg TAT"], color="#152D1F")
               .highlight_max(subset=["Avg WT", "Avg TAT"], color="#2D1515")
               .format({"Avg WT": "{:.3f}", "Avg TAT": "{:.3f}"})
        )
        st.dataframe(styled, use_container_width=True, hide_index=True)

        best_algo = cmp.loc[best_wt, "Algorithm"]
        st.markdown(
            f'<div style="background:rgba(251,191,36,0.08);border:1px solid rgba(251,191,36,0.3);'
            f'border-radius:10px;padding:12px 18px;margin-top:10px;">'
            f'⭐ <strong style="color:#FBBF24">Best Algorithm</strong> by lowest Avg Waiting Time: '
            f'<span class="badge badge-gold">{best_algo}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Comparison bar chart ──────────────────────────────────────────
        st.markdown(
            '<div class="section-label">Comparison Chart</div>',
            unsafe_allow_html=True
        )
        fig_cmp = plot_comparison(cmp)
        st.pyplot(fig_cmp, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Gantt charts for each algorithm ──────────────────────────────
        with st.expander("🗂️  View Gantt Charts for All Algorithms", expanded=False):
            for name in ALGORITHM_REGISTRY:
                res = _run_algorithm(name, st.session_state.processes,
                                      st.session_state.quantum)
                st.markdown(f"**{name}**")
                fig = plot_gantt(res["gantt"], title=name)
                st.pyplot(fig, use_container_width=True)
                st.markdown("<br>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# TAB 3 — EXPORT
# ═══════════════════════════════════════════════════════════════════════════

with tab_export:
    st.markdown(
        '<div class="section-label">📥 Export Results</div>',
        unsafe_allow_html=True
    )

    result    = st.session_state.last_result
    algo_name = st.session_state.last_algo
    cmp       = st.session_state.comparison

    if result is None and cmp is None:
        st.info("Run a simulation or comparison first to enable exports.")
    else:
        e1, e2, e3, e4 = st.columns(4)

        if result:
            csv_bytes = results_to_csv(result, algo_name)
            e1.download_button(
                "⬇️  Download CSV (Single)",
                data=csv_bytes,
                file_name=f"cpu_schedule_{algo_name.replace(' ','_')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

            txt_content = results_to_txt(result, algo_name)
            e2.download_button(
                "⬇️  Download TXT Report",
                data=txt_content,
                file_name=f"cpu_schedule_{algo_name.replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True,
            )

            # Preview
            st.markdown(
                '<div class="section-label">Text Report Preview</div>',
                unsafe_allow_html=True
            )
            st.code(txt_content, language="text")

        if cmp is not None:
            cmp_csv = comparison_to_csv(cmp)
            e3.download_button(
                "⬇️  Download Comparison CSV",
                data=cmp_csv,
                file_name="cpu_comparison.csv",
                mime="text/csv",
                use_container_width=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="info-callout">'
        '💡 CSV exports are compatible with Excel, Google Sheets, and any spreadsheet software.'
        '</div>',
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    '<hr style="border-color:#1D3254; margin: 0;">'
    '<div style="text-align:center;padding:14px;color:#4A6285;font-size:0.78rem;">'
    'Advanced CPU Scheduling Simulator &nbsp;·&nbsp; '
    'Built with Python + Streamlit &nbsp;·&nbsp; '
    'Operating Systems Lab Project'
    '</div>',
    unsafe_allow_html=True,
)
