"""
Advent Of Code 2018 day 14

The scratchpad has lots of failures on this one.

I started out trying to find a match in all recipes,
until it dawned on me that I was specifically looking
for the lists starting at the indices I had in elves.

"""

# import system modules
from __future__ import annotations
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def build_recipes(recipes, elves):
    """
    Function to build next recipes

    Args:
        recipes: list(int()) recipe values
        elves: list(int) current recipe for each elf

    Returns:
        recipes: list(int()) recipe values
        elves: list(int) current recipe for each elf
    """
    # add current recipes to together
    total = sum(recipes[elf] for elf in elves)
    # get the digits from the sum as the new recipe(s)
    new_recipes = [int(num) for num in list(str(total))]
    # append new recipes
    recipes += new_recipes
    # move elves to new positions
    for elf_id, position in enumerate(elves):
        position += recipes[position] + 1
        # set elf position in the list
        elves[elf_id] = position % len(recipes)
    # return updates
    return recipes, elves


def print_data(recipes, elves):
    """
    Function to print recipes for debugging

    Args:
        recipes: list(int()) recipe values
        elves: list(int) current recipe for each elf

    Returns:
        None
    """
    # init string
    my_string = ""
    # walk recipes
    for idx, recipe in enumerate(recipes):
        # if this one is not a current elf position,
        # print with spaces
        if idx not in elves:
            my_string += f" {recipe} "
            continue
        # if elf 1, print with ()
        if idx == elves[0]:
            my_string += f"({recipe})"
            continue
        # elf 2, print with []
        my_string += f"[{recipe}]"
    # print the string
    print(my_string)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # init target_strings, recipes and elves, common for both parts
    recipes = [3, 7]
    elves = [0, 1]
    target_strings = input_value
    # part 1
    if part == 1:
        # init target to make pylint happy
        target = 0
        # walk targets
        for target in (int(num) for num in target_strings):
            # loop until we are big enough
            while len(recipes) < target + 10:
                # update recipes and elves to next iteration
                recipes, elves = build_recipes(recipes, elves)
        # return string of ten digits after target
        return int("".join([str(num) for num in recipes[target : target + 10]]))
    # part 2
    # init targets
    targets = {}
    # walk target strings: this makes a lot more sense in testing
    # where I passed more than one target
    for target_string in target_strings:
        # define targets
        targets[target_string] = [int(char) for char in target_string]

    # init found
    found = {}
    # while found is shorter than targets
    while len(found.keys()) < len(targets.keys()):
        # build new recipes
        recipes, elves = build_recipes(recipes, elves)
        # walk targets
        for target_string, target_list in targets.items():
            # if we have already found this target, try the next
            if target_string in found:
                continue
            # walk elves
            for elf in elves:
                # is our target list after this elf?
                if target_list == recipes[elf : elf + len(target_list)]:
                    # yes, add to found
                    found[target_string] = "".join([str(num) for num in recipes])
    # init result
    result = ""
    # walk found items
    for sequence, recipe_string in found.items():
        # update result to last
        result = int(recipe_string.find(sequence))
    # do the thing
    return result


YEAR = 2018
DAY = 14
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
