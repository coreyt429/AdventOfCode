"""
Advent Of Code 2016 day 1

This was another newer solution, so it is already pretty efficient.
Just repackaged into my current format.
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


HEADING_DIRECTIONS = {
    "N": {"L": "W", "R": "E"},
    "S": {"L": "E", "R": "W"},
    "E": {"L": "N", "R": "S"},
    "W": {"L": "S", "R": "N"},
}

DIRECTIONAL_MOVEMENTS = {
    "N": {"x": 0, "y": 1},
    "S": {"x": 0, "y": -1},
    "E": {"x": 1, "y": 0},
    "W": {"x": -1, "y": 0},
}


def parse_input(input_text):
    """
    Parse input text into (turn, steps) tuples.
    """
    return [
        (direction[0], int(direction[1:]))
        for direction in input_text.strip().split(", ")
    ]


def follow_direction(direction, block_count, fd_x, fd_y, heading):
    """
    follow direction
    """
    heading = HEADING_DIRECTIONS[heading][direction]
    visited_blocks = set()
    for _ in range(block_count):
        fd_x += DIRECTIONAL_MOVEMENTS[heading]["x"]
        fd_y += DIRECTIONAL_MOVEMENTS[heading]["y"]
        visited_blocks.add((fd_x, fd_y))
    return fd_x, fd_y, heading, visited_blocks


def solve(directions, part):
    """
    Function to solve puzzle
    """
    my_x = 0
    my_y = 0
    my_heading = "N"
    path = [(my_x, my_y)]
    visited = {(my_x, my_y)}
    part2_coord = None
    for my_direction, blocks in directions:
        my_x, my_y, my_heading, visits = follow_direction(
            my_direction, blocks, my_x, my_y, my_heading
        )
        path.append((my_x, my_y))
        for coord in visits:
            if coord in visited:
                if part2_coord is None:
                    part2_coord = coord
            visited.add(coord)
    part1 = abs(my_x) + abs(my_y)
    part2 = abs(part2_coord[0]) + abs(part2_coord[1]) if part2_coord else None
    return part1 if part == 1 else part2


YEAR = 2016
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
