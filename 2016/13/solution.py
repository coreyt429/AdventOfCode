"""
Advent Of Code 2016 day 13

"""

import logging
import argparse
from heapq import heappop, heappush
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_input(input_text):
    """
    Return integer seed value.
    """
    return int(input_text.strip())


def is_wall(point, seed):
    """
    Function to determine if a point is a wall or open space
    Find x*x + 3*x + 2*x*y + y + y*y.
    Add the office designer's favorite number (seed).
    Find the binary representation of that sum; count the number of bits that are 1.
    If the number of bits that are 1 is even, it's an open space.
    If the number of bits that are 1 is odd, it's a wall.
    """
    point_x, point_y = point
    int_value = point_x**2 + 3 * point_x + 2 * point_x * point_y + point_y + point_y**2
    int_value += seed
    one_count = bin(int_value)[2:].count("1")
    return one_count % 2 == 1


def neighbors(point, seed):
    """
    Funcition to return valid neighbors for a point
    """
    set_neighbors = set()
    for p_x in [point[0] + 1, point[0] - 1]:
        if p_x >= 0:
            if not is_wall((p_x, point[1]), seed):
                set_neighbors.add((p_x, point[1]))

    for p_y in [point[1] + 1, point[1] - 1]:
        if p_y >= 0:
            if not is_wall((point[0], p_y), seed):
                set_neighbors.add((point[0], p_y))
    return set_neighbors


def solve(seed, part):
    """
    Function to solve puzzle
    For part == 1, we are doing a bfs to find the minimum steps to get to (31, 39)
    For part == 2, we run our bfs, but we are only interested in the count of
    locations we can reach in 50 steps or less.
    """
    start = (1, 1)
    target = (31, 39)
    visited = set()
    heap = []
    heappush(heap, (0, start, ()))
    min_steps = float("infinity")
    while heap:
        steps, point, path = heappop(heap)
        # How many locations (distinct x,y coordinates, including your starting location)
        # can you reach in at most 50 steps?
        if part == 2 and steps > 50:
            continue
        visited.add(point)
        if point == target:
            min_steps = min(steps, min_steps)
            continue
        new_path = tuple(list(path) + [point])
        for neighbor in neighbors(point, seed):
            if neighbor not in visited:
                heappush(heap, (steps + 1, neighbor, new_path))
    if part == 1:
        return min_steps
    # part 2
    return len(visited)


YEAR = 2016
DAY = 13
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
