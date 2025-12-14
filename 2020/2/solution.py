"""
Advent Of Code 2020 day 2

"""

# import system modules
import logging
import argparse
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_data(lines):
    """
    Function to parse input data
    """
    passwords = []
    pattern_rule = re.compile(r"(\d+)-(\d+) (\w): (\S+)")
    for line in lines:
        match = pattern_rule.match(line)
        if match:
            passwords.append(
                {
                    "password": match.group(4),
                    "min": int(match.group(1)),
                    "max": int(match.group(2)),
                    "letter": match.group(3),
                }
            )
    return passwords


def is_valid(p_d, part):
    """
    Function to validate passwords against rules
    """
    if part == 1:
        count = p_d["password"].count(p_d["letter"])
        return p_d["min"] <= count <= p_d["max"]
    # Part 2
    # Exactly one of these positions must contain the given letter.
    if p_d["password"][p_d["min"] - 1] == p_d["password"][p_d["max"] - 1]:
        return False
    return (
        p_d["letter"]
        in p_d["password"][p_d["min"] - 1] + p_d["password"][p_d["max"] - 1]
    )


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    data = parse_data(input_value)
    counter = 0
    for password in data:
        if is_valid(password, part):
            counter += 1
        # print(password, is_valid(password))
    return counter


YEAR = 2020
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
