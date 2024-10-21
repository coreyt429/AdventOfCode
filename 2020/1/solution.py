"""
Advent Of Code 2020 day 1

"""
# import system modules
import time
from itertools import combinations
from math import prod
# import my modules
import aoc # pylint: disable=import-error

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    numbers = [int(line) for line in input_value]
    factors = 2
    if part == 2:
        # what is the product of the three entries that sum to 2020
        factors = 3
    for nums in combinations(numbers, factors):
        # find the two entries that sum to 2020
        if sum(nums) == 2020:
            # and then multiply those two numbers together.
            return prod(nums)
    return None

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020,1)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {
        1: 1,
        2: 2
    }
    # dict to store answers
    answer = {
        1: None,
        2: None
    }
    # correct answers once solved, to validate changes
    correct = {
        1: 691771,
        2: 232508760
    }
    # dict to map functions
    funcs = {
        1: solve,
        2: solve
    }
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
