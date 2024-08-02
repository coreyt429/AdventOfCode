"""
Advent Of Code 2016 day 3

This was also already fast.  Refactoring to current format, let me simplify the logic a bit.

pylint almost ran clean the first time, only one instance of trailing-whitespace to fix
"""
# import system modules
import time
import re

# import my modules
import aoc # pylint: disable=import-error

def parse_input(lines):
    """
    Function to parse input
    Args:
        lines - list of strings
    
    Returns:
        num_list  - list of integers
        num_list3 - list of integers
    """
    num_list = []
    num_list_2 = []
    num_list_3 = []
    number_pattern = re.compile(r'\d+')
    for line in lines:
        num_list_2.append([int(num) for num in number_pattern.findall(line)])
        num_list.append(sorted([int(num) for num in number_pattern.findall(line)]))
    for row in range(0, len(num_list_2), 3):
        for col in range(3):
            num_list_3.append(
                sorted([
                    num_list_2[row][col],
                    num_list_2[row + 1][col],
                    num_list_2[row + 2][col]
                ])
            )
    return num_list, num_list_3

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    data = {}
    data[1], data[2] = parse_input(input_value)
    counter = 0
    for side_a, side_b, side_c in data[part]:
        if side_a + side_b > side_c:
            counter += 1
    return counter

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2016,3)
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
