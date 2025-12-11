"""
Advent Of Code 2018 day 25

"""

# import system modules
from __future__ import annotations
import logging
import argparse
from collections import deque

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import manhattan_distance  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_data(lines):
    """parse input data"""
    points = []
    for line in lines:
        data = [int(num) for num in line.split(",")]
        points.append(tuple(data))
    return points


def group_points(points, distance_threshold=3):
    """
    Function to group points into constellations
    """
    # init visited and groups
    visited = set()
    groups = []

    def bfs(start_point):
        """breadth first search"""
        # init queue and group
        queue = deque([start_point])
        group = []
        # process queue
        while queue:
            # get next point
            point = queue.popleft()
            # check visited
            if point in visited:
                continue
            # add to visited and group
            visited.add(point)
            group.append(point)

            # Check all other points to see if they are within the threshold distance
            for neighbor in points:
                if (
                    neighbor not in visited
                    and manhattan_distance(point, neighbor) <= distance_threshold
                ):
                    queue.append(neighbor)
        return group

    # walk points
    for point in points:
        # if not visited
        if point not in visited:
            # get group
            group = bfs(point)
            # append group
            groups.append(group)

    return groups


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return part
    constellations = group_points(parse_data(input_value))
    return len(constellations)


YEAR = 2018
DAY = 25
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
