"""
Advent Of Code 2015 day 13

"""

# import system modules
import logging
import argparse
import itertools
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

# Regex pattern for input
# Alice would gain 2 happiness units by sitting next to Bob.
pattern_input = re.compile(r"(\w+) would (gain|lose) (\d+) .* to (\w+).")


def parse_input(input_text):
    """
    Function to parse input
    """
    # happiness score structure
    scores = {}
    # loop through lines
    for line in input_text.strip().splitlines():
        if not line:
            continue
        # match pattern
        match = pattern_input.match(line)
        if match:
            # get values
            (peep, gain_lose, happiness, neighbor) = match.groups()
            # initialize peep if not already
            if not peep in scores:
                scores[peep] = {}
            # get integer value for happiness
            happiness = int(happiness)
            # if lose, negate hapiness
            if gain_lose == "lose":
                happiness *= -1
            # store score
            scores[peep][neighbor] = happiness
    return scores


def score(my_map, my_peeps):
    """
    function to score seating arrangement
    """
    happiness = {}
    # print(my_map)
    for idx, current_peep in enumerate(my_peeps):
        if not current_peep in happiness:
            # initialize score
            happiness[current_peep] = 0
        # if first
        # get next peep
        next_peep = my_peeps[(idx + 1) % len(my_peeps)]
        # get previous peep
        prev_peep = my_peeps[(idx - 1) % len(my_peeps)]

        # add next_peep happiness
        happiness[current_peep] += my_map[current_peep][next_peep]
        # add prev_peep happiness
        happiness[current_peep] += my_map[current_peep][prev_peep]
    # return sum of hapiness
    return sum(happiness.values())


def solve(parsed_data, part):
    """
    Function to solve puzzle
    """
    # part 2
    if part == 2:
        # add Me
        parsed_data["Me"] = {}
        # for add peep relations to me
        for peep in parsed_data.keys():
            if not peep == "Me":
                parsed_data["Me"][peep] = 0
                parsed_data[peep]["Me"] = 0
    # initialize max_happiness
    max_happiness = 0
    # get people
    peeps = set(parsed_data.keys())
    # use itertools to get permutations of people
    options = list(itertools.permutations(peeps))
    # test all options
    for option in options:
        # get score
        my_score = score(parsed_data, option)
        # if greater happiness
        max_happiness = max(max_happiness, my_score)
    # return results
    return max_happiness


YEAR = 2015
DAY = 13
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
