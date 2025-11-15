"""
Advent Of Code 2015 day 15

FIXME:  this one needs review

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


# Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
def parse_input(lines):
    """
    Funciton to parse input
    """

    ingredients = {}
    # walk lines
    for line in lines:
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


def solve(lines, part):
    """
    Function to solve puzzle
    """
    # if part 1
    if part == 1:
        # parse input text
        parsed_data = parse_input(lines)
        # recurse find_recipe
        find_recipe(parsed_data)
        # return max scores
        return max(scores)
    # part 2 return max scores2
    return max(scores2)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015, 15)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
