"""
Advent Of Code 2023 day 13

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


def parse_input(data: str) -> list[list[str]]:
    """Parses the input data into a list of patterns"""
    patterns = []
    # Split the data into lines
    blocks = data.strip().split("\n\n")
    for block in blocks:
        patterns.append(block.split("\n"))
    return patterns


def find_reflection(block: list[str], smudge_target: int = 0) -> int:
    """
    Returns the number of lines above the horizontal reflection line,
    or zero if there is no horizontal reflection line. Where the reflection line
    is chosen such that there are exactly smudge_target "smudges"
    """
    retval = 0
    for split in range(len(block) - 1):
        smudges = 0
        for i in range(split + 1):
            if split + i + 1 >= len(block):
                continue

            row_above = block[split - i]
            row_below = block[split + i + 1]
            for a, b in zip(row_above, row_below):
                if a != b:
                    smudges += 1
        if smudges == smudge_target:
            retval = split + 1
            break
    return retval


def print_block(block: list[str]):
    """Print a block"""
    for row in block:
        print(row)


def transpose_block(block: list[str]) -> list[str]:
    """Transpose a block of text"""
    transpose = []
    for i in range(len(block[0])):
        transpose.append("".join([row[i] for row in block]))
    return transpose


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    retval = 0
    h_total = 0
    v_total = 0
    parsed_data = parse_input(input_value)
    for block in parsed_data:
        transpose = transpose_block(block)
        h_total += find_reflection(block, part - 1)
        v_total += find_reflection(transpose, part - 1)
    retval = v_total + 100 * h_total
    return retval


YEAR = 2023
DAY = 13
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
