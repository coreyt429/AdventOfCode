"""
Advent Of Code YEAR day DAY

"""

# import system modules
import sys
import logging

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    return part


year = YEAR
day = DAY
input_format = {
    1: "lines",
    2: "lines",
}

funcs = {
    1: solve,
    2: solve,
}

SUBMIT = False

if len(sys.argv) > 1 and sys.argv[1].lower() == "submit":
    SUBMIT = True

if __name__ == "__main__":
    aoc = AdventOfCode(year=year, day=day, input_formats=input_format, funcs=funcs)
    aoc.run(submit=SUBMIT)
