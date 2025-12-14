"""
Advent Of Code 2019 day 21

This one was simple to implement. The real puzzle was the logic
of the spring code.  I was a bit busy at work, and too low energy to
work that out at lunch, so I cheated a bit.

Explanation of spring code logic: https://www.youtube.com/watch?v=3TEU2FCLgmA&t=1027s

Credit to u/finloa for linking the video in your solution.

"""

# import system modules
import logging
import argparse

# import my modules
from intcode import IntCodeComputer  # pylint: disable=import-error
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


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
                print(chr(output), end="")
    return part


def parse_input(input_text):
    """
    Return stripped program text.
    """
    return input_text.strip()


YEAR = 2019
DAY = 21
input_format = {
    1: parse_input,
    2: parse_input,
}

funcs = {
    1: solve,
    2: solve,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    aoc = AdventOfCode(
        year=YEAR,
        day=DAY,
        input_formats=input_format,
        funcs=funcs,
        test_mode=args.test,
    )
    aoc.run(submit=args.submit)
