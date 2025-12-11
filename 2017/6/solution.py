"""
Advent Of Code 2017 day 6

"""

# import system modules
from __future__ import annotations
import logging
import argparse
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)


def redistribute(num_tuple):
    """
    Function to redistribute blocks
    """
    num_list = list(num_tuple)
    num_list_len = len(num_list)
    max_val = max(num_list)
    idx = num_list.index(max_val)
    move_blocks = max_val
    num_list[idx] = 0
    while move_blocks:
        idx += 1
        if idx > -num_list_len:
            idx = idx % num_list_len
        num_list[idx] += 1
        move_blocks -= 1
    return tuple(num_list)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    start_tuple = tuple(int(num) for num in re.findall(r"(\d+)", input_value))
    counter = 0
    seen = set()
    current_tuple = start_tuple
    loop_count = 0
    loop_tuple = None
    last_counter = 0
    while True:
        if current_tuple in seen:
            if part == 1:
                return counter
            if not loop_tuple:
                loop_tuple = current_tuple
                last_counter = counter
        if part == 2 and current_tuple == loop_tuple:
            loop_count += 1
            if loop_count > 1:
                return counter - last_counter
        seen.add(current_tuple)
        current_tuple = redistribute(current_tuple)
        counter += 1


YEAR = 2017
DAY = 6
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
