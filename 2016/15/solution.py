"""
Advent Of Code 2016 day 15

This one is not 100% in my current style, but it does produce the same output.
It is structually in the same spirit, so moving on.

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


def parse_input(input_text):
    """
    Function to parse input
    """
    disks = []
    for line in input_text.strip().splitlines():
        match = re.findall(r"\d+", line)
        if match:
            disks.append(tuple(int(data) for data in match))
    return disks


def solve(disks, part):
    """
    Function to solve puzzle
    """
    local_disks = [tuple(disk) for disk in disks]
    if part == 2:
        local_disks.append((7, 11, 0, 0))
    # initialize delay and drops
    delay = 0
    drops = {}
    # walk disks
    for disk in local_disks:
        # increment delay for each disk
        delay += 1
        # identify first clock tick of first slot
        first_slot = disk[1] - disk[3]
        # initialize drops
        drops[disk] = set()
        # This works, but causes some disks to start negative
        current_drop = first_slot - delay
        # this worked, but there has to be a better way to loop this
        # I tried a few more elegant solutions, but they were too slow
        # see jupyter notebook for other trials
        # collect the first 1100000 drop times for the disk
        while len(drops[disk]) < 1100000:
            drops[disk].add(current_drop)
            current_drop += disk[1]
    # initialize common drops, to store drops that are common to all disks
    # used the first disk as the initial common
    common_drops = drops[local_disks[0]]
    # walk disks again
    for disk in local_disks:
        # reduce common_drops to the intersection of iteself and the current disk
        common_drops = common_drops.intersection(drops[disk])
    # return the lowest value in common_drops
    return sorted(list(common_drops))[0]


YEAR = 2016
DAY = 15
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
