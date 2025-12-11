"""
Advent Of Code 2017 day 16

"""

# import system modules
from __future__ import annotations
import logging
import argparse
from collections import deque
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)

pattern_nums = re.compile(r"(\d+)")
pattern_p = re.compile(r"p(\w+)/(\w+)")


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    count = 1 if part == 1 else 1_000_000_000
    steps = input_value.split(",")
    dancers = deque([chr(idx) for idx in range(ord("a"), ord("a") + 16)])
    states = []
    state = "".join(dancers)
    states.append(state)
    for idx in range(1, count + 1):
        for step in steps:
            if step.startswith("s"):
                dancers.rotate(int(step[1:]))
            if step.startswith("x"):
                matches = pattern_nums.findall(step)
                p_1 = int(matches[0])
                p_2 = int(matches[1])
                dancers[p_1], dancers[p_2] = dancers[p_2], dancers[p_1]
            match = pattern_p.match(step)
            if match:
                p_1 = dancers.index(match.group(1))
                p_2 = dancers.index(match.group(2))
                dancers[p_1], dancers[p_2] = dancers[p_2], dancers[p_1]
        state = "".join(dancers)
        if state in states:
            break
        states.append(state)
    idx = count % len(states)
    state = states[idx]
    return state


YEAR = 2017
DAY = 16
input_format = {
    1: "text",
    2: "text",
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
