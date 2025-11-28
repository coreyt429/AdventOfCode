"""
AdventOfCode utility Module
contains utility functions for working AdventOfCode puzzles
"""

import sys
import json
import re
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
        self.start_time = time.time()

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

    def post(self, url, data=None):
        """post to url using session"""
        return self.session.post(url, data=data)

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

    def __init__(self, year=None, day=None, input_formats=None, funcs=None):
        self.session = AdventOfCodeSession(os.getenv("AOC_SESSION_ID"), year, day)
        self.parts = {1: 1, 2: 2}
        self.answer = {1: None, 2: None}
        self.correct = {1: None, 2: None}
        self.funcs = funcs or {1: None, 2: None}
        input_formats = input_formats or {1: "lines", 2: "lines"}
        self.inputs = {}
        for k, v in input_formats.items():
            if callable(v):
                self.inputs[k] = v(self.load_text())
            elif v == "lines":
                self.inputs[k] = self.load_lines()
            elif v == "integers":
                self.inputs[k] = self.load_integers()
            elif v == "grid":
                self.inputs[k] = self.load_grid()
            elif v == "text":
                self.inputs[k] = self.load_text()
            else:
                raise ValueError(f"Unknown input format: {v}")
        self.fetch_answers()

    def _parse_submit_status(self, html_text):
        """
        Parse the HTML response from an answer submission to determine the result.
        """
        status = "unknown"
        message = ""
        # Heuristics based on AoC response texts.
        if "That's the right answer" in html_text:
            status = "correct"
            message = "That's the right answer!"
        elif "That's not the right answer" in html_text:
            status = "incorrect"
            if "too low" in html_text:
                status = "too_low"
                message = "That's not the right answer; your answer is too low."
            elif "too high" in html_text:
                status = "too_high"
                message = "That's not the right answer; your answer is too high."
            else:
                message = "That's not the right answer."
        elif "You gave an answer too recently" in html_text:
            status = "wait"
            # AoC usually tells you how long to wait in the same paragraph.
            message = (
                "You submitted too recently; AoC wants you to wait before trying again."
            )
        elif (
            "You already completed it" in html_text
            or "Did you already complete it" in html_text
        ):
            status = "already_solved"
            message = "This puzzle level is already marked as solved."
        elif "You don't seem to be solving the right level" in html_text:
            status = "bad_level"
            message = "This answer was submitted for the wrong level."
        else:
            message = "Submission response could not be classified; check the AoC page for details."

        return status, message

    def submit(self, part=1, answer=None):
        """
        Submit an answer for the given part to Advent of Code.

        If `answer` is not provided, the value from self.answer[part] is used.

        Behavior:
        - POSTs the answer to AoC.
        - Parses the HTML for feedback (right/wrong, too high/low, wait, etc.).
        - If correct, updates self.correct[part] and answers.json cache.

        Returns:
            dict: {
                "status": one of
                    "correct", "incorrect", "too_high", "too_low",
                    "wait", "already_solved", "bad_level", "error", "unknown",
                "message": short human-readable message (str),
            }
        """
        if part not in self.parts:
            raise ValueError(
                f"Invalid part: {part!r}. Expected one of {sorted(self.parts)}"
            )

        if answer is None:
            answer = self.answer.get(part)

        if answer is None:
            raise ValueError(
                f"No answer available for part {part}; pass answer=... or run your solver first."
            )

        url = f"https://adventofcode.com/{self.session.year}/day/{self.session.day}/answer"
        payload = {"level": str(part), "answer": str(answer)}
        logger.debug("url: %s payload: %s", url, payload)
        try:
            response = self.session.post(url, data=payload)
        except Exception as exc:  # pylint: disable=broad-except
            logger.warning("Failed to submit answer to %s: %s", url, exc)
            return {"status": "error", "message": f"Submission failed: {exc}"}

        if response.status_code != 200:
            msg = f"Unexpected status {response.status_code} when submitting answer."
            logger.warning(msg)
            return {"status": "error", "message": msg}

        text = response.text
        logger.debug("Submission response text: %s", text)
        status, message = self._parse_submit_status(text)

        # If correct (or AoC says already solved and we provided a value),
        # update in-memory correct answers and the answers.json cache.
        if status in {"correct", "already_solved"} and self.correct.get(part) is None:
            self.correct[part] = answer

            # Persist into {year}/{day}/answers.json
            dir_path = os.path.join(str(self.session.year), str(self.session.day))
            answers_path = os.path.join(dir_path, "answers.json")
            try:
                os.makedirs(dir_path, exist_ok=True)
                cached = {}
                if os.path.exists(answers_path):
                    try:
                        with open(answers_path, "r", encoding="utf-8") as f:
                            cached = json.load(f)
                    except json.JSONDecodeError as exc:  # corrupt cache, start over
                        logger.warning(
                            "Failed to parse %s as JSON (%s); recreating cache",
                            answers_path,
                            exc,
                        )
                        cached = {}
                cached[str(part)] = answer
                with open(answers_path, "w", encoding="utf-8") as f:
                    json.dump(cached, f, ensure_ascii=False, indent=2)
                logger.info(
                    "Updated cached answer for year %s day %s part %s in %s",
                    self.session.year,
                    self.session.day,
                    part,
                    answers_path,
                )
            except OSError as exc:
                logger.warning(
                    "Failed to write answers cache %s: %s", answers_path, exc
                )

        logger.info(
            "Submit result for year %s day %s part %s: %s",
            self.session.year,
            self.session.day,
            part,
            status,
        )

        if message:
            print(message)

        return {"status": status, "message": message}

    def fetch_answers(self):
        """
        Attempt to fetch the known answers for this puzzle from the Advent of Code
        web page for the current year/day, caching them in answers.json so we
        don't have to scrape the page every time.

        Any parts found will be stored in self.correct[part]. Parts not found
        will be set to None.

        Returns:
            dict: A mapping from part number (1, 2) to the extracted answer
                  (string or int), or None if not available.
        """
        # Default all parts to None up front
        for part in self.parts:
            self.correct[part] = None

        # Path for cached answers: {year}/{day}/answers.json
        dir_path = os.path.join(str(self.session.year), str(self.session.day))
        answers_path = os.path.join(dir_path, "answers.json")

        # Try to load cached answers first
        try:
            with open(answers_path, "r", encoding="utf-8") as f:
                cached = json.load(f)
            # cached is expected to be a dict with string keys "1", "2"
            for part in self.parts:
                key = str(part)
                if key in cached:
                    self.correct[part] = cached[key]
            logger.debug(
                "Loaded cached answers for year %s day %s from %s",
                self.session.year,
                self.session.day,
                answers_path,
            )
            return self.correct
        except FileNotFoundError:
            # No cache yet; we'll fetch from the web
            pass
        except json.JSONDecodeError as exc:
            logger.warning(
                "Failed to parse %s as JSON (%s); ignoring cache and refetching",
                answers_path,
                exc,
            )

        # No usable cache; fetch from the AoC puzzle page
        url = f"https://adventofcode.com/{self.session.year}/day/{self.session.day}"
        try:
            response = self.session.get(url)
        except Exception as exc:  # pylint: disable=broad-except
            logger.warning("Failed to fetch puzzle page %s: %s", url, exc)
            return self.correct

        if response.status_code != 200:
            logger.warning(
                "Unexpected status %s while fetching puzzle page %s",
                response.status_code,
                url,
            )
            return self.correct

        # AoC typically embeds solved answers like:
        #   "Your puzzle answer was <code>12345</code>."
        # (One occurrence per solved part, part 1 first, then part 2.)
        matches = re.findall(
            r"Your puzzle answer was <code>(.*?)</code>",
            response.text,
        )

        for idx, raw_answer in enumerate(matches, start=1):
            if idx not in self.parts:
                # Ignore any unexpected extras
                continue
            # Store as int when possible, otherwise keep as string.
            ans_value = raw_answer.strip()
            try:
                ans_value = int(ans_value)
            except ValueError:
                # Non-numeric answers (occasionally appear) stay as strings.
                pass
            self.correct[idx] = ans_value
            logger.info(
                "Fetched AoC answer for year %s day %s part %s: %r",
                self.session.year,
                self.session.day,
                idx,
                ans_value,
            )

        # Persist answers to answers.json so we don't need to re-fetch
        try:
            os.makedirs(dir_path, exist_ok=True)
            cache_payload = {str(part): self.correct[part] for part in self.parts}
            with open(answers_path, "w", encoding="utf-8") as f:
                json.dump(cache_payload, f, ensure_ascii=False, indent=2)
            logger.debug(
                "Cached answers for year %s day %s to %s",
                self.session.year,
                self.session.day,
                answers_path,
            )
        except OSError as exc:
            logger.warning("Failed to write answers cache %s: %s", answers_path, exc)

        return self.correct

    def run(self, submit=False):
        """
        Function to run the functions for each part
        """
        # loop parts
        for part in self.parts:
            # log start time
            self.session.start_time = time.time()
            # get answer
            self.answer[part] = self.funcs[part](self.inputs[part], part)
            # log end time
            end_time = time.time()
            logger.info(
                "%d.%dPart %s: %s, took %.5f seconds",
                self.session.year,
                self.session.day,
                part,
                self.answer[part],
                end_time - self.session.start_time,
            )
            if submit:
                result = self.submit(part=part, answer=self.answer[part])
                if result["status"] == "correct":
                    logger.info("Part %s submitted successfully.", part)
                else:
                    logger.info("Part %s submission result: %s", part, result["status"])
            assert self.correct[part] == self.answer[part]

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

    content = content.replace("9999", str(year))
    content = content.replace("99", str(day))

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
