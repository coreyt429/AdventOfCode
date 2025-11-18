"""
Advent Of Code 2024 day 21

"""

# import system modules
import logging

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

logger = logging.getLogger(__name__)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    logger.info(input_value)
    return part


if __name__ == "__main__":
    aoc = AdventOfCode(2024, 21)
    aoc.load_text()
    # aoc.load_list()
    # correct answers once solved, to validate changes
    aoc.correct[1] = None
    aoc.correct[2] = None
    aoc.funcs[1] = solve
    aoc.funcs[2] = solve
    aoc.run()
