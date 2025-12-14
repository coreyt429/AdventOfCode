"""
Advent Of Code 2021 day 1

This one was pretty easy.

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
    depths = [int(num) for num in input_value]
    previous = None
    increase = 0
    if part == 2:
        for idx, depth in enumerate(depths[:-2]):
            measurement = sum(depths[idx : idx + 3])
            if previous and measurement > previous:
                increase += 1
            previous = measurement
        return increase
    for depth in depths:
        if previous and depth > previous:
            increase += 1
        previous = depth
    return increase


YEAR = 2021
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
