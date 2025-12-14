"""
Advent Of Code 2019 day 20

Grid() made pretty quick work of this one.

find_portals identifies the portals, and makes a reverse map:
    point -> portal
    portal -> [points]

shortest path is a basic dijkstra with added logic for stepping through the portals.

For part 2, I just had to add the logic to make the portals walls, or warps to a new
level, and add the level into the heap and seen structures.

"""

# import system modules
import logging
import argparse
import string
from heapq import heappop, heappush

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def find_portals(grid):
    """
    Function to identify portals in the map
    """
    portals = {}
    for point in grid:
        current = grid.get_point(point)
        if current in string.ascii_uppercase:
            neighbors = grid.get_neighbors(
                point=point, directions=["n", "s", "e", "w"], invalid=" #"
            )
            if len(neighbors) == 2:
                # north - south or east - west
                if "n" in neighbors:
                    if grid.get_point(point=neighbors["n"]) == ".":
                        label = f"{current}{grid.get_point(point=neighbors['s'])}"
                        portal_point = neighbors["n"]
                    else:
                        label = f"{grid.get_point(point=neighbors['n'])}{current}"
                        portal_point = neighbors["s"]
                else:
                    if grid.get_point(point=neighbors["w"]) == ".":
                        label = f"{current}{grid.get_point(point=neighbors['e'])}"
                        portal_point = neighbors["w"]
                    else:
                        label = f"{grid.get_point(point=neighbors['w'])}{current}"
                        portal_point = neighbors["e"]
                if label not in portals:
                    portals[label] = []
                portals[label].append(portal_point)
                portals[portal_point] = label
    return portals


def is_outer_portal(point, grid, portals):
    """
    Function to determine if a point is an outside portal
    """
    if point not in portals:
        return False
    label = portals[point]
    # changed to false, so AA and ZZ are considered at level 0
    if label in ["AA", "ZZ"]:
        return False
    # top or left
    if point[0] < 3 or point[1] < 3:
        return True
    # right or bottom
    if point[0] > grid.cfg["max"][0] - 3 or point[1] > grid.cfg["max"][1] - 3:
        return True
    return False


def get_other_end(point, portals):
    """
    Function to get the opposite point in a portal connection
    """
    if point not in portals:
        return None
    portal = portals[point]
    for other in portals[portal]:
        if other == point:
            continue
        return other
    return None


def shortest_path(grid, portals, start, goal, part):
    """
    Function to find shortest path
    """
    heap = []
    seen = set()
    heappush(heap, (0, 0, start))
    min_steps = float("infinity")
    while heap:
        steps, level, current_point = heappop(heap)
        # print(steps, level, current_point)
        if part == 2:
            # when at the outermost level, only the outer labels AA and ZZ function
            if level == 0 and is_outer_portal(current_point, grid, portals):
                continue
            # At any other level, AA and ZZ count as walls
            if level > 0 and current_point in portals["AA"] + portals["ZZ"]:
                continue
        else:
            level = 0
        if steps > min_steps or (level, current_point) in seen:
            # print(f"{current_point} in {seen}")
            continue
        seen.add((level, current_point))
        if current_point == goal:
            min_steps = min(steps, min_steps)

        point = get_other_end(current_point, portals)
        if point:
            # At any other level, AA and ZZ count as walls,
            # but the other outer labeled tiles bring you one level outward.
            if is_outer_portal(current_point, grid, portals):
                heappush(heap, (steps + 1, level - 1, point))
            else:
                heappush(heap, (steps + 1, level + 1, point))
        neighbors = grid.get_neighbors(
            point=current_point,
            directions=["n", "s", "e", "w"],
            invalid=" #" + string.ascii_uppercase,
        )
        # print(neighbors)
        for point in neighbors.values():
            heappush(heap, (steps + 1, level, point))
    return min_steps


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid(input_value, use_overrides=False)
    portals = find_portals(grid)
    return shortest_path(grid, portals, portals["AA"][0], portals["ZZ"][0], part)


def parse_input(input_text):
    """
    Return list of map lines.
    """
    return [line.rstrip("\n") for line in input_text.splitlines() if line.strip()]


YEAR = 2019
DAY = 20
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
