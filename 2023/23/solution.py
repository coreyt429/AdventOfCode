"""
Advent Of Code 2023 day 23

"""

# import system modules
import logging
import argparse
from collections import deque

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid, Point  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

nodes = {}


class Node:
    """
    Node class for graph
    """

    def __init__(
        self, point: Point, grid: Grid, container: list[Point], value: str = ""
    ):
        if not isinstance(point, Point):
            point = Point(*point)
        self.point = point
        self.grid = grid
        self.value = value
        self.container = container
        self.neighbors = {}
        self.idx = None

    @property
    def key(self):
        """return (x, y) tuple as key"""
        return (self.point.x, self.point.y)

    def __str__(self):
        return (
            f"Node({self.point}): neighbors="
            f"{list(f'{k}:{v}' for k, v in self.neighbors.items())}"
        )


def find_node_paths(grid, start, node_points, ignore_slopes=False):
    """
    Find paths from start to all other nodes
    """
    start = (start.x, start.y) if isinstance(start, Point) else start
    # Ensure node_points is a concrete set (not a generator) and uses tuple coords
    node_points = set((p.x, p.y) if isinstance(p, Point) else p for p in node_points)
    queue = deque()
    queue.append((start, 0))
    visited = set()
    next_nodes = {}
    while queue:
        current, steps = queue.popleft()
        if current in node_points and current != start:
            next_nodes[current] = steps
            continue
        visited.add(current)
        neighbors = grid.get_neighbors(current, directions=["n", "s", "e", "w"])
        logger.debug(
            "At %s, value: %s, ignore_slopes: %s", current, grid[current], ignore_slopes
        )
        if not ignore_slopes and grid[current] in direction_map:
            # only allow movement in the direction of the slope
            dir_allowed = direction_map[grid[current]]
            neighbors = {k: v for k, v in neighbors.items() if k == dir_allowed}
            logger.debug(
                "  slope detected, only allowing direction %s, neighbors: %s",
                dir_allowed,
                neighbors,
            )
        for neighbor in neighbors.values():
            if neighbor in visited or grid[neighbor] == "#":
                continue
            queue.append((neighbor, steps + 1))
    logger.debug("Found neighbors from %s: %s", start, next_nodes)
    return next_nodes


direction_map = {
    "^": "n",
    "v": "s",
    "<": "w",
    ">": "e",
}


def grid_to_nodes(grid, start, end, ignore_slopes=False):
    """
    Convert grid to graph
    """
    nodes.clear()
    # start and end are nodes regardless.
    start_node = Node(point=start, grid=grid, container=nodes, value=".")
    nodes[start_node.key] = start_node
    end_node = Node(point=end, grid=grid, container=nodes, value=".")
    nodes[end_node.key] = end_node
    for point in grid:
        if isinstance(point, tuple):
            point = Point(*point)
        if grid.get_point(point) == "#":
            continue
        # other points are nodes if they have decision points
        neighbors = {
            k: v
            for k, v in grid.get_neighbors(
                point, directions=["n", "s", "e", "w"]
            ).items()
            if grid[v] != "#"
        }
        if len(neighbors) > 2:
            node = Node(
                point=point,
                grid=grid,
                container=nodes,
                value=grid.get_point(point),
            )
            nodes[node.key] = node
    node_values = {
        (n.point.x, n.point.y) if isinstance(n, Node) else (n[0], n[1]) for n in nodes
    }
    for n_1 in nodes.values():
        n_1.neighbors = find_node_paths(
            grid, n_1.key, node_values, ignore_slopes=ignore_slopes
        )
    logger.debug("Total nodes: %d", len(nodes))
    for idx, point in enumerate(nodes.keys()):
        nodes[point].idx = idx


def longest_path(start, end, current=None, visited=0, length_so_far=0):
    """
    Find longest path in graph from start to end
    """
    logger.debug(
        "longest_path called: start=%s, end=%s, current=%s, visited=%s",
        start,
        end,
        current,
        visited,
    )
    if current is None:
        current = start
    logger.debug("Visiting node %s(%s)", type(current), current)
    visited = visited | (1 << nodes[current].idx)
    if current == end:
        logger.debug("Reached end: %s", visited)
        # Here we need to sum the weights of the path
        return length_so_far
    max_length = 0
    logger.debug("node keys: %s", list(nodes.keys()))
    logger.debug(
        "At node %s, neighbors: %s, visited: %s",
        current,
        nodes[current].neighbors,
        visited,
    )
    for neighbor in nodes[current].neighbors.keys():
        logger.debug("Checking neighbor %s in %s", neighbor, visited)
        if visited & (1 << nodes[neighbor].idx):
            continue
        max_length = max(
            max_length,
            longest_path(
                start,
                end,
                neighbor,
                visited,
                length_so_far + nodes[current].neighbors[neighbor],
            ),
        )
    return max_length


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    ignore_slopes = False
    if part == 2:
        ignore_slopes = True
    grid = Grid(input_value)
    start = grid.index(".")
    end = grid.index(".", idx=-1)
    grid_to_nodes(grid, start, end, ignore_slopes=ignore_slopes)
    return longest_path(start, end)


YEAR = 2023
DAY = 23
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
