"""Format, lint, and run Advent of Code solutions in parallel."""

from __future__ import annotations

import argparse
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
import importlib
import os
from pathlib import Path
import re
import subprocess
import time
from typing import Any

import yaml
from rich import box
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.table import Table

from solution_template import TEMPLATE_VERSION as CURRENT_TEMPLATE_VERSION


BASE = Path(".")
SLOW_THRESHOLD = 60.0
console = Console()


def run_cmd(command: list[str], timeout: float | None = None) -> dict[str, Any]:
    """Run a command and return a picklable description of its outcome."""
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
        return {
            "return_code": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as error:
        return {
            "return_code": None,
            "stdout": ensure_text(error.stdout),
            "stderr": ensure_text(error.stderr),
            "timed_out": True,
        }


def ensure_text(value: str | bytes | None) -> str:
    """Normalize subprocess output, which may be bytes after a timeout."""
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    return value or ""


def get_template_version(module_name: str) -> Any:
    """Import a solution and return its template version, if it declares one."""
    try:
        module = importlib.import_module(module_name)
    except (ImportError, AttributeError):
        return None
    return getattr(module, "TEMPLATE_VERSION", None)


def check_solution(year: int, day: int, slow_threshold: float) -> dict[str, Any]:
    """Format, lint, and execute one solution. Runs inside a worker process."""
    file_name = BASE / f"{year:04d}" / str(day) / "solution.py"
    module_name = f"{year}.{day}.solution"
    result: dict[str, Any] = {
        "module": module_name,
        "year": year,
        "day": day,
        "path": str(file_name),
        "status": "not_run",
        "elapsed_seconds": None,
        "return_code": None,
        "format_return_code": None,
        "format_output": "",
        "pylint_score": None,
        "pylint_return_code": None,
        "pylint_output": "",
        "run_output": "",
        "template_version": None,
        "uses_aoc_run": False,
    }

    if not file_name.exists():
        result["status"] = "missing"
        return result

    result["template_version"] = get_template_version(module_name)

    format_result = run_cmd(["uv", "run", "ruff", "format", str(file_name)])
    result["format_return_code"] = format_result["return_code"]
    result["format_output"] = combine_output(format_result)

    lint_result = run_cmd(["uv", "run", "pylint", module_name])
    result["pylint_return_code"] = lint_result["return_code"]
    result["pylint_output"] = combine_output(lint_result)
    score_match = re.search(
        r"Your code has been rated at ([0-9.]+)/10", lint_result["stdout"]
    )
    if score_match:
        result["pylint_score"] = float(score_match.group(1))

    start = time.monotonic()
    run_result = run_cmd(
        ["uv", "run", "python", "-m", module_name], timeout=slow_threshold
    )
    elapsed = time.monotonic() - start
    result["run_output"] = combine_output(run_result)

    if run_result["timed_out"]:
        result["status"] = "timeout"
        return result

    result["elapsed_seconds"] = elapsed
    result["return_code"] = run_result["return_code"]
    result["status"] = "ok" if run_result["return_code"] == 0 else "failed"
    return result


def combine_output(command_result: dict[str, Any]) -> str:
    """Combine and trim captured output for diagnostic reports."""
    return "\n".join(
        part.strip()
        for part in (command_result["stdout"], command_result["stderr"])
        if part and part.strip()
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("year", nargs="?", type=int, help="only check this year")
    parser.add_argument(
        "-j",
        "--workers",
        type=int,
        default=max(1, os.cpu_count() or 1),
        help="worker processes (default: available CPUs)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=SLOW_THRESHOLD,
        help=f"per-solution timeout in seconds (default: {SLOW_THRESHOLD:g})",
    )
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("--workers must be at least 1")
    if args.timeout <= 0:
        parser.error("--timeout must be greater than 0")
    return args


def discover_solutions(year: int | None) -> tuple[list[int], list[tuple[int, int]]]:
    years = (
        [year]
        if year is not None
        else sorted(
            int(directory.name)
            for directory in BASE.iterdir()
            if directory.is_dir() and directory.name.isdigit()
        )
    )
    solutions = [
        (solution_year, day)
        for solution_year in years
        for day in range(1, 13 if solution_year >= 2025 else 26)
    ]
    return years, solutions


def run_solutions(
    solutions: list[tuple[int, int]], workers: int, slow_threshold: float
) -> list[dict[str, Any]]:
    """Run solution checks concurrently and render one aggregate progress meter."""
    results: list[dict[str, Any]] = []
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("[yellow]Waiting {task.fields[waiting]}"),
        TextColumn("[cyan]Running {task.fields[running]}"),
        TextColumn("[green]Completed {task.fields[completed_count]}"),
        TextColumn("[bold]Total {task.fields[total_count]}"),
        TimeElapsedColumn(),
        TextColumn("•"),
        TimeRemainingColumn(),
        console=console,
    )
    with progress, ProcessPoolExecutor(max_workers=workers) as executor:
        total = len(solutions)
        task_id = progress.add_task(
            "Checking solutions",
            total=total,
            waiting=total,
            running=0,
            completed_count=0,
            total_count=total,
        )
        futures = {
            executor.submit(check_solution, year, day, slow_threshold): (year, day)
            for year, day in solutions[:workers]
        }
        next_solution = len(futures)
        pending = set(futures)
        while pending:
            completed_futures, pending = wait(
                pending, timeout=0.1, return_when=FIRST_COMPLETED
            )
            for future in completed_futures:
                year, day = futures[future]
                try:
                    result = future.result()
                except (
                    Exception
                ) as error:  # Keep one broken worker from hiding the rest.
                    result = worker_error_result(year, day, error)
                results.append(result)

                if next_solution < total:
                    next_year, next_day = solutions[next_solution]
                    next_solution += 1
                    next_future = executor.submit(
                        check_solution, next_year, next_day, slow_threshold
                    )
                    futures[next_future] = (next_year, next_day)
                    pending.add(next_future)

            completed = len(results)
            running = len(pending)
            waiting = total - completed - running
            progress.update(
                task_id,
                completed=completed,
                waiting=waiting,
                running=running,
                completed_count=completed,
            )

    return sorted(results, key=lambda result: (result["year"], result["day"]))


def worker_error_result(year: int, day: int, error: Exception) -> dict[str, Any]:
    module_name = f"{year}.{day}.solution"
    return {
        "module": module_name,
        "year": year,
        "day": day,
        "path": str(BASE / str(year) / str(day) / "solution.py"),
        "status": "worker_error",
        "elapsed_seconds": None,
        "return_code": None,
        "format_return_code": None,
        "format_output": "",
        "pylint_score": None,
        "pylint_return_code": None,
        "pylint_output": "",
        "run_output": f"{type(error).__name__}: {error}",
        "template_version": None,
        "uses_aoc_run": False,
    }


def problem_rows(results: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Return one row for every actionable problem found by any check."""
    problems: list[dict[str, str]] = []
    for result in results:
        module = result["module"]
        status = result["status"]
        if status == "missing":
            problems.append(
                {"module": module, "check": "missing", "details": result["path"]}
            )
            continue
        if result["format_return_code"] not in (None, 0):
            problems.append(
                {
                    "module": module,
                    "check": "format",
                    "details": diagnostic(result["format_output"]),
                }
            )
        score = result["pylint_score"]
        if score is None:
            problems.append(
                {
                    "module": module,
                    "check": "pylint",
                    "details": diagnostic(result["pylint_output"], "no score produced"),
                }
            )
        elif score < 10.0:
            problems.append(
                {"module": module, "check": "pylint", "details": f"{score:.2f}/10"}
            )
        if status == "timeout":
            problems.append(
                {
                    "module": module,
                    "check": "run",
                    "details": "timed out",
                }
            )
        elif status in {"failed", "worker_error"}:
            detail = f"exit code {result['return_code']}"
            problems.append(
                {
                    "module": module,
                    "check": "run",
                    "details": diagnostic(result["run_output"], detail),
                }
            )
        if result["template_version"] != CURRENT_TEMPLATE_VERSION:
            problems.append(
                {
                    "module": module,
                    "check": "template",
                    "details": f"version {result['template_version']!r}; expected {CURRENT_TEMPLATE_VERSION!r}",
                }
            )
    return problems


def diagnostic(output: str, fallback: str = "command failed") -> str:
    """Use the final non-empty output line as a compact problem description."""
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return lines[-1] if lines else fallback


def build_stats(
    results: list[dict[str, Any]], elapsed: float, workers: int
) -> dict[str, Any]:
    run_times = [
        result["elapsed_seconds"]
        for result in results
        if result["elapsed_seconds"] is not None
    ]
    return {
        "solutions_checked": len(results),
        "passed": sum(result["status"] == "ok" for result in results),
        "failed": sum(
            result["status"] in {"failed", "worker_error"} for result in results
        ),
        "timed_out": sum(result["status"] == "timeout" for result in results),
        "missing": sum(result["status"] == "missing" for result in results),
        "legacy_templates": sum(
            result["status"] != "missing"
            and result["template_version"] != CURRENT_TEMPLATE_VERSION
            for result in results
        ),
        "lint_issues": sum(
            result["status"] != "missing"
            and (result["pylint_score"] is None or result["pylint_score"] < 10.0)
            for result in results
        ),
        "wall_time_seconds": elapsed,
        "solution_time_seconds": sum(run_times),
        "workers": workers,
    }


def print_summary(stats: dict[str, Any], problems: list[dict[str, str]]) -> None:
    console.rule("[bold magenta]SUMMARY")
    stats_table = Table(box=box.MINIMAL_HEAVY_HEAD, show_header=False)
    stats_table.add_column("Metric", style="bold")
    stats_table.add_column("Value", justify="right")
    labels = (
        ("Solutions checked", "solutions_checked"),
        ("Passed", "passed"),
        ("Failed", "failed"),
        ("Timed out", "timed_out"),
        ("Missing", "missing"),
        ("Lint issues", "lint_issues"),
        ("Legacy templates", "legacy_templates"),
        ("Workers", "workers"),
    )
    for label, key in labels:
        stats_table.add_row(label, str(stats[key]))
    stats_table.add_row("Wall time", f"{stats['wall_time_seconds']:.2f}s")
    stats_table.add_row(
        "Combined solution time", f"{stats['solution_time_seconds']:.2f}s"
    )
    console.print(stats_table)

    if not problems:
        console.print("[bold green]All checks passed.[/bold green]")
        return

    console.print(f"\n[bold red]Problems ({len(problems)})[/bold red]")
    problem_table = Table(box=box.MINIMAL_HEAVY_HEAD, header_style="bold red")
    problem_table.add_column("Module", no_wrap=True)
    problem_table.add_column("Check", no_wrap=True)
    problem_table.add_column("Details", overflow="fold")
    for problem in problems:
        problem_table.add_row(problem["module"], problem["check"], problem["details"])
    console.print(problem_table)


def write_reports(
    years: list[int],
    results: list[dict[str, Any]],
    problems: list[dict[str, str]],
    stats: dict[str, Any],
    slow_threshold: float,
) -> None:
    """Write machine-readable YAML and a concise Markdown summary."""
    timeouts = [result["module"] for result in results if result["status"] == "timeout"]
    failures = [
        {"module": result["module"], "exit_code": result["return_code"]}
        for result in results
        if result["status"] in {"failed", "worker_error"}
    ]
    missing = [
        {
            "year": result["year"],
            "day": result["day"],
            "module": result["module"],
            "path": result["path"],
        }
        for result in results
        if result["status"] == "missing"
    ]
    legacy = [
        {
            "year": result["year"],
            "day": result["day"],
            "module": result["module"],
            "template_version": result["template_version"],
            "path": result["path"],
        }
        for result in results
        if result["status"] != "missing"
        and result["template_version"] != CURRENT_TEMPLATE_VERSION
    ]
    summary = {
        "slow_threshold_seconds": slow_threshold,
        "total_runtime_seconds": round(stats["wall_time_seconds"], 3),
        "years": years,
        "stats": stats,
        "results": results,
        "problems": problems,
        "timeouts": timeouts,
        "failures": failures,
        "missing": missing,
        "pylint": [
            {"module": result["module"], "score": result["pylint_score"]}
            for result in results
            if result["status"] != "missing"
        ],
        "legacy_template": legacy,
    }
    yaml_path = BASE / "run_all.yaml"
    with yaml_path.open("w", encoding="utf-8") as output_file:
        yaml.safe_dump(summary, output_file, sort_keys=False)

    markdown = [
        "# run_all Summary\n\n",
        f"**Wall time:** `{stats['wall_time_seconds']:.2f}s`  \n",
        f"**Workers:** `{stats['workers']}`  \n",
        f"**Passed:** `{stats['passed']}/{stats['solutions_checked']}`\n\n",
        "## Stats\n\n",
        "| Failed | Timed out | Missing | Lint issues | Legacy templates |\n",
        "|-------:|----------:|--------:|------------:|-----------------:|\n",
        f"| {stats['failed']} | {stats['timed_out']} | {stats['missing']} | "
        f"{stats['lint_issues']} | {stats['legacy_templates']} |\n\n",
        "## Problems\n\n",
    ]
    if problems:
        markdown.extend(
            [
                "| Module | Check | Details |\n",
                "|--------|-------|---------|\n",
                *(
                    f"| {problem['module']} | {problem['check']} | "
                    f"{problem['details'].replace('|', '&#124;')} |\n"
                    for problem in problems
                ),
            ]
        )
    else:
        markdown.append("_No problems detected._\n")
    md_path = BASE / "run_all.md"
    with md_path.open("w", encoding="utf-8") as output_file:
        output_file.writelines(markdown)

    console.print(
        f"Reports written to [bold]{yaml_path}[/bold] and [bold]{md_path}[/bold]"
    )


def main() -> int:
    args = parse_args()
    years, solutions = discover_solutions(args.year)
    start = time.monotonic()
    results = run_solutions(solutions, args.workers, args.timeout)
    elapsed = time.monotonic() - start
    problems = problem_rows(results)
    stats = build_stats(results, elapsed, args.workers)
    print_summary(stats, problems)
    write_reports(years, results, problems, stats, args.timeout)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
