"""
Advent Of Code 2016 day 18

"""

import logging
import argparse
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def next_row(last_row):
    """
    Function to determine next row based on:
    Its left and center tiles are traps, but its right tile is not.
    Its center and right tiles are traps, but its left tile is not.
    Only its left tile is a trap.
    Only its right tile is a trap.
    """
    new_row = ""
    for col in range(len(last_row)):
        # left wall safe, doesn't matter what center is: _.^, _^^, _^., _..
        if col == 0:
            new_row += last_row[1]  # safe or trap
        # right wall safe, doesn't matter what center is:  .^_, ^^_, ^._, .._
        elif col == len(last_row) - 1:
            new_row += last_row[-2]  # safe or trap
        # all traps, this tile must be safe ^^^
        elif "." not in last_row[col - 1 : col + 2]:
            new_row += "."  # safe
        # all safe, this tile must be safe ...
        elif "^" not in last_row[col - 1 : col + 2]:
            new_row += "."  # safe
        # both left and right, or neither left nor right: '^.^','.^.'
        elif last_row[col - 1 : col + 2] in ["^.^", ".^."]:
            new_row += "."  # safe
        # Remaining trap scenarios: .^^, ..^, , ^^.
        else:
            new_row += "^"
    return new_row


def solve(first_row, part):
    """
    Count safe tiles for the requested number of rows.
    """
    targets = {1: 40, 2: 400000}
    current = first_row.strip()
    safe_tiles = current.count(".")
    for _ in range(1, targets[part]):
        current = next_row(current)
        safe_tiles += current.count(".")
    return safe_tiles


YEAR = 2016
DAY = 18
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
