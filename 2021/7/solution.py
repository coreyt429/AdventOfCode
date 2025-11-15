"""
Advent Of Code 2021 day 7

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


def calc_fuel(target, positions, mode=1):
    """Function to calculate total fuel to get to a position"""
    fuel = 0
    for position in positions:
        if mode == 1:
            # Each change of 1 step in horizontal position of
            # a single crab costs 1 fuel.
            fuel += abs(position - target)
        elif mode == 2:
            # As it turns out, crab submarine engines don't burn
            # fuel at a constant rate. Instead, each change of 1
            # step in horizontal position costs 1 more unit of fuel
            # than the last: the first step costs 1, the second step
            # costs 2, the third step costs 3, and so on.
            #
            # Triangular Numbers: The n-th triangular number is the
            # sum of the integers from 1 to n
            # so the Tn = n(n+1)/2
            steps = abs(position - target)
            fuel += steps * (steps + 1) // 2
    return fuel


def find_min_fuel(positions, mode=1):
    """Function to find minimum fuel burn to get all subs to teh same position"""
    min_fuel = float("infinity")
    for position in range(min(positions), max(positions) + 1):
        fuel = calc_fuel(position, positions, mode)
        min_fuel = min(min_fuel, fuel)
    return min_fuel


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    data = [int(num) for num in input_value.split(",")]
    return find_min_fuel(data, part)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021, 7)
    input_data = my_aoc.load_text()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 352254, 2: 99053143}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
