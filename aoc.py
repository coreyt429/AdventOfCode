"""
AdventOfCode utility Module
contains utility functions for working AdventOfCode puzzles
"""
import sys
import re
import json
from datetime import datetime
import requests
import os
from getpass import getpass

class AdventOfCode:
    def __init__(self, year=None, day=None):
        today = datetime.today()

        self.year = year if year is not None else today.year
        self.day = day if day is not None else today.day
        matches = re.match(r'(.*AdventOfCode).*',os.getcwd())
        if matches:
            base_dir = matches.group(1)
        else:
            base_dir = os.getcwd()

        self.session_file = os.path.join(base_dir,'.aoc.session')
        self.session_id = self.get_session_id()

    def get_session_id(self):
        if os.path.exists(self.session_file):
            with open(self.session_file, 'r') as f:
                self.session_id =  f.read().strip()
                return self.session_id
        return None

    def save_session_id(self):
        with open(self.session_file, 'w') as f:
            f.write(self.session_id)

    def test_session(self):
        response = self.session.get('https://adventofcode.com')
        return 'Advent of Code' in response.text

    def get_input(self):
        self.init_session()
        url = f'https://adventofcode.com/{self.year}/day/{self.day}/input'
        response = self.session.get(url)
        if response.status_code == 200:
            self.save_input(response.text)
            print(f"Input for day {self.day} of year {self.year} has been saved.")
            return response.text
        else:
            print(f"Failed to retrieve input. Status code: {response.status_code}")
            return None

    def save_input(self, content):
        if not os.path.exists(f'{self.year}'):
            os.makedirs(f'{self.year}')
        with open(f'{self.year}/{self.day}/input.txt', 'w') as f:
            f.write(content)

    def login_to_aoc(self):
        self.session = requests.Session()
        self.session.cookies.set('session', self.session_id)
        return self.session

    def init_session(self):
        self.get_session_id()
        self.session = None

        while True:
            if self.session_id:
                self.session = self.login_to_aoc()
                if self.test_session():
                    break
                else:
                    print("Saved session ID is invalid.")
                    self.session_id = None
            else:
                print("Please enter your Advent of Code session ID.")
                print("You can find this in your browser's cookies for adventofcode.com")
                self.session_id = getpass("Session ID: ")
                self.save_session_id()

    def set_date(self, year, day):
        """
        Function to set the year and day used by functions
        This is likely deprecated by passing the year and day to init
        """
        self.year = year
        self.day = day

    def get_file(self, file_name=None):
        """
        Utility function to open an input file

        Parameters:
            - file_name - string name of file to load, default input.txt

        Returns:
            - file handle
        """
        if file_name is None:
            file_name = f"{self.year}/{self.day}/input.txt"
        try:
            return open(file_name, 'r', encoding='utf-8')
        except OSError as error_message:
            try:
                self.get_input()
                return open(file_name, 'r', encoding='utf-8')
            except OSError as error_message:
                # file is missing, lets download it
                print(f"Error opening file {file_name}: {error_message}")
                sys.exit()

    def load_lines(self, file_name=None):
        """
        Function to load an input file

        Parameters:
            - file_name - string name of file to load, default input.txt

        Returns:
            - list of lines from the file
        """
        return self.load_text(file_name).rstrip().split('\n')
        
    def load_text(self, file_name=None):
        """
        Function to load an input file

        Parameters:
            - file_name - string name of file to load, default input.txt

        Returns:
            - text content of the file
        """
        with self.get_file(file_name) as file:
            return file.read().rstrip()

    def load_integers(self, file_name=None):
        """
        Function to load an input file

        Parameters:
            - file_name - string name of file to load, default input.txt

        Returns:
            - list of ints from file
        """
        return [int(x) for x in self.load_lines(file_name)]

    def load_grid(self, file_name=None):
        """
        Function to load an input file

        Parameters:
            - file_name - string name of file to load, default input.txt

        Returns:
            - list of lists from file
        """
        return [list(line) for line in self.load_lines(file_name)]



"""
Below here are functions to support the __main__:

This is code to build the aoc structure for the puzzle you are working on

"""

import os
import sys
import shutil
from datetime import datetime
import subprocess

def get_year_day():
    current_year = datetime.now().year
    current_day = datetime.now().day

    if len(sys.argv) == 3:
        return str(int(sys.argv[1])), str(int(sys.argv[2]))
    else:
        year = input(f"Enter year (default: {current_year}): ") or str(current_year)
        day = input(f"Enter day (default: {current_day}): ") or f"{current_day}"
        while not day.isdigit() and year.isdigit:
            print(f"Non Numeric input: {year} {day}")
            year = input(f"Enter year (default: {current_year}): ") or str(current_year)
            day = input(f"Enter day (default: {current_day}): ") or f"{current_day}"
        return str(int(year)), str(int(day))

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
    # load config
    file_path = '.aoc.cfg.json'
    with open(file_path, 'r') as file:
        cfg = json.load(file)
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
    #subprocess.run([cfg['editor'], solution_path], shell=False)
    subprocess.Popen([cfg['editor'], solution_path], start_new_session=True)

    old_solution_path = os.path.join(day_dir, 'script.py')
    if os.path.exists(old_solution_path):
        subprocess.Popen([cfg['editor'], old_solution_path], start_new_session=True)

    # Note, terminal currently only supports windows terminal
    # we could replace the command line parameters with a template from cfg
    print("Opening Shell")
    #  powershell -NoExit -Command "function global:run { python -m 2016.21.solution};function global:check { pylint 2016/21/solution.py }"
    #func_run = f"function global:run {{ python -m {year}.{day}.solution }}"
    #func_check = f"function global:check {{ pylint {year}/{day}/solution.py }}"

    command = f"aoc.ps1 {year} {day}"

    print(' '.join([
        cfg['terminal'], '-w', '0', 'sp', '-H', '-s', '0.7', '-d', '.',
        '--title', 'AdventOfCode', 'powershell.exe', '-NoExit',
        '-Command', f'"{command}"'
    ]))

    subprocess.run(
        [
            cfg['terminal'], '-w', '0', 'sp', '-H', '-s', '0.7', '-d', '.',
            '--title', 'AdventOfCode', 'powershell.exe', '-NoExit',
            '-Command', f'"{command}"'
        ], shell=True)
        
    notebook_path = os.path.join(day_dir, 'scratch_pad.ipynb')
    notebook_template_path = 'scratch_pad_template.ipynb'
    #create_jupyter_notebook(notebook_path, year, day)
    copy_and_modify_template(year, day, notebook_template_path, notebook_path)
    print("Opening Puzzle")
    os.startfile(f'https://adventofcode.com/{year}/day/{day}')
    #os.startfile(f'https://adventofcode.com/{year}/day/{day}/input')
    #Insert code to pull input file here (or not, input should be pulled with
    # an aoc method from the solution)

    print("Launching Jupyter notebook...")
    os.chdir(original_dir)  # Change back to the original directory
    subprocess.run(['jupyter', 'notebook', notebook_path])

if __name__ == "__main__":
    main()
