"""
Advent Of Code 2019 day 1

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


def required_fuel(mass):
    """part 1 fuel calculation"""
    return mass // 3 - 2


def required_fuel_2(mass):
    """part 2 recursive fuel calculation"""
    fuel = mass // 3 - 2
    if fuel < 0:
        return 0
    return fuel + required_fuel_2(fuel)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    fuel = sum((required_fuel(mass) for mass in input_value))
    if part == 1:
        return fuel
    # fuel = required_fuel(100756)
    fuel = sum((required_fuel_2(mass) for mass in input_value))
    return fuel


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019, 1)
    # input_text = my_aoc.load_text()
    # print(input_text)
    input_lines = my_aoc.load_integers()
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
