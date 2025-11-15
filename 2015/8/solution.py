"""
Advent Of Code 2015 day 8

"""

# import system modules
import time
import re


# import my modules
import aoc  # pylint: disable=import-error

pattern_hex = re.compile(r"(\\x[0-9a-f]{2})")
WHITESPACE_CHARS = " \t\n\r"  # Space, tab, newline, carriage return


def part1(parsed_data):
    """
    Function to dolve part 1
    """
    replacement_pairs = (("\\\\", "#"), (r"\"", "#"), ('"', ""))
    sums = {1: 0, 2: 0}
    for line in parsed_data:
        sums[1] += len(line)
        for replace_pair in replacement_pairs:
            line = line.replace(*replace_pair)
        line = pattern_hex.sub("#", line)
        for char in WHITESPACE_CHARS:
            line = line.replace(char, "")
        sums[2] += len(line)
    return sums[1] - sums[2]


def part2(parsed_data):
    """
    Function to solve part 2
    """
    replacement_pairs = (
        ("\\\\", "#"),
        ('"', "%"),
        ('"', '\\"'),
        ("#", "\\\\\\\\"),
        ("%", '"\\"'),
    )
    sums = {1: 0, 2: 0}
    for line in parsed_data:
        sums[1] += len(line)
        for replace_pair in replacement_pairs:
            line = line.replace(*replace_pair)
        line = pattern_hex.sub("\\\\\\\\xNN", line)
        for char in WHITESPACE_CHARS:
            line = line.replace(char, "")
        sums[2] += len(line)
    return sums[2] - sums[1]


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015, 8)
    input_lines = my_aoc.load_lines()

    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # dict to map functions
    funcs = {1: part1, 2: part2}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_lines)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
