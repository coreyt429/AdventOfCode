"""
Advent Of Code 2021 day 2

Pylint 10.00/10 without making changes, I think that is a first.

For part two, h_val doesn't change. So we just need to calculate
the depth differently.

Added answer[2] storing to short circuit the second pass.  What's
a minutes work to shave milliseconds :)
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

# dict to store answers
answer = {1: None, 2: None}


def parse_data(lines):
    """function to parse data"""
    course = []
    for line in lines:
        command, value = line.split(" ")
        course.append(tuple([command, int(value)]))
    return tuple(course)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return answer[2]
    course = parse_data(input_value)
    h_val = 0
    depth = {1: 0, 2: 0}
    aim = 0
    for step in course:
        command, value = step
        # forward X increases the horizontal position by X units.
        # forward X does two things:
        #     It increases your horizontal position by X units.
        #     It increases your depth by your aim multiplied by X.
        if command == "forward":
            h_val += value
            depth[2] += aim * value
        # down X increases the depth by X units.
        # down X increases your aim by X units.
        elif command == "down":
            depth[1] += value
            aim += value
        # up X decreases the depth by X units.
        # up X decreases your aim by X units.
        elif command == "up":
            depth[1] -= value
            aim -= value
        answer[2] = h_val * depth[2]
    return h_val * depth[part]


YEAR = 2021
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
