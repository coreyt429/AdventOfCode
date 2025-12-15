"""
Advent Of Code 2024 day 14

"""

# import system modules
import logging
import argparse
import re
import math

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def blank_grid(height=7, width=11):
    """Function to initialize a blank grid of a particular size"""
    grid_seed = []
    for row in range(height):
        row = []
        for _ in range(width):
            row.append(".")
        grid_seed.append(row)

    grid = Grid(grid_seed, use_overrides=False)
    return grid


pattern_digit = re.compile(r"(\-?\d+)")


def parse_input(lines):
    """Function to parse input"""
    robots = []
    for line in lines:
        values = [int(num) for num in pattern_digit.findall(line)]
        robots.append({"position": tuple(values[:2]), "velocity": tuple(values[2:])})
    return robots


def new_position(grid, current, velocity, moves):
    """Function to calculate position of a robot"""
    new = [0, 0]
    for dim in (0, 1):
        new[dim] = (current[dim] + (velocity[dim] * moves)) % (grid.cfg["max"][dim] + 1)
    return tuple(new)


def safety_factor(grid):
    """Funciton to calculate safety_factor based on grid values"""
    quadrants = [0, 0, 0, 0]
    for point, value in grid.items():
        if value == ".":
            continue
        if point[0] < grid.cfg["max"][0] // 2:
            if point[1] < grid.cfg["max"][1] // 2:
                quadrants[0] += value
            elif point[1] > grid.cfg["max"][1] // 2:
                quadrants[1] += value
        elif point[0] > grid.cfg["max"][0] // 2:
            if point[1] < grid.cfg["max"][1] // 2:
                quadrants[2] += value
            elif point[1] > grid.cfg["max"][1] // 2:
                quadrants[3] += value
    return math.prod(quadrants)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    robots = parse_input(input_value)
    grid = blank_grid(height=103, width=101)
    if part == 1:
        moves = 100
        for robot in robots:
            robot["position"] = new_position(
                grid, robot["position"], robot["velocity"], moves
            )
            current = grid.get_point(robot["position"])
            if current == ".":
                grid.set_point(robot["position"], 1)
            else:
                grid.set_point(robot["position"], current + 1)
        return safety_factor(grid)
    moves = 1000000
    for robot in robots:
        robot["position"] = new_position(
            grid, robot["position"], robot["velocity"], 7000
        )
    for move in range(7000, moves):
        for point in grid:
            grid.set_point(point, ".")
        for robot in robots:
            robot["position"] = new_position(
                grid, robot["position"], robot["velocity"], 1
            )
            current = grid.get_point(robot["position"])
            if current == ".":
                grid.set_point(robot["position"], 1)
            else:
                grid.set_point(robot["position"], current + 1)
        if "111111111111111111111" in str(grid):
            return move + 1
    return part


YEAR = 2024
DAY = 14
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
