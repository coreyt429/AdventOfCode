"""
Advent Of Code 2019 day 1

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


def required_fuel(mass):
    """part 1 fuel calculation"""
    return mass // 3 - 2


def required_fuel_2(mass):
    """part 2 recursive fuel calculation"""
    fuel = mass // 3 - 2
    if fuel < 0:
        return 0
    return fuel + required_fuel_2(fuel)


def parse_input(input_text):
    """
    Parse input into a list of integers.
    """
    return [int(line) for line in input_text.strip().splitlines() if line.strip()]


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    part1 = sum(required_fuel(mass) for mass in input_value)
    part2 = sum(required_fuel_2(mass) for mass in input_value)
    return part1 if part == 1 else part2


YEAR = 2019
DAY = 1
input_format = {
    1: parse_input,
    2: parse_input,
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
