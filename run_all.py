import subprocess
from pathlib import Path
import time
import re
import sys
import importlib

import yaml
from rich.console import Console
from rich.table import Table
from rich import box
from solution_template import TEMPLATE_VERSION as CURRENT_TEMPLATE_VERSION

base = Path(".")
SLOW_THRESHOLD = 60.0
SUCCESS = "\u2705 "
FAILURE = "\u274C "
STEP_LABEL_WIDTH = 26
console = Console()

failed_runs = []
timeout_runs = []
pylint_scores = []  # (mod_name, score_as_float)
missing_files = []  # list of dicts: year, day, module, path
results = []  # per-module run results, for YAML
legacy_template = []  # solutions not using  current template


def print_step_label(label: str) -> None:
    """
    Print a left‑padded blue label so that SUCCESS/FAILURE icons line up in a column.
    """
    padded = f"{label:<{STEP_LABEL_WIDTH}}"
    console.print(f"• [blue]{padded}[/blue]", end=" ")


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
    years = sorted([int(d.name) for d in base.iterdir() if d.is_dir() and d.name.isdigit()])

solutions = []
for year in years:
    days = range(1, 26)
    if year >=2025:
        days = range(1, 13) # only 12 days in 2025
    for day in days:
        solutions.append((year, day))

total_start = time.monotonic()

total_days = len(solutions)

for idx, (year, day) in enumerate(solutions):
    file_name = base / f"{year:04d}" / f"{day}" / "solution.py"
    mod_name = f"{year}.{day}.solution"

    result_entry = {
        "module": mod_name,
        "year": year,
        "day": day,
        "status": "not_run",
        "elapsed_seconds": None,
        "return_code": None,
        "pylint_score": None,
        "uses_aoc_run": False,
    }
    results.append(result_entry)
    if not file_name.exists():
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
    # ---- Check for legacy template ----
    try:
        import importlib
        module = importlib.import_module(mod_name)
        result_entry['template_version'] = getattr(module, 'TEMPLATE_VERSION', None)
    except (ImportError, AttributeError):
        result_entry['template_version'] = None

    
    if result_entry.get("template_version") != CURRENT_TEMPLATE_VERSION:
        legacy_template.append(
            {
                "year": year,
                "day": day,
                "module": mod_name,
                "template_version": result_entry.get("template_version"),
                "path": str(file_name),
            }
        )
    console.rule(
        f"[bold magenta]{mod_name}[/bold magenta] "
        f"[green]({result_entry.get('template_version')})[/green]"
    )

    # ---- Ruff format ----
    print_step_label("Formatting with ruff...")
    fmt_cmd = ["uv", "run", "ruff", "format", str(file_name)]
    response = run_cmd(fmt_cmd)
    if response.returncode == 0:
        console.print(SUCCESS)
    else:
        console.print(FAILURE)

    # ---- Run pylint ----
    print_step_label("Running pylint...")
    pylint_cmd = ["uv", "run", "pylint", mod_name]
    lint_result = run_cmd(pylint_cmd)

    score = None
    if isinstance(lint_result, subprocess.TimeoutExpired):
        console.print(f"{FAILURE}[red]TIMEOUT running pylint[/red]")
    else:
        m = re.search(
            r"Your code has been rated at ([0-9.]+)/10",
            lint_result.stdout,
        )
        if m:
            score = float(m.group(1))

        if score is None:
            console.print(f"{FAILURE}[yellow]No pylint score produced[/yellow]")
        elif score == 10.0:
            console.print(f"{SUCCESS}[bold green]{score}/10[/bold green]")
        else:
            console.print(f"{FAILURE}[bold yellow]{score:.2f}/10[/bold yellow]")

    pylint_scores.append((mod_name, score))
    result_entry["pylint_score"] = score

    # ---- Run the solution with a hard timeout ----
    print_step_label("Running solution...")
    run_cmd_list = ["uv", "run", "python", "-m", mod_name]

    start = time.monotonic()
    result = run_cmd(run_cmd_list, timeout=SLOW_THRESHOLD)
    elapsed = time.monotonic() - start

    if isinstance(result, subprocess.TimeoutExpired):
        console.print(
            f"{FAILURE}[red]TIMEOUT:[/red] {mod_name} exceeded {SLOW_THRESHOLD}s"
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
            f"{FAILURE}[red]ERROR:[/red] {mod_name} -> exit code {result.returncode}"
        )
        failed_runs.append((mod_name, result.returncode))
        result_entry["status"] = "failed"
    else:
        console.print(f"{SUCCESS}[green]Completed in {elapsed:.2f}s[/green]")
        result_entry["status"] = "ok"

    percentage = ((idx + 1) / total_days) * 100
    cumulative_time = time.monotonic() - total_start
    console.rule(
        f"[magenta]{idx+1}/{total_days}[/magenta] modules completed "
        f"([green]{percentage:.1f}%[/green]) - "
        f"[cyan]Cumulative time:[/cyan] [cyan]{cumulative_time:.2f}s[/cyan]\n"
    )
    console.print()
    # ---- End of main loop ----

total_elapsed = time.monotonic() - total_start

# -------- SUMMARY --------

console.rule("[bold magenta]SUMMARY[/bold magenta]")
console.print(f"Total runtime: [bold]{total_elapsed:.2f}s[/bold]")

if timeout_runs:
    console.print(f"\n[bold]Timed-out runs (> {SLOW_THRESHOLD:.0f}s):[/bold]")
    table = Table(show_header=True, header_style="bold red", box=box.MINIMAL_HEAVY_HEAD)
    table.add_column("Module")
    for name in timeout_runs:
        table.add_row(name)
    console.print(table)
else:
    console.print("\n[green]No timeouts![/green]")

if failed_runs:
    console.print("\n[bold]Failed runs:[/bold]")
    table = Table(show_header=True, header_style="bold red", box=box.MINIMAL_HEAVY_HEAD)
    table.add_column("Module")
    table.add_column("Exit code")
    for name, code in failed_runs:
        table.add_row(name, str(code))
    console.print(table)
else:
    console.print("\n[green]No failed runs.[/green]")

if missing_files:
    console.print("\n[bold]Missing solution.py files:[/bold]")
    table = Table(show_header=True, header_style="bold yellow", box=box.MINIMAL_HEAVY_HEAD)
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
    table = Table(show_header=True, header_style="bold magenta", box=box.MINIMAL_HEAVY_HEAD)
    table.add_column("Module")
    table.add_column("Score")
    for name, score in bad_lint:
        table.add_row(name, "-" if score is None else f"{score:.2f}")
    console.print(table)
else:
    console.print("\n[green]All pylint scores are 10/10 — heroic perfection.[/green]")

# ---- Legacy aoc.run() template summary ----
if legacy_template:
    console.print("\n[bold]Solutions using older template:[/bold]")
    table = Table(
        show_header=True,
        header_style="bold cyan",
        box=box.MINIMAL_HEAVY_HEAD,
    )
    table.add_column("Module")
    table.add_column("Template version")
    table.add_column("Path")
    for item in legacy_template:
        table.add_row(
            item["module"],
            str(item.get("template_version")),
            item["path"],
        )
    console.print(table)
else:
    console.print("\n[green]No older templates detected.[/green]")

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
    "legacy_template": legacy_template,
}

output_path = base / "run_all.yaml"
with output_path.open("w", encoding="utf-8") as f:
    yaml.safe_dump(summary, f, sort_keys=False)

console.print(f"\n[cyan]Summary written to[/cyan] [bold]{output_path}[/bold]")

# -------- MARKDOWN OUTPUT --------

md_lines = []
md_lines.append("# run_all Summary\n")

md_lines.append(f"**Total runtime:** `{total_elapsed:.2f}s`\n")
md_lines.append(f"**Slow threshold:** `{SLOW_THRESHOLD}s`\n")

# Timeouts
md_lines.append(f"\n## Timed-out runs (> {SLOW_THRESHOLD:.0f}s)\n")
if timeout_runs:
    md_lines.append("| Module |\n")
    md_lines.append("|--------|\n")
    for name in timeout_runs:
        md_lines.append(f"| {name} |\n")
else:
    md_lines.append("_No timeouts._\n")

# Failures
md_lines.append("\n## Failed runs\n")
if failed_runs:
    md_lines.append("| Module | Exit code |\n")
    md_lines.append("|--------|-----------|\n")
    for name, code in failed_runs:
        md_lines.append(f"| {name} | {code} |\n")
else:
    md_lines.append("_No failed runs._\n")

# Missing files
md_lines.append("\n## Missing solution.py files\n")
if missing_files:
    md_lines.append("| Module | Path |\n")
    md_lines.append("|--------|-------|\n")
    for item in missing_files:
        md_lines.append(f"| {item['module']} | {item['path']} |\n")
else:
    md_lines.append("_No missing files._\n")

# Pylint
md_lines.append("\n## Pylint scores < 10\n")
if bad_lint:
    md_lines.append("| Module | Score |\n")
    md_lines.append("|--------|--------|\n")
    for name, score in bad_lint:
        sval = "-" if score is None else f"{score:.2f}"
        md_lines.append(f"| {name} | {sval} |\n")
else:
    md_lines.append("_All scores are 10/10._\n")

# Legacy template
md_lines.append("\n## Solutions using older template\n")
if legacy_template:
    md_lines.append("| Module | Template version | Path |\n")
    md_lines.append("|--------|------------------|-------|\n")
    for item in legacy_template:
        md_lines.append(
            f"| {item['module']} | {item.get('template_version')} | {item['path']} |\n"
        )
else:
    md_lines.append("_No legacy templates detected._\n")

md_path = base / "run_all.md"
with md_path.open("w", encoding="utf-8") as f:
    f.writelines(md_lines)

console.print(f"[cyan]Markdown summary written to[/cyan] [bold]{md_path}[/bold]")
