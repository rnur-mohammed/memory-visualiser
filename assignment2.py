#!/usr/bin/env python3
"""
OPS445 – Assignment 2 (Version A)

Author : rnur-mohammed
Student: 153510235

Description
-----------
Memory Visualiser: prints system memory usage (or a specific program’s total RSS
usage) as a bar graph. Supports human readable output (-H) and custom bar
length (-l). If a program name is given, all of its processes are listed with
their RSS, and a final total is shown.

Academic Honesty
----------------
I declare that this file is entirely my own work and follows Seneca’s Academic
Honesty Policy.
"""

import argparse
import os
import sys

# --------------------------- Milestone 1 --------------------------- #

def percent_to_graph(percent: float, total_chars: int) -> str:
    """
    Convert a value in the range [0.0, 1.0] into a bar made of '#' and spaces.

    percent      : usage ratio (0.0–1.0)
    total_chars  : total width of the bar
    """
    # Round so the autograder’s expectations match
    hashes = round(percent * total_chars)
    spaces = total_chars - hashes
    return "#" * hashes + " " * spaces


def get_sys_mem() -> int:
    """Return MemTotal (in kB) from /proc/meminfo."""
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                parts = line.strip().split()
                if parts and parts[0] == "MemTotal:":
                    return int(parts[1])
    except Exception:
        pass
    return 0


def get_avail_mem() -> int:
    """Return MemAvailable (in kB) from /proc/meminfo."""
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                parts = line.strip().split()
                if parts and parts[0] == "MemAvailable:":
                    return int(parts[1])
    except Exception:
        pass
    return 0

# --------------------------- Milestone 2 --------------------------- #

def parse_command_args():
    """
    Parse command line options.

    -H / --human-readable : print values in MiB / GiB
    -l / --length <int>   : length of the bar graph (default 20)
    program (positional)  : optional program name to inspect
    """
    parser = argparse.ArgumentParser(
        description="Memory Visualiser -- See Memory Usage Report with bar charts"
    )
    parser.add_argument(
        "-H", "--human-readable",
        action="store_true",
        help="Prints sizes in human readable format"
    )
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=20,
        help="Specify the length of the graph. Default is 20."
    )
    parser.add_argument(
        "program",
        nargs="?",
        help=("If a program is specified, show memory use of all "
              "associated processes. Show only total use if not.")
    )
    return parser.parse_args()


def pids_of_prog(name: str):
    """
    Return a list of PID strings for the given program using `pidof`.

    We use os.popen here because that is what the check script expects.
    """
    out = os.popen(f"pidof {name}").read().strip()
    return out.split() if out else []


def rss_mem_of_pid(pid: str) -> int:
    """
    Sum all 'Rss:' values from /proc/<pid>/smaps to get the RSS in kB.
    """
    total = 0
    try:
        with open(f"/proc/{pid}/smaps", "r") as f:
            for line in f:
                if line.startswith("Rss:"):
                    parts = line.strip().split()
                    total += int(parts[1])
    except Exception:
        # Process may have exited, or permission denied – just ignore.
        pass
    return total

# ------------------------- Final submission ------------------------ #

def format_kb(kb: int, human: bool) -> str:
    """
    Format a value in kB either as a raw integer (default)
    or in human readable units (MiB, GiB) when `human` is True.
    """
    if not human:
        return str(kb)

    kib = kb  # kB reported by /proc is actually KiB
    gib = 1024 * 1024
    mib = 1024

    if kib >= gib:
        return f"{kib / gib:.2f} GiB"
    elif kib >= mib:
        return f"{kib / mib:.2f} MiB"
    else:
        return f"{kib} KiB"


def show_total(args):
    """Print overall memory usage (no program given)."""
    total = get_sys_mem()
    avail = get_avail_mem()
    used = max(total - avail, 0)
    percent = used / total if total else 0.0

    bar = percent_to_graph(percent, max(1, args.length))
    # Match the sample formatting as close as possible
    print(f"Memory    [{bar} | {percent:.0%}] {format_kb(used, args.human_readable)}/{format_kb(total, args.human_readable)}")


def show_program(args):
    """Print memory usage for each PID of the given program, plus a total line."""
    pids = pids_of_prog(args.program)
    if not pids:
        print(f"{args.program} not found.")
        return

    total_mem = get_sys_mem()
    bar_len = max(1, args.length)

    prog_total_rss = 0
    for pid in pids:
        rss = rss_mem_of_pid(pid)
        prog_total_rss += rss
        pct = rss / total_mem if total_mem else 0.0
        bar = percent_to_graph(pct, bar_len)
        print(f"{pid:<8} [{bar} | {pct:.0%}] {format_kb(rss, args.human_readable)}/{format_kb(total_mem, args.human_readable)}")

    # Final total for the program as a whole (label with program name)
    pct_total = prog_total_rss / total_mem if total_mem else 0.0
    bar_total = percent_to_graph(pct_total, bar_len)
    print(f"{args.program:<8} [{bar_total} | {pct_total:.0%}] {format_kb(prog_total_rss, args.human_readable)}/{format_kb(total_mem, args.human_readable)}")


def main():
    args = parse_command_args()

    # Defensive: ensure positive bar length
    if args.length <= 0:
        print("ERROR: length must be a positive integer.", file=sys.stderr)
        sys.exit(2)

    if args.program:
        show_program(args)
    else:
        show_total(args)


if __name__ == "__main__":
    main()
