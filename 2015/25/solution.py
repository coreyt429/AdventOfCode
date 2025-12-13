"""
Advent Of Code 2015 25 25

This was another one that was already fast, and clean. Just changed
it to read the input file and use current structure.

"""

# import system modules
import logging
import argparse
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

START_CODE = 20151125
MULTIPLIER = 252533
DIVISOR = 33554393


def parse_input(input_text):
    """
    Function to parse target row and column
    """
    row, col = (int(value) for value in re.findall(r"(\d+)", input_text))
    return row, col


def solve(target, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return "Press the button"
    target_row, target_col = target
    current_code = START_CODE
    row = 1
    col = 1
    next_row = 2
    # print(current_code,row,col)
    previous_code = current_code
    while True:
        row -= 1
        col += 1
        if row < 1:
            row = next_row
            next_row += 1
            col = 1
        current_code = (previous_code * MULTIPLIER) % DIVISOR
        if row == target_row and col == target_col:
            return current_code
        previous_code = current_code


YEAR = 2015
DAY = 25
input_format = {
    1: parse_input,
    2: parse_input,
}

funcs = {
    1: solve,
    2: solve,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    aoc = AdventOfCode(
        year=YEAR,
        day=DAY,
        input_formats=input_format,
        funcs=funcs,
        test_mode=args.test,
    )
    aoc.run(submit=args.submit)
