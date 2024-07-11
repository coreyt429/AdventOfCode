"""
AdventOfCode utility Module
contains utility functions for working AdventOfCode puzzles
"""
import sys
from datetime import datetime

class AdventOfCode:
    def __init__(self, year=None, day=None):
        today = datetime.today()
        self.year = year if year is not None else today.year
        self.day = day if day is not None else today.day

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
        with self.get_file(file_name) as file:
            return file.read().rstrip().split('\n')

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

# Example usage:
# aoc = AdventOfCode()
# aoc.set_date(2021, 1)
# lines = aoc.load_lines()
# text = aoc.load_text()
