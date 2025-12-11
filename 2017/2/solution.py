"""
Advent Of Code 2017 day 2

easy peasy, and pylint ran clean the first time.  Maybe I'm learning!

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


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    checksum = 0
    checksum2 = 0
    for line in input_value:
        nums = [int(num) for num in re.findall(r"(\d+)", line)]
        if not nums:
            continue
        checksum += max(nums) - min(nums)
        if part == 2:
            found = False
            for idx_1, num_1 in enumerate(nums):
                for idx_2, num_2 in enumerate(nums):
                    if idx_1 == idx_2:
                        continue
                    if num_1 % num_2 == 0:
                        checksum2 += num_1 // num_2
                        found = True
                        break
                if found:
                    break
    if part == 2:
        return checksum2
    return checksum


YEAR = 2017
DAY = 2
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
