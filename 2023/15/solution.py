"""
Advent Of Code 2023 day 15

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


def parse_input(lines: list[str]) -> tuple:
    """parse input data into codes tuple"""
    codes = []
    for line in lines:
        for code in line.split(","):
            codes.append(code)

    return tuple(codes)


def hash_code(input_string: str) -> int:
    """Generate hash value for input string"""
    hash_val = 0
    for char in input_string:
        # Determine the ASCII code for the current character of the string.
        # Increase the current value by the ASCII code you just determined.
        hash_val += ord(char)
        # Set the current value to itself multiplied by 17.
        hash_val *= 17
        # Set the current value to the remainder of dividing itself by 256.
        hash_val = hash_val % 256
    return hash_val


def calculate_power(box_index: int, slot_index: int, focal_length: int) -> int:
    """Calculate power for a given lens in a box"""
    power = box_index + 1  # Box number (1-based)
    power *= slot_index + 1  # Slot number (1-based)
    power *= focal_length  # Focal length
    return power


def total_power(boxes: list[list[list]]) -> int:
    """Calculate total power for all lenses in boxes"""
    total = 0
    for idx, box in enumerate(boxes):
        for idx2, slot in enumerate(box):
            total += calculate_power(idx, idx2, slot[1])
    return total


def part2(parsed_data: tuple) -> int:
    """Solve part 2 of puzzle"""
    boxes = [[] for _ in range(256)]
    pattern_code = r"([a-z]+)([=-])(\d*)"
    for code in parsed_data:
        matches = re.findall(pattern_code, code)
        for match in matches:
            label, op, fl = match
            codehash = hash_code(label)
            box = boxes[codehash]
            if op == "=":
                replaced = False
                newbox = []
                for item in box:
                    if not item[0] == label:
                        newbox.append(item)
                    else:
                        newbox.append([label, int(fl)])
                        replaced = True
                if not replaced:
                    newbox.append([label, int(fl)])
                boxes[codehash] = newbox
            elif op == "-":
                box = [item for item in box if not item[0] == label]
                boxes[codehash] = box
    return total_power(boxes)


def solve(input_value: list[str], part: int) -> int:
    """
    Function to solve puzzle
    """
    parsed_data = parse_input(input_value)
    if part == 1:
        retval = 0
        for code in parsed_data:
            retval += hash_code(code)
        return retval

    return part2(parsed_data)


YEAR = 2023
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
