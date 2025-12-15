"""
Advent Of Code 2023 day 1

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

pattern_digit = re.compile(r"(\d)")


def calibrate(lines):
    """
    Function to calibrate weather machine
    """
    total = 0
    for line in lines:
        digits = pattern_digit.findall(line)
        if digits:
            # If not empty, proceed with your operation
            digit = digits[0] + digits[-1]
        else:
            # Handle the case where the list is empty
            digit = 0
        total += int(digit)
    return total


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    lines = input_value
    if part == 2:
        num_strs = [
            "zero",
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
        ]
        lines = []
        for line in input_value:
            for idx, num_str in enumerate(num_strs):
                line = line.replace(num_str, num_str[0] + str(idx) + num_str[-1])
            lines.append(line)
    return calibrate(lines)


YEAR = 2023
DAY = 1
input_format = {
    1: "lines",
    2: "lines",
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
