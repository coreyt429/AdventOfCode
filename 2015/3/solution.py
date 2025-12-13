"""
Advent Of Code 2015 day 3

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


def part1(data, _part=None):
    """
    Function to solve part 1
    """
    lattitude = 0
    longitude = 0
    houses = {f"{lattitude}-{longitude}": 1}
    for char in data:
        if char == ">":
            longitude += 1
        elif char == "<":
            longitude -= 1
        elif char == "v":
            lattitude -= 1
        elif char == "^":
            lattitude += 1
        house_name = f"{lattitude}-{longitude}"
        if house_name in houses:
            houses[house_name] += 1
        else:
            houses[house_name] = 1
    return len(houses)


def part2(data, _part=None):
    """
    Function to solve part 2
    """
    vehicles = ["Santa", "RoboSanta"]
    lattitude = {"Santa": 0, "RoboSanta": 0}
    longitude = {"Santa": 0, "RoboSanta": 0}
    houses = {f"{lattitude['Santa']}-{longitude['Santa']}": 2}
    for idx, char in enumerate(list(data)):
        v_idx = idx % 2
        vehicle = vehicles[v_idx]
        if char == ">":
            longitude[vehicle] += 1
        elif char == "<":
            longitude[vehicle] -= 1
        elif char == "v":
            lattitude[vehicle] -= 1
        elif char == "^":
            lattitude[vehicle] += 1
        house_name = f"{lattitude[vehicle]}-{longitude[vehicle]}"
        if house_name in houses:
            houses[house_name] += 1
        else:
            houses[house_name] = 1
    return len(houses)


YEAR = 2015
DAY = 3
input_format = {
    1: "text",
    2: "text",
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
