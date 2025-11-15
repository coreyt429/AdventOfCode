"""
Advent Of Code 2023 day 1

"""

# import system modules
import time
import re

# import my modules
import aoc  # pylint: disable=import-error

pattern_digit = re.compile(r"(\d)")


def calibrate(lines):
    """
    Function to calibrate weather machine
    """
    total = 0
    for line in lines:
        digits = pattern_digit.findall(line)
        if len(digits) > 0:
            # If not empty, proceed with your operation
            digit = digits[0] + digits[-1]
        else:
            # Handle the case where the list is empty
            digit = 0
        total += int(digit)
    return total


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    lines = input_value
    if part == 2:
        num_strs = [
            "zero",
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
        ]
        lines = []
        for line in input_value:
            for idx, num_str in enumerate(num_strs):
                line = line.replace(num_str, num_str[0] + str(idx) + num_str[-1])
            lines.append(line)
    return calibrate(lines)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2023, 1)
    # fetch input
    input_lines = my_aoc.load_lines()
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
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
