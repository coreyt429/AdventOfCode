"""
Advent Of Code 2022 day 8

One of these days I'll read the instructions more carefully :)

"""

# import system modules
import time
import math

# import my modules
import aoc  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error


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


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2022, 8)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 1798, 2: 259308}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
