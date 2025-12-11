"""
Advent Of Code 2017 day 13

"""

# import system modules
from __future__ import annotations
import logging
import argparse
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)


def parse_input(lines):
    """
    Function to parse input
    """
    data = {}
    for line in lines:
        pos, scan_range = [int(num) for num in re.findall(r"(\d+)", line)]
        data[pos] = scan_range
    return data


def position(scanner_range, picosecond):
    """
    Function to calculate scanner position
    """
    picosecond = picosecond % ((scanner_range * 2) - 2)
    if picosecond < scanner_range:
        return picosecond
    return (scanner_range - 2) - (picosecond - scanner_range)


def severity(scanners):
    """
    function to calculate severity
    """
    total = 0
    for picosecond in range(max(scanners.keys()) + 1):
        layer = picosecond
        if layer in scanners:
            pos = position(scanners[layer], picosecond)
            if pos == 0:
                total += layer * scanners[layer]
    return total


def success(scanners, delay):
    """
    Function to test for successful firewall pass
    """
    max_layer = max(scanners.keys())
    for picosecond in range(delay, max_layer + delay + 1):
        layer = picosecond - delay
        if layer in scanners:
            pos = position(scanners[layer], picosecond)
            if pos == 0:
                return False
    return True


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    scanners = parse_input(input_value)
    if part == 1:
        return severity(scanners)
    delay = 3_800_000
    while True:
        if success(scanners, delay):
            return delay
        delay += 1


YEAR = 2017
DAY = 13
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
