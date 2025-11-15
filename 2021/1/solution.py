"""
Advent Of Code 2021 day 1

This one was pretty easy.

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    depths = [int(num) for num in input_value]
    previous = None
    increase = 0
    if part == 2:
        for idx, depth in enumerate(depths[:-2]):
            measurement = sum(depths[idx : idx + 3])
            if previous and measurement > previous:
                increase += 1
            previous = measurement
        return increase
    for depth in depths:
        if previous and depth > previous:
            increase += 1
        previous = depth
    return increase


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021, 1)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 1387, 2: 1362}
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
