"""
Advent Of Code 2017 day 15

"""
# import system modules
import time
import itertools
import re

# import my modules
import aoc # pylint: disable=import-error

def generator_func(seed, factor, divisor=None):
    """
    Function to generate Lehmer random numbers
    Args:
        seed: int() seed for generator
        factor: int() "a" value for generator
        divisor: int() or None, used in part 2
    Yields:
        current: int() random number
    """
    # start with seed
    current = seed
    # loop
    while True:
        # calculate next number
        current = current * factor % 2147483647
        # if part 1, or divisible by part 2 divisor
        if not divisor or current % divisor == 0:
            # we have a number, cough it up
            yield current

def parse_input(lines):
    """
    Function to parse input
        Args:
            lines: list(str()) input lines
        Returns:
            results['A']: int() seed_a
            results['B']: int() seed_b
    """
    # init results
    results = {}
    # walk lines
    for line in lines:
        # regex match
        match = re.match(r'Generator (\w) starts with (\d+)', line)
        if match:
            # store int value
            results[match.group(1)] = int(match.group(2))
    # return seed_a, seed_b
    return results['A'], results['B']

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # get seeds from input
    seed_a, seed_b = parse_input(input_value)
    if part == 1:
        # Part 1, generators run without divisor for 40M cycles
        gen_a = generator_func(seed_a, 16807)
        gen_b = generator_func(seed_b, 48271)
        cycles = 40000000
    else:
        # Part 2, generators run with divisor for 5M cycles
        gen_a = generator_func(seed_a, 16807, 4)
        gen_b = generator_func(seed_b, 48271, 8)
        cycles = 5000000
    # init counter
    counter = 0
    # Mask for the last 16 bits
    mask = 0xFFFF
    # iterate over cycles
    # note, using islice shaved a few seconds, see scratchpad for
    # my original routine. Thanks to u/sciyoshi for sharing this in your solution
    for val_a, val_b in itertools.islice(zip(gen_a, gen_b), cycles):
        # check for match in least significant 16 bits
        if (val_a & mask) == (val_b & mask):
            # increment counter
            counter += 1
    # yay! and answer :)
    return counter

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017,15)
    # fetch input
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
