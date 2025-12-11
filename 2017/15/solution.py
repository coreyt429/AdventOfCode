"""
Advent Of Code 2017 day 15

"""

# import system modules
from __future__ import annotations
import logging
import argparse
import itertools
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)


def generator_func(seed, factor, divisor=None):
    """
    Function to generate Lehmer random numbers
    """
    current = seed
    while True:
        current = current * factor % 2147483647
        if not divisor or current % divisor == 0:
            yield current


def parse_input(lines):
    """
    Function to parse input
    """
    results = {}
    for line in lines:
        match = re.match(r"Generator (\w) starts with (\d+)", line)
        if match:
            results[match.group(1)] = int(match.group(2))
    return results["A"], results["B"]


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    seed_a, seed_b = parse_input(input_value)
    if part == 1:
        gen_a = generator_func(seed_a, 16807)
        gen_b = generator_func(seed_b, 48271)
        cycles = 40_000_000
    else:
        gen_a = generator_func(seed_a, 16807, 4)
        gen_b = generator_func(seed_b, 48271, 8)
        cycles = 5_000_000
    counter = 0
    mask = 0xFFFF
    for val_a, val_b in itertools.islice(zip(gen_a, gen_b), cycles):
        if (val_a & mask) == (val_b & mask):
            counter += 1
    return counter


YEAR = 2017
DAY = 15
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
