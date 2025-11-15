"""
Advent Of Code 2017 day 16

"""

# import system modules
import time
from collections import deque
import re

# import my modules
import aoc  # pylint: disable=import-error

# regex patterns
pattern_nums = re.compile(r"(\d+)")
pattern_p = re.compile(r"p(\w+)/(\w+)")


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # part 1 loop count
    count = 1
    if part == 2:
        # part 2 loop count
        count = 1000000000
    # parse input
    steps = input_value.split(",")
    # init dancers a-p
    dancers = deque([chr(idx) for idx in range(ord("a"), ord("a") + 16)])
    # init states
    states = []
    # initial state
    state = "".join(dancers)
    states.append(state)
    # loop
    for idx in range(1, count + 1):
        # run steps
        for step in steps:
            # spin
            if step.startswith("s"):
                dancers.rotate(int(step[1:]))
            # exchange
            if step.startswith("x"):
                matches = pattern_nums.findall(step)
                p_1 = int(matches[0])
                p_2 = int(matches[1])
                dancers[p_1], dancers[p_2] = dancers[p_2], dancers[p_1]
            # partner
            match = pattern_p.match(step)
            if match:
                p_1 = dancers.index(match.group(1))
                p_2 = dancers.index(match.group(2))
                dancers[p_1], dancers[p_2] = dancers[p_2], dancers[p_1]
        # get state
        state = "".join(dancers)
        # check against states
        if state in states:
            # we have looped, so break the loop
            # the rest of the sequence will just repeat what we have
            # in states
            break
        # add state
        states.append(state)
    # idx id the modulus of count and the length of states
    # since this is an infinite loop of the sequence we have discovered
    # we just need to know how many more would have been executed
    # after the last repeated sequence
    idx = count % len(states)
    # get the state for out target iteration
    state = states[idx]
    return state


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017, 16)
    input_text = my_aoc.load_text()
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
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
