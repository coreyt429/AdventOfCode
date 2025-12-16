"""
Advent Of Code 2023 day 8

"""

# import system modules
import logging
import argparse
import re
import math
from functools import reduce

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_input(data: str) -> dict:
    """parse input data into structured format"""
    retval = {}
    # Split the data into lines
    parts = data.strip().split("\n\n")

    retval["instructions"] = parts[0]

    map_data = {}
    map_regex = r"(...) = \((...), (...)\)"
    for line in parts[1].split("\n"):
        # print(line)
        coordinates = re.findall(map_regex, line)
        # print(coordinates)
        map_data[coordinates[0][0]] = {"L": coordinates[0][1], "R": coordinates[0][2]}
    retval["map"] = map_data
    return retval


def part1(parsed_data: dict) -> int:
    """Solve part 1 of the puzzle"""
    steps = 0
    position = "AAA"
    while position != "ZZZ":
        for left_right in parsed_data["instructions"]:
            steps += 1
            position = parsed_data["map"][position][left_right]
            if position == "ZZZ":
                break
    return steps


def lcm_of_list(numbers: list[int]) -> int:
    """Lease common multiple of a list of numbers"""
    return reduce(math.lcm, numbers)


def part2(parsed_data: dict) -> int:
    """Solve part 2 of the puzzle"""
    positions = []
    map_data = parsed_data["map"]
    for currpos in map_data.keys():
        if currpos[2] == "A":
            positions.append(currpos)
    results = []
    for startposition in positions:
        steps = 0
        position = startposition
        while position[2] != "Z":
            for left_right in parsed_data["instructions"]:
                steps += 1
                position = parsed_data["map"][position][left_right]
                if position[2] == "Z":
                    break
        results.append(steps)
    return lcm_of_list(results)


def part2_brute_force(parsed_data: dict) -> int:
    """Solve part 2 of the puzzle using brute force method"""
    steps = 0
    positions = []
    map_data = parsed_data["map"]
    for currpos in map_data.keys():
        if currpos[2] == "A":
            positions.append(currpos)
    proceed = True
    while proceed:
        for left_right in parsed_data["instructions"]:
            steps += 1
            print(f"Step {steps}")
            proceed = False
            for position in positions:
                position = parsed_data["map"][position][left_right]
                print(position[2])
                if position[2] != "Z":
                    proceed = True
            if not proceed:
                break
    return steps


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    parsed_data = parse_input(input_value)
    if part == 1:
        return part1(parsed_data)
    return part2(parsed_data)


YEAR = 2023
DAY = 8
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
