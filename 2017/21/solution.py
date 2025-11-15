"""
Advent Of Code 2017 day 21

"""

# import system modules
import time
import math

# import my modules
import aoc  # pylint: disable=import-error


def parse_rules(lines):
    """
    Function to parse rules
    """
    rules = {}
    for line in lines:
        key, value = line.split(" => ")
        # storing with \n instead of / to reduce conversions later
        rules[key.replace("/", "\n")] = value.replace("/", "\n")
    return rules


def rotate_90_degress(in_string):
    """
    Function to rotate grid 90 degrees
    """
    lines = in_string.split("\n")
    matrix = []
    for line in lines:
        matrix.append(list(char for char in line))
    matrix = [list(row) for row in zip(*matrix[::-1])]
    return "\n".join(["".join(row) for row in matrix])


def flip_horizontal(in_string):
    """
    Function to flip grid horizontally
    """
    lines = in_string.split("\n")
    matrix = [list(line) for line in lines]
    flipped_matrix = [row[::-1] for row in matrix]
    return "\n".join(["".join(row) for row in flipped_matrix])


def flip_vertical(in_string):
    """
    Function to flip grid veritcally
    """
    lines = in_string.split("\n")
    matrix = [list(line) for line in lines]
    flipped_matrix = matrix[::-1]
    return "\n".join(["".join(row) for row in flipped_matrix])


def iterations(in_string):
    """
    Iterate over possible flips and rotations
    """
    possibilities = set()
    text = str(in_string)
    for _ in range(4):
        text = rotate_90_degress(text)
        possibilities.add(text)
        possibilities.add(flip_horizontal(text))
        # tests indicated flipping vertically as well didn't
        # produce more results than just flipping horizontally
        # this shaved 8 seconds off of my time with no change
        # possibilities.add(flip_vertical(text))
    return possibilities


def join_strings(in_strings):
    """
    Function to joing strings back to larger grid
    """
    num_strings = len(in_strings)
    # Determine the size of the square (e.g., 2x2, 3x3, etc.)
    square_size = int(math.ceil(math.sqrt(num_strings)))

    work_list = []
    for in_string in in_strings:
        work_list.append(in_string.split("\n"))

    # Adjust the work_list to fit into a perfect square by adding empty strings if necessary
    while len(work_list) < square_size**2:
        work_list.append([""] * len(work_list[0]))

    result = ""

    # Combine the strings into the square
    for row_block in range(0, square_size):
        for line_idx in range(len(work_list[0])):
            combined_line = ""
            for col_block in range(0, square_size):
                combined_line += work_list[row_block * square_size + col_block][
                    line_idx
                ]
            result += combined_line + "\n"

    return result.rstrip()


def split_string(in_string):
    """
    Function to split grid into smaller grids
    """
    lines = in_string.strip().split("\n")
    num_lines = len(lines)
    if num_lines % 2 == 0:
        # Split into 2x2 squares
        square_size = 2
    else:
        # Split into 3x3 squares
        square_size = 3
    squares = []
    for i in range(0, num_lines, square_size):
        for j in range(0, len(lines[i]), square_size):
            square = []
            for k in range(square_size):
                square.append(lines[i + k][j : j + square_size])
            squares.append(square)
    return ["\n".join(square) for square in squares]


def process_string(input_string, rules):
    """
    Function to process string for one cycle
    """
    if len(input_string) in [2, 3]:
        rule = None
        for my_string in iterations(input_string):
            if my_string in rules:
                rule = rules[my_string]
                break
        return rule
    new_strings = split_string(input_string)
    expanded_strings = []
    for new_string in new_strings:
        for my_string in iterations(new_string):
            if my_string in rules:
                expanded_strings.append(rules[my_string])
    return join_strings(expanded_strings)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    my_string = """.#.
..#
###"""
    rules = parse_rules(input_value)
    counter = 5
    if part == 2:
        # part 2, increase counter
        counter = 18
    for _ in range(counter):
        my_string = process_string(my_string, rules)
    return my_string.count("#")


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017, 21)
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
