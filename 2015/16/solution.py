"""
Advent Of Code 2015 day 16

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

TICKER_TAPE = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


# Sue 1: goldfish: 9, cars: 0, samoyeds: 9
def parse_input(lines):
    """
    Function to parse input file
    """
    # init aunts
    aunts = {}
    # walk lines
    for line in lines:
        # split key/value pairs
        aunt, properties_str = line.split(": ", 1)
        properties = {}
        # split properties by ', ''
        for prop in properties_str.split(", "):
            # split prop_name and prop_value by ': '
            prop_name, prop_value = prop.split(": ")
            # store int value of prop_value
            properties[prop_name] = int(prop_value)
        # store aunt
        aunts[aunt] = properties
    return aunts


def part1(parsed_data, matches):
    """
    Function to solve part 1
    """
    # walk aunts
    for aunt, properties in parsed_data.items():
        # walk ticket tape properties
        for prop_name, prop_value in TICKER_TAPE.items():
            # does the aunt have prop_name?
            if prop_name in properties.keys():
                # does the aunt match prop_value
                if properties[prop_name] == prop_value:
                    # increment aunt
                    matches[aunt] += 1
    # Find the aunt with the largest value
    aunt_with_largest_value = max(matches, key=matches.get)
    logger.debug("matches: %s", matches)
    match = re.search(r"\d+", aunt_with_largest_value)
    logger.debug("match: %s", match)
    key_int = None
    if match:
        key_int = int(match.group(0))
    return key_int


def part2(parsed_data, matches):
    """
    Function to solve part 1
    """
    # walk aunts
    for aunt, properties in parsed_data.items():
        # walk ticket tape
        for prop_name, prop_value in TICKER_TAPE.items():
            # does aunt have prop_name?
            if prop_name in properties.keys():
                # special handling for cats and trees
                if prop_name in ["cats", "trees"]:
                    # aunt > than prop_value?
                    if properties[prop_name] > prop_value:
                        # increment aunt
                        matches[aunt] += 1
                # special handling for pomeranians and goldfish
                elif prop_name in ["pomeranians", "goldfish"]:
                    # aunt < prop_value
                    if properties[prop_name] < prop_value:
                        # increment aunt
                        matches[aunt] += 1
                # normal processing for other properties
                elif properties[prop_name] == prop_value:
                    # increment aunt
                    matches[aunt] += 1
    # Find the key with the largest value
    key_with_largest_value = max(matches, key=matches.get)
    logger.debug("matches: %s", matches)
    match = re.search(r"\d+", key_with_largest_value)
    logger.debug("match: %s", match)
    key_int = None
    if match:
        key_int = int(match.group(0))
    return key_int


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # init matches
    matches = {}
    # parse data
    parsed_data = parse_input(input_value)
    # init aunts
    # pylint's cheese has slipped off its cracker, I'm not using the value fo parsed_data
    # in this loop, and it complains that I shoudl use items().  but if I do that it
    # complains that I don't use properties
    for aunt in parsed_data.keys():  # pylint: disable=consider-iterating-dictionary
        matches[aunt] = 0
    # part 1
    if part == 1:
        return part1(parsed_data, matches)
    # part 2
    return part2(parsed_data, matches)


YEAR = 2015
DAY = 16
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
