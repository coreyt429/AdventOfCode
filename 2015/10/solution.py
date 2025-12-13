"""
Advent Of Code 2015 day 10

Part1: 252594
Part2: 3579328

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


def look_and_say_mine(sequence):
    """
    Function to perform look and say conversion
    """
    result = ""
    current_digit = sequence[0]
    count = 1

    for digit in sequence[1:]:
        if digit == current_digit:
            count += 1
        else:
            result += str(count) + current_digit
            current_digit = digit
            count = 1
    result += str(count) + current_digit
    return result


def look_and_say(sequence):
    """
    Function to perform look and say conversion
    After completing this, I ran my solution through claude.ai for performance suggestions
    storing result as a list rather than string, shaved 1 second off of part 2
    """
    result = []
    current_digit = sequence[0]
    count = 1

    for digit in sequence[1:]:
        if digit == current_digit:
            count += 1
        else:
            result.extend([str(count), current_digit])
            current_digit = digit
            count = 1

    result.extend([str(count), current_digit])
    return "".join(result)


def solve(input_string, part):
    """
    Function to solve puzzle
    """
    num_iters = 40 if part == 1 else 50
    new_string = input_string.strip()
    for _ in range(num_iters):
        new_string = look_and_say(new_string)
    return len(new_string)


YEAR = 2015
DAY = 10
input_format = {
    1: "text",
    2: "text",
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
