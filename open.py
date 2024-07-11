import os
import sys
import shutil
from datetime import datetime
import subprocess

def get_year_day():
    current_year = datetime.now().year
    current_day = datetime.now().day

    if len(sys.argv) == 3:
        return sys.argv[1], sys.argv[2]
    else:
        year = input(f"Enter year (default: {current_year}): ") or str(current_year)
        day = input(f"Enter day (default: {current_day:02d}): ") or f"{current_day:02d}"
        return year, day

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def create_init_file(path):
    init_file = os.path.join(path, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            pass  # Create an empty file
        print(f"Created empty __init__.py in: {path}")
        subprocess.run(['git', 'add', init_file], check=True)

def copy_and_modify_template(year, day, src, dst):
    if os.path.exists(dst):
        print(f"File already exists: {dst}")
        return

    with open(src, 'r') as f:
        content = f.read()
    
    content = content.replace('YEAR', year)
    content = content.replace('DAY', day)
    
    with open(dst, 'w') as f:
        f.write(content)
    print(f"Created and modified: {dst}")
    subprocess.run(['git', 'add', dst], check=True)

def create_jupyter_notebook(path, year, day):
    if os.path.exists(path):
        print(f"File already exists: {path}")
        return

    notebook_content = {
     "cells": [
        {
            "cell_type": "code",
            "execution_count": 1,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "import sys\n",
                "sys.path.append(os.path.realpath('../..'))\n",
                "import aoc\n",
                f"aoc.set_date({year},{day})"
            ]
        }
     ],
     "metadata": {},
     "nbformat": 4,
     "nbformat_minor": 4
    }
    
    with open(path, 'w') as f:
        import json
        json.dump(notebook_content, f)
    print(f"Created Jupyter notebook: {path}")
    subprocess.run(['git', 'add', path], check=True)

def main():
    year, day = get_year_day()
    original_dir = os.getcwd()
    year_dir = year
    day_dir = os.path.join(year_dir, day)
    
    create_directory(year_dir)
    create_directory(day_dir)
    
    # Create __init__.py files
    create_init_file(year_dir)
    create_init_file(day_dir)
    
    template_path = 'solution_template.py'
    solution_path = os.path.join(day_dir, 'solution.py')
    copy_and_modify_template(year, day, template_path, solution_path)
    
    print("Opening solution.py ...")
    # FIXME: this should use some kind of configuration for editor
    subprocess.run(['C:/Program Files/Sublime Text/sublime_text.exe', solution_path], shell=False)

    print("Opening Shell")
    # FIXME: shell should also be configurable
    wt = os.path.join(
            'c:/Users/Corey',
            'AppData/Local/Microsoft/WindowsApps',
            'Microsoft.WindowsTerminalPreview_8wekyb3d8bbwe',
            'wt.exe'
        )
    print(' '.join([
            wt,
            '-w 0 sp -H -s 0.7',
            f'-d {original_dir}',
            '--title AdventOfCode',
            'powershell.exe -NoExit',
            f'-Command "function global:run {{ python -m {year}.{day}.solution }}"'
        ]))

    subprocess.run(
        #wt -w 0 sp -H -s 0.7 -d C:\Users\corey\Dev\AdventOfCode\ --title AdventOfCode
        #wt -w 0 sp -H -s 0.7 -d C:\Users\corey\Dev\AdventOfCode\ --title AdventOfCode powershell.exe -NoExit -Command "function global:run { python -m 2016.9.solution }"
        #wt -w 0 sp -H -s 0.7 -d C:\Users\corey\Dev\AdventOfCode\ --title AdventOfCode powershell.exe -NoExit -Command "function global:run { python -m 2016.9.solution }"
        [
            wt, '-w', '0', 'sp', '-H', '-s', '0.7', '-d', '.',
            '--title', 'AdventOfCode', 'powershell.exe', '-NoExit',
            '-Command', f'"function global:run {{ python -m {year}.{day}.solution }}"'
        ], shell=True)
        
    notebook_path = os.path.join(day_dir, 'scratch_pad.ipynb')
    create_jupyter_notebook(notebook_path, year, day)

    print("Opening Puzzle")
    os.startfile(f'https://adventofcode.com/{year}/day/{day}')
    os.startfile(f'https://adventofcode.com/{year}/day/{day}/input')

    print("Launching Jupyter notebook...")
    os.chdir(original_dir)  # Change back to the original directory
    subprocess.run(['jupyter', 'notebook', notebook_path])

if __name__ == "__main__":
    main()


"""
Todo:
  - .aoc.cfg.json
  - store editor path
  - store wt path
"""