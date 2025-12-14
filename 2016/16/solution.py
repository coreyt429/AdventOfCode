"""
Advent Of Code 2016 day 16
This one was pretty easy.  I worked it out in the jupyter notebook, then just cleaned it up here
"""

import logging
import argparse
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def dragon_curve(str_a):
    """
    Function to generate dragon curve of string
    """
    # str_b = str_a reveresed, with the '1's replaced with '2's
    str_b = str_a[::-1].replace("1", "2")
    # replace the '0's with '1's
    str_b = str_b.replace("0", "1")
    # replace the '2's with '0's
    str_b = str_b.replace("2", "0")
    # return concatenated string
    return f"{str_a}0{str_b}"


def checksum(input_string):
    """
    Function to generate checksum
    """
    my_checksum = ""
    # walk every other index of the string
    for idx in range(0, len(input_string), 2):
        # if idx matches idx+1
        if input_string[idx] == input_string[idx + 1]:
            my_checksum += "1"
        else:
            my_checksum += "0"
    # if length is odd, return
    if len(my_checksum) % 2 == 1:
        return my_checksum
    # return recursively until we get an odd checksum
    return checksum(my_checksum)


def solve(input_data, part):
    """
    Generate the disk checksum for the requested part.
    """
    size = {1: 272, 2: 35651584}
    data = input_data.strip()
    while len(data) < size[part]:
        data = dragon_curve(data)
    data = data[: size[part]]
    return int(checksum(data))


YEAR = 2016
DAY = 16
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
