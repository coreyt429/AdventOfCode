"""
Advent Of Code 2024 day 10

In my failure to read instructions, I essentially solved part 2 before part 1.
After a bit of debugging on the example data, a reread of the instructions
pointed out the problem.  This made part 2, a little bit easy.

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


def convert_to_int(grid):
    """Function to convert grid values to integers."""
    for point, value in grid.items():
        if isinstance(value, str) and value.isdigit():
            grid.set_point(point, int(value))


def find_trailheads(grid):
    """Function to identifiy trailheads on a map."""
    for point, value in grid.items():
        if value == 0:
            yield point


def count_trails(grid, point, history=()):
    """Function to count trails recursively."""
    paths = set()
    current = grid.get_point(point)
    history += (point,)
    if current == 9:
        return {history}

    neighbors = grid.get_neighbors(point=point, directions=["n", "s", "e", "w"])
    for neighbor in neighbors.values():
        value = grid.get_point(neighbor)
        if value == current + 1:
            paths.update(count_trails(grid, neighbor, history))

    return paths


def solve(input_value, part):
    """
    Function to solve puzzle.
    """
    grid = Grid(input_value, use_overrides=False)
    convert_to_int(grid)
    score = 0
    for point in find_trailheads(grid):
        paths = count_trails(grid, point)
        if part == 1:
            end_points = set()
            for path in paths:
                end_points.add(path[-1])
            score += len(end_points)
        elif part == 2:
            score += len(paths)
    return score


YEAR = 2024
DAY = 10
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
