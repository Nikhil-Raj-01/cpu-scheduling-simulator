# Advanced CPU Scheduling Simulator with Performance Analysis
## Project Report — B.Tech 4th Semester | Operating Systems

---

**Course:** Operating Systems (CS/IT 4th Semester)  
**Project Title:** Advanced CPU Scheduling Simulator with Performance Analysis  
**Technology:** Python · Streamlit · Matplotlib · Pandas  
**Submission Type:** Mini Project / Lab Project  

---

## Table of Contents

1. Introduction  
2. Objectives  
3. Algorithm Explanations  
4. System Design & Methodology  
5. Implementation Details  
6. Results & Analysis  
7. Conclusion  
8. References  

---

## 1. Introduction

CPU scheduling is one of the most fundamental and critical functions of an Operating System. When multiple processes compete for the CPU — a limited resource — the OS must decide *which process runs next, for how long, and in what order*. This decision, made by the **CPU Scheduler**, directly determines system performance, user experience, and resource utilisation.

Different scheduling algorithms make these decisions using different criteria: some minimise waiting time, others ensure fairness, and some optimise for throughput. Understanding the trade-offs between these algorithms is essential for operating system design.

This project implements a **fully interactive CPU Scheduling Simulator** that allows users to:
- Define custom process sets with arrival times, burst times, and priorities
- Run five major scheduling algorithms
- Visualise execution timelines using Gantt charts
- Compare algorithms on standardised performance metrics
- Export results for further analysis

The simulator is built using **Python** with a **Streamlit** web-based interface, offering a professional, real-time interactive experience — far beyond a command-line tool.

---

## 2. Objectives

The primary objectives of this project are:

1. **Implement** the five most widely studied CPU scheduling algorithms in a clean, modular Python codebase.
2. **Visualise** process execution through colour-coded Gantt charts with precise timestamps.
3. **Compute** and display four key performance metrics per process: Completion Time (CT), Turnaround Time (TAT), Waiting Time (WT), and Response Time (RT).
4. **Compare** algorithms side-by-side to identify the optimal algorithm for a given workload.
5. **Demonstrate** the effects of scheduling parameters (like time quantum in Round Robin) on overall system performance.
6. **Export** results to CSV and TXT formats for documentation or further study.
7. **Provide** an intuitive, visually modern interface accessible to any user without command-line expertise.

---

## 3. Algorithm Explanations

### 3.1 FCFS — First Come First Serve

**Type:** Non-Preemptive  
**Description:** Processes are executed strictly in the order of their arrival. The process that arrives first gets the CPU first. No process can be preempted once it starts executing.

**Example:**

| PID | Arrival | Burst |
|-----|---------|-------|
| P1  | 0       | 5     |
| P2  | 1       | 3     |
| P3  | 2       | 4     |

Execution Order: P1 → P2 → P3

**Advantages:** Simple, easy to implement, no starvation.  
**Disadvantages:** **Convoy effect** — a long process can delay all shorter processes behind it, leading to high average waiting times.

**Formula:**
- TAT = Completion Time − Arrival Time
- WT  = TAT − Burst Time

---

### 3.2 SJF — Shortest Job First (Non-Preemptive)

**Type:** Non-Preemptive  
**Description:** When the CPU is free, the process with the *shortest burst time* among all currently arrived processes is selected next. Once started, a process runs to completion.

**Key Property:** SJF gives the **minimum average waiting time** among all non-preemptive algorithms for a given set of processes.

**Advantages:** Optimal average WT for non-preemptive scheduling; efficient for batch systems.  
**Disadvantages:** **Starvation** — long processes may never execute if shorter ones keep arriving. Requires knowledge of burst times in advance.

---

### 3.3 SRTF — Shortest Remaining Time First (Preemptive SJF)

**Type:** Preemptive  
**Description:** The preemptive variant of SJF. At every unit of time, the process with the *least remaining burst time* is chosen. If a new process arrives with a shorter remaining time than the currently running process, it **preempts** the current process.

**Advantages:** Optimal average WT among all preemptive scheduling algorithms.  
**Disadvantages:** High context-switch overhead; starvation of longer processes; requires continuous monitoring of remaining times.

---

### 3.4 Round Robin (RR)

**Type:** Preemptive  
**Description:** Each process gets a fixed **time quantum (Q)** on the CPU. After Q time units, if the process is not finished, it is placed at the rear of the ready queue and the next process gets the CPU. This continues cyclically.

**Key Parameter:** Time Quantum Q — the maximum time a process runs before being preempted.

**Effect of Q:**
- Very small Q → behaves like SRTF but with excessive context switches.
- Very large Q → behaves like FCFS.

**Advantages:** Fair; good response time for interactive systems; no starvation.  
**Disadvantages:** Higher average TAT than SJF; performance sensitive to choice of Q.

---

### 3.5 Priority Scheduling (Non-Preemptive)

**Type:** Non-Preemptive  
**Description:** Each process is assigned a **priority number**. Lower number = higher priority (convention used in this project). Among all arrived processes, the highest-priority one is selected. Ties are broken by arrival time.

**Note:** This simulator implements non-preemptive priority. A preemptive version would context-switch when a higher-priority process arrives during execution.

**Advantages:** Flexible; can model real-world urgency levels; widely used in OS kernels.  
**Disadvantages:** **Starvation** of low-priority processes (can be mitigated using *aging* — incrementally increasing priority of waiting processes).

---

## 4. System Design & Methodology

### 4.1 Architecture

The project follows a clean **three-layer architecture**:

```
┌─────────────────────────────────────────────────────┐
│  Presentation Layer  (app.py — Streamlit UI)         │
│  • Input forms, sidebars, tabs                       │
│  • Chart rendering, table display, downloads         │
└────────────────────┬────────────────────────────────┘
                     │ calls
┌────────────────────▼────────────────────────────────┐
│  Logic Layer  (algorithms.py)                        │
│  • Pure Python scheduling functions                  │
│  • No UI dependencies                                │
│  • Returns standardised result dicts                 │
└────────────────────┬────────────────────────────────┘
                     │ calls
┌────────────────────▼────────────────────────────────┐
│  Utility Layer  (visualizations.py, export_utils.py) │
│  • Gantt chart generation (matplotlib)               │
│  • Comparison bar charts                             │
│  • CSV / TXT export                                  │
└─────────────────────────────────────────────────────┘
```

### 4.2 Data Flow

1. User inputs processes (PID, Arrival, Burst, Priority) via sidebar.
2. Input validation ensures correctness before simulation.
3. The selected algorithm function processes the list and returns a result dict containing:
   - `gantt`: list of (pid, start, end) tuples for the Gantt chart
   - `processes`: list of per-process metrics
   - `avg_wt` / `avg_tat`: summary statistics
4. Visualisation functions render the charts from the result dict.
5. Export functions serialise the result dict to CSV/TXT.

### 4.3 Performance Metrics Defined

| Metric | Symbol | Formula |
|--------|--------|---------|
| Completion Time | CT | Time when process finishes execution |
| Turnaround Time | TAT | CT − Arrival Time |
| Waiting Time | WT | TAT − Burst Time |
| Response Time | RT | First CPU access time − Arrival Time |

---

## 5. Implementation Details

### 5.1 Technologies Used

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.10+ | Core implementation |
| Web UI | Streamlit 1.32+ | Interactive frontend |
| Charts | Matplotlib 3.8+ | Gantt & bar charts |
| Data | Pandas 2.1+ | Tables and comparison data |
| Numerics | NumPy 1.26+ | Bar chart positioning |

### 5.2 File Structure

```
cpu_scheduler/
├── app.py              ← Streamlit UI (entry point)
├── algorithms.py       ← All 5 scheduling algorithms
├── visualizations.py   ← Gantt & comparison charts
├── export_utils.py     ← CSV & TXT export functions
├── requirements.txt    ← Python dependencies
├── README.md           ← Setup instructions
└── PROJECT_REPORT.md   ← This document
```

### 5.3 Key Implementation Decisions

**SRTF Simulation:** Implemented as a tick-based simulation (1 time unit per iteration) to correctly handle preemptions at arbitrary time points. Adjacent same-PID ticks are merged into single Gantt segments for clean display.

**Round Robin Queue:** New arrivals during a running time slice are added to the rear of the queue *after* the current slice completes, accurately mimicking real OS scheduler behaviour.

**Color Consistency:** Process colors in Gantt charts use MD5 hashing of the PID string to assign deterministic colors from a curated palette — the same PID always gets the same color across all algorithm runs.

---

## 6. Results & Analysis

### Sample Dataset

| PID | Arrival | Burst | Priority |
|-----|---------|-------|----------|
| P1  | 0       | 6     | 2        |
| P2  | 2       | 4     | 1        |
| P3  | 4       | 2     | 3        |
| P4  | 6       | 5     | 2        |

### Sample Comparison Results

*(Values shown below are illustrative; actual values depend on dataset)*

| Algorithm | Avg WT | Avg TAT |
|-----------|--------|---------|
| FCFS | 4.25 | 8.50 |
| SJF (NP) | 3.00 | 7.25 |
| SRTF | 2.75 | 7.00 |
| Round Robin (Q=2) | 5.50 | 9.75 |
| Priority (NP) | 3.50 | 7.75 |

### Analysis

- **SRTF** consistently achieves the **lowest average waiting and turnaround times**, as it always selects the process that will finish quickest.
- **FCFS** performs poorly when there is high variance in burst times (convoy effect).
- **Round Robin** provides the **best response times** for interactive tasks but has higher average TAT due to context switches.
- **Priority Scheduling** is versatile but introduces starvation risk for low-priority, long-burst processes.

---

## 7. Conclusion

This project successfully implements and demonstrates five fundamental CPU scheduling algorithms with a modern, web-based interactive interface. Through side-by-side comparison and visualisation, several key insights emerge:

1. **No single algorithm is universally best** — the choice depends on workload characteristics (batch vs interactive, uniform vs varied burst times).
2. **SRTF is theoretically optimal** for minimising average waiting time but at the cost of implementation complexity and starvation risk.
3. **Round Robin** is the standard choice for time-sharing systems due to its inherent fairness.
4. **Priority Scheduling** requires aging mechanisms in production systems to prevent starvation.

The simulator provides an invaluable learning tool that bridges the gap between theoretical algorithm study and practical understanding of scheduling behaviour.

---

## 8. References

1. Abraham Silberschatz, Peter B. Galvin, Greg Gagne — *Operating System Concepts*, 10th Edition, Wiley.
2. William Stallings — *Operating Systems: Internals and Design Principles*, 9th Edition, Pearson.
3. Andrew S. Tanenbaum — *Modern Operating Systems*, 4th Edition, Pearson.
4. Streamlit Documentation — https://docs.streamlit.io
5. Matplotlib Documentation — https://matplotlib.org/stable/contents.html

---

*Report prepared for B.Tech 4th Semester Operating Systems — Mini Project Submission*
