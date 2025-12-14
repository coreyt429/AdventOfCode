"""
Advent Of Code 2020 day 6

python sets make this one pretty easy.

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


def parse_groups(input_string):
    """Function to parse groups"""
    groups = []
    # Each group's answers are separated by a blank line
    input_groups = input_string.split("\n\n")
    for group in input_groups:
        # within each group, each person's answers are on a single line.
        groups.append(group.splitlines())
    return groups


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    groups = parse_groups(input_value)
    total = 0
    total_2 = 0
    for group in groups:
        all_answers = set()
        first = True
        # part 2:
        # You don't need to identify the questions to which anyone answered "yes";
        # you need to identify the questions to which everyone answered "yes"!
        # so for the people in the group, we will use set intersection to
        # identify the questions answered by all in the group
        for person in group:
            # print(f"all_answers: {all_answers}, person: {person}")
            if first:
                all_answers = set(person)
                first = False
            else:
                all_answers.intersection_update(set(person))
        group_answers = set("".join(group))

        # print(f"Final all_answers: {all_answers} ")
        total_2 += len(all_answers)
        # For each group, count the number of questions to which anyone answered "yes".
        # What is the sum of those counts?
        total += len(group_answers)
    if part == 2:
        # print(all_answers)
        return total_2
    return total


YEAR = 2020
DAY = 6
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
