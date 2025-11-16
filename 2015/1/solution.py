"""
Advent Of Code 2015 day 1

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    retval = 0
    if part == 1:
        for char in input_value:
            if char == "(":
                retval += 1
            elif char == ")":
                retval -= 1
        return retval
    floor = 0
    for i, char in enumerate(input_value):
        if char == "(":
            floor += 1
        elif char == ")":
            floor -= 1
        if floor == -1:
            retval = i + 1
            break
    return retval


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015, 1)
    input_text = my_aoc.load_text()
    # print(input_text)
    # input_lines = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
