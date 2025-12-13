"""
Advent Of Code 2015 day 20

My original solution for this worked, but was a bit ugly

I have reworked part1 to use sympy.divisors



"""

# import system modules
import logging
import argparse
from sympy import divisors

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

answer = {1: None, 2: None}


def part1(target):
    """
    Function to solve part 1
    """
    # optimization guess work
    # starting point 20% of 10% of target
    current_house = target // 10 // 5
    # If guesswork fails, uncomment next line and wait 6 seconds longer
    # current_house = 1
    # loop
    while True:
        # get factors
        factors = divisors(current_house)
        # calculate presents
        presents = sum(factors) * 10
        # have we exceeded the target?
        if presents > target:
            break
        # increment current_house
        # optimization cheat, once we determined that both answers are divisible by 40
        current_house += 40
        # current_house += 1
    return current_house


def part2(target):
    """
    Function to solve part 2
    """
    # optimization guess work
    # lets start with the previous answer, as this shoudl be higher
    current_house = answer[1]
    # If guesswork fails, uncomment next line and wait 6 seconds longer
    # current_house = 1
    # loop
    while True:
        # get factors
        factors = divisors(current_house)
        lazy_factors = set()
        for factor in factors:
            if factor * 50 >= current_house:
                lazy_factors.add(factor)
        # calculate presents
        presents = sum(factor * 11 for factor in lazy_factors)
        # have we exceeded the target?
        if presents > target:
            break
        # increment current_house
        # optimization cheat, once we determined that both answers are divisible by 40
        current_house += 40
        # current_house += 1
    return current_house


def solve(input_data, part):
    """
    Function to solve puzzle
    """
    target = int(input_data.strip())
    if part == 1:
        answer[1] = part1(target)
        return answer[1]
    if answer[1] is None:
        answer[1] = part1(target)
    return part2(target)


YEAR = 2015
DAY = 20
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
