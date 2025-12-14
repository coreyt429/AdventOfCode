"""
Advent Of Code 2022 day 12

Struggled on this one with a simple miss.  We can only go up one level, but we
can apparently go down more. Which was stated in the rules, I just misunderstood.

I was thinking my input was bad, because I got the right anser by changing 1 character.
Until I ran my input through the solution from u/themanushiya, and found that it worked.
reviewing I saw that solution was just checking for the next step to be less than current + 1.

I made that change in my code, and it worked.

part 2 takes longer than I would like, but I'll likely leave it for now.
Maybe not, I forgot I did the work to make Grid hashable, so lru_cache worked for get_next()

"""

# import system modules
import logging
import argparse
from heapq import heappop, heappush
from functools import lru_cache
from string import ascii_lowercase

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def calc_values():
    """Function to calculate height values"""
    base = ord("a") - 1
    values = {char: ord(char) - base for char in ascii_lowercase}
    values["S"] = values["a"]
    values["E"] = values["z"]
    return values


@lru_cache(maxsize=None)
def get_next(grid, current):
    """Function to get next points to try"""
    current_height = grid.get_point(current)
    values = calc_values()
    neighbors = grid.get_neighbors(point=current, directions=["n", "s", "e", "w"])
    next_points = []
    for neighbor in neighbors.values():
        if values[grid.get_point(neighbor)] <= values[current_height] + 1:
            next_points.append(neighbor)
    return next_points


@lru_cache(maxsize=None)
def shortest_path(grid, start, goal):
    """Function to calculate shortest path"""
    heap = []
    heappush(heap, (0, start))
    min_path = float("infinity")
    visited = set()
    while heap:
        steps, current = heappop(heap)

        # print(len(heap), steps, current, grid.get_point(current))
        if current == goal:
            # print(f"reached goal in {steps}")
            min_path = min(min_path, steps)
            return min_path
        if current in visited:
            # print("already been here, discarding")
            continue
        visited.add(current)
        for next_point in get_next(grid, current):
            heappush(heap, (steps + 1, next_point))
    return min_path


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid(input_value, use_overrides=False)
    start = None
    goal = None
    low_points = set()
    for point in grid:
        char = grid.get_point(point)
        if char == "S":
            start = point
            low_points.add(point)
        if char == "E":
            goal = point
        if char == "a":
            low_points.add(point)
    if part == 1:
        return shortest_path(grid, start, goal)
    # part 2, iterate over lowest points to find the shortest path
    shortest = float("infinity")
    for point in low_points:
        shortest = min(shortest, shortest_path(grid, point, goal))
    return shortest


YEAR = 2022
DAY = 12
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
