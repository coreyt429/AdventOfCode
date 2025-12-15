"""
Advent Of Code 2024 day 16

"""

# import system modules
import logging
import argparse
from heapq import heappop, heappush

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

answer = {1: None, 2: None}


def has_duplicates(test_tup):
    """Function to check for duplicates"""
    return len(test_tup) != len(set(test_tup))


def shortest_path(grid, start, goal):
    """Find all shortest paths with the minimum score in the maze."""
    heap = []
    best_paths = []
    heappush(heap, (0, start, "e", (start,)))
    seen = {}
    min_path_score = float("infinity")

    while heap:
        current = {}
        current["score"], current["point"], current["direction"], current["path"] = (
            heappop(heap)
        )

        if current["score"] > min_path_score:
            continue

        if current["point"] == goal:
            if current["score"] < min_path_score:
                min_path_score = current["score"]
                best_paths = [current["path"]]
            elif current["score"] == min_path_score:
                best_paths.append(current["path"])
            continue

        signature = (current["point"], current["direction"])
        if signature in seen and seen[signature] < current["score"]:
            continue
        seen[signature] = current["score"]

        neighbors = grid.get_neighbors(
            point=current["point"], directions=["n", "s", "e", "w"]
        )

        forward_point = neighbors[current["direction"]]
        if (
            forward_point not in current["path"]
            and grid.get_point(point=forward_point) != "#"
        ):
            heappush(
                heap,
                (
                    current["score"] + 1,
                    forward_point,
                    current["direction"],
                    current["path"] + (forward_point,),
                ),
            )

        turns = ["e", "w"] if current["direction"] in ["n", "s"] else ["n", "s"]
        for turn in turns:
            neighbor = neighbors[turn]
            if (
                neighbor not in current["path"]
                and grid.get_point(point=neighbor) != "#"
            ):
                heappush(
                    heap,
                    (current["score"] + 1000, current["point"], turn, current["path"]),
                )

    return min_path_score, best_paths


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return answer[part]
    maze = Grid(input_value, use_overrides=False)
    start = None
    goal = None
    for point, char in maze.items():
        if char == "S":
            start = point
        if char == "E":
            goal = point
        if all([start is not None, goal is not None]):
            break
    score, paths = shortest_path(maze, start, goal)
    points = set()
    print(f"{len(paths)} paths")
    for path in paths:
        for point in path:
            points.add(point)
    answer[2] = len(points)
    return score


YEAR = 2024
DAY = 16
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
