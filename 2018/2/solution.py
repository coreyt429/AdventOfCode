"""
Advent Of Code 2018 day 2

"""

# import system modules
from __future__ import annotations
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def check_sum(box_ids):
    """
    checksum box_ids
    """
    matches = {2: set(), 3: set()}
    for box_id in box_ids:
        for char in set(list(box_id)):
            count = box_id.count(char)
            if count in matches:
                matches[count].add(box_id)
    # print(matches)
    return len(matches[2]) * len(matches[3])


def is_match(id_1, id_2):
    """
    check box_id for match
    """
    length = len(id_1)
    target = length - 1
    count = 0
    mismatch = None
    for idx, char in enumerate(id_1):
        if id_2[idx] == char:
            count += 1
        else:
            mismatch = idx
    # print(f"{target}: {count}: {id_1} {id_2}")
    if not count == target:
        return False, None
    # note this will fail if the mismatch is at 0, but I don't think it is
    return True, mismatch


def find_matches(box_ids):
    """
    find box_ids that mostly match
    """
    potentials = set()
    for box_id in box_ids:
        for box_id2 in box_ids:
            if box_id == box_id2:
                continue
            match, mismatch = is_match(box_id, box_id2)
            if match:
                potentials.add(tuple([mismatch] + sorted([box_id, box_id2])))
    if len(potentials) == 1:
        mismatch, box_id, _ = potentials.pop()
        box_id = list(box_id)
        box_id.pop(mismatch)
        return "".join(box_id)
    return "somethin bad happened"


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        # part 2
        return find_matches(input_value)
    # part 1
    return check_sum(input_value)


YEAR = 2018
DAY = 2
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
