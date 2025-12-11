"""
Advent Of Code 2017 day 12

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


def trace_pipe(pipes, current, visited=()):
    """
    Function to trace from one pipe to find connections
    """
    visited = (*visited, current)
    for target in pipes[current]:
        if target not in visited:
            visited = trace_pipe(pipes, target, visited)
    return visited


def load_pipes(lines):
    """
    Function to read input and build pipe connections
    """
    connections = {}
    all_nums = set()
    for line in lines:
        nums = [int(num) for num in re.findall(r"(\d+)", line)]
        all_nums.update(nums)
        current = nums.pop(0)
        for num in nums:
            connections.setdefault(current, set()).add(num)
            connections.setdefault(num, set()).add(current)
    return connections, all_nums


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    pipes, all_programs = load_pipes(input_value)
    connected = trace_pipe(pipes, 0)
    disconnected = all_programs.difference(connected)
    if part == 1:
        return len(connected)
    groups = [connected]
    while disconnected:
        connected = trace_pipe(pipes, disconnected.pop())
        groups.append(connected)
        disconnected.difference_update(connected)
    return len(groups)


YEAR = 2017
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
