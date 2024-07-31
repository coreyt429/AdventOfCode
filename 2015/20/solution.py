"""
Advent Of Code 2015 day 20

My original solution for this worked, but was a bit ugly

I have reworked part1 to use sympy.divisors



"""
# import system modules
import time
from sympy import divisors

# import my modules
import aoc # pylint: disable=import-error

def part1(target):
    """
    Function to solve part 1
    """
    # optimization guess work
    # starting point 20% of 10% of target
    current_house = target // 10 // 5
    # If guesswork fails, uncomment next line and wait 6 seconds longer
    #current_house = 1
    # loop
    while True:
        # get factors
        factors = divisors(current_house)
        # calculate presents
        presents = sum(factors) * 10
        # have we exceeded the target?
        if presents > target:
            break
        # increment current_house
        # optimization cheat, once we determined that both answers are divisible by 40
        current_house += 40
        #current_house += 1
    return current_house


def part2(target):
    """
    Function to solve part 2
    """
    # optimization guess work
    # lets start with the previous answer, as this shoudl be higher
    current_house = answer[1]
    # If guesswork fails, uncomment next line and wait 6 seconds longer
    #current_house = 1
    # loop
    while True:
        # get factors
        factors = divisors(current_house)
        lazy_factors = set()
        for factor in factors:
            if factor * 50 >= current_house:
                lazy_factors.add(factor)
        # calculate presents
        presents = sum(factor * 11 for factor in lazy_factors)
        # have we exceeded the target?
        if presents > target:
            break
        # increment current_house
        # optimization cheat, once we determined that both answers are divisible by 40
        current_house += 40
        #current_house += 1
    return current_house

def solve(input_data, part):
    """
    Function to solve puzzle
    """
    target = int(input_data)
    if part == 1:
        return part1(target)
    return part2(target)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015,20)
    input_text = my_aoc.load_text()
    # parts dict to loop
    parts = {
        1: 1,
        2: 2
    }
    # dict to store answers
    answer = {
        1: None,
        2: None
    }
    # dict to map functions
    funcs = {
        1: solve,
        2: solve
    }
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
