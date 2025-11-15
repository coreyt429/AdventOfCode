"""
Advent Of Code 2020 day 21

Easy peasy.  I needed that after the last couple of days.

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


def parse_data(lines):
    """Function to parse input data"""
    food_data = []
    for line in lines:
        ingredient_str, allergen_str = line.split(" (contains ")
        allergen_str = allergen_str.replace(")", "")
        ingredients = ingredient_str.split(" ")
        allergens = allergen_str.split(", ")
        # print(f"{ingredients} <> {allergens}")
        food_data.append((tuple(ingredients), tuple(allergens)))
    return tuple(food_data)


def identify_ingredients_and_allergens(data):
    """Function to extract ingredient and allergen sets"""
    allergen_set = set()
    ingredient_set = set()
    for ingredients, allergens in data:
        for allergen in allergens:
            for ingredient in ingredients:
                allergen_set.add(allergen)
                ingredient_set.add(ingredient)
    return allergen_set, ingredient_set


def identify_allergen_ingredients(data, allergen_set, ingredient_set):
    """Function to identify allergen ingredients"""
    data_map = {}
    for allergen in allergen_set:
        data_map[allergen] = set(ingredient_set)

    for ingredients, allergens in data:
        for allergen, possible_ingredients in data_map.items():
            if allergen in allergens:
                deletes = set()
                for ingredient in possible_ingredients:
                    if ingredient not in ingredients:
                        deletes.add(ingredient)
                possible_ingredients.difference_update(deletes)

    changed = True
    while changed:
        changed = False
        for allergen, ingredients in data_map.items():
            if len(ingredients) == 1:
                ingredient = list(ingredients)[0]
                for other, other_ingredients in data_map.items():
                    if other != allergen and ingredient in other_ingredients:
                        changed = True
                        other_ingredients.remove(ingredient)

    allergen_ingredients = set()
    for ingredients in data_map.values():
        allergen_ingredients.update(ingredients)
    return allergen_ingredients, data_map


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    data = parse_data(input_value)
    allergen_set, ingredient_set = identify_ingredients_and_allergens(data)
    allergen_ingredients, allergen_ingredient_map = identify_allergen_ingredients(
        data, allergen_set, ingredient_set
    )
    if part == 2:
        # What is your canonical dangerous ingredient list?
        return ",".join(
            [
                str(list(value)[0])
                for key, value in sorted(
                    allergen_ingredient_map.items(), key=lambda item: item[0]
                )
            ]
        )
    non_allergen_ingredients = ingredient_set.difference(allergen_ingredients)
    # How many times do any of those ingredients appear?
    count = 0
    for ingredients, _ in data:
        for ingredient in ingredients:
            if ingredient in non_allergen_ingredients:
                count += 1
    return count


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020, 21)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 2098, 2: "ppdplc,gkcplx,ktlh,msfmt,dqsbql,mvqkdj,ggsz,hbhsx"}
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
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
