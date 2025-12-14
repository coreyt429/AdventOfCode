"""
Advent Of Code 2022 day 4

This one was fairly quick.  solve_original() is my original infinite list of
if statements.

solve() is the solution from chatGPT optimizing my solution.
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


def solve_original(input_value, part):
    """
    Function to solve puzzle
    """
    count = 0
    for line in input_value:
        elf_1, elf_2 = line.split(",")
        elf_1 = [int(num) for num in elf_1.split("-")]
        elf_2 = [int(num) for num in elf_2.split("-")]
        if elf_1[0] <= elf_2[0] and elf_1[1] >= elf_2[1]:
            count += 1
            continue
        if elf_2[0] <= elf_1[0] and elf_2[1] >= elf_1[1]:
            count += 1
            continue
        if part == 2:
            if elf_1[0] <= elf_2[0] <= elf_1[1]:
                count += 1
                continue
            if elf_1[0] <= elf_2[1] <= elf_1[1]:
                count += 1
                continue
            if elf_2[0] <= elf_1[0] <= elf_2[1]:
                count += 1
                continue
            if elf_2[0] <= elf_1[1] <= elf_2[1]:
                count += 1
                continue
    return count


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    count = 0
    for line in input_value:
        # Parse input into ranges
        (start1, end1), (start2, end2) = [
            tuple(map(int, elf.split("-"))) for elf in line.split(",")
        ]

        # Check full containment
        if (start1 <= start2 <= end2 <= end1) or (start2 <= start1 <= end1 <= end2):
            count += 1
        elif part == 2:
            # Check partial overlap
            if not (end1 < start2 or end2 < start1):
                count += 1
    return count


YEAR = 2022
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
