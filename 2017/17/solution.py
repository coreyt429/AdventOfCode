"""
Advent Of Code 2017 day 17

Okay, this one I tripped myself.  My first thought was to use deque and spin instead
of middle insert.  Buuut, I convinced myself that I would have to spin it back, and
that would possibly be less efficient than a list.  So I tried list, and it was horribly
slow. Looked at a few other implementations, and kicked myself for not sticking with
deque. So here is my fianlish deque solution.  I still feel like there is a faster
math solution here, and I just don't have the energy for that today, so maybe later
"""

# import system modules
import time
from collections import deque

# import my modules
import aoc  # pylint: disable=import-error


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # get steps from input as int()
    steps = int(input_value[0])
    # initialize buffer
    buffer = deque([0])
    # 2017 cycles for part 1
    cycles = 2017
    if part == 2:
        # 50,000,000 cycles for part 2
        cycles = 50000000
    # loop through cycles
    for idx in range(1, cycles + 1):
        # rotate buffer -1 * steps
        # this simulates moving forward steps in a list
        # just much more efficirently
        buffer.rotate(-steps)
        # add idx to the end of the deque
        buffer.append(idx)
    if part == 1:
        # part 1, return the first element in the buffer
        # next element after the one we just put on the end
        return buffer[0]
    # part 2, return the number after 0
    return buffer[buffer.index(0) + 1]


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017, 17)
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
