"""
Advent Of Code 2024 day 3

Nice regex challenge.  Not much else to say on this one.


"""

# import system modules
import time
import re
import math

# import my modules
import aoc  # pylint: disable=import-error


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # regex patterns
    pattern_mul_digits = re.compile(r"mul\((-?\d+),(-?\d+)\)")
    pattern_do_dont_mul = re.compile(r"(mul\(-?\d+,-?\d+\))|(do\(\))|(don't\(\))")
    pairs = []
    do_mul = True
    for line in input_value:
        # find all do, don't and mul commands
        for command in pattern_do_dont_mul.findall(line):
            for item in command:
                if "do()" in item:
                    do_mul = True
                    continue
                if "don't()" in item:
                    do_mul = False
                    continue
                # part 1, add the pair no matter what
                # part 2, only add the pair if we are in a do block
                if "mul" in item and any([do_mul, part == 1]):
                    pair = pattern_mul_digits.findall(item)[0]
                    pairs.append([int(num) for num in pair])
    # return the sum of the product of each pair
    return sum((math.prod(pair) for pair in pairs))


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2024, 3)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 175700056, 2: 71668682}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
