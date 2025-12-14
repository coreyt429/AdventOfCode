"""
Advent Of Code 2022 day 5

Fun with stacks :)

"""

# import system modules
import logging
import argparse
from collections import defaultdict

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_input(input_value):
    """Function to parse input text into columns and moves"""
    stacks, instructions = input_value.split("\n\n")
    # reverse stacks, so we can build from the boottom up
    stacks = list(reversed(stacks.splitlines()))
    labels = stacks.pop(0)
    positions = {}
    columns = defaultdict(list)
    # identify column positions
    for idx, char in enumerate(labels):
        if char != " ":
            positions[idx] = int(char)
    # process remaining rows to build columns
    while stacks:
        line = stacks.pop(0)
        for idx, char in enumerate(line):
            if idx in positions and char != " ":
                columns[positions[idx]].append(char)
    # process instructions:
    moves = []
    for line in instructions.splitlines():
        data = line.split(" ")
        moves.append((int(data[1]), int(data[3]), int(data[5])))
    return moves, columns


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    moves, columns = parse_input(input_value)
    for move in moves:
        qty, source, destination = move
        if part == 1:
            # Crates are moved one at a time
            for _ in range(qty):
                columns[destination].append(columns[source].pop())
        else:
            # The CrateMover 9001 is notable for many new and exciting features: air conditioning,
            # leather seats, an extra cup holder, and the ability to pick up and move multiple
            # crates at once.
            columns[destination].extend(columns[source][-qty:])
            columns[source] = columns[source][:-qty]
    return "".join([column[-1] for column in columns.values()])


YEAR = 2022
DAY = 5
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
