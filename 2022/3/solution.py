"""
Advent Of Code 2022 day 3

set() and string slicing made this one fairly easy.

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


def item_priority(item):
    """Function to calculate item priority"""
    if item.islower():
        # Lowercase item types a through z have priorities 1 through 26.
        return ord(item) - ord("a") + 1
    # Uppercase item types A through Z have priorities 27 through 52.
    return ord(item) - ord("A") + 1 + 26


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    total = 0
    if part == 1:
        for line in input_value:
            half = len(line) // 2
            set_a = set(line[:half])
            set_b = set(line[half:])
            # Find the item type that appears in both compartments of each rucksack.
            total += item_priority(set_a.intersection(set_b).pop())
        # What is the sum of the priorities of those item types?
        return total
    # part 2
    for idx in range(0, len(input_value), 3):
        # Find the item type that corresponds to the badges of each three-Elf group.
        # Every set of three lines in your list corresponds to a single group
        common_set = set(input_value[idx])
        common_set.intersection_update(input_value[idx + 1])
        common_set.intersection_update(input_value[idx + 2])
        total += item_priority(common_set.pop())
    # What is the sum of the priorities of those item types?
    return total


YEAR = 2022
DAY = 3
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
