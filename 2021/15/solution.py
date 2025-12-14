"""
Advent Of Code 2021 day 15

Part 1 went pretty smooth.  Simple heapq shortest path problem.

Part 2 would have been much the same except for two mistakes.

1) I didn't clear the Grid() neighbor_cache, so the original grid
   edges were not returning their extended neighbors.
2) expand_grid was hard coded for the 10x10 test grid, so I was
   generating the wrong grid for the puzzle data

Not realizing these two issues, I spend a lot of time tweaking
the algorithm.  I finally gave up on it, and replemented as A*.
Which gave me the same wrong answers, just not quite as fast :(

After fixing those two mistakes, both solutions work.  The A*
solution is unusually slow, so I must have broken something
in playing with it.


"""

# import system modules
import logging
import argparse
from heapq import heappop, heappush
from queue import PriorityQueue

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid, manhattan_distance, Node  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

directions = ["n", "s", "e", "w"]


class MyNode(Node):
    """Extend Node Class"""

    def __init__(self, position, goal, parent=None, **kwargs):
        """init"""
        super().__init__(position, goal, parent, skip_scoring=True, **kwargs)
        # risk_level
        self.g_score = self.calc_g_score()
        # manhattan distance
        self.h_score = self.calc_h_score()
        self.f_score = self.calc_f_score()
        self.path_tuple = self.position
        if self.parent:
            self.path_tuple = self.parent.position, self.position

    def calc_h_score(self):
        """h score"""
        return manhattan_distance(self.position, self.goal) / 1000
        # if self.parent is None:
        #     return 100
        # return self.parent.h_score  // 2

    def calc_g_score(self):
        """g score"""
        if self.parent is None:
            return 0
        # add risk_level
        # print(self.position, self.parent.g_score, self.grid.get_point(self.position))
        return self.parent.g_score + self.grid.get_point(self.position)

    def calc_f_score(self):
        """f score"""
        return self.g_score + self.h_score


def safest_path_a_star(start, goal, grid):
    """
    Function to execute A* algorithm to detect shortest path between each pair
    Note, for now this only supports screen coordinate tuple dicts

    Args:
        start: tuple() x/y coordinate
        goal: tuple() x/y coordinate
        grid: Grid() object

    Returns:
        path: list(tuple()) x/y coordinates of path

    A* Node parameters:
        position: tuple() x/y coordinates
        g_score: int() risk_level
        h_score: int() heuristic manhattan_distance(position, goal)

    """
    # init shortest_paths and shortest_length
    shortest_paths = []
    shortest_nodes = []
    max_paths = 1
    shortest_length = float("infinity")
    # set start_node  (position, g_score, h_score)
    start_node = MyNode(start, goal, grid=grid)
    # initialize PriorityQueue
    open_set = PriorityQueue()
    # add start_node to priority_queue (f_score, node)
    open_set.put((start_node.f_score, start_node))
    # initialize closed set
    closed_set = set()

    # process open set
    while not open_set.empty():
        # get current node
        current_node = open_set.get()[1]
        if any(
            [
                current_node.loop,
                current_node.path_tuple in closed_set,
                current_node.g_score > shortest_length,
            ]
        ):
            continue

        # are we at the goal?
        if current_node.position == goal:
            path = current_node.path()
            if current_node.g_score == shortest_length:
                # add  path to shortest paths
                shortest_paths.append(path)
                shortest_nodes.append(current_node)

            elif current_node.g_score < shortest_length:
                # set shortest paths to reverse path
                shortest_paths = [path]
                shortest_nodes = [current_node]
                shortest_length = current_node.g_score
                if len(shortest_paths) == max_paths:
                    break
            continue

        # add to closed set movement from parent to current
        closed_set.add(current_node.path_tuple)
        # get neighbors
        neighbors = grid.get_neighbors(
            point=current_node.position, directions=directions
        )
        for neighbor in neighbors.values():
            if neighbor is None:
                continue
            if grid.get_point(neighbor, None, None) is None:
                continue
            for neighbor_node in current_node.get_children(neighbor):
                # skip if already closed
                if neighbor_node.path_tuple in closed_set:
                    continue
                # if not already in open_set, add it
                open_set.put((neighbor_node.f_score, neighbor_node))
    return shortest_length


def safest_path(start, end, grid):
    """Function to find the safest path's risk_level"""
    heap = []
    heappush(heap, (0, start))
    min_risk_level = float("infinity")
    visited = set()
    # visited = {}
    while heap:
        risk_level, current = heappop(heap)
        if current == end:
            min_risk_level = min(min_risk_level, risk_level)
            continue
        if (risk_level) > min_risk_level:
            continue
        if current in visited:
            continue
        visited.add(current)
        for neighbor in grid.get_neighbors(
            point=current, directions=directions
        ).values():
            heappush(heap, (risk_level + grid.get_point(neighbor), neighbor))

    return min_risk_level


def expand_grid(grid, size=5):
    """function to expand grid by 5"""
    grid.cfg["default_value"] = None
    grid.cfg["ob_default_value"] = None
    rows, cols = grid.cfg["max"]
    original_rows = rows + 1
    original_cols = cols + 1
    rows = (rows + 1) * size
    cols = (cols + 1) * size
    for y_val in range(rows):
        for x_val in range(cols):
            above = grid.get_point(
                (x_val, y_val - original_rows), default=None, ob_default=None
            )
            left = grid.get_point(
                (x_val - original_cols, y_val), default=None, ob_default=None
            )
            if above is None and left is None:
                # original block, don't change
                continue
            if above is not None:
                new_val = above + 1
            elif left is not None:
                new_val = left + 1
            if new_val == 10:
                new_val = 1
            grid.set_point((x_val, y_val), new_val)
    grid.update()
    grid.clear_neighbor_cache()


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid(input_value, use_overrides=False)
    grid.convert_to_ints()
    if part == 2:
        expand_grid(grid)
    target = tuple(grid.cfg["max"])
    start = (0, 0)
    risk_level = safest_path(start, target, grid)
    # part 2, 3036 too high
    #         3033 too high
    return risk_level


YEAR = 2021
DAY = 15
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
