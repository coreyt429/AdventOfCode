"""
Advent Of Code 2015 day 4

"""

# import system modules
import logging
import argparse
import hashlib
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def part1(my_key, _part=None):
    """
    Function to solve part1
    """
    my_num = 0
    # Create an MD5 hash object
    hash_object = hashlib.md5()
    hex_md5 = ""
    while not re.match("^00000", hex_md5):
        my_num += 1
        # Create a new MD5 hash object for each iteration
        hash_object = hashlib.md5()
        hash_object.update(f"{my_key}{my_num}".encode())
        hex_md5 = hash_object.hexdigest()
    return my_num


def part2(my_key, _part=None):
    """
    Function to solve part 2
    """
    my_num = 0
    # Create an MD5 hash object
    hash_object = hashlib.md5()
    hex_md5 = ""
    while not re.match("^000000", hex_md5):
        my_num += 1
        # Create a new MD5 hash object for each iteration
        hash_object = hashlib.md5()
        hash_object.update(f"{my_key}{my_num}".encode())
        hex_md5 = hash_object.hexdigest()
    return my_num


YEAR = 2015
DAY = 4
input_format = {
    1: "text",
    2: "text",
}

funcs = {
    1: part1,
    2: part2,
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
