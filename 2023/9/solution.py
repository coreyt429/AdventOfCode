"""
Advent Of Code 2023 day 9

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


def parse_input(lines: list[str]) -> list[list[int]]:
    """Parse input data into list of lists of integers"""
    # Split the data into lines
    retval = []
    # loop through lines
    for line in lines:
        int_data_list = []
        for str_data in line.split():
            int_data_list.append(int(str_data))
        retval.append(int_data_list)
    return retval


def prev_value(data_list: list[int]) -> int:
    """Get previous value in sequence"""
    my_data = data_list.copy()
    new_data = []
    for i in range(0, len(my_data) - 1):
        new_data.append(my_data[i + 1] - my_data[i])
    allzeros = True
    for i in new_data:
        if i != 0:
            allzeros = False
    if not allzeros:
        new_data.insert(0, prev_value(new_data))
    return my_data[0] - new_data[0]


def next_value(data_list: list[int]) -> int:
    """Get next value in sequence"""
    my_data = data_list.copy()
    new_data = []
    for i in range(0, len(my_data) - 1):
        new_data.append(my_data[i + 1] - my_data[i])
    allzeros = True
    for i in new_data:
        if i != 0:
            allzeros = False
    if not allzeros:
        new_data.append(next_value(new_data))
    return my_data[-1] + new_data[-1]


def part1(parsed_data: list[list[int]]) -> int:
    """Solve part 1 of puzzle"""
    retval = 0
    for int_data_list in parsed_data:
        next_val = next_value(int_data_list)
        retval += next_val
    return retval


def part2(parsed_data: list[list[int]]) -> int:
    """Solve part 2 of puzzle"""
    retval = 0
    for int_data_list in parsed_data:
        next_val = prev_value(int_data_list)
        retval += next_val
    return retval


def solve(input_value: list[str], part: int) -> int:
    """
    Function to solve puzzle
    """
    parsed_data = parse_input(input_value)
    if part == 1:
        return part1(parsed_data)
    return part2(parsed_data)


YEAR = 2023
DAY = 9
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
