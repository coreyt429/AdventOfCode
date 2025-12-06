"""
Advent Of Code 2025 day 6

Notes:

 for part 2, we need to update how we are parsing the operands.

 spacing in the input matters.  The logec for convert_operands is probably good
 but we need to keep the spaces to line things up correctly.

"""

# import system modules
import logging
import argparse
from math import prod


# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def get_problems(input_value):
    """
    Function to parse input into problems
    """
    stops = set()
    # look at -1 to get spacing
    for idx, char in enumerate(input_value[-1]):
        if char != " ":
            logger.debug("char at %d: '%s'", idx, char)
            stops.add(idx)
    stops = list(sorted(stops))
    logger.debug("stops: %s", stops)
    problems = []
    for line in input_value:
        problem = [line[i:j] for i, j in zip(stops, stops[1:] + [None])]
        logger.debug("problem line: %s", problem)
        # ['0123', '4567', '8901', '23456']
        # problem = [element for element in line.strip().split(' ') if element != '']
        problems.append(problem)
    return list(zip(*problems, strict=True))


def convert_operands(operands):
    """
    Function to convert operands for part 2
    """
    logger.debug("original operands: %s", operands)
    max_len = max(len(op) for op in operands)
    converted = ["" for _ in range(max_len + 1)]
    for n in range(max_len - 1, -1, -1):
        for idx, op in enumerate(operands):
            logger.debug("op[%d]: '%s'", idx, op)
            if n < len(op):
                converted[n] += op[n]
                logger.debug("converted[%d]: '%s'", n, converted[n])
    logger.debug("converted operands: %s", converted)
    return [num for num in converted if num.replace(" ", "").isdigit()]


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    problems = get_problems(input_value)
    logger.debug("problems: %s", problems)
    result = 0
    for problem in problems:
        operands = problem[:-1]
        if part == 2:
            operands = convert_operands(operands)
        operator = problem[-1].replace(" ", "")
        logger.debug("operands: %s", operands)
        logger.debug("operator: %s", operator)
        if operator == "+":
            result += sum(int(op.replace(" ", "")) for op in operands)
        elif operator == "*":
            result += prod(int(op.replace(" ", "")) for op in operands)
    return result


YEAR = 2025
DAY = 6
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
