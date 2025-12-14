"""
Advent Of Code 2016 day 6

slight modification to get into new format

"""

# import system modules
import logging
import argparse
from collections import Counter

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_input(input_text):
    """
    Return list of message strings.
    """
    return [line.strip() for line in input_text.splitlines() if line.strip()]


def solve(lines, part):
    """
    Function to solve puzzle
    """
    most_common = []
    least_common = []
    for column in zip(*lines):
        counts = Counter(column)
        most_common.append(min(counts.items(), key=lambda item: (-item[1], item[0]))[0])
        least_common.append(min(counts.items(), key=lambda item: (item[1], item[0]))[0])
    part1 = "".join(most_common)
    part2 = "".join(least_common)
    return part1 if part == 1 else part2


YEAR = 2016
DAY = 6
input_format = {
    1: parse_input,
    2: parse_input,
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
