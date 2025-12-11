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
from __future__ import annotations
import logging
import argparse
from collections import deque

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    steps = int(input_value[0])
    buffer = deque([0])
    cycles = 2017 if part == 1 else 50_000_000
    for idx in range(1, cycles + 1):
        buffer.rotate(-steps)
        buffer.append(idx)
    if part == 1:
        return buffer[0]
    return buffer[buffer.index(0) + 1]


YEAR = 2017
DAY = 17
input_format = {
    1: "lines",
    2: "lines",
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
