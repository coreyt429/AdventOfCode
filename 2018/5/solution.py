"""
Advent Of Code 2018 day 5

"""

# import system modules
from __future__ import annotations
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def generate_pairs():
    """
    Function to generate unit pairs
    """
    # init new_pairs
    new_pairs = []
    # for range from A - Z
    for idx in range(65, 91):
        # add Aa and aA
        new_pairs.append(f"{chr(idx)}{chr(idx + 32)}")
        new_pairs.append(f"{chr(idx + 32)}{chr(idx)}")
    return new_pairs


def reduce_string(pairs, start_string):
    """
    Function to reduce polymer string
    """
    # init last_string and current_string
    last_string = ""
    current_string = start_string
    # loop until they are the same (no more reduction)
    while last_string != current_string:
        # update last_string
        last_string = current_string
        # loop pairs
        for pair in pairs:
            # remove from current_string
            current_string = current_string.replace(pair, "")
    # return final current_string
    return current_string


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # init pairs
    pairs = generate_pairs()
    # How many units remain after fully reacting the polymer you scanned?
    if part == 1:
        # reduce initial scanned string
        reduced_string = reduce_string(pairs, input_value)
        # return length (not the string like I did at first)
        return len(reduced_string)
    # part 2:
    # init min string to max size
    min_string = input_value
    # loop pairs
    for idx, pair in enumerate(pairs):
        # we only need to process every other pair
        # aA and Aa are the same for this
        if idx % 2 == 1:
            continue
        # copy input_string
        test_string = input_value
        # replace a and A
        test_string = test_string.replace(pair[0], "")
        test_string = test_string.replace(pair[1], "")
        # reduce the new string
        reduced_string = reduce_string(pairs, test_string)
        # if we have found a new shortest string, save it
        if len(reduced_string) < len(min_string):
            min_string = reduced_string
    # return length of shortest string
    return len(min_string)


YEAR = 2018
DAY = 5
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
