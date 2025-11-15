"""
AdventOfCode utility Module
contains utility functions for working AdventOfCode puzzles
"""

import sys
import json
import logging
from datetime import datetime
import subprocess
import os
import time
import webbrowser
from getpass import getpass
import dotenv
import requests

dotenv.load_dotenv()
logger = logging.getLogger(__name__)


class AdventOfCodeSession:
    """
    Advent of Code Session class to handle session management
    """

    def __init__(self, session_id=None, year=None, day=None):
        self.session_id = session_id
        today = datetime.today()
        self.day = day or today.day
        self.year = year or today.year
        self.session = self.init_session()

    def init_session(self):
        """Initialize session, using stored/ENV session id or prompting the user."""
        # Reload env in case it changed
        dotenv.load_dotenv()
        if not self.session_id:
            self.session_id = os.getenv("AOC_SESSION_ID")

        session = None

        max_attempts = 3
        attempt = 0
        while attempt < max_attempts:
            if not self.session_id:
                # Last resort: ask the user nicely
                self.prompt_for_session_id()

            session = self.login()
            self.session = session
            if self.test():
                return session  # success

            # If we get here, the session was invalid
            print("The provided session ID appears to be invalid.")
            self.session_id = None
        raise RuntimeError(
            "Failed to obtain a valid session ID after multiple attempts."
        )

    def get(self, url):
        """get url using session"""
        return self.session.get(url)

    def test(self):
        """test session to see if valid"""
        response = self.session.get("https://adventofcode.com")
        logger.debug("Testing session id, response code: %s", response.status_code)
        logger.debug("Testing session id, response text: %s", response.text)
        return "Advent of Code" in response.text

    def login(self):
        """login to advent of code site, return session"""
        self.session = requests.Session()
        self.session.cookies.set("session", self.session_id)
        return self.session

    def prompt_for_session_id(self):
        """
        Interactively prompt the user for their Advent of Code session ID
        and save it for future runs.
        """
        print("\nAdvent of Code session required to download your puzzle input.")
        print("Steps to get it:")
        print("  1. Log in to https://adventofcode.com in your browser.")
        print("  2. Open your browser's developer tools.")
        print("  3. Find the cookies for adventofcode.com.")
        print("  4. Copy the value of the cookie named 'session'.\n")

        # You can keep getpass if you want it not echoed; input() is fine too.
        session_id = getpass(
            "Paste your Advent of Code session value here (or press Enter to cancel): "
        ).strip()
        if not session_id:
            raise RuntimeError("No session ID provided; cannot continue.")

        self.session_id = session_id
        self.save_session_id()
        print("Session ID saved for future runs.\n")

    def save_session_id(self):
        """
        Save the session ID to the .env file for future use.
        """
        env_path = ".env"
        lines = []
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

        with open(env_path, "w", encoding="utf-8") as f:
            found = False
            for line in lines:
                if line.startswith("AOC_SESSION_ID="):
                    f.write(f"AOC_SESSION_ID={self.session_id}\n")
                    found = True
                else:
                    f.write(line)
            if not found:
                f.write(f"AOC_SESSION_ID={self.session_id}\n")


class AdventOfCode:
    """
    Advent of Code class to handle common functions for solving puzzles
    """

    def __init__(self, year=None, day=None):
        self.session = AdventOfCodeSession(os.getenv("AOC_SESSION_ID"), year, day)
        self.input_data = None
        self.start_time = time.time()
        self.parts = {1: 1, 2: 2}
        self.answer = {1: None, 2: None}
        self.correct = {1: 0, 2: 0}
        self.funcs = {1: None, 2: None}

    def run(self):
        """
        Function to run the functions for each part
        """
        # loop parts
        for my_part in self.parts:
            # log start time
            self.start_time = time.time()
            # get answer
            self.answer[my_part] = self.funcs[my_part](self.input_data, my_part)
            # log end time
            end_time = time.time()
            logger.info(
                "Part %s: %s, took %s seconds",
                my_part,
                self.answer[my_part],
                end_time - self.start_time,
            )
            if self.correct[my_part]:
                assert self.correct[my_part] == self.answer[my_part]

    def get_input(self):
        """get input from advent of code site"""
        url = (
            f"https://adventofcode.com/{self.session.year}/day/{self.session.day}/input"
        )
        response = self.session.get(url)
        if response.status_code == 200:
            self.save_input(response.text)
            logger.info(
                "Input for day %s of year %s has been saved.",
                self.session.day,
                self.session.year,
            )
            return response.text
        logger.info("Failed to retrieve input. Status code: %s", response.status_code)
        return None

    def save_input(self, content):
        """save input to file"""
        if not os.path.exists(f"{self.session.year}"):
            os.makedirs(f"{self.session.year}")
        with open(
            f"{self.session.year}/{self.session.day}/input.txt", "w", encoding="utf-8"
        ) as f:
            f.write(content)

    def set_date(self, year, day):
        """
        Function to set the year and day used by functions
        This is likely deprecated by passing the year and day to init
        """
        self.session.year = year
        self.session.day = day

    def get_file(self, file_name=None):
        """
        Utility function to open an input file

        Parameters:
            - file_name - string name of file to load, default input.txt

        Returns:
            - file handle
        """
        if file_name is None:
            file_name = f"{self.session.year}/{self.session.day}/input.txt"
        try:
            return open(file_name, "r", encoding="utf-8")
        except OSError as e:
            logger.warning("Could not open file %s: %s", file_name, e)
            try:
                self.get_input()
                return open(file_name, "r", encoding="utf-8")
            except OSError as e2:
                # file is missing, lets download it
                logger.info("Error opening file %s: %s", file_name, e2)
                sys.exit()

    def load_lines(self, file_name=None):
        """
        Function to load an input file

        Parameters:
            - file_name - string name of file to load, default input.txt

        Returns:
            - list of lines from the file
        """
        self.input_data = self.load_text(file_name).rstrip().split("\n")
        return self.input_data

    def load_text(self, file_name=None):
        """
        Function to load an input file

        Parameters:
            - file_name - string name of file to load, default input.txt

        Returns:
            - text content of the file
        """
        with self.get_file(file_name) as file:
            self.input_data = file.read().rstrip()
            return self.input_data

    def load_integers(self, file_name=None):
        """
        Function to load an input file

        Parameters:
            - file_name - string name of file to load, default input.txt

        Returns:
            - list of ints from file
        """
        self.input_data = [int(x) for x in self.load_lines(file_name)]
        return self.input_data

    def load_grid(self, file_name=None):
        """
        Function to load an input file

        Parameters:
            - file_name - string name of file to load, default input.txt

        Returns:
            - list of lists from file
        """
        self.input_data = [list(line) for line in self.load_lines(file_name)]
        return self.input_data


# #################################################
# Below here are functions to support the __main__:
#
# This is code to build the aoc structure for the puzzle you are working on
#
# #################################################


def get_year_day():
    """Get the current year and day, or prompt the user for input."""
    current_year = datetime.now().year
    current_day = datetime.now().day

    if len(sys.argv) == 3:
        return str(int(sys.argv[1])), str(int(sys.argv[2]))
    year = input(f"Enter year (default: {current_year}): ") or str(current_year)
    day = input(f"Enter day (default: {current_day}): ") or f"{current_day}"
    while not day.isdigit() and year.isdigit:
        print(f"Non Numeric input: {year} {day}")
        year = input(f"Enter year (default: {current_year}): ") or str(current_year)
        day = input(f"Enter day (default: {current_day}): ") or f"{current_day}"
    return str(int(year)), str(int(day))


def create_directory(path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")


def create_init_file(path):
    """Create __init__.py file in the specified directory if it doesn't exist."""
    init_file = os.path.join(path, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, "w", encoding="utf-8") as f:
            f.write("")  # create empty file
        print(f"Created empty __init__.py in: {path}")
        subprocess.run(["git", "add", init_file], check=True)


def copy_and_modify_template(year, day, src, dst):
    """Copy template file and modify YEAR and DAY placeholders."""
    if os.path.exists(dst):
        print(f"File already exists: {dst}")
        return

    with open(src, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace("YEAR", year)
    content = content.replace("DAY", day)

    with open(dst, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created and modified: {dst}")
    subprocess.run(["git", "add", dst], check=True)


def create_jupyter_notebook(path, year, day):
    """Create a Jupyter notebook with basic setup."""
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
                    f"aoc.set_date({year},{day})",
                ],
            }
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 4,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(notebook_content, f)
    print(f"Created Jupyter notebook: {path}")
    subprocess.run(["git", "add", path], check=True)


def main():
    """Main function to setup Advent of Code puzzle structure"""
    # load config
    file_path = ".aoc.cfg.json"
    aoc = AdventOfCode()
    print(aoc.session.session_id)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            cfg = json.load(file)
    except FileNotFoundError:
        logger.warning("Config file not found: %s", file_path)
        cfg = {"editor": "code"}
    year, day = get_year_day()
    original_dir = os.getcwd()
    year_dir = year
    day_dir = os.path.join(year_dir, day)
    create_directory(year_dir)
    create_directory(day_dir)
    # Create __init__.py files
    create_init_file(year_dir)
    create_init_file(day_dir)
    template_path = "solution_template.py"
    solution_path = os.path.join(day_dir, "solution.py")
    copy_and_modify_template(year, day, template_path, solution_path)

    notebook_path = os.path.join(day_dir, "scratch_pad.ipynb")
    notebook_template_path = "scratch_pad_template.ipynb"
    copy_and_modify_template(year, day, notebook_template_path, notebook_path)
    url = f"https://adventofcode.com/{year}/day/{day}"
    logger.info("Opening Puzzle: %s", url)
    webbrowser.open(url)

    logger.info("Launching vs code...")
    os.chdir(original_dir)  # Change back to the original directory
    # subprocess.run(['jupyter', 'notebook', notebook_path])
    # update, we can run this from vs code now
    # pylint: disable=consider-using-with
    subprocess.Popen([cfg["editor"], notebook_path], start_new_session=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
