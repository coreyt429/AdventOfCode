"""
Advent Of Code 2022 day 13

Fairly simple recursive comparison puzzle.

I did learn three things in this one.
  1: The use of ast.literal_eval instead of eval
  2: The else statement on the for loop
  3: cmp_to_key to use my compare function as a sort key

"""

# import system modules
import logging
import argparse
from functools import cmp_to_key
import math
import ast

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_input(in_text):
    """Function to parse input data"""
    pairs = []
    for pair_text in in_text.split("\n\n"):
        pair = []
        for line in pair_text.splitlines():
            pair.append(ast.literal_eval(line))
        pairs.append(pair)
    return pairs


def compare(left, right):
    """function to compare two values"""
    state = -2
    # print(f"compare({type(left)}{left}, {type(right)}{right})")
    if isinstance(left, int) and isinstance(right, int):
        # print(f"{(left < right)} - {(left > right)} = {(left < right) - (left > right)}")
        state = (left < right) - (left > right)

    if isinstance(left, list) and isinstance(right, list):
        for idx, val in enumerate(left):
            if idx >= len(right):
                state = -1
                break
            state = compare(val, right[idx])
            if state != 0:
                break
        else:
            # at this point we have run through the left, and have been equal so it is
            # a matter of is the left list shorter than the right, so just compare length
            state = compare(len(left), len(right))

    if isinstance(left, list) and isinstance(right, int):
        state = compare(left, [right])

    if isinstance(left, int) and isinstance(right, list):
        state = compare([left], right)
    return state


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    pairs = parse_input(input_value)
    valid = []
    if part == 2:
        dividers = [[[2]], [[6]]]
        decoder = []
        for idx, line in enumerate(
            reversed(
                sorted(
                    [item for pair in pairs for item in pair] + dividers,
                    key=cmp_to_key(compare),
                )
            )
        ):
            if line in dividers:
                decoder.append(idx + 1)
        # What is the decoder key for the distress signal?
        return math.prod(decoder)
    for idx, pair in enumerate(pairs):
        state = compare(*pair)
        if state == 1:
            # The first pair has index 1, the second pair has index 2, and so on.
            valid.append(idx + 1)
    # What is the sum of the indices of those pairs?
    return sum(valid)


YEAR = 2022
DAY = 13
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
