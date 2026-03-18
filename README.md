# System Resource Monitor

A lightweight CLI-based system resource monitor that displays real-time CPU, memory, and disk usage along with the top running processes.

## Task Description

The objective of this CLI application is to provide a lightweight and practical way to monitor system health directly from the terminal. The tool is designed to show both high-level resource usage and detailed process-level information in real time.

## Implementation Overview

The application runs in a loop and refreshes the dashboard every second. It first collects system-wide metrics such as CPU utilization, RAM usage, disk usage, and CPU frequency. It then gathers process data including PID, process status, CPU percentage, memory percentage, memory usage in MB, thread count, and process name. After collecting this information, the program formats it into a structured dashboard using Rich panels, progress bars, and tables.

The implementation is organized into small helper functions for tasks such as:

- choosing colors for CPU usage levels
- styling process states
- formatting memory values
- building metric panels and progress bars
- collecting and ranking processes
- rendering the dashboard output

This structure keeps the code readable, modular, and easier to maintain.

## Design Decisions

Several design decisions were made to keep the application effective and user-friendly:

- `psutil` was selected because it offers reliable, cross-platform access to system and process statistics.
- `rich` was used to improve terminal presentation through color, tables, borders, and progress bars, making the output easier to read at a glance.
- The program is divided into focused helper functions instead of putting all logic into one loop, which improves maintainability and makes future enhancements easier.
- Process collection is limited to a fixed number of processes and only the top entries are displayed, which helps keep the interface responsive and avoids overwhelming the user with too much data.
- Color-coded output is used to make important information stand out quickly, especially for CPU load and process states.


## Features

- **Real-time System Metrics** - Live CPU, RAM, and disk usage with color-coded indicators
- **Process Monitoring** - Track top 20 processes by CPU or memory consumption
- **Color-Coded Display** - Green (good), yellow (warning), red (critical) for quick visual feedback
- **Minimal Dependencies** - Uses only `psutil` and `rich` libraries

## Requirements

- Python 3.7 or higher
- `psutil`
- `rich`

## Installation

1. Clone or download this project
2. Install required dependencies:
   ```bash
   pip install psutil rich
   ```

## Run the Application

```bash
python monitor.py
```

## Output

When the program runs, it shows:

- a resource summary panel for CPU, memory, and disk usage
- a ranked table of the top processes
- a live timestamp showing the latest refresh time

Press `Ctrl+C` to stop the monitor.

## Notes

- The monitor refreshes every 1 second to reduce flickering and CPU overhead

- The application requires administrator/root privileges to access information for all processes
