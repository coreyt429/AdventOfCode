"""
Advent Of Code 2017 day 3

This one was a bit more fun.  I went with a more mathematical solution for part 1,
and that didn't work well for part 2. So I tried building a traversal routine to
make the grid, but that was too slow for part 1.  So taking different approaches
for each part.

"""

# import system modules
from __future__ import annotations
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import manhattan_distance, Grid  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)

# x/y constants
X = 0
Y = 1


def get_target_coordinates(target):
    """
    Part 1 solution.  Calculates values instead of building large grid
    """
    total = 1
    counter = 1
    new = 0
    while total < target:
        counter += 2
        new = (counter - 1) * 4
        total += new
    corner = counter // 2
    point = [corner, -1 * corner]
    diff = total - target
    if diff < counter:
        point[X] -= diff
    elif diff < counter + (counter - 2):
        offset = diff - counter
        point[X] -= counter - 1
        point[Y] += offset + 1
    elif diff < counter * 2 + (counter - 2):
        offset = diff - (counter + (counter - 2))
        point[X] -= counter - 1
        point[X] += offset
        point[Y] *= -1
    else:
        offset = diff - (counter * 2 + (counter - 2))
        point[Y] += (counter - 2) - offset
    return tuple(point)


def traverse(target):
    """
    Part 2 solultions, builds out grid so we can evaluate neighbors
    """
    grid = Grid(grid_map=[[1]], type="infinite")
    logger.debug("grid:\n%s", grid)
    current_pos = (0, 0)
    current_value = 1
    while current_value <= target:
        neighbors = grid.get_neighbors(point=current_pos, diagonals=True)
        logger.debug("neighbors: %s", neighbors)
        for k, v in neighbors.items():
            logger.debug("  %s: %s = %s", k, v, grid.map.get(v))
        neighbor_values = {
            k: grid.map.get(v)
            for k, v in neighbors.items()
            if grid.map.get(v) is not None
        }
        logger.debug("neighbor values: %s", neighbor_values)
        if not neighbor_values:
            current_value = 1
            current_pos = neighbors["e"]
            grid.set_point(current_pos, current_value)
            grid.update()
            logger.debug("grid:\n%s", grid)
            continue
        current_value = sum(neighbor_values.values())
        grid.set_point(current_pos, current_value)
        grid.update()
        logger.debug("grid:\n%s", grid)
        key = ".".join(sorted(neighbor_values.keys()))
        logger.debug("key: %s", key)
        if key in ["w", "nw.w", "nw.s.sw.w", "s.sw.w"]:
            current_pos = neighbors["n"]
            continue
        if key in ["s.sw", "e.s.se", "e.s.se.sw"]:
            current_pos = neighbors["w"]
            continue
        if key in ["e.se", "e.n.ne", "e.n.ne.se"]:
            current_pos = neighbors["s"]
            continue
        if key in ["n.ne", "n.ne.nw.w", "n.nw.w"]:
            current_pos = neighbors["e"]
            continue
    return current_value


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    target = int(input_value)
    if part == 1:
        point = get_target_coordinates(target)
        return manhattan_distance(point, (0, 0))
    return traverse(target)


YEAR = 2017
DAY = 3
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
