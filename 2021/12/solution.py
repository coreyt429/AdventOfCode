"""
Advent Of Code 2021 day 12

Part 1, I tripped on not building reverse maps for the caves.
Other than that, fairly simple heapq implementation to build the
path list.

Part 2, Counter() made this easy.  Just count the .islower()
nodes in the path.  If it is > 1 skip the small cave.

"""

# import system modules
import logging
import argparse
from heapq import heappop, heappush
from collections import defaultdict, Counter

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def find_paths(cave_map, mode=1):
    """Function to identify valid paths through the cave system"""
    paths = []
    heap = []
    heappush(heap, (0, "start", ""))
    while heap:
        step, node, path = heappop(heap)
        new_path = f"{path},{node}".replace(",start", "start")
        if node == "end":
            paths.append(new_path)
            continue
        # It would be a waste of time to visit any small cave more than once
        if node.islower():
            # print(f"node: {node} is lowercase")
            if node in path and mode == 1:
                # print(f"node: {node} is in {path}")
                continue

            if node in path and mode == 2:
                # print(f"node: {node} is in {path}")
                # After reviewing the available paths, you realize you might
                # have time to visit a single small cave twice.
                if node in ["start", "end"]:
                    # However, the caves named start and end can only be visited exactly
                    # once each: once you leave the start cave, you may not return to it,
                    # and once you reach the end cave, the path must end immediately.
                    continue
                # Specifically, big caves can be visited any number of times, a single small
                # cave can be visited at most twice, and the remaining small caves
                # can be visited at most once.
                counter = Counter(
                    [tmp_node for tmp_node in path.split(",") if tmp_node.islower()]
                )
                # print(f"max counter: {counter.values()}")
                if max(counter.values()) > 1:
                    # print(f"not adding {node} to {path}")
                    continue
        # add possible next steps
        for next_node in cave_map[node]:
            # print(f"node: {node}, next_node: {next_node}")
            heappush(heap, (step + 1, next_node, new_path))
    return paths


def build_cave_map(lines):
    """Function to build cave map from text input"""
    cave_map = defaultdict(list)
    for line in lines:
        node, path = line.split("-")
        cave_map[node].append(path)
        # add reverse mapping as well
        cave_map[path].append(node)
    return cave_map


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    cave_map = build_cave_map(input_value)
    paths = find_paths(cave_map, part)
    path_count = len(paths)
    return path_count


YEAR = 2021
DAY = 12
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
