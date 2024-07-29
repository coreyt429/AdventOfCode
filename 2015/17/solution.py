"""
Advent Of Code 2015 day 17

"""
# import system modules
import time
from itertools import combinations

# import my modules
import aoc # pylint: disable=import-error

# global list combos, part1 will populate
combos = []
# target is 150 liters

TARGET=150

def solve(containers, part):
    """
    Function to solve puzzle
    """
    # part 1
    if part == 1:
        for idx, _ in enumerate(containers):
            # get combinations of lentgh idx
            for combo in combinations(containers, idx):
                # does this add up to TARGET
                if sum(combo) == TARGET:
                    # save
                    combos.append(combo)
        # return count of combos
        return len(combos)
    # part 2
    # init minimum and min_combos
    minimum = float('infinity')
    min_combos = set()
    # walk combos
    for combo in combos:
        # if current < minimum
        if len(combo) < minimum:
            # set new minimum
            minimum = len(combo)
            min_combos = set([combo])
        elif len(combo) == minimum:
            min_combos.add(combo)
    # return count fo min_combos
    return len(min_combos)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015,17)
    #input_text = my_aoc.load_text()
    #print(input_text)
    #input_lines = my_aoc.load_lines()
    input_data = my_aoc.load_integers()
    #print(input_data)
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
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
