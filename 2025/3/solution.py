"""
Advent Of Code 2025 day 3

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


already = set()


def joltage_from_bank(bank, joltage=0, length=2):
    """
    Given a bank of digits, pick `length` digits in order to form
    the largest possible number.
    """
    n = len(bank)
    if length > n:
        return joltage  # or 0, depending on how you want to treat this

    start = 0
    chosen = []

    # We need to choose exactly `length` digits
    for remaining in range(length, 0, -1):
        # The current choice must come from [start, n - remaining]
        end = n - remaining

        best_digit = -1
        best_idx = start

        # Find the largest digit we can take in this window
        for i in range(start, end + 1):
            d = bank[i]
            if d > best_digit:
                best_digit = d
                best_idx = i
                if d == 9:  # can't beat 9, early exit
                    break

        chosen.append(best_digit)
        start = best_idx + 1

    value = int("".join(str(d) for d in chosen))
    return max(joltage, value)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    batteries = []
    for line in input_value:
        ints = [int(x) for x in line]
        batteries.append(tuple(ints))
    length = 2
    if part == 2:
        length = 12
    joltage = 0
    for idx, bank in enumerate(batteries):
        already.clear()
        new_joltage = joltage_from_bank(bank, 0, length)
        logger.debug("New joltage from bank %s %s: %s", idx + 1, bank, new_joltage)
        joltage += new_joltage
    return joltage


YEAR = 2025
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
