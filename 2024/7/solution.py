"""
Advent Of Code 2024 day 7

"""

# import system modules
import logging
import argparse
import math
from heapq import heappop, heappush

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_input(lines):
    """Function to parse puzzle input"""
    inputs = []
    for line in lines:
        value_text, nums_text = line.split(": ")
        value = int(value_text)
        nums = [int(num) for num in nums_text.split(" ")]
        inputs.append((value, tuple(nums)))
    return tuple(inputs)


def can_solve(target, nums, operators, next_op="None", value=None):
    """Function to determine if equation is solveable"""
    heap = []
    heappush(heap, (len(nums), nums, "None", None))

    while heap:
        _, nums, next_op, value = heappop(heap)
        nums = list(nums)
        if not nums:
            if value == target:
                return True
            continue
        if value is None:
            value = nums.pop(0)
        if next_op == "None":
            for try_op in operators.keys():
                heappush(heap, (len(nums), tuple(nums), try_op, value))
        else:
            value = operators[next_op](value, nums.pop(0))
            heappush(heap, (len(nums), tuple(nums), "None", value))
    if not nums and value == target:
        return True
    return False


def concat(num_1, num_2):
    """function to concatenate two numbers"""
    if num_2 == 0:
        return num_1 * 10
    return num_2 + (num_1 * 10 ** math.ceil(math.log10(num_2) + 1e-7))


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    operators = {"+": lambda a, b: a + b, "*": lambda a, b: a * b}
    if part == 2:
        operators["||"] = concat
    total = 0
    equations = parse_input(input_value)
    for equation in equations:
        if can_solve(equation[0], equation[1], operators):
            total += equation[0]
    return total


YEAR = 2024
DAY = 7
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
