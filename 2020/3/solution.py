"""
Advent Of Code 2020 day 3

Another easy one.

Grid() did the heavy lifting.  The trees_on_slope counted the trees
on the given line.

For part 2, used math.prod to get the product of the tree counts.

"""

# import system modules
import time
from math import prod

# import my modules
import aoc  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error


def trees_on_slope(grid, slope):
    """
    Function to count the trees on a line in the map
    from (0,0) following a given slope
    """
    x_val = 0
    counter = 0
    # don't forget to add one to grid max y.  I missed this and had
    # to wait 4 minutes to submit my answer
    for y_val in range(0, grid.cfg["max"][1] + 1, slope[1]):
        # print(f"point: {(x_val, y_val)} - {grid.get_point(point=(x_val, y_val))}")
        if grid.get_point(point=(x_val, y_val)) == "#":
            counter += 1
        x_val += slope[0]
        # These aren't the only trees, though; due to something you read about once
        # involving arboreal genetics and biome stability, the same pattern repeats
        # to the right many times
        # simulate this by just looping through the x values
        x_val %= grid.cfg["max"][0] + 1
    return counter


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid(input_value, use_overrides=False)
    if part == 1:
        return trees_on_slope(grid, (3, 1))
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    return prod([trees_on_slope(grid, slope) for slope in slopes])
    # result = 1
    # for slope in slopes:
    #     result *= trees_on_slope(grid, slope)
    # return result


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020, 3)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 252, 2: 2608962048}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
