"""
Advent Of Code 2024 day 1

List/tuple manipulation and number comparison.  For part 1, I made myself use zip(),
I usually don't naturally go there decades of nested for loops are hard to unwind :)

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
    list_1 = []
    list_2 = []
    for line in lines:
        num_1, num_2 = (int(num) for num in line.split("   "))
        list_1.append(num_1)
        list_2.append(num_2)
    return tuple(list_1), tuple(list_2)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    loc_lists = parse_data(input_value)
    if part == 2:
        similarity = 0
        for num in loc_lists[0]:
            count = loc_lists[1].count(num)
            similarity += num * count
        return similarity
    distance = 0
    for num_a, num_b in zip(*(sorted(loc_list) for loc_list in loc_lists)):
        distance += abs(num_a - num_b)
    return distance


YEAR = 2024
DAY = 1
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
