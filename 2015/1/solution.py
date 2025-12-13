"""
Advent Of Code 2015 day 1

"""

# import system modules
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    retval = 0
    if part == 1:
        for char in input_value:
            if char == "(":
                retval += 1
            elif char == ")":
                retval -= 1
        return retval
    floor = 0
    for i, char in enumerate(input_value):
        if char == "(":
            floor += 1
        elif char == ")":
            floor -= 1
        if floor == -1:
            retval = i + 1
            break
    return retval


YEAR = 2015
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
