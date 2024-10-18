"""
Advent Of Code 2019 day 21

This one was simple to implement. The real puzzle was the logic
of the spring code.  I was a bit busy at work, and too low energy to
work that out at lunch, so I cheated a bit.

Explanation of spring code logic: https://www.youtube.com/watch?v=3TEU2FCLgmA&t=1027s

Credit to u/finloa for linking the video in your solution.

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
    icc = IntCodeComputer(input_value)
    icc.output = []
    # ((NOT A OR NOT B) OR NOT C) AND D
    instructions = """NOT A T
    NOT B J
    OR T J
    NOT C T
    OR T J
    AND D J
    WALK""".splitlines()
    if part == 2:
        instructions = """NOT A T
NOT B J
OR T J
NOT C T
OR T J
AND D J
NOT I T
NOT T T
OR F T
AND E T
OR H T
AND T J
RUN""".splitlines()
    # instructions = """NOT D J
    # WALK""".splitlines()
    # icc.inputs.extend([ord(char) for char in instruction])
    use_live_feed = False
    while True:
        # break if out of bounds
        if not 0 <= icc.ptr < len(icc.program):
            break
        if icc.next_op_code() == 3 and not icc.inputs:
            if not instructions:
                break
            instruction = instructions.pop(0)
            icc.inputs.extend([ord(char) for char in instruction])
            icc.inputs.append(10)

        # step through program
        icc.step()
        # if there are outputs, check them
        while len(icc.output) > 0:
            # get next output
            output = icc.output.pop(0)
            # if output is outside of printable characters
            if output > 256:
                # return
                return output
            if use_live_feed:
                # print feed if enabled
                print(chr(output),end='')
    return part

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019,21)
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
    # correct answers once solved, to validate changes
    correct = {
        1: 19348404,
        2: 1139206699
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
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
