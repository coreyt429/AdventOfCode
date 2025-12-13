"""
Advent Of Code 2015 day 12

"""

# import system modules
import logging
import argparse
import re
import json

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def sum_json_vals(current_object):
    """
    Function to recuse json structure, and distill it to the sum of a list of ints
    """
    # If integer, return the integer
    if isinstance(current_object, int):
        return current_object
    # if list, sum the recursed values for contained objects
    if isinstance(current_object, list):
        return sum(sum_json_vals(next_object) for next_object in current_object)
    # if not int, list, or dict, we aren't interested
    if not isinstance(current_object, dict):
        return 0
    # prune dicts that contain "red" as a value
    if "red" in current_object.values():
        return 0
    # return recursed values
    return sum_json_vals(list(current_object.values()))


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        pattern = r"-*\d+"
        return sum(int(num) for num in re.findall(pattern, input_value))
    # part 2
    return sum_json_vals(json.loads(input_value))


YEAR = 2015
DAY = 12
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
