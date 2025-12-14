"""
Advent Of Code 2021 day 7

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


def calc_fuel(target, positions, mode=1):
    """Function to calculate total fuel to get to a position"""
    fuel = 0
    for position in positions:
        if mode == 1:
            # Each change of 1 step in horizontal position of
            # a single crab costs 1 fuel.
            fuel += abs(position - target)
        elif mode == 2:
            # As it turns out, crab submarine engines don't burn
            # fuel at a constant rate. Instead, each change of 1
            # step in horizontal position costs 1 more unit of fuel
            # than the last: the first step costs 1, the second step
            # costs 2, the third step costs 3, and so on.
            #
            # Triangular Numbers: The n-th triangular number is the
            # sum of the integers from 1 to n
            # so the Tn = n(n+1)/2
            steps = abs(position - target)
            fuel += steps * (steps + 1) // 2
    return fuel


def find_min_fuel(positions, mode=1):
    """Function to find minimum fuel burn to get all subs to teh same position"""
    min_fuel = float("infinity")
    for position in range(min(positions), max(positions) + 1):
        fuel = calc_fuel(position, positions, mode)
        min_fuel = min(min_fuel, fuel)
    return min_fuel


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    data = [int(num) for num in input_value.split(",")]
    return find_min_fuel(data, part)


YEAR = 2021
DAY = 7
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
