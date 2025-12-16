"""
Advent Of Code 2023 day 18

"""

# import system modules
import logging
import argparse
import re
import math

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_input(lines: list[str]) -> list[dict[str, object]]:
    """Parse input data into a list of instructions"""
    retval = []
    # R 6 (#70c710)
    pattern = r"([RDUL]) (\d+) \((#[a-f0-9]*)\)"
    for line in lines:
        matches = re.match(pattern, line)
        # print(f'{matches.group(1)} {matches.group(2)} {matches.group(3)}')
        retval.append(
            {
                "direction": matches.group(1),
                "meters": int(matches.group(2)),
                "color": matches.group(3),
            }
        )
    return retval


def get_edge_points(instructions: list[dict[str, object]]) -> list[list[int]]:
    """Get the edge points from the instructions"""
    curr_x = 0
    curr_y = 0
    points = [[curr_x, curr_y]]
    # {'direction': 'R', 'meters': 6, 'color': '#70c710'}

    for instruction in instructions:
        if instruction["direction"] == "R":
            curr_x += instruction["meters"]
        elif instruction["direction"] == "D":
            curr_y -= instruction["meters"]
        elif instruction["direction"] == "L":
            curr_x -= instruction["meters"]
        elif instruction["direction"] == "U":
            curr_y += instruction["meters"]
        points.append([curr_x, curr_y])

    min_x = min(x for x, y in points)
    min_y = min(y for x, y in points)
    for point in points:
        point[0] += abs(min_x)
        point[1] += abs(min_y)
    return points


def picks(points: list[list[int]]) -> int:
    """Calculate the number of picks needed using Pick's Theorem"""
    # a+1-b/2 = i
    a = polygon_area(points)
    b = calculate_perimeter(points)
    assert b % 2 == 0
    i = a + 1 - (b // 2)
    return int(i + b)


def calculate_perimeter(points: list[list[int]]) -> float:
    """Calculate the perimeter of the polygon defined by the points"""
    perimeter = 0
    n = len(points)
    for i in range(n):
        # Get the current point and the next point (with wrap-around)
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        # Calculate the distance between the points
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        # Add to the total perimeter
        perimeter += distance
    return perimeter


def polygon_area(points: list[list[int]]) -> float:
    """Calculate the area of the polygon defined by the points using the shoelace formula"""
    n = len(points)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    area = abs(area) / 2.0
    return area


def solve(input_value: list[str], part: int) -> int:
    """
    Function to solve puzzle
    """
    parsed_data = parse_input(input_value)
    if part == 1:
        edge_points = get_edge_points(parsed_data)
        return picks(edge_points)
    newinstructions = []
    pattern = "#([a-f0-9]{5})([0-3])"
    directions = ["R", "D", "L", "U"]
    for instruction in parsed_data:
        matches = re.match(pattern, instruction["color"])
        newinstructions.append(
            {
                "direction": directions[int(matches.group(2))],
                "meters": int(matches.group(1), 16),
            }
        )
    edge_points = get_edge_points(newinstructions)
    return picks(edge_points)


YEAR = 2023
DAY = 18
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
