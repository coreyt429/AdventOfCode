"""
Advent Of Code 2023 day 23

"""

# import system modules
import logging
import argparse
from collections import defaultdict, deque
from functools import cache
from dataclasses import dataclass

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  , Point# pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

@dataclass
class Node:
    """
    Node class for graph
    """
    point: Point
    grid: Grid
    value: str = ""
    container: list[Point]
    neighbors: dict[Point, int]

    def __str__(self):
        return f"Node({self.point}): neighbors={list(f"{k}:{v}" for k, v in self.neighbors.items())}"

def path_exists(grid, start, end, node_points):
    """
    Check if path exists between two points without crossing other node points
    """
    
    start = (start.x, start.y) if isinstance(start, Point) else start
    end = (end.x, end.y) if isinstance(end, Point) else end

    # Ensure node_points is a concrete set (not a generator) and uses tuple coords
    node_points = set(
        (p.x, p.y) if isinstance(p, Point) else p
        for p in node_points
    )

    queue = deque()
    queue.append((start, 0))
    visited = set()
    while queue:
        current, steps = queue.popleft()
        if current == end:
            return steps
        if current in node_points and current != start and current != end:
            continue
        visited.add(current)
        neighbors = grid.get_neighbors(current, directions=["n", "s", "e", "w"])
        for neighbor in neighbors.values():
            if neighbor in visited or grid[neighbor] == "#":
                continue
            queue.append((neighbor, steps + 1))
    return 0


def grid_to_nodes(grid, start, end):
    """
    Convert grid to graph
    """
    nodes = []
    # start and end are nodes regardless.  
    nodes.append(Node(point=start, grid=grid, container=nodes, value='.', neighbors={}))
    nodes.append(Node(point=end, grid=grid, container=nodes, value='.', neighbors={}))
    for point in grid:
        if isinstance(point, tuple):
            point = Point(*point)
        if grid.get_point(point) == "#":
            continue
        # other points are nodes if they have decision points
        neighbors = {k: v for k, v in grid.get_neighbors(point, directions=["n", "s", "e", "w"]).items() if grid[v] != "#"}
        if point == Point(x=6, y=2, z=0):
            logger.debug('point: %s, value: %s, neighbors: %s', point, grid.get_point((point.x, point.y)), neighbors)
            for k, v in neighbors.items():
                logger.debug(' direction: %s, neighbor: %s value: %s',k, v, grid.get_point(v))
        
        if len(neighbors) > 2:
            node = Node(point=point, grid=grid, container=nodes, value=grid.get_point(point), neighbors={})
            nodes.append(node)
    node_values = {
        (n.point.x, n.point.y) if isinstance(n.point, Point) else (n.point[0], n.point[1])
        for n in nodes
    }
    for n_1 in nodes:
        for n_2 in nodes:
            if n_1 == n_2:
                continue
            if n_1.neighbors.get(n_2.point):
                continue
            path_length = path_exists(grid, n_1.point, n_2.point, node_values)
            if path_length > 0:
                n_1.neighbors[n_2.point] = path_length
                n_2.neighbors[n_1.point] = path_length
    logger.debug('Total nodes: %d', len(nodes))
    return nodes

def longest_path(nodes, start, end, current=None, visited=None):
    """
    Find longest path in graph from start to end
    """
    if visited is None:
        visited = set()
    if current is None:
        current = start
    visited.add(current)
    if current == end:
        return visited
    max_length = 0
    for neighbor, weight in nodes[current].neighbors.items():
        if neighbor in visited:
            continue
        path_length = longest_path(nodes, neighbor, end, visited.copy())
        if path_length + weight > max_length:
            max_length = path_length + weight
    return max_length

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return 1
    grid = Grid(input_value)
    start = grid.index(".")
    end = grid.index(".", idx=-1)
    graph = grid_to_nodes(grid, start, end)
    for k, v in graph.items():
        v.add_adjacent_nodes()

    return 1


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
