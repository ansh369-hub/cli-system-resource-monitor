# System Resource Monitor

A lightweight CLI-based system resource monitor that displays real-time CPU, memory, and disk usage along with the top running processes.

## Features

- **Real-time System Metrics** - Live CPU, RAM, and disk usage with color-coded indicators
- **Process Monitoring** - Track top 20 processes by CPU or memory consumption
- **Dynamic Sorting** - Toggle between CPU and memory sorting with ascending/descending order
- **Color-Coded Display** - Green (good), yellow (warning), red (critical) for quick visual feedback
- **Minimal Dependencies** - Uses only `psutil` and `rich` libraries

## Requirements

- Python 3.7+
- Windows, macOS, or Linux

## Installation

1. Clone or download this project
2. Install required dependencies:
   ```bash
   pip install psutil rich
   ```

## Usage

Run the monitor:
```bash
python monitor.py
```

### Keyboard Controls

While the monitor is running, use

- **`Ctrl+C`** - Exit the monitor


## Example Output

```
attached the output screenshots

```

## Notes

- The monitor refreshes every 1 second to reduce flickering and CPU overhead

- The application requires administrator/root privileges to access information for all processes
