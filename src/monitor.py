import os
import time

import psutil
from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table

console = Console()
SORT_BY_CPU = True
PROCESS_LIMIT = 200
TOP_N = 20


def get_cpu_color(cpu_percent):
    if cpu_percent < 50:
        return "green"
    if cpu_percent < 70:
        return "yellow"
    return "red"


def get_status_style(status):
    styles = {
        "running": "green",
        "sleeping": "blue",
        "stopped": "red",
        "zombie": "red dim",
    }
    return styles.get(status.lower(), "white")


def format_gb(value_in_bytes):
    return value_in_bytes / (1024 ** 3)


def build_progress_bar(label, value, color, value_text=None):
    progress = Progress(
        TextColumn(f"[bold white]{label:<4}[/bold white]"),
        BarColumn(
            bar_width=30,
            complete_style=f"bold {color}",
            finished_style=f"bold {color}",
            pulse_style=f"{color} dim",
        ),
        TextColumn(f"[bold {color}]{value_text or f'{value:>5.1f}%'}[/bold {color}]"),
        expand=False
    )
    progress.add_task("", completed=value, total=100)
    return progress


def build_metric_panel(label, value, color, value_text=None):
    return Panel.fit(
        build_progress_bar(label, value, color, value_text),
        border_style=color,
        padding=(0, 1),
    )


def read_process_info(process):
    try:
        with process.oneshot():
            cpu_p = process.cpu_percent(None) / max(psutil.cpu_count() or 1, 1)
            mem_pct = process.memory_percent()
            mem_mb = process.memory_info().rss / (1024 * 1024)
            return {
                "pid": process.pid,
                "status": process.status(),
                "cpu": cpu_p,
                "mem_pct": mem_pct, 
                "mem_mb": mem_mb,
                "threads": process.num_threads(),
                "name": process.name()[:25],
            }
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def build_resource_panel():
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    cpu_freq = psutil.cpu_freq()

    cpu_speed_ghz = (cpu_freq.current / 1000) if cpu_freq else 0
    used_ram_gb = format_gb(mem.used)
    total_ram_gb = format_gb(mem.total)

    cpu_bar = build_metric_panel("CPU", cpu, get_cpu_color(cpu), f"{cpu:.0f}% ({cpu_speed_ghz:.2f} GHz)")
    mem_bar = build_metric_panel("RAM", mem.percent, "cyan", f"{used_ram_gb:.1f}/{total_ram_gb:.1f} GB ({mem.percent:.0f}%)")
    disk_bar = build_metric_panel("Disk", disk.percent, "magenta")

    return Panel(
        Columns([cpu_bar, mem_bar, disk_bar], align="center", padding=(0, 4), expand=True),
        title="[bold bright_blue] System Resource Monitor[/bold bright_blue]",
        subtitle="[dim]Live CPU, memory, and disk usage[/dim]",
        border_style="bright_blue",
        padding=(1, 3),
    )


def collect_processes():
    processes = []
    for pid in psutil.pids()[-PROCESS_LIMIT:]:
        try:
            process = psutil.Process(pid)
            process.cpu_percent(None)
            processes.append(process)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    time.sleep(0.1)

    ranked_processes = []
    for process in processes:
        info = read_process_info(process)
        if not info:
            continue

        score = info["cpu"] if SORT_BY_CPU else info["mem_pct"]
        ranked_processes.append((info, score))

    return sorted(ranked_processes, key=lambda item: item[1], reverse=True)[:TOP_N]


def build_process_table(processes):
    table = Table(
        title=f"[bold] Top {TOP_N} Processes[/bold] [dim](Sorted by {'CPU' if SORT_BY_CPU else 'Memory'})[/dim]",
        box=box.SIMPLE_HEAVY,
        header_style="bold bright_white on dark_blue",
        show_header=True,
        show_edge=False,
        pad_edge=False,
        row_styles=["none", "dim"],
    )

    table.add_column("PID", style="cyan bold", justify="right", min_width=8)
    table.add_column("Status", style="yellow", justify="center", min_width=8)
    table.add_column("CPU %", style="green", justify="right", min_width=6)
    table.add_column("MEM %", style="magenta", justify="right", min_width=6)
    table.add_column("Threads", style="blue", justify="right", min_width=7)
    table.add_column("MEM (MB)", style="red", justify="right", min_width=9)
    table.add_column("Process Name", style="white bold", min_width=15)

    for info, _ in processes:
        status_style = get_status_style(info["status"])
        table.add_row(
            f"[cyan]{info['pid']}[/cyan]",
            f"[{status_style}]{info['status']}[/{status_style}]",
            f"[green]{info['cpu']:.1f}[/green]",
            f"[magenta]{info['mem_pct']:.1f}[/magenta]",
            f"[blue]{info['threads']}[/blue]",
            f"[red]{info['mem_mb']:.0f}[/red]",
            f"[white bold]{info['name']}[/white bold]",
        )

    return table


def render_dashboard():
    clear_screen()

    console.print()
    with console.status("[bold green]Monitoring system resources...[/bold green]", spinner="dots"):
        console.print(build_resource_panel())

    top_processes = collect_processes()
    table = build_process_table(top_processes)

    console.print()
    console.print(table)
    console.print(
        f"\n[dim]Last updated:[/dim] [bold green]{time.strftime('%H:%M:%S')}[/bold green] "
        f"[dim]| Press Ctrl+C to exit[/dim]\n"
    )


def main():
    try:
        while True:
            render_dashboard()
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[dim]Monitor stopped.[/dim]")


if __name__ == "__main__":
    main()
