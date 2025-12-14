"""
Advent Of Code 2019 day 9

"""

# import system modules
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from intcode import IntCodeComputer  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_input(input_text):
    """
    Return the raw intcode program.
    """
    return input_text.strip()


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # init output
    output = []
    # init icc with input data
    icc = IntCodeComputer(input_value)
    # attach output queue
    icc.set_output(output)
    # run program with specified input (maybe not so) coincidentally the part number
    icc.run(input_val=part)
    # return the output code
    return output[0]


YEAR = 2019
DAY = 9
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
