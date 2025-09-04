# Memory Visualiser (OPS445 Assignment 2)

A Python CLI tool that visualises **system memory usage** and optionally shows memory usage of specific programs. The program prints results as bar graphs, supports human-readable units, and allows configurable bar lengths.

## ✨ Features
- Show overall system memory usage.
- Display usage for specific programs (all PIDs + total).
- Bar graph visualisation with adjustable length (`-l`).
- Human-readable output (`-H` → MiB / GiB).
- Defensive error handling (invalid options, no program found).

## 🚀 Usage
Run from the command line:

```bash
# Show overall memory usage
python3 assignment2.py

# Show usage in human readable units
python3 assignment2.py -H

# Show usage with a custom bar length
python3 assignment2.py -l 40

# Show memory usage of a specific program (e.g. firefox)
python3 assignment2.py firefox

# Combine options
python3 assignment2.py -H -l 50 firefox



Example output:
Memory    [######               | 28%] 2162200/7782796
1952     [#                    | 6%] 487836/7782796
firefox  [#                    | 6%] 487836/7782796
