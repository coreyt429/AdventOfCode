"""
Advent Of Code 2019 day 9

"""
# import system modules
import time

# import my modules
from intcode import IntCodeComputer # pylint: disable=import-error
import aoc # pylint: disable=import-error

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # init output
    output = []
    # init icc with input data
    icc = IntCodeComputer(input_value)
    # attach output queue
    icc.set_output(output)
    # run program with specified input (maybe not so) coincidentally the part number
    icc.run(input_val=part)
    # return the output code
    return output[0]

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019,9)
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
    # correct answers for validating future changes to icc
    correct = {
        1: 2932210790,
        2: 73144
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
        # check answer
        assert correct[my_part] == answer[my_part]
