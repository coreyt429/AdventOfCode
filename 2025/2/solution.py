"""
Advent Of Code 2025 day 2



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


def get_ranges(line):
    """
    Function to get ranges from line
    """
    id_ranges = line.split(",")
    for id_range in id_ranges:
        parts = id_range.split("-")
        yield tuple(int(part) for part in parts)


def has_repeats_part1(num):
    """
    Function to check for repeats for part 1
    """
    half = len(str(num)) // 2
    num_str = str(num)
    if num_str[0:half] == num_str[half:]:
        return True
    return False


def has_repeats_part2(num):
    """
    Function to check for repeats for part 2
    """
    half = len(str(num)) // 2
    num_str = str(num)
    for i in range(1, half + 1):
        sub_num = num_str[0:i]
        for j in range(0, len(num_str) + 1):
            if i * j > len(num_str):
                break
            if sub_num * j == num_str:
                return True
    return False


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    logger.debug("Input value: %s", input_value)
    invalid = []
    for id_range in get_ranges(input_value.strip()):
        logger.debug("ID Range: %s", id_range)
        range_invalid = set()
        for num in range(id_range[0], id_range[1] + 1):
            logger.debug("  Number: %d", num)
            half = len(str(num)) // 2
            num_str = str(num)
            if has_repeats_part1(num):
                logger.debug("...... Found repeat: %s in %s", num_str[0:half], num)
                range_invalid.add(num)
            logger.debug(
                "part: %s, num: %s, range_invalid: %s", part, num, range_invalid
            )
            if part == 2 and num not in range_invalid:
                if has_repeats_part2(num):
                    logger.debug("...... Found spaced repeat in %s", num)
                    range_invalid.add(num)
        logger.debug("Range (%s) invalid numbers: %s", id_range, range_invalid)
        # part 2 2022------- too low
        # so yeah, that was my part 1 answer, and I had None cached as the answer so
        # it has bailing on incorrect answer for part 1.
        invalid.extend(list(range_invalid))
    return sum(invalid)


YEAR = 2025
DAY = 2
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
