"""
Advent Of Code 2024 day 2

A bit of simple iteration and recursion makes part 2 work.

This technique runs in 0.01 seconds, so not really looking for a faster method.

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


def parse_data(lines):
    """Function to parse input data"""
    reports = []
    for line in lines:
        report = [int(num) for num in line.split(" ")]
        reports.append(tuple(report))
    return tuple(reports)


def dampen_report(report, dampener):
    """Function to dampen reports: Part 2"""
    if dampener == 1:
        return False
    for idx in range(len(report)):
        my_list = list(report)
        my_list.pop(idx)
        if is_safe(tuple(my_list), dampener - 1):
            return True
    return False


def is_safe(report, dampener=1):
    """Function to determine if a report is safe"""
    safe = True
    if report not in [tuple(sorted(report)), tuple(reversed(sorted(report)))]:
        return dampen_report(report, dampener)
    for idx, num in enumerate(report[:-1]):
        if report[idx + 1] == num:
            return dampen_report(report, dampener)
        if not -4 < report[idx + 1] - num < 4:
            return dampen_report(report, dampener)
    return safe


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    reports = parse_data(input_value)
    counter = 0
    for report in reports:
        if is_safe(report, part):
            counter += 1
    return counter


YEAR = 2024
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
