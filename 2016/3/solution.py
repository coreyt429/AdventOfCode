"""
Advent Of Code 2016 day 3

This was also already fast.  Refactoring to current format, let me simplify the logic a bit.

pylint almost ran clean the first time, only one instance of trailing-whitespace to fix
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


def parse_input(input_text):
    """
    Function to parse input
    """
    num_list = []
    num_list_2 = []
    num_list_3 = []
    number_pattern = re.compile(r"\d+")
    lines = input_text.strip().splitlines()
    for line in lines:
        num_list_2.append([int(num) for num in number_pattern.findall(line)])
        num_list.append(sorted([int(num) for num in number_pattern.findall(line)]))
    for row in range(0, len(num_list_2), 3):
        for col in range(3):
            num_list_3.append(
                sorted(
                    [
                        num_list_2[row][col],
                        num_list_2[row + 1][col],
                        num_list_2[row + 2][col],
                    ]
                )
            )
    return {1: num_list, 2: num_list_3}


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    data = parse_input(input_value)
    counter = 0
    for side_a, side_b, side_c in data[part]:
        if side_a + side_b > side_c:
            counter += 1
    return counter


YEAR = 2016
DAY = 3
input_format = {
    1: "text",
    2: "text",
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
