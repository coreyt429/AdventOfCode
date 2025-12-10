"""
Advent Of Code 2022 day 20

"""

# import system modules
import logging
import argparse
from collections import deque

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def decrypt_file(start_state, passes=1):
    """
    Function to decrypt file
    """
    deq = deque((i, val) for i, val in enumerate(start_state))
    length = len(start_state)
    for _ in range(passes):
        for original_index, value in enumerate(start_state):
            for i in range(length):
                if deq[i][0] == original_index:
                    current_index = i
                    break
            deq.rotate(-current_index)
            item = deq.popleft()
            deq.rotate(-value)
            deq.appendleft(item)
    return deq


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    start_state = tuple(int(x) for x in input_value)
    passes = 1
    if part == 2:
        start_state = tuple(x * 811589153 for x in start_state)
        passes = 10
    deq = decrypt_file(start_state, passes)
    logger.debug("Decrypted state: %s", deq)
    answer = 0
    while deq[0][1] != 0:
        deq.rotate(-1)
    for _ in range(3):
        deq.rotate(-1000)
        logger.debug("Value at position(%d): %s", 1000, deq[0][1])
        answer += deq[0][1]
    return answer


YEAR = 2022
DAY = 20
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
