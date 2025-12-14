"""
Advent Of Code 2016 day 20

Okay, I tried the brute force method, and it was brutal.

Had to think this one through myself, and didn't resort to looking
at other answers.  Yay!!!

"""

import logging
import argparse
import re
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

MAX_IP = 4294967295
pattern_range = re.compile(r"(\d+)-(\d+)")


def parse_input(input_text):
    """
    Parse the blacklist ranges.
    """
    ranges = []
    for line in input_text.strip().splitlines():
        match = pattern_range.match(line)
        if match:
            ranges.append((int(match.group(1)), int(match.group(2))))
    return ranges


def compute_allowed(ranges):
    """
    Function to solve puzzle
    """
    # set max, so we can find any unblocked on the end
    # ironically, this was necessary for the sample data
    # and not for my input data
    # set smallest and last_smallest
    smallest = 0
    last_smallest = -1
    # clone lines into remainig
    remaining = list(ranges)
    # empty allowed ip set
    allowed = set()
    # empty last blocked address
    max_blocked = 0
    # loop while we have entries in remaining
    while remaining:
        # do we have a new smallest?
        if last_smallest == smallest:
            # add it to allowe
            allowed.add(smallest)
            # update last_smallest
            last_smallest = smallest
            # increment smallest
            smallest += 1
        else:
            # update last_smallest
            last_smallest = smallest
        # clone lines from remainig
        blocks = list(remaining)
        # reset remaining
        remaining = []
        # walk lines in numeric order
        for start, end in sorted(blocks):
            # is smallest blocked by this rule?
            if start <= smallest <= end:
                # increment to end of this block + 1
                smallest = end + 1
            # is smallest smaller than the last number blocked
            if smallest < end:
                # add to remaining for next pass
                remaining.append((start, end))
            # does this rule extend the blocked range
            max_blocked = max(max_blocked, end)
    # lastly, were there any addresses after the last block
    for addr in range(max_blocked + 1, MAX_IP + 1):
        allowed.add(addr)
    # return the allowed set
    return allowed


def solve(ranges, part):
    """
    Return the minimum allowed IP (part 1) or the count of allowed IPs (part 2).
    """
    allowed = compute_allowed(ranges)
    if part == 1:
        return min(allowed)
    return len(allowed)


YEAR = 2016
DAY = 20
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
