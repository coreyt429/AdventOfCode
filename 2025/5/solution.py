"""
Advent Of Code 2025 day 5

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


def parse_input(input_value):
    """
    Function to parse input
    """
    fresh_txt, ingredients_text = input_value.split("\n\n")
    fresh = set()
    ingredients = []
    for fresh_range in fresh_txt.splitlines():
        start, end = fresh_range.split("-")
        fresh.add(tuple([int(start), int(end)]))
    for ingredient in ingredients_text.splitlines():
        ingredients.append(int(ingredient))
    return fresh, ingredients


def consolidate_ranges(ranges):
    """
    Function to consolidate overlapping ranges
    """
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    consolidated = []
    current_start, current_end = sorted_ranges[0]
    for start, end in sorted_ranges[1:]:
        if start <= current_end:
            current_end = max(current_end, end)
        else:
            consolidated.append((current_start, current_end))
            current_start, current_end = start, end
    consolidated.append((current_start, current_end))
    return tuple(consolidated)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    fresh, ingredients = parse_input(input_value)
    counter = 0
    if part == 2:
        consolidated = consolidate_ranges(fresh)
        for start, end in consolidated:
            logger.debug("Consolidated range: %d-%d", start, end)
            counter += end - start + 1
        logger.debug("Total fresh ingredients: %d", counter)
        return counter
    logger.debug("Fresh: %s", fresh)
    logger.debug("Ingredients: %s", ingredients)
    counter = 0
    for ingredient in ingredients:
        for fresh_range in fresh:
            if fresh_range[0] <= ingredient <= fresh_range[1]:
                counter += 1
                break
    return counter


YEAR = 2025
DAY = 5
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
