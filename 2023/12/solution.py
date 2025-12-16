"""
Advent Of Code 2023 day 12

"""

# import system modules
import logging
import argparse
import functools


# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_input(lines: list[str]) -> list[dict]:
    """parse input into list of records"""
    records = []
    for line in lines:
        record, counts = line.split(" ")
        records.append(
            {"record": record, "counts": [int(count) for count in counts.split(",")]}
        )
    return records


@functools.cache
def n_arrangements(s, groups_left, group_sz):
    """
    s = what is left of input line
    groups_left = groups left (tuple)
    group_sz = current size of group in consumed line (s)
    """
    # base case for recursion
    if len(s) == 0:
        if len(groups_left) == 0 and group_sz == 0:
            # No groups left, it's a match
            return 1
        if len(groups_left) == 1 and group_sz == groups_left[0]:
            # 1 group left the same size as current group, match
            return 1
        # No match
        return 0

    # consumed groups larger than groups left
    if len(groups_left) > 0 and group_sz > groups_left[0]:
        return 0
    # don't expect any more groups but I am in a group
    # I need group therapy
    if len(groups_left) == 0 and group_sz > 0:
        return 0

    # all good so far
    n = 0

    spring = s[0]

    # If ? is # or if spring is # is the same case
    if spring in ("#", "?"):
        n += n_arrangements(s[1:], groups_left, group_sz + 1)

    # If ? is . or if spring is . is the same case
    if spring in (".", "?"):
        if len(groups_left) > 0 and group_sz == groups_left[0]:
            n += n_arrangements(s[1:], groups_left[1:], 0)
        elif group_sz == 0:
            n += n_arrangements(s[1:], groups_left, 0)

    # so above ? will recurse 2 times while . or # will recurse
    # 1 time, each case consuming one input line (s) character
    return n


def part1(parsed_data):
    """solve part 1"""
    retval = 0
    for record in parsed_data:
        template = record["record"]
        counts = []
        for count in record["counts"]:
            counts.append(count)
        counts = tuple(counts)
        n = n_arrangements(template, counts, 0)
        # print(template,counts, n)
        retval += n
    return retval


def part2(parsed_data):
    """solve part 2"""
    retval = 0
    for record in parsed_data:
        template = "?".join(
            [
                record["record"],
                record["record"],
                record["record"],
                record["record"],
                record["record"],
            ]
        )
        counts = []
        for _ in range(5):
            for count in record["counts"]:
                counts.append(count)
        counts = tuple(counts)
        n = n_arrangements(template, counts, 0)
        # print(template,counts, n)
        retval += n
    return retval


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    records = parse_input(input_value)
    if part == 1:
        return part1(records)
    return part2(records)


YEAR = 2023
DAY = 12
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
