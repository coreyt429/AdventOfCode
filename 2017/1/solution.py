"""
Advent Of Code 2017 day 1

This one was pretty easy. I sorted it all out in the scratchpad, and code translated
immediately into the solve function.  I'll go through and document, but nothing
interesting here.

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


def solve(input_string, part):
    """
    Function to solve puzzle
    """
    # set index offset, this is the diffrentiator between part 1 and part 2
    idx_offset = 1
    # convert input_string into a list of integers
    int_list = [int(char) for char in input_string]
    # save list length so we don't keep calculating it
    int_list_length = len(int_list)
    # part 2, change idx_offset
    if part == 2:
        idx_offset = int_list_length // 2
    # init total
    total = 0
    # walk number list
    for idx, num in enumerate(int_list):
        # does current number match its mate?
        if num == int_list[(idx + idx_offset) % (int_list_length)]:
            # increment total
            total += num
    return total


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017, 1)
    input_text = my_aoc.load_text()
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
