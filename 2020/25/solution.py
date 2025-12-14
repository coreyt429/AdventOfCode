"""
Advent Of Code 2020 day 25

Nice easy finish for the year.

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


def transform(value, subject_number=7):
    """function to transform a number"""
    # Set the value to itself multiplied by the subject number.
    value *= subject_number
    # Set the value to the remainder after dividing the value by 20201227.
    return value % 20201227


def transform_loop(value, loops, subject_number=7):
    """function to transform in a loop"""
    for _ in range(loops):
        value = transform(value, subject_number)
    return value


def find_loop(target):
    """function to find loopsize for a public key"""
    value = 1
    counter = 0
    while value != target:
        value = transform(value)
        counter += 1
    return counter


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return "Pay the Deposit"
    public_keys = {"door": int(input_value.pop(0)), "card": int(input_value.pop(0))}
    loop_size = {}
    for key, public_key in public_keys.items():
        loop_size[key] = find_loop(public_key)
    encryption_key = {
        "door": transform_loop(1, loop_size["door"], public_keys["card"]),
        "card": transform_loop(1, loop_size["card"], public_keys["door"]),
    }
    return encryption_key["door"]


YEAR = 2020
DAY = 25
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
