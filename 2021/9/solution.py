"""
Advent Of Code 2021 day 9

convert_to_ints highlighted a bug in Grid().set_point().  The logic for detecting
an empty value was using "not value" instead of "value is None".  So when I passed
0 to it, I was getting ' ' instead of 0

Part 1, simply iterate through the points and check to see if any neighbors are
lower, if not, then it is a low point.

Part 2, used the loop from Part 1 to detect low points,

"""

# import system modules
import logging
import argparse
import math
from heapq import heappop, heappush

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def is_low_point(point, grid):
    """
    Function to check if a point is a low point
    """
    low_point = True
    for neighbor in grid.get_neighbors(
        point=point, directions=["n", "s", "e", "w"]
    ).values():
        value = grid.get_point(point)
        if value >= grid.get_point(neighbor):
            low_point = False
            break
    return low_point


def convert_to_ints(grid):
    """convert character digits to integers for mathing"""
    for point in grid:
        value = grid.get_point(point)
        grid.set_point(point, int(value))


def calculate_basin_size(point, grid):
    """Function to calculate basin_size for a low_point"""
    heap = []
    basin = set()
    directions = ["n", "s", "e", "w"]
    heappush(
        heap,
        (point, list(grid.get_neighbors(point=point, directions=directions).values())),
    )
    while heap:
        current, neighbors = heappop(heap)
        current_value = grid.get_point(current)
        # Locations of height 9 do not count as being in any basin
        if current_value == 9:
            continue
        basin.add(current)
        for neighbor in neighbors:
            if neighbor in basin:
                continue
            neighbor_value = grid.get_point(neighbor)
            # Locations of height 9 do not count as being in any basin
            if neighbor_value == 9:
                continue
            # this condition works with my input, and may be invalid for other inputs
            # my input works if I leave this condition out and just go ahead and
            # push it to the heap from here.
            # I'm leaving it in, because it is dramatically faster with this condition
            # 0.09 seconds vs 1.21 seconds
            if neighbor_value >= current_value:
                heappush(
                    heap,
                    (
                        neighbor,
                        list(
                            grid.get_neighbors(
                                point=neighbor, directions=directions
                            ).values()
                        ),
                    ),
                )
    return len(basin)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid(input_value)
    convert_to_ints(grid)
    total = 0
    basins = {}
    for point in grid:
        if is_low_point(point, grid):
            risk_level = int(grid.get_point(point)) + 1
            total += risk_level
            if part == 2:
                basins[point] = calculate_basin_size(point, grid)
    if part == 2:
        basin_sizes = list(reversed(sorted(basins.values())))
        return math.prod(basin_sizes[:3])
    # 1280 too high  >= not >  this one tripped on 9 not being less than [9, 9, 9, 9]
    return total


YEAR = 2021
DAY = 9
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
