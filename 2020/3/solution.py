"""
Advent Of Code 2020 day 3

Another easy one.

Grid() did the heavy lifting.  The trees_on_slope counted the trees
on the given line.

For part 2, used math.prod to get the product of the tree counts.

"""

# import system modules
import logging
import argparse
from math import prod

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def trees_on_slope(grid, slope):
    """
    Function to count the trees on a line in the map
    from (0,0) following a given slope
    """
    x_val = 0
    counter = 0
    # don't forget to add one to grid max y.  I missed this and had
    # to wait 4 minutes to submit my answer
    for y_val in range(0, grid.cfg["max"][1] + 1, slope[1]):
        # print(f"point: {(x_val, y_val)} - {grid.get_point(point=(x_val, y_val))}")
        if grid.get_point(point=(x_val, y_val)) == "#":
            counter += 1
        x_val += slope[0]
        # These aren't the only trees, though; due to something you read about once
        # involving arboreal genetics and biome stability, the same pattern repeats
        # to the right many times
        # simulate this by just looping through the x values
        x_val %= grid.cfg["max"][0] + 1
    return counter


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid(input_value, use_overrides=False)
    if part == 1:
        return trees_on_slope(grid, (3, 1))
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    return prod([trees_on_slope(grid, slope) for slope in slopes])


YEAR = 2020
DAY = 3
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
