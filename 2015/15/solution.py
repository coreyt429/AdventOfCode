"""
Advent Of Code 2015 day 15

FIXME:  this one needs review

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


# Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
def parse_input(input_text):
    """
    Funciton to parse input
    """

    ingredients = {}
    # walk lines
    for line in input_text.strip().splitlines():
        if not line:
            continue
        # get ingredient and properties
        ingredient, properties = line.split(": ")
        # init ingredient
        ingredients[ingredient] = {}
        # walk properties
        for prop in properties.split(", "):
            # split property and value
            prop, value = prop.split(" ")
            # store property and value
            ingredients[ingredient][prop] = int(value)
    return ingredients


# global sets for scores
scores = set()
scores2 = set()


def score_recipe(properties, ingredients, qty):
    """
    Funciton to score recipe
    """
    # init retva, props and values
    retval = 1
    props = set()
    values = {}
    # add properties from ingredients from poperties to props
    for ingredient in properties.values():
        for prop in ingredient:
            props.add(prop)
    # calculate values for properties
    for prop in props:
        # skip calories
        if prop == "calories":
            continue
        # init to 0
        values[prop] = 0
        # walk ingredients
        for i, ingredient in enumerate(ingredients):
            # value of property = sum of ingredient property value and quantity
            values[prop] += properties[ingredient][prop] * qty[i]
    # set 0 as floor for values, removing any negative values, and multiply retval by value
    for val in values.values():
        val = max(val, 0)
        retval *= val
    # init calories
    calories = 0
    # calculate calories for recipe
    for i, ingredient in enumerate(ingredients):
        calories += properties[ingredient]["calories"] * qty[i]
    # if calories == 500, save in scores2 for part2
    if calories == 500:
        scores2.add(retval)
    # return part 1 score
    return retval


def find_recipe(properties, ingredients=(), qty=()):
    """
    Function to find recipe
    """
    # initialize ingredients
    if not ingredients:
        ingredients = tuple(ingredient for ingredient in properties)
    # initialize q
    quantity = sum(qty)

    # if quantities is less than ingredients
    if len(qty) < len(ingredients):
        # for 100 - q down to 1
        for i in range(100 - quantity, 0, -1):
            find_recipe(properties, ingredients, tuple(list(qty) + [i]))
    elif quantity < 100 or quantity > 100:
        # not a complete recipe
        return -1
    else:
        # calculate score for recipe
        score = score_recipe(properties, ingredients, qty)
        # add to scores for part1
        scores.add(score)
        return score
    return 0


def solve(parsed_data, part):
    """
    Function to solve puzzle
    """
    scores.clear()
    scores2.clear()
    find_recipe(parsed_data)
    if part == 1:
        return max(scores)
    return max(scores2)


YEAR = 2015
DAY = 15
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
