"""
Advent Of Code 2017 day 4

This one was fairly straight forward. I did trip up in version two, I didn't
initially test to make sure I wasn't comparing the first passphrase to itself
and ended up with 0.  I didn't think that would be the answer, and submitted it
anyway.  I was right.  Found the issue and added enumerates and an if statement
to compare indexes.

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

pattern_words = re.compile(r"(\w+)")


def check_passphrase(input_string, version=1):
    """
    Function to check passphrases
    """
    pp_list = pattern_words.findall(input_string)
    for idx, passphrase in enumerate(pp_list):
        if pp_list.count(passphrase) > 1:
            return False
        if version == 2:
            for idx2, passphrase2 in enumerate(pp_list):
                if idx == idx2:
                    continue
                if sorted(passphrase) == sorted(passphrase2):
                    return False
    return True


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    counter = 0
    for line in input_value:
        if check_passphrase(line, part):
            counter += 1
    return counter


YEAR = 2017
DAY = 4
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
