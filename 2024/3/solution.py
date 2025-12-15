"""
Advent Of Code 2024 day 3

Nice regex challenge.  Not much else to say on this one.


"""

# import system modules
import logging
import argparse
import re
import math

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    pattern_mul_digits = re.compile(r"mul\((-?\d+),(-?\d+)\)")
    pattern_do_dont_mul = re.compile(r"(mul\(-?\d+,-?\d+\))|(do\(\))|(don't\(\))")
    pairs = []
    do_mul = True
    for line in input_value:
        for command in pattern_do_dont_mul.findall(line):
            for item in command:
                if "do()" in item:
                    do_mul = True
                    continue
                if "don't()" in item:
                    do_mul = False
                    continue
                if "mul" in item and any([do_mul, part == 1]):
                    pair = pattern_mul_digits.findall(item)[0]
                    pairs.append([int(num) for num in pair])
    return sum((math.prod(pair) for pair in pairs))


YEAR = 2024
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
