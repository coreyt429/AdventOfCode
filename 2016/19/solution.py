"""
Advent Of Code 2016 day 19

This one needed a creative solution, and more familiarity with collections.deque.

Good learning opportunity for me.

"""

import logging
import argparse
import collections

from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_input(input_text):
    """
    Return elf count as int.
    """
    return int(input_text.strip())


def _solve_part1(input_value):
    """
    Function to solve puzzle.
    This solves part1 efficiently, and I'm sure it would solve part 2
    eventually.  I'm just not that patient (I found coded, tested, and documented
    another solution while it was running, and still killed it without an answer)
    """
    # Initialize deque with elf indices
    queue = collections.deque(range(1, input_value + 1))
    # loop until we have an answer
    while len(queue) > 1:
        # select elf1 and elf2 based on rules for problem part
        # first two in the queue
        elf1 = queue.popleft()
        elf2 = queue.popleft()
        # silly call to make pylint happy, and leave code readable
        if elf2:
            pass
        # Put elf1 back at the end
        queue.append(elf1)
    return queue.popleft()


def solve_part2(input_value):
    """
    Function to solve part 2
    part two solution:  thanks to u/aceshades for the idea to split the queue
    the split queue lets us "rotate" the queue by using pop and popleft instead
    of rotate
    """
    # populate left with the first half of the elves
    left = collections.deque(range(1, input_value // 2 + 1))
    # populate right with the second half reversed
    right = collections.deque(range(input_value, input_value // 2, -1))
    # loop until one side is empty
    while left and right:
        # pop from the longer half
        if len(left) > len(right):
            left.pop()
        else:
            right.pop()

        # rotate, moving from the front of the logical queue (front of left)
        # to the end of the logical queue (beginning of right)
        right.appendleft(left.popleft())
        # moving from middle right  of logical queue (end of right) to
        # middle left of logical queue (beginning of left)
        left.append(right.pop())
    # return whichever remains
    return left[0] or right[0]


def solve(input_value, part):
    """
    Entry point for either puzzle part.
    """
    if part == 1:
        return _solve_part1(input_value)
    return solve_part2(input_value)


YEAR = 2016
DAY = 19
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
