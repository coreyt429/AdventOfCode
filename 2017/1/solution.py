"""
Advent Of Code 2017 day 1

This one was pretty easy. I sorted it all out in the scratchpad, and code translated
immediately into the solve function.  I'll go through and document, but nothing
interesting here.

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


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    digits = input_value.strip()
    if not digits:
        return 0
    numbers = [int(char) for char in digits]
    idx_offset = 1 if part == 1 else len(numbers) // 2
    total = 0
    for idx, num in enumerate(numbers):
        if num == numbers[(idx + idx_offset) % len(numbers)]:
            total += num
    return total


YEAR = 2017
DAY = 1
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
