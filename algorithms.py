"""
algorithms.py
=============
CPU Scheduling Algorithms — pure logic, no UI dependencies.
Each function accepts a list of process dicts and returns a results dict.

Process dict schema:
    {
        "pid": str,          # Process ID e.g. "P1"
        "arrival": int,      # Arrival time
        "burst": int,        # CPU burst time
        "priority": int      # Lower number = higher priority (for Priority Scheduling)
    }

Result dict schema returned by each algorithm:
    {
        "gantt": [(pid, start, end), ...],    # Gantt chart segments
        "processes": [                         # Per-process metrics
            {
                "pid", "arrival", "burst", "priority",
                "completion", "tat", "wt", "rt"
            }, ...
        ],
        "avg_wt":  float,
        "avg_tat": float,
    }
"""

import copy


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _sort_by_arrival(processes):
    """Return a new list sorted by arrival time (ties broken by original order)."""
    return sorted(processes, key=lambda p: p["arrival"])


def _compute_averages(results):
    """Attach avg_wt and avg_tat to a results dict (in-place) and return it."""
    n = len(results["processes"])
    if n == 0:
        results["avg_wt"] = 0.0
        results["avg_tat"] = 0.0
        return results
    results["avg_wt"]  = sum(p["wt"]  for p in results["processes"]) / n
    results["avg_tat"] = sum(p["tat"] for p in results["processes"]) / n
    return results


# ─────────────────────────────────────────────────────────────────────────────
# 1. FCFS — First Come First Serve
# ─────────────────────────────────────────────────────────────────────────────

def fcfs(processes):
    """
    Non-preemptive. Processes are served in arrival order.
    Ties in arrival time are broken by the order they appear in the input list.
    """
    procs = _sort_by_arrival(copy.deepcopy(processes))
    gantt   = []
    results = []
    time    = 0

    for p in procs:
        # CPU may be idle while waiting for the first arriving process
        if time < p["arrival"]:
            time = p["arrival"]

        start      = time
        completion = time + p["burst"]
        tat        = completion - p["arrival"]
        wt         = tat - p["burst"]
        rt         = start - p["arrival"]   # First time on CPU

        gantt.append((p["pid"], start, completion))

        results.append({
            **p,
            "completion": completion,
            "tat": tat,
            "wt":  wt,
            "rt":  rt,
        })
        time = completion

    return _compute_averages({"gantt": gantt, "processes": results})


# ─────────────────────────────────────────────────────────────────────────────
# 2. SJF — Non-Preemptive (Shortest Job First)
# ─────────────────────────────────────────────────────────────────────────────

def sjf_non_preemptive(processes):
    """
    At each CPU-free moment pick the arrived process with the shortest burst.
    Once a process starts, it runs to completion.
    """
    procs     = copy.deepcopy(processes)
    n         = len(procs)
    done      = [False] * n
    gantt     = []
    results   = []
    time      = 0
    completed = 0

    # Track response time (first time process gets CPU)
    rt_map = {}

    while completed < n:
        # Collect processes that have arrived and are not yet done
        available = [
            i for i in range(n)
            if not done[i] and procs[i]["arrival"] <= time
        ]

        if not available:
            # CPU idle — jump to the next arrival
            next_arrival = min(procs[i]["arrival"] for i in range(n) if not done[i])
            time = next_arrival
            continue

        # Pick shortest burst; tie-break by arrival, then by list order
        idx = min(available, key=lambda i: (procs[i]["burst"], procs[i]["arrival"]))
        p   = procs[idx]

        start      = time
        completion = time + p["burst"]
        tat        = completion - p["arrival"]
        wt         = tat - p["burst"]
        rt         = start - p["arrival"]

        gantt.append((p["pid"], start, completion))
        results.append({
            **p,
            "completion": completion,
            "tat": tat,
            "wt":  wt,
            "rt":  rt,
        })

        done[idx] = True
        completed += 1
        time = completion

    return _compute_averages({"gantt": gantt, "processes": results})


# ─────────────────────────────────────────────────────────────────────────────
# 3. SRTF — Shortest Remaining Time First (Preemptive SJF)
# ─────────────────────────────────────────────────────────────────────────────

def sjf_preemptive(processes):
    """
    Preemptive version of SJF. At every time unit, the process with the
    shortest *remaining* burst is selected. If a new process arrives with a
    shorter remaining burst than the running process, it preempts it.
    """
    procs      = copy.deepcopy(processes)
    n          = len(procs)
    remaining  = {p["pid"]: p["burst"] for p in procs}
    completed  = 0
    time       = 0
    gantt      = []          # raw (pid, tick) pairs — compressed later
    start_map  = {}          # pid → first time on CPU  (response time base)
    finish_map = {}          # pid → completion time
    last_pid   = None
    seg_start  = 0

    # Total simulation ticks = until all processes complete
    max_time = sum(p["burst"] for p in procs) + max(p["arrival"] for p in procs) + 1

    while completed < n and time <= max_time:
        available = [
            p for p in procs
            if p["arrival"] <= time and remaining[p["pid"]] > 0
        ]

        if not available:
            # Flush any open Gantt segment
            if last_pid is not None:
                gantt.append((last_pid, seg_start, time))
                last_pid = None
            time += 1
            continue

        # Select process with smallest remaining burst
        current = min(available, key=lambda p: (remaining[p["pid"]], p["arrival"]))
        pid     = current["pid"]

        # Record first CPU access for response time
        if pid not in start_map:
            start_map[pid] = time

        # Gantt segment tracking
        if pid != last_pid:
            if last_pid is not None:
                gantt.append((last_pid, seg_start, time))
            seg_start = time
            last_pid  = pid

        remaining[pid] -= 1
        time += 1

        # Check completion
        if remaining[pid] == 0:
            finish_map[pid] = time
            completed += 1

    # Close last Gantt segment
    if last_pid is not None:
        gantt.append((last_pid, seg_start, time))

    # Build per-process results
    results = []
    pid_map = {p["pid"]: p for p in procs}
    for pid, p in pid_map.items():
        completion = finish_map[pid]
        tat        = completion - p["arrival"]
        wt         = tat - p["burst"]
        rt         = start_map[pid] - p["arrival"]
        results.append({
            **p,
            "completion": completion,
            "tat": tat,
            "wt":  wt,
            "rt":  rt,
        })

    # Sort results by completion order for cleaner display
    results.sort(key=lambda x: x["completion"])

    return _compute_averages({"gantt": gantt, "processes": results})


# ─────────────────────────────────────────────────────────────────────────────
# 4. Round Robin
# ─────────────────────────────────────────────────────────────────────────────

def round_robin(processes, quantum=2):
    """
    Circular queue. Each process gets at most `quantum` time units per turn.
    New arrivals and preempted processes are added to the rear of the queue.
    """
    procs     = _sort_by_arrival(copy.deepcopy(processes))
    n         = len(procs)
    remaining = {p["pid"]: p["burst"] for p in procs}
    arrived   = {p["pid"]: p["arrival"] for p in procs}
    queue     = []        # Ready queue (pids)
    gantt     = []
    results   = {}
    start_map = {}        # pid → first CPU access

    time      = 0
    idx       = 0         # Pointer into sorted arrival list

    # Seed with processes that arrive at time 0
    while idx < n and procs[idx]["arrival"] <= time:
        queue.append(procs[idx]["pid"])
        idx += 1

    while queue:
        pid = queue.pop(0)

        # CPU may still be behind the next arrival
        proc_arrival = arrived[pid]
        if time < proc_arrival:
            time = proc_arrival

        # Record first time on CPU
        if pid not in start_map:
            start_map[pid] = time

        run_time   = min(quantum, remaining[pid])
        seg_start  = time
        time      += run_time
        remaining[pid] -= run_time

        gantt.append((pid, seg_start, time))

        # Enqueue newly arrived processes (arrived during this slice)
        while idx < n and procs[idx]["arrival"] <= time:
            queue.append(procs[idx]["pid"])
            idx += 1

        if remaining[pid] > 0:
            # Process not finished — re-enqueue at rear
            queue.append(pid)
        else:
            # Process finished
            pid_obj = next(p for p in procs if p["pid"] == pid)
            completion = time
            tat = completion - pid_obj["arrival"]
            wt  = tat - pid_obj["burst"]
            rt  = start_map[pid] - pid_obj["arrival"]
            results[pid] = {
                **pid_obj,
                "completion": completion,
                "tat": tat,
                "wt":  wt,
                "rt":  rt,
            }

        # If queue is empty but processes remain (CPU idle gap)
        if not queue and idx < n:
            time = procs[idx]["arrival"]
            queue.append(procs[idx]["pid"])
            idx += 1

    result_list = [results[p["pid"]] for p in procs if p["pid"] in results]
    return _compute_averages({"gantt": gantt, "processes": result_list})


# ─────────────────────────────────────────────────────────────────────────────
# 5. Priority Scheduling (Non-Preemptive)
# ─────────────────────────────────────────────────────────────────────────────

def priority_non_preemptive(processes):
    """
    Non-preemptive Priority scheduling.
    Lower `priority` number = higher priority (1 is highest).
    Ties in priority broken by arrival time, then list order.
    """
    procs     = copy.deepcopy(processes)
    n         = len(procs)
    done      = [False] * n
    gantt     = []
    results   = []
    time      = 0
    completed = 0

    while completed < n:
        available = [
            i for i in range(n)
            if not done[i] and procs[i]["arrival"] <= time
        ]

        if not available:
            next_arrival = min(procs[i]["arrival"] for i in range(n) if not done[i])
            time = next_arrival
            continue

        # Pick highest priority (lowest number); tie → arrival → index
        idx = min(available, key=lambda i: (
            procs[i]["priority"], procs[i]["arrival"], i
        ))
        p = procs[idx]

        start      = time
        completion = time + p["burst"]
        tat        = completion - p["arrival"]
        wt         = tat - p["burst"]
        rt         = start - p["arrival"]

        gantt.append((p["pid"], start, completion))
        results.append({
            **p,
            "completion": completion,
            "tat": tat,
            "wt":  wt,
            "rt":  rt,
        })

        done[idx] = True
        completed += 1
        time = completion

    return _compute_averages({"gantt": gantt, "processes": results})


# ─────────────────────────────────────────────────────────────────────────────
# Registry — easy lookup by name
# ─────────────────────────────────────────────────────────────────────────────

ALGORITHM_REGISTRY = {
    "FCFS":                   fcfs,
    "SJF (Non-Preemptive)":   sjf_non_preemptive,
    "SRTF (Preemptive SJF)":  sjf_preemptive,
    "Round Robin":             round_robin,
    "Priority (Non-Preemptive)": priority_non_preemptive,
}
