"""
Advent Of Code 2023 day 16

20251216:  I didnt' feel up to cleaning up my old slow code from script.py.
So I rewrote it from scratch using a precalculated path approach which is much
faster and cleaner.

"""

# import system modules
import sys
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

sys.setrecursionlimit(5000)

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

direction_map = {
    ".": {"n": ("n",), "s": ("s",), "e": ("e",), "w": ("w",)},
    "|": {"n": ("n",), "s": ("s",), "e": ("n", "s"), "w": ("n", "s")},
    "-": {"n": ("e", "w"), "s": ("e", "w"), "e": ("e",), "w": ("w",)},
    "/": {"n": ("e",), "s": ("w",), "e": ("n",), "w": ("s",)},
    "\\": {"n": ("w",), "s": ("e",), "e": ("s",), "w": ("n",)},
}

precalculated_paths = {}


def calculate_paths(grid):
    """
    Precalculate all paths through the grid
    """
    for point in grid:
        cell = grid[point]
        neighbors = grid.get_neighbors(point=point, include_diagonals=False)
        logger.debug(
            "Calculating paths for %s at %s: %s",
            cell,
            point,
            direction_map.get(cell, {}),
        )
        for direction in direction_map.get(cell, {}):
            next_points = []
            for next_direction in direction_map[cell][direction]:
                if next_direction not in neighbors:
                    continue
                next_point = neighbors.get(next_direction)
                next_points.append((next_point, next_direction))
            precalculated_paths[(point, direction)] = next_points
            logger.debug("  %s going %s -> %s", point, direction, next_points)
        # logger.debug("Precalculated paths: %s", precalculated_paths)


def trace_path(grid, start_pos, direction):
    """
    Trace a path through the grid from start_pos in the given direction
    """
    logger.debug(
        "Tracing path from %s going %s: %s", start_pos, direction, grid[start_pos]
    )
    heap = []
    heap.append((start_pos, direction))
    path = set()
    while heap:
        current_pos, direction = heap.pop()
        if (current_pos, direction) in path or current_pos is None:
            continue
        path.add((current_pos, direction))
        logger.debug(
            "At %s (%s) going %s: %s",
            current_pos,
            grid[current_pos],
            direction,
            precalculated_paths.get((current_pos, direction), []),
        )
        for item in precalculated_paths.get((current_pos, direction), []):
            heap.append(item)
    return path


def points_energized(grid, start_pos, direction):
    """
    Calculate number of points energized from start_pos in given direction
    """
    path = trace_path(grid, start_pos, direction)
    points = set()
    for point, _ in path:
        points.add(point)
    return len(points)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid(input_value, use_overrides=False)
    if not precalculated_paths:
        calculate_paths(grid)
    if part == 1:
        return points_energized(grid, (0, 0), "e")
    max_energized = 0
    for point in grid:
        directions = []
        if point[0] == (grid.cfg["min"][0]):
            directions.append("e")
        if point[0] == (grid.cfg["max"][0]):
            directions.append("w")
        if point[1] == (grid.cfg["min"][1]):
            directions.append("s")
        if point[1] == (grid.cfg["max"][1]):
            directions.append("n")
        for direction in directions:
            energized = points_energized(grid, point, direction)
            logger.debug(
                "From %s going %s energizes %d points", point, direction, energized
            )
            max_energized = max(max_energized, energized)
    return max_energized


YEAR = 2023
DAY = 16
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
