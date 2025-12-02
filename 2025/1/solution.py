"""
Advent Of Code 2025 day 1

"""

# import system modules
import sys
import logging
import argparse
from collections import deque


# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251201"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    moves = []
    for line in input_value:
        logger.debug("Line: %s", line)
        moves.append((line[0], int(line[1:])))
    logger.debug("Moves: %s", moves)
    dial = deque(range(100))
    dial.rotate(50)
    logger.debug("Initial dial: %s", dial)
    counter = 0
    if part == 1:
        for direction, steps in moves:
            if direction == "R":
                dial.rotate(-steps)
            else:
                dial.rotate(steps)
            logger.debug("The dial is rotated %s%s to point at %s", direction, steps, dial[0])
            if dial[0] == 0:
                counter += 1
                logger.debug("Hit zero! Counter is now %s", counter)
        return counter
    for direction, steps in moves:
        for _ in range(steps):
            if direction == "R":
                dial.rotate(-1)
            else:
                dial.rotate(1)
            logger.debug("The dial is rotated %s1 to point at %s", direction, dial[0])
            if dial[0] == 0:
                counter += 1
                logger.debug("Hit zero! Counter is now %s", counter)
    return counter



YEAR = 2025
DAY = 1
input_format = {
    1: "lines",
    2: "lines",
}

funcs = {
    1: solve,
    2: solve,
}

SUBMIT = False

if len(sys.argv) > 1 and sys.argv[1].lower() == "submit":
    SUBMIT = True

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
