"""
Advent Of Code 2025 day 4

"""

# import system modules
import logging
import argparse


# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def get_removable_rolls(grid):
    """
    Docstring for get_removable_rolls

    :param grid: Grid()
    :return: set of points to remove
    """
    removed = set()
    for point in grid:
        if grid[point] == "@":
            neighbors = grid.get_neighbors(point=point, diagonal=True)
            count = 0
            for neighbor in neighbors.values():
                if grid[neighbor] == "@":
                    count += 1
            if count < 4:
                removed.add(point)
    return removed


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid(input_value)
    if part == 1:
        return len(get_removable_rolls(grid))
    removed = True
    while removed:
        removed = False
        for point in get_removable_rolls(grid):
            removed = True
            grid[point] = "x"
    counter = 0
    for point in grid:
        if grid[point] == "x":
            counter += 1
    return counter


YEAR = 2025
DAY = 4
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
