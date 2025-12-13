"""
Advent Of Code 2015 day 2

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


def parse_input(input_text):
    """
    Function to parse input
    """
    presents = []
    for line in input_text.strip().splitlines():
        if not line:
            continue
        presents.append([int(dimension) for dimension in line.split("x")])
    return presents


def area_plus_side(present):
    """
    Function to calculate the surface area
    """
    present.sort()
    sides = []
    sides.append(2 * present[0] * present[1])  # l*w*2
    sides.append(2 * present[1] * present[2])  # w*h*2
    sides.append(2 * present[0] * present[2])  # l*h*2
    sides.append(present[0] * present[1])  # area of smallest side
    return sum(sides)


def ribbon(present):
    """
    Function to calculate ribbon length
    """
    # sort present dimensions so shortest sides are first
    present.sort()
    # calculate and return length
    return 2 * present[0] + 2 * present[1] + present[0] * present[1] * present[2]


def part1(parsed_data, _part=None):
    """
    Funciton to solve part 1
    """
    retval = 0
    for present in parsed_data:
        retval += area_plus_side(present)
    return retval


def part2(parsed_data, _part=None):
    """
    Function to solve part 2
    A present with dimensions 2x3x4 requires 2+2+3+3 = 10 feet of ribbon to wrap the present
    plus 2*3*4 = 24 feet of ribbon for the bow,
    for a total of 34 feet.
    """
    retval = 0
    for present in parsed_data:
        retval += ribbon(present)
    return retval


YEAR = 2015
DAY = 2
input_format = {
    1: parse_input,
    2: parse_input,
}

funcs = {
    1: part1,
    2: part2,
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
