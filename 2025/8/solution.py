"""
Advent Of Code 2025 day 8

"""

# import system modules
import logging
import argparse
from math import prod
from itertools import combinations
import numpy as np
from scipy.spatial.distance import pdist, squareform


def calculate_distances(points):
    coords = np.array([(p.x, p.y, p.z) for p in points])
    dists = squareform(pdist(coords))

    pairs = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            pairs.append(((points[i], points[j]), dists[i, j]))

    pairs.sort(key=lambda item: item[1])
    return dict(pairs)


# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import linear_distance_numpy as linear_distance  # pylint: disable=import-error
from grid import Point  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

# global for TEST  so we can use it deeper in functions
TEST = False


def get_points_from_input(input_value):
    """
    Function to parse input into list of Points
    """
    points = []
    for line in input_value:
        x_str, y_str, z_str = line.split(",")
        point = Point(int(x_str), int(y_str), int(z_str))
        points.append(point)
    return points


def calculate_distances(points):
    """
    Function to calculate distances between all points
    arguments:
        points: list of Point objects
    returns:
        dict with keys as (Point, Point) tuples and Float values as distances
    """
    coords = np.array([(p.x, p.y, p.z) for p in points])
    dists = squareform(pdist(coords))

    pairs = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            pairs.append(((points[i], points[j]), dists[i, j]))

    pairs.sort(key=lambda item: item[1])
    return dict(pairs)


def calculate_distances_old(points):
    """
    Function to calculate distances between all points
    arguments:
        points: list of Point objects
    returns:
        dict with keys as (Point, Point) tuples and Float values as distances
    """
    dist = linear_distance
    distances = [((a, b), dist(a, b)) for a, b in combinations(points, 2)]
    distances.sort(key=lambda item: item[1])
    return dict(distances)


def can_merge(connections):
    """
    Function to determine if two connections can be merged
    """
    seen = set()
    for point in [point for connection in connections for point in connection]:
        if point in seen:
            return True
        seen.add(point)
    return False


def merged_connection(connections):
    """
    Function to merge connections that share points
    """
    merged = True
    while merged:
        merged = False
        new_connections = []
        while connections:
            current = set(connections.pop())
            for other in connections[:]:
                if current.intersection(other):
                    current.update(other)
                    connections.remove(other)
                    merged = True
            new_connections.append(current)
        connections = new_connections
    return connections


def add_connection(connections, p1, p2):
    """
    Function to add connections
    """
    found = False
    for connection in connections:
        if p1 in connection or p2 in connection:
            connection.add(p1)
            connection.add(p2)
            logger.debug(
                "Adding to existing connection %s for points: %s, %s",
                len(connection),
                p1,
                p2,
            )
            found = True
            break
    if not found:
        logger.debug("Creating new connection for points: %s, %s", p1, p2)
        connections.append(set([p1, p2]))


def part_2(points, distance_map):
    """
    Function to solve part 2
    """
    connections = []
    last_pair = None
    for pair in distance_map.keys():
        logger.debug("Processing pair: %s", pair)
        add_connection(connections, *pair)
        if can_merge(connections):
            connections = merged_connection(connections)
            logger.debug("Merged connections, total now: %d", len(connections))
        if len(connections) == 1 and len(connections[0]) == len(points):
            logger.debug("All points connected.")
            last_pair = pair
            break
    p1, p2 = last_pair
    return p1.x * p2.x


def part_1(points, distance_map):
    """
    Function to solve part 1
    """
    connections = []
    connection_limit = 1000
    if TEST:
        connection_limit = 10
    for pair in list(distance_map.keys())[:connection_limit]:
        logger.debug("Processing pair: %s", pair)
        add_connection(connections, *pair)
    if can_merge(connections):
        connections = merged_connection(connections)
        logger.debug("Merged connections, total now: %d", len(connections))
    for p in points:
        in_connection = any(p in connection for connection in connections)
        if not in_connection:
            connections.append(set([p]))
            logger.debug("Adding isolated point as new connection: %s", p)
    logger.debug("Total Connections: %s", len(connections))
    sizes = []
    for connection in connections:
        sizes.append(len(connection))
        logger.debug("Size: %d, Connection: %s", len(connection), connection)
    sizes.sort(reverse=True)
    logger.debug("All sizes: %s", sizes)
    logger.debug("Top 3 sizes: %s", sizes[:3])
    logger.debug("points: %s <-> %s", len(points), sum(sizes))
    return prod(sizes[:3])


# globals to cache input parsing and distance calculations
input_points = []
initial_distance_map = {}


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # these don't change between parts, so cache them globally
    # shaves 1.3 seconds off total runtime
    if not input_points:
        logger.debug("Parsing input points")
        input_points.extend(get_points_from_input(input_value))
    if not initial_distance_map:
        logger.debug("Calculating initial distance map")
        initial_distance_map.update(calculate_distances(input_points))
    if part == 1:
        return part_1(input_points, initial_distance_map)
    return part_2(input_points, initial_distance_map)


YEAR = 2025
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
    TEST = args.test
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
