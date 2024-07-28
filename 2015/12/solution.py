"""
Advent Of Code 2015 day 12

"""
# import system modules
import time
import re
import json

# import my modules
import aoc # pylint: disable=import-error

def sum_json_vals(current_object):
    """
    Function to recuse json structure, and distill it to the sum of a list of ints
    """
    # If integer, return the integer
    if isinstance(current_object, int):
        return current_object
    # if list, sum the recursed values for contained objects
    if isinstance(current_object, list):
        return sum(sum_json_vals(next_object) for next_object in current_object)
    # if not int, list, or dict, we aren't interested
    if not isinstance(current_object, dict):
        return 0
    # prune dicts that contain "red" as a value
    if "red" in current_object.values():
        return 0
    # return recursed values
    return sum_json_vals(list(current_object.values()))

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        pattern = r'-*\d+'
        return sum(int(num) for num in re.findall(pattern, input_value))
    # part 2
    return sum_json_vals(json.loads(input_value))

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015,12)
    input_text = my_aoc.load_text()
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
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
