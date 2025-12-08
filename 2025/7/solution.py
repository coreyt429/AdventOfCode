"""
Advent Of Code 2025 day 7

"""

# import system modules
import logging
import argparse
from copy import deepcopy
from collections import defaultdict

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

nodes = {}


class Node:
    """
    Node class for graph traversal
    """

    def __init__(self, point, grid):
        self.point = point
        self.grid = grid
        self.children = []
        self.timelines = 0
        self.find_children()

    def add_child(self, child_node):
        """
        Add a child node
        """
        self.children.append(child_node)

    def add_child_point(self, child_point):
        """
        Add a child node by point
        """
        if child_point in nodes:
            child_node = nodes[child_point]
        else:
            child_node = Node(child_point, self.grid)
            nodes[child_point] = child_node
        if child_node not in self.children:
            self.add_child(child_node)

    def get_children(self):
        """
        List child node
        """
        yield from sorted(self.children)

    def find_children(self):
        """
        Find child nodes
        """
        neighbors = self.grid.get_neighbors(point=self.point, diagonal=True)
        if "s" not in neighbors:
            return
        if self.grid[neighbors["s"]] == ".":
            child_point = neighbors["s"]
            self.add_child_point(child_point)
        elif self.grid[neighbors["s"]] == "^":
            for direction in ["sw", "se"]:
                if direction not in neighbors:
                    continue
                neighbor = neighbors.get(direction)
                if neighbor and self.grid[neighbor] == ".":
                    child_point = neighbor
                    self.add_child_point(child_point)

    def __hash__(self):
        return hash(self.point)

    def __str__(self):
        my_str = (
            f"Node({self.point}): children=["
            f"{''.join([str(child.point) for child in self.children])}]"
        )
        return my_str

    def __lt__(self, other):
        if self.point[0] < other.point[0]:
            return True
        if self.point[0] == other.point[0]:
            return self.point[1] < other.point[1]
        return False


def count_splits_oop_dag(grid):
    """
    Count splits using OOP DAG traversal
    """
    start_point = find_start(grid)
    start_node = Node(start_point, grid)
    nodes[start_point] = start_node
    p1_counter = 0
    for node in nodes.values():
        logger.debug("Node: %s", node)
        if len(node.children) > 1:
            p1_counter += 1
    logger.debug("Number of splits: %s", p1_counter)
    return p1_counter


def count_timelines_oop_dag(grid):
    """
    Count timelines using OOP DAG traversal
    """
    start_point = find_start(grid)
    start_node = Node(start_point, grid)
    nodes[start_point] = start_node
    start_node.timelines = 1
    total_timelines = 0

    for point in grid:
        if point in nodes:
            node = nodes[point]
            if len(node.children) == 0:
                # Leaf node
                total_timelines += node.timelines
            else:
                for child in node.get_children():
                    child.timelines += node.timelines
    return total_timelines


def is_tachyon(point, grid):
    """
    Determine if a point is a tachyon
    """
    return grid[point] in ("S", "|")


def is_bottom_row(point, grid):
    """
    Determine if a point is in the bottom row
    """
    logger.debug("Point %s max_y %s", point, grid.cfg["max"])
    return point[1] == grid.cfg["max"][1]


def find_start(grid):
    """
    Find the start point 'S' in the grid
    """
    for p in grid:
        if grid[p] == "S":
            return p
    raise ValueError("No start S found")


def count_timelines_dp(grid):
    """
    Dag traversal counting number of timelines reaching bottom row

    :param grid: Grid() object
    """
    # Find start
    start = find_start(grid)

    # ways[(x, y)] = number of ways to have a tachyon at that cell
    ways = defaultdict(int)
    ways[start] = 1

    # Process row by row downward
    # assuming y increases downward, like you used in is_bottom_row
    for y in range(start[1], grid.cfg["max"][1]):
        # Collect only points on this row that currently have ways>0
        current_row_points = [(x, yy) for (x, yy) in ways.keys() if yy == y]
        if not current_row_points:
            continue

        new_ways = defaultdict(int)

        for point in current_row_points:
            if ways[point] == 0:
                continue

            neighbors = grid.get_neighbors(point=point, diagonal=True)
            s = neighbors["s"]
            s_val = grid[s]

            if s_val == ".":
                # Continue straight down
                new_ways[s] += ways[point]

            elif s_val == "^":
                # Split diagonally if spots are open
                for direction in ["sw", "se"]:
                    if direction not in neighbors:
                        continue
                    neighbor = neighbors[direction]
                    if grid[neighbor] == ".":
                        new_ways[neighbor] += ways[point]

        # Merge new_ways into ways (or just replace row slice)
        for p, c in new_ways.items():
            ways[p] += c

    # At the bottom row, sum all ways
    total = 0
    for (_, y), c in ways.items():
        if y == grid.cfg["max"][1]:
            total += c
    return total


def count_timelines(grid, overrides=None):
    """
    Count the number of timelines in the grid
    This works, but the problem explodes combinatorially very quickly.
    """
    logger.debug("Counting timelines with overrides: %s", overrides)
    grid.cfg["use_overrides"] = True
    completed = set()
    if overrides is None:
        overrides = {}
    grid.overrides = overrides
    last_tachyon = get_last_tachyon(grid, overrides=overrides)
    logger.debug("Last tachyon at %s", last_tachyon)
    if is_bottom_row(last_tachyon, grid):
        logger.debug("  Tachyon at bottom row, timeline complete")
        completed.add(str(grid))
    else:
        neighbors = grid.get_neighbors(point=last_tachyon, diagonal=True)
        logger.debug("  Neighbors: %s", neighbors)
        if grid[neighbors["s"]] == ".":
            logger.debug("\n%s", grid)
            logger.debug("  %s Moving south to %s", last_tachyon, neighbors["s"])
            new_overrides = deepcopy(overrides)
            new_overrides[neighbors["s"]] = "|"
            completed.update(count_timelines(grid, overrides=new_overrides))
        elif grid[neighbors["s"]] == "^":
            for direction in ["sw", "se"]:
                if direction not in neighbors:
                    continue
                neighbor = neighbors.get(direction)
                if neighbor and grid[neighbor] == ".":
                    logger.debug("\n%s", grid)
                    logger.debug("  overrides: %s", overrides)
                    logger.debug(
                        "  %s Moving %s to %s", last_tachyon, direction, neighbor
                    )
                    new_overrides = deepcopy(overrides)
                    new_overrides[neighbor] = "|"
                    completed.update(count_timelines(grid, overrides=new_overrides))
                else:
                    logger.debug(
                        "  %s Blocked to the %s at %s: %s",
                        last_tachyon,
                        direction,
                        neighbor,
                        grid[neighbor],
                    )
        else:
            logger.debug(
                "  %s Blocked going south at %s: %s",
                last_tachyon,
                neighbors["s"],
                grid[neighbors["s"]],
            )
            raise ValueError("No valid moves for tachyon")
    logger.debug("\n%s", grid)
    return completed


def get_last_tachyon(grid, overrides=None):
    """
    Get the last tachyon in the grid
    """
    logger.debug("Getting last tachyon with overrides: %s", overrides)
    last_tachyon = None
    if overrides is not None and len(overrides) > 0:
        logger.debug("Using overrides: %s", overrides)
        for point in overrides:
            if last_tachyon is None:
                last_tachyon = point
            x, y = last_tachyon
            if point[1] > y or (point[1] == y and point[0] > x):
                last_tachyon = point
        logger.debug("Last tachyon with overrides at %s", last_tachyon)
        return last_tachyon
    for point in grid:
        if is_tachyon(point, grid):
            last_tachyon = point
    return last_tachyon


def count_splits(grid):
    """
    Count the number of splits in the grid
    """
    counter = 0
    timelines = defaultdict(int)
    for point in grid:
        logger.debug("Point %s: %s", point, grid[point])
        if is_tachyon(point, grid) and not is_bottom_row(point, grid):
            # this should only happen at the start
            if point not in timelines:
                timelines[point] = 1
                logger.debug("  New timeline at %s", point)
            neighbors = grid.get_neighbors(point=point, diagonal=True)
            if grid[neighbors["s"]] == ".":
                grid[neighbors["s"]] = "|"
                # Move the timelines down
                timelines[neighbors["s"]] += timelines[point]
                logger.debug(
                    "  Move timeline at %s to %s: %s",
                    point,
                    neighbors["s"],
                    timelines[neighbors["s"]],
                )
                continue
            if grid[neighbors["s"]] == "^":
                counter += 1
                for direction in ["sw", "se"]:
                    if direction not in neighbors:
                        continue
                    neighbor = neighbors.get(direction)
                    if neighbor and grid[neighbor] in (".", "|"):
                        grid[neighbor] = "|"
                        # Split the timelines
                        timelines[neighbor] += timelines[point]
                        logger.debug(
                            "  Split timeline at %s to %s: %s",
                            point,
                            neighbor,
                            timelines[neighbor],
                        )
                    else:
                        logger.debug(
                            "  Blocked to the %s at %s: %s",
                            direction,
                            neighbor,
                            grid[neighbor],
                        )
    logger.debug("Final timelines: %s", timelines)
    logger.debug("grid:\n%s", grid)
    timeline_count = sum(
        timelines[point] for point in timelines if is_bottom_row(point, grid)
    )
    logger.debug("Total timelines reaching bottom: %s", timeline_count)
    return counter


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid(input_value, use_overrides=False)
    logger.debug("\n%s", grid)
    if part == 2:
        return count_timelines_oop_dag(grid)

    if part == 2:
        return count_timelines_dp(grid)
    return count_splits_oop_dag(grid)


YEAR = 2025
DAY = 7
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
