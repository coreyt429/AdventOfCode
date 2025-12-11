"""
Advent Of Code 2018 day 1

"""

# import system modules
from __future__ import annotations
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
    # Starting with a frequency of zero
    frequency = 0
    if part == 1:
        # what is the resulting frequency after all of the changes in frequency have been applied?
        for change in input_value:
            frequency += change
        return frequency
    # part 2:
    # What is the first frequency your device reaches twice?
    # set to track history
    already_seen = set([frequency])
    # Note that your device might need to repeat its list of frequency changes many times before a
    # duplicate frequency is found
    while True:
        # run changes
        for change in input_value:
            # add change to frequency
            frequency += change
            # have we seen this frequency?
            if frequency in already_seen:
                # return it
                return frequency
            # add to already seen
            already_seen.add(frequency)


YEAR = 2018
DAY = 1
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
