"""
Advent Of Code 2015 day 8

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

pattern_hex = re.compile(r"(\\x[0-9a-f]{2})")
WHITESPACE_CHARS = " \t\n\r"  # Space, tab, newline, carriage return


def part1(parsed_data, _part=None):
    """
    Function to dolve part 1
    """
    replacement_pairs = (("\\\\", "#"), (r"\"", "#"), ('"', ""))
    sums = {1: 0, 2: 0}
    for line in parsed_data:
        sums[1] += len(line)
        for replace_pair in replacement_pairs:
            line = line.replace(*replace_pair)
        line = pattern_hex.sub("#", line)
        for char in WHITESPACE_CHARS:
            line = line.replace(char, "")
        sums[2] += len(line)
    return sums[1] - sums[2]


def part2(parsed_data, _part=None):
    """
    Function to solve part 2
    """
    replacement_pairs = (
        ("\\\\", "#"),
        ('"', "%"),
        ('"', '\\"'),
        ("#", "\\\\\\\\"),
        ("%", '"\\"'),
    )
    sums = {1: 0, 2: 0}
    for line in parsed_data:
        sums[1] += len(line)
        for replace_pair in replacement_pairs:
            line = line.replace(*replace_pair)
        line = pattern_hex.sub("\\\\\\\\xNN", line)
        for char in WHITESPACE_CHARS:
            line = line.replace(char, "")
        sums[2] += len(line)
    return sums[2] - sums[1]


YEAR = 2015
DAY = 8
input_format = {
    1: "lines",
    2: "lines",
}

funcs = {
    1: part1,
    2: part2,
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
