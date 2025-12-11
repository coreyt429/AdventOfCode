"""
Advent Of Code 2017 day 9

Oh boy, regex fun.

"""

# import system modules
from __future__ import annotations
import logging
import argparse
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)


def prep_string(in_string):
    """
    Function to prep string
    """
    out_string = re.sub(r"!.", "", in_string)
    out_string = re.sub(r"<[^>]*>", "", out_string)
    return out_string


def score_string(in_string):
    """
    Function to score string
    """
    total = 0
    points = 0
    for char in in_string:
        if char == "{":
            points += 1
        if char == "}":
            total += points
            points -= 1
    return total


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        out_string = re.sub(r"!.", "", input_value)
        matches = re.findall(r"<([^>]*)>", out_string)
        return sum(len(tmp_string) for tmp_string in matches)
    new_string = prep_string(input_value)
    return score_string(new_string)


YEAR = 2017
DAY = 9
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
