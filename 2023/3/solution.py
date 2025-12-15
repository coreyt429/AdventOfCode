"""
Advent Of Code 2023 day 3

"""

# import system modules
import logging
import argparse
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_parts(lines):
    """
    Parse input
    """
    numbers = []
    for idx, line in enumerate(lines):
        for match in re.finditer(r"\d+", line):
            numbers.append(
                {
                    "line": idx,
                    "number": int(match.group()),
                    "start": match.start(),
                    "end": match.end(),
                }
            )

    symbols = []
    for idx, line in enumerate(lines):
        for match in re.finditer(r"[^\d\.]", line.strip()):
            symbols.append(
                {
                    "line": idx,
                    "symbol": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                }
            )
    return [numbers, symbols]


def part1(numbers, symbols):
    """
    solve part 1
    """
    result = 0
    for num in numbers:
        partnum = 0
        for sym in symbols:
            if (
                sym["line"] == num["line"] - 1 or sym["line"] == num["line"] + 1
            ):  # line before
                # look for sym start/end to be num start/end+/-1
                if num["start"] - 1 <= sym["start"] and num["end"] + 1 >= sym["end"]:
                    partnum = 1
            elif sym["line"] == num["line"]:
                # look for sym start/end to be num start-1 or num end +1
                if num["start"] - 1 == sym["start"] or num["end"] + 1 == sym["end"]:
                    partnum = 1
        if partnum:
            result += num["number"]
    return result


def part2(numbers, symbols):
    """
    solve part 2
    """
    result = 0
    for sym in symbols:
        count = 0
        gearratio = 1  # sum of gear part numbers
        if sym["symbol"] == "*":
            for num in numbers:
                if (
                    sym["line"] == num["line"] - 1 or sym["line"] == num["line"] + 1
                ):  # line before
                    # look for sym start/end to be num start/end+/-1
                    if (
                        num["start"] - 1 <= sym["start"]
                        and num["end"] + 1 >= sym["end"]
                    ):
                        count += 1
                        gearratio *= num["number"]
                elif sym["line"] == num["line"]:
                    # look for sym start/end to be num start-1 or num end +1
                    if num["start"] - 1 == sym["start"] or num["end"] + 1 == sym["end"]:
                        count += 1
                        gearratio *= num["number"]
            if count == 2:
                result += gearratio
    return result


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    numbers, symbols = parse_parts(input_value)
    if part == 2:
        return part2(numbers, symbols)
    return part1(numbers, symbols)


YEAR = 2023
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
