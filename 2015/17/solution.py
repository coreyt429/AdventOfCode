"""
Advent Of Code 2015 day 17

"""

# import system modules
import logging
import argparse
from itertools import combinations

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

# global list combos, part1 will populate
combos = []
# target is 150 liters

TARGET = 150


def solve(containers, part):
    """
    Function to solve puzzle
    """
    # part 1
    if part == 1:
        combos.clear()
        for idx, _ in enumerate(containers):
            # get combinations of lentgh idx
            for combo in combinations(containers, idx):
                # does this add up to TARGET
                if sum(combo) == TARGET:
                    # save
                    combos.append(combo)
        # return count of combos
        return len(combos)
    # part 2
    # init minimum and min_combos
    minimum = float("infinity")
    min_combos = set()
    # walk combos
    for combo in combos:
        # if current < minimum
        if len(combo) < minimum:
            # set new minimum
            minimum = len(combo)
            min_combos = set([combo])
        elif len(combo) == minimum:
            min_combos.add(combo)
    # return count fo min_combos
    return len(min_combos)


YEAR = 2015
DAY = 17
input_format = {
    1: "integers",
    2: "integers",
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
