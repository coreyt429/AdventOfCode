"""
Advent Of Code 2017 day 9

Oh boy, regex fun. 

"""
# import system modules
import time
import re

# import my modules
import aoc # pylint: disable=import-error

def prep_string(in_string):
    """
    Function to prep string
    """
    # remove cancelled characters
    out_string = re.sub(r'!.', '', in_string)
    # remove garbage
    out_string = re.sub(r'<[^>]*>', '', out_string)
    return out_string

def score_string(in_string):
    """
    Function to score string
    """
    # init total and points
    total = 0
    points = 0
    # walk string
    for char in in_string:
        # start a group, so increment points
        if char == '{':
            points += 1
        # end a group, so give out the points
        if char == '}':
            total +=  points
            points -= 1
    return total

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # part 2, simpler processing, so just do it here
    if part == 2:
        # strip cancelled characters
        out_string = re.sub(r'!.', '', input_value)
        # match characters inside garbage
        matches = re.findall(r'<([^>]*)>', out_string)
        # find any?
        if matches:
            # add up the lengths of garbage groups, and return
            return sum(len(tmp_string) for tmp_string in matches)
    # part 1
    # prep the string
    new_string = prep_string(input_value)
    # score the string
    score = score_string(new_string)
    return score

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017,9)
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
