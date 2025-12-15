"""
Advent Of Code 2023 6

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
logger.debug("Advent of Code Template Version %s", TEMPLATE_VERSION)


def parse_input(data):
    """pare input for part 1"""
    lines = data.strip().split("\n")
    time_values = [int(value) for value in lines[0].split()[1:]]
    distance_values = [int(value) for value in lines[1].split()[1:]]
    return list(zip(time_values, distance_values))


def parse_input2(data):
    """pare input for part 2"""
    lines = data.strip().replace(" ", "").split("\n")
    time_values = [int(value) for value in lines[0].split(":")[1:]]
    distance_values = [int(value) for value in lines[1].split(":")[1:]]
    return list(zip(time_values, distance_values))


def solve(input_value, _):
    """
    Function to solve puzzle
    """
    retval = 1
    for time, distance in input_value:
        wins = 0
        for ms in range(1, time):
            if ms * (time - ms) > distance:
                wins += 1
        retval *= wins
    return retval


YEAR = 2023
DAY = 6
input_format = {
    1: parse_input,
    2: parse_input2,
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
