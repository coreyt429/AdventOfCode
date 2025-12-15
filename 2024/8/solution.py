"""
Advent Of Code 2024 day 8

Part 1, it took a few iterations to detemine if I should int() or round() in a couple
of places.

Part 2, was made easy by my approach to part 1.  I already had all the points that
were rounded to the line.  I just had to check them to be sure they were "exactly"
collinnear.  Luckily I already had a function in my grid module for that.

"""

# import system modules
import logging
import argparse
from collections import defaultdict
from itertools import combinations

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid, linear_distance, are_collinear  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def get_line(p_1, p_2, grid):
    """Function to get the points colinear to two points"""
    d_x = p_2[0] - p_1[0]
    d_y = p_2[1] - p_1[1]
    slope = d_y / d_x
    intercept = p_1[1] - slope * p_1[0]
    x_range = (grid.cfg["min"][0], grid.cfg["max"][0])
    y_range = (grid.cfg["min"][1], grid.cfg["max"][1])
    points = []
    for x_val in range(x_range[0], x_range[1] + 1):
        y_val = slope * x_val + intercept
        y_val = round(y_val)
        if y_range[0] <= y_val <= y_range[1]:
            points.append((x_val, y_val))
    return points


def is_antinode(point, pair):
    """Function to check if a point is an antinode for a pair"""
    if point in pair:
        return False
    distances = []
    for node in pair:
        distances.append(linear_distance(point, node))
    distances.sort()
    return abs(distances[1] / distances[0]) == 2


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid(input_value, use_overrides=False)
    signal_points = defaultdict(set)
    for point, char in grid.items():
        if char != ".":
            signal_points[char].add(point)

    antinodes = set()
    for points in signal_points.values():
        for pair in combinations(points, 2):
            for point in get_line(*pair, grid):
                if is_antinode(point, pair):
                    antinodes.add(point)
                if part == 2 and are_collinear(point, *pair):
                    antinodes.add(point)
    return len(antinodes)


YEAR = 2024
DAY = 8
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
