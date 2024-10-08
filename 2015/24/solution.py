"""
Advent Of Code 2015 day 24

This was already pretty fast and clean on this one, just needed to refactor into current format.

"""
# import system modules
import time
from heapq import heappop, heappush
import math
from itertools import combinations

# import my modules
import aoc # pylint: disable=import-error

def find_shortest_combinations(big_list, splits):
    """
    find all equal weight three way splits of big_list
    """
    num = len(big_list)
    total = sum(big_list)
    one_third = int(total / splits)
    equal_weight_combinations = []
    # Iterate over possible sizes for the first list
    for i in range(1, num - 1):
        for _ in range(1, num - i):
            # Generate combinations for the first list
            for combo1 in combinations(big_list, i):
                if sum(combo1) == one_third:
                    equal_weight_combinations.append(combo1)
        if len(equal_weight_combinations) > 0:
            break
    return equal_weight_combinations

def solve(presents, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        shortest_combos = find_shortest_combinations(presents, 3)
        heap = []
        for list1 in shortest_combos:
            quantum_entanglement=math.prod(list1)
            leg_room=len(list1)
            heappush(heap,(leg_room, quantum_entanglement, list1))
        return heappop(heap)[1]
    # part 2
    shortest_combos = find_shortest_combinations(presents, 4)
    heap = []
    for list1 in shortest_combos:
        quantum_entanglement = math.prod(list1)
        leg_room = len(list1)
        heappush(heap, (leg_room, quantum_entanglement, list1))
    return heappop(heap)[1]

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015,24)
    input_lines = my_aoc.load_integers()
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
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
