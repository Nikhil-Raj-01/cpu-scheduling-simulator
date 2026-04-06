# ⚙️ Advanced CPU Scheduling Simulator

A professional, interactive CPU Scheduling Simulator built with Python + Streamlit.
Implements FCFS, SJF (NP), SRTF, Round Robin, and Priority Scheduling with
Gantt charts, performance metrics, algorithm comparison, and CSV/TXT export.

---

## 🚀 Quick Start

### Step 1 — Install Python (if not installed)
Download Python 3.10 or newer from: https://www.python.org/downloads/
Make sure to check **"Add Python to PATH"** during installation.

### Step 2 — Install Dependencies

Open a terminal (Command Prompt / PowerShell / Terminal) in the project folder:

```bash
pip install -r requirements.txt
```

This installs: `streamlit`, `matplotlib`, `pandas`, `numpy`

### Step 3 — Run the App

```bash
streamlit run app.py
```

Your browser will automatically open at `http://localhost:8501`

---

## 📁 Project Files

| File | Description |
|------|-------------|
| `app.py` | Main Streamlit application (UI layer) |
| `algorithms.py` | All 5 CPU scheduling algorithm implementations |
| `visualizations.py` | Gantt charts and comparison bar charts (matplotlib) |
| `export_utils.py` | CSV and TXT export functionality |
| `requirements.txt` | Python package dependencies |
| `PROJECT_REPORT.md` | Full project report (ready to submit) |
| `VIVA_QA.md` | 17 viva questions with detailed answers |

---

## 🎯 Features

- ✅ **5 Scheduling Algorithms:** FCFS, SJF (NP), SRTF (Preemptive SJF), Round Robin, Priority
- ✅ **Dynamic Process Input:** Add/remove processes; random generation
- ✅ **Input Validation:** No negative values, duplicate PIDs caught
- ✅ **Gantt Chart Visualisation:** Colour-coded, timestamped, dark-themed
- ✅ **Performance Metrics:** CT, TAT, WT, RT per process + averages
- ✅ **Algorithm Comparison Mode:** All algorithms on same dataset, best highlighted
- ✅ **Comparison Bar Chart:** Side-by-side Avg WT and Avg TAT
- ✅ **Export:** CSV and TXT download buttons
- ✅ **Professional Dark UI:** Custom CSS, modern typography

---

## 🖥️ Usage Guide

### Adding Processes
- Use the **sidebar → Add New Process** expander
- Fill in PID, Arrival Time, Burst Time, Priority
- Click **Add Process**

### Random Generation
- Use **sidebar → Random Generator**
- Choose number of processes (3–10)
- Click **Generate Random Processes**

### Running a Simulation
1. Select an algorithm from the **Algorithm** dropdown in the sidebar
2. If Round Robin, set the **Time Quantum** slider
3. Go to the **Simulator** tab
4. Click **▶ Run Simulation**

### Comparing Algorithms
1. Go to the **Comparison Mode** tab
2. Click **🔄 Run All Algorithms**
3. View the comparison table, best algorithm highlight, and bar chart

### Exporting Results
1. Run a simulation first
2. Go to the **Export Results** tab
3. Click the download button for CSV or TXT format

---

## 🔧 Troubleshooting

**"streamlit: command not found"**
```bash
python -m streamlit run app.py
```

**Port already in use**
```bash
streamlit run app.py --server.port 8502
```

**ModuleNotFoundError**
```bash
pip install --upgrade -r requirements.txt
```

---

## 📊 Algorithms Implemented

| Algorithm | Type | Key Characteristic |
|-----------|------|-------------------|
| FCFS | Non-Preemptive | Arrival order; simple but convoy effect |
| SJF | Non-Preemptive | Shortest burst first; optimal avg WT |
| SRTF | Preemptive | Shortest remaining time; globally optimal |
| Round Robin | Preemptive | Fixed quantum; fair, good response time |
| Priority | Non-Preemptive | Priority number (lower = higher); starvation risk |

---

*B.Tech 4th Semester — Operating Systems Mini Project*
