"""
Advent Of Code 2022 day 8

One of these days I'll read the instructions more carefully :)

"""

# import system modules
import logging
import argparse
import math

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def check_neighbor(trees, tree, direction, value):
    """Recursive function to check direction"""
    neighbors = trees.get_neighbors(point=tree, directions=[direction])
    if not neighbors:
        return True
    if trees.get_point(neighbors[direction]) >= value:
        return False
    return check_neighbor(trees, neighbors[direction], direction, value)


def max_scenic_score(trees):
    """Function to find the highest score of all trees"""
    max_score = 0
    for tree in trees:
        height = trees.get_point(tree, 0)
        tree_counts = []
        for direction in ["n", "s", "e", "w"]:
            tree_counts.append(scenic_score(trees, tree, height, direction, 0))
        # print(f"{tree}: {math.prod(tree_counts)} - {tree_counts}")
        max_score = max(max_score, math.prod(tree_counts))
    return max_score


def scenic_score(trees, tree, height, direction, counter):
    """Recursive function to get scenic score in one direction"""
    neighbors = trees.get_neighbors(point=tree, directions=[direction])
    if not neighbors:
        return counter
    if trees.get_point(neighbors[direction]) >= height:
        return counter + 1
    return scenic_score(trees, neighbors[direction], height, direction, counter + 1)


def count_visible_trees(trees):
    """Check each tree to see if it is visible, and return count of visible trees"""
    visible = set()
    for tree in trees:
        height = trees.get_point(tree, 0)
        for direction in ["n", "s", "e", "w"]:
            if check_neighbor(trees, tree, direction, height):
                visible.add(tree)
                break
    return len(visible)


def convert_to_int(trees):
    """Function to convert grid values to int()"""
    for tree in trees:
        trees.set_point(tree, int(trees.get_point(tree)))


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    trees = Grid(input_value, use_overrides=False)
    convert_to_int(trees)
    if part == 2:
        return max_scenic_score(trees)
    return count_visible_trees(trees)


YEAR = 2022
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
