import subprocess
from pathlib import Path
import time
import re
import sys

import yaml
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

base = Path(".")
SLOW_THRESHOLD = 30.0

console = Console()

failed_runs = []
timeout_runs = []
pylint_scores = []  # (mod_name, score_as_float)
missing_files = []  # list of dicts: year, day, module, path
results = []  # per-module run results, for YAML


def run_cmd(cmd, timeout=None):
    try:
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as e:
        return e


# ----- Year argument handling -----
if len(sys.argv) > 1:
    try:
        only_year = int(sys.argv[1])
    except ValueError:
        console.print(f"[red]Invalid year argument:[/red] {sys.argv[1]}")
        sys.exit(1)
    years = [only_year]
else:
    years = list(range(2015, 2025))

total_start = time.monotonic()

# ----- Main Loop with progress -----
total_days = len(years) * 25

with Progress() as progress:
    task = progress.add_task("[cyan]Running solutions[/cyan]", total=total_days)

    for year in years:
        for day in range(1, 26):
            file_name = base / f"{year:04d}" / f"{day}" / "solution.py"
            mod_name = f"{year}.{day}.solution"

            progress.advance(task)

            result_entry = {
                "module": mod_name,
                "year": year,
                "day": day,
                "status": "not_run",
                "elapsed_seconds": None,
                "return_code": None,
                "pylint_score": None,
            }
            results.append(result_entry)

            if not file_name.exists():
                console.print(f"[yellow]Missing:[/yellow] {file_name}")
                missing_files.append(
                    {
                        "year": year,
                        "day": day,
                        "module": mod_name,
                        "path": str(file_name),
                    }
                )
                result_entry["status"] = "missing"
                continue

            console.rule(f"[bold magenta]{mod_name}[/bold magenta]")

            # ---- Ruff format ----
            console.print("• [blue]Formatting with ruff...[/blue]")
            fmt_cmd = ["uv", "run", "ruff", "format", str(file_name)]
            run_cmd(fmt_cmd)

            # ---- Run the solution with a hard timeout ----
            console.print("• [blue]Running solution...[/blue]")
            run_cmd_list = ["uv", "run", "python", "-m", mod_name]

            start = time.monotonic()
            result = run_cmd(run_cmd_list, timeout=SLOW_THRESHOLD)
            elapsed = time.monotonic() - start

            if isinstance(result, subprocess.TimeoutExpired):
                console.print(
                    f"[red]TIMEOUT:[/red] {mod_name} exceeded {SLOW_THRESHOLD}s"
                )
                timeout_runs.append(mod_name)
                result_entry["status"] = "timeout"
                result_entry["elapsed_seconds"] = None
                result_entry["return_code"] = None
                continue

            result_entry["elapsed_seconds"] = elapsed
            result_entry["return_code"] = result.returncode

            if result.returncode != 0:
                console.print(
                    f"[red]ERROR:[/red] {mod_name} -> exit code {result.returncode}"
                )
                failed_runs.append((mod_name, result.returncode))
                result_entry["status"] = "failed"
            else:
                console.print(f"[green]Completed in {elapsed:.2f}s[/green]")
                result_entry["status"] = "ok"

            # ---- Run pylint ----
            console.print("• [blue]Running pylint...[/blue]")
            pylint_cmd = ["uv", "run", "pylint", mod_name]
            lint_result = run_cmd(pylint_cmd)

            # extract score from pylint output
            score = None
            if not isinstance(lint_result, subprocess.TimeoutExpired):
                m = re.search(
                    r"Your code has been rated at ([0-9.]+)/10",
                    lint_result.stdout,
                )
                if m:
                    score = float(m.group(1))

            pylint_scores.append((mod_name, score))
            result_entry["pylint_score"] = score

            if score is not None:
                console.print(f"Pylint score: [bold]{score}/10[/bold]")
            else:
                console.print("[yellow]Pylint did not produce a score![/yellow]")

total_elapsed = time.monotonic() - total_start

# -------- SUMMARY --------

console.rule("[bold magenta]SUMMARY[/bold magenta]")
console.print(f"Total runtime: [bold]{total_elapsed:.2f}s[/bold]")

if timeout_runs:
    console.print("\n[bold]Timed-out runs (> 30s):[/bold]")
    table = Table(show_header=True, header_style="bold red")
    table.add_column("Module")
    for name in timeout_runs:
        table.add_row(name)
    console.print(table)
else:
    console.print("\n[green]No timeouts![/green]")

if failed_runs:
    console.print("\n[bold]Failed runs:[/bold]")
    table = Table(show_header=True, header_style="bold red")
    table.add_column("Module")
    table.add_column("Exit code")
    for name, code in failed_runs:
        table.add_row(name, str(code))
    console.print(table)
else:
    console.print("\n[green]No failed runs.[/green]")

if missing_files:
    console.print("\n[bold]Missing solution.py files:[/bold]")
    table = Table(show_header=True, header_style="bold yellow")
    table.add_column("Module")
    table.add_column("Path")
    for item in missing_files:
        table.add_row(item["module"], item["path"])
    console.print(table)
else:
    console.print("\n[green]No missing solution.py files.[/green]")

bad_lint = [(m, s) for m, s in pylint_scores if s is None or s < 10.0]
if bad_lint:
    console.print("\n[bold]Pylint < 10:[/bold]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Module")
    table.add_column("Score")
    for name, score in bad_lint:
        table.add_row(name, "-" if score is None else f"{score:.2f}")
    console.print(table)
else:
    console.print("\n[green]All pylint scores are 10/10 — heroic perfection.[/green]")

# -------- YAML OUTPUT --------

summary = {
    "slow_threshold_seconds": SLOW_THRESHOLD,
    "total_runtime_seconds": round(total_elapsed, 3),
    "years": years,
    "results": results,
    "timeouts": timeout_runs,
    "failures": [{"module": m, "exit_code": c} for m, c in failed_runs],
    "missing": missing_files,
    "pylint": [{"module": m, "score": s} for m, s in pylint_scores],
}

output_path = base / "run_all.yaml"
with output_path.open("w", encoding="utf-8") as f:
    yaml.safe_dump(summary, f, sort_keys=False)

console.print(f"\n[cyan]Summary written to[/cyan] [bold]{output_path}[/bold]")
