"""
Advent Of Code 2016 day 5

Simple refactor, already ran ok,  it takes 39 seconds to answer both parts though.
Could we make it faster?
"""

# import system modules
import logging
import argparse
import hashlib

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def md5_checksum(input_string):
    """
    returns md5sum of input_string
    """
    md5_obj = hashlib.md5()
    md5_obj.update(input_string.encode("utf-8"))
    return md5_obj.hexdigest()


def parse_input(input_text):
    """
    Return stripped door id.
    """
    return input_text.strip()


def solve(door_id, part):
    """
    Function to solve puzzle
    """
    counter = 0
    password = ""
    password_list = ["-"] * 8
    while "-" in password_list:
        if counter != 0:
            counter += 1
        md5_hash = md5_checksum(door_id + str(counter))
        while not md5_hash.startswith("00000"):
            counter += 1
            md5_hash = md5_checksum(door_id + str(counter))
        if (len(password)) < 8:
            password += md5_hash[5]
        if md5_hash[5] in "01234567":
            idx = int(md5_hash[5])
            if password_list[idx] == "-":
                password_list[idx] = md5_hash[6]
    part2 = "".join(password_list)
    return password if part == 1 else part2


YEAR = 2016
DAY = 5
input_format = {
    1: parse_input,
    2: parse_input,
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
