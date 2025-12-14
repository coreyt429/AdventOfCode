"""
Advent Of Code 2016 day 2

This solution was already fast, just needed to be cleaned up a bit
and restructured
"""

# import system modules
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

KEYPAD = {
    #  012
    # 0 123
    # 1 456
    # 2 789
    1: {
        (0, 0): "1",
        (0, 1): "2",
        (0, 2): "3",
        (1, 0): "4",
        (1, 1): "5",
        (1, 2): "6",
        (2, 0): "7",
        (2, 1): "8",
        (2, 2): "9",
    },
    #  01234
    # 0   1
    # 1  234
    # 2 56789
    # 3  ABC
    # 4   D
    2: {
        (0, 2): "1",
        (1, 1): "2",
        (1, 2): "3",
        (1, 3): "4",
        (2, 0): "5",
        (2, 1): "6",
        (2, 2): "7",
        (2, 3): "8",
        (2, 4): "9",
        (3, 1): "A",
        (3, 2): "B",
        (3, 3): "C",
        (4, 2): "D",
    },
}

START_KEYS = {1: (1, 1), 2: (2, 0)}
MOVEMENTS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


def next_key(keypad, current_key_loc, new_move_direction):
    """
    Function to find next key to try:
      Args:
        keypad - dict keys arecoordinate tuples, values are key numbers
        current_key_location - coordinate tuple of current key
        new_move_direction - direction to attempt
    """
    # init new_key_location as list of current_key_location
    new_key_loc = list(current_key_loc)
    # for coord in x,y
    for coord in (0, 1):
        # get new xy value vy adding offsets for direction
        new_key_loc[coord] += MOVEMENTS[new_move_direction][coord]
    # convert back to tuple
    new_key_loc = tuple(new_key_loc)
    # is this a valid key
    if new_key_loc in keypad:
        # yes, return new key
        return new_key_loc
    # no, return previous key
    return current_key_loc


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    code_instructions = input_value
    bathroom_code = ""
    keypad = KEYPAD[part]
    current_key = START_KEYS[part]
    for current_instruction in code_instructions:
        for current_movement in current_instruction:
            current_key = next_key(keypad, current_key, current_movement)
        bathroom_code += keypad[tuple(current_key)]
    if bathroom_code.isdigit():
        return int(bathroom_code)
    return bathroom_code


YEAR = 2016
DAY = 2
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
