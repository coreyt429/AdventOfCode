"""
Advent Of Code 2017 day 5

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def follow_jumps(offsets, part=1):
    """
    function to follow jump values
    """
    # init idx and counter
    idx = 0
    counter = 0
    # loop while idx is valid for offsets
    while 0 <= idx < len(offsets):
        # store next idx in idx2
        idx2 = idx + offsets[idx]
        # part 2 decrement if >=3
        if part == 2 and offsets[idx] >= 3:
            offsets[idx] -= 1
        else: # part 1 or part 2 < 3 increment
            offsets[idx] += 1
        # increment counter
        counter += 1
        # set idx to next idx
        idx = idx2
    # return step counter
    return counter

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # run follow jumps with a copy of input_value so input_value doesn't change
    return follow_jumps(list(tuple(input_value)), part)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017,5)
    input_lines = my_aoc.load_integers()
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
