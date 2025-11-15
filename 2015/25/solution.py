"""
Advent Of Code 2015 25 25

This was another one that was already fast, and clean. Just changed
it to read the input file and use current structure.

"""

# import system modules
import time
import re


# import my modules
import aoc  # pylint: disable=import-error

START_CODE = 20151125
MULTIPLIER = 252533
DIVISOR = 33554393
TARGET_ROW, TARGET_COL = None, None


def solve(part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return "Press the button"
    current_code = START_CODE
    row = 1
    col = 1
    next_row = 2
    # print(current_code,row,col)
    previous_code = current_code
    while True:
        row -= 1
        col += 1
        if row < 1:
            row = next_row
            next_row += 1
            col = 1
        current_code = (previous_code * MULTIPLIER) % DIVISOR
        if row == TARGET_ROW and col == TARGET_COL:
            return current_code
        previous_code = current_code


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015, 25)
    input_text = my_aoc.load_text()
    TARGET_ROW, TARGET_COL = (int(input) for input in re.findall(r"(\d+)", input_text))
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
        answer[my_part] = funcs[my_part](my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
