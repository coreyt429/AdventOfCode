import subprocess
from pathlib import Path
import time
import re
import sys

base = Path(".")
SLOW_THRESHOLD = 30.0

failed_runs = []
timeout_runs = []
pylint_scores = []   # (mod_name, score_as_float)

def run_cmd(cmd, timeout=None):
    try:
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout
        )
    except subprocess.TimeoutExpired as e:
        return e

# ----- Year argument handling -----
if len(sys.argv) > 1:
    try:
        only_year = int(sys.argv[1])
    except ValueError:
        print(f"Invalid year argument: {sys.argv[1]}")
        sys.exit(1)
    years = [only_year]
else:
    years = list(range(2015, 2025))

# ----- Main Loop -----
for year in years:
    for day in range(1, 26):
        file_name = base / f"{year:04d}" / f"{day}" / "solution.py"
        mod_name = f"{year}.{day}.solution"

        if not file_name.exists():
            print(f"Missing: {file_name}")
            continue

        print(f"\n=== {mod_name} ===")

        # ---- Ruff format ----
        print("• Formatting with ruff...")
        fmt_cmd = ["uv", "run", "ruff", "format", str(file_name)]
        run_cmd(fmt_cmd)

        # ---- Run the solution with a hard timeout ----
        print("• Running solution...")
        run_cmd_list = ["uv", "run", "python", "-m", mod_name]

        start = time.monotonic()
        result = run_cmd(run_cmd_list, timeout=SLOW_THRESHOLD)
        elapsed = time.monotonic() - start

        if isinstance(result, subprocess.TimeoutExpired):
            print(f"TIMEOUT: {mod_name} exceeded {SLOW_THRESHOLD}s")
            timeout_runs.append(mod_name)
            continue

        if result.returncode != 0:
            print(f"ERROR: {mod_name} -> exit code {result.returncode}")
            failed_runs.append((mod_name, result.returncode))
        else:
            print(f"Completed in {elapsed:.2f}s")

        # ---- Run pylint ----
        print("• Running pylint...")
        pylint_cmd = ["uv", "run", "pylint", mod_name]
        lint_result = run_cmd(pylint_cmd)

        # extract score from pylint output
        score = None
        m = re.search(r"Your code has been rated at ([0-9.]+)/10",
                      lint_result.stdout)
        if m:
            score = float(m.group(1))
            pylint_scores.append((mod_name, score))
            print(f"Pylint score: {score}/10")
        else:
            print("Pylint did not produce a score!")
            pylint_scores.append((mod_name, None))

# -------- SUMMARY --------

print("\n===== SUMMARY =====")

if timeout_runs:
    print("\nTimed-out runs (> 30s):")
    for name in timeout_runs:
        print(f"  {name}")
else:
    print("\nNo timeouts!")

if failed_runs:
    print("\nFailed runs:")
    for name, code in failed_runs:
        print(f"  {name} (exit code {code})")
else:
    print("\nNo failed runs.")

bad_lint = [(m, s) for m, s in pylint_scores if s is None or s < 10.0]
if bad_lint:
    print("\nPylint < 10:")
    for name, score in bad_lint:
        print(f"  {name}: {score}")
else:
    print("\nAll pylint scores are 10/10 — heroic perfection.")
