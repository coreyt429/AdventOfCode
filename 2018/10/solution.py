"""
Advent Of Code 2018 day 10

"""

# import system modules
from __future__ import annotations
import logging
import argparse
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


X = 0
Y = 1
pattern_nums = re.compile(r"(-*\d+)")

# dict to store answers
answer = {1: None, 2: None}


def parse_data(lines):
    """Parse input data into list of points with position and velocity"""
    points = []
    for line in lines:
        data = [int(datum) for datum in pattern_nums.findall(line)]
        point = {"position": ((data[0]), data[1]), "velocity": (data[2], data[3])}
        points.append(point)
    return points


def advance_points(points, reverse=False):
    """Advance points by one time step"""
    for point in points:
        position = list(point["position"])
        velocity = point["velocity"]
        for axis in [X, Y]:
            if reverse:
                position[axis] -= velocity[axis]
            else:
                position[axis] += velocity[axis]
        point["position"] = tuple(position)
    return points


def string_lights(points, message="lights"):
    """Return string representation of lights"""
    retval = f"{message:}\n"
    x_values = [point["position"][X] for point in points]
    y_values = [point["position"][Y] for point in points]
    max_x = max(x_values)
    max_y = max(y_values)
    min_x = min(x_values)
    min_y = min(y_values)
    lights = [point["position"] for point in points]
    for pos_y in range(min_y, max_y + 1):
        for pos_x in range(min_x, max_x + 1):
            if (pos_x, pos_y) in lights:
                retval += "#"
            else:
                retval += "."
        retval += "\n"
    retval += "\n"
    return retval


def print_lights(points, message="lights"):
    """Print representation of lights"""
    print(f"{message:}")
    x_values = [point["position"][X] for point in points]
    y_values = [point["position"][Y] for point in points]
    max_x = max(x_values)
    max_y = max(y_values)
    min_x = min(x_values)
    min_y = min(y_values)
    lights = [point["position"] for point in points]
    for pos_y in range(min_y, max_y + 1):
        for pos_x in range(min_x, max_x + 1):
            if (pos_x, pos_y) in lights:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return answer[2]
    points = parse_data(input_value)
    last_seconds = 0
    last_diff_y = float("infinity")
    seconds = 0
    while True:
        # x_values = [point['position'][X] for point in points]
        y_values = [point["position"][Y] for point in points]
        # max_x = max(x_values)
        max_y = max(y_values)
        # min_x = min(x_values)
        min_y = min(y_values)
        # diff_x = max_x - min_x
        diff_y = max_y - min_y
        # points are moving back apart
        if diff_y > last_diff_y:
            break
        points = advance_points(points)
        last_diff_y = diff_y
        last_seconds = seconds
        seconds += 1
    points = advance_points(points, reverse=True)
    lights = string_lights(points, f"{last_seconds} seconds)")
    print(lights)
    answer[2] = last_seconds
    return "FNRGPBHR"


YEAR = 2018
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
