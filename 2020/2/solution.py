"""
Advent Of Code 2020 day 2

"""
# import system modules
import time
import re

# import my modules
import aoc # pylint: disable=import-error

def parse_data(lines):
    """
    Function to parse input data
    """
    passwords = []
    pattern_rule = re.compile(r'(\d+)-(\d+) (\w): (\S+)')
    for line in lines:
        match = pattern_rule.match(line)
        if match:
            passwords.append(
                {
                    "password": match.group(4),
                    "min": int(match.group(1)),
                    "max": int(match.group(2)),
                    "letter": match.group(3)
                }
            )
    return passwords

def is_valid(p_d, part):
    """
    Function to validate passwords against rules
    """
    if part == 1:
        count = p_d['password'].count(p_d["letter"])
        return p_d['min'] <= count <= p_d['max']
    # Part 2
    # Exactly one of these positions must contain the given letter.
    if p_d['password'][p_d['min'] - 1] == p_d['password'][p_d['max'] - 1]:
        return False
    return p_d["letter"] in p_d['password'][p_d['min'] - 1] + p_d['password'][p_d['max'] - 1]

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    data = parse_data(input_value)
    counter = 0
    for password in data:
        if is_valid(password, part):
            counter += 1
        # print(password, is_valid(password))
    return counter

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020,2)
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
    # correct answers once solved, to validate changes
    correct = {
        1: 645,
        2: 737
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
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
