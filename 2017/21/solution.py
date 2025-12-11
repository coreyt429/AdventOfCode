"""
Advent Of Code 2017 day 21

"""

# import system modules
from __future__ import annotations
import logging
import argparse
import math

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)


def parse_rules(lines):
    """
    Function to parse rules
    """
    rules = {}
    for line in lines:
        key, value = line.split(" => ")
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
    return possibilities


def join_strings(in_strings):
    """
    Function to joing strings back to larger grid
    """
    num_strings = len(in_strings)
    square_size = int(math.ceil(math.sqrt(num_strings)))
    work_list = []
    for in_string in in_strings:
        work_list.append(in_string.split("\n"))
    while len(work_list) < square_size**2:
        work_list.append([""] * len(work_list[0]))
    result = ""
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
        square_size = 2
    else:
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
        for my_string in iterations(input_string):
            if my_string in rules:
                return rules[my_string]
        return None
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
    counter = 5 if part == 1 else 18
    for _ in range(counter):
        my_string = process_string(my_string, rules)
    return my_string.count("#")


YEAR = 2017
DAY = 21
input_format = {
    1: "lines",
    2: "lines",
}

funcs = {
    1: solve,
    2: solve,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    aoc = AdventOfCode(
        year=YEAR,
        day=DAY,
        input_formats=input_format,
        funcs=funcs,
        test_mode=args.test,
    )
    aoc.run(submit=args.submit)
