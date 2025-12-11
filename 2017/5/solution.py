"""
Advent Of Code 2017 day 5

"""

# import system modules
from __future__ import annotations
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)


def follow_jumps(offsets, part=1):
    """
    function to follow jump values
    """
    idx = 0
    counter = 0
    while 0 <= idx < len(offsets):
        idx2 = idx + offsets[idx]
        if part == 2 and offsets[idx] >= 3:
            offsets[idx] -= 1
        else:
            offsets[idx] += 1
        counter += 1
        idx = idx2
    return counter


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    return follow_jumps(list(input_value), part)


YEAR = 2017
DAY = 5
input_format = {
    1: "integers",
    2: "integers",
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
