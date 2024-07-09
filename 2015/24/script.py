"""
AdventOfcode 2015 day 24
"""

from heapq import heappop,heappush
import math
import itertools
import sys

def find_shortest_combinations(big_list,splits):
    """
    find all equal weight three way splits of big_list
    """
    n = len(big_list)
    total = sum(big_list)
    one_third = int(total/splits)
    print(f"Split {total} into {splits} buckets of {one_third}")
    all_combinations = []
    equal_weight_combinations = []
    # Iterate over possible sizes for the first list
    for i in range(1, n - 1):
        print(f"Trying length {i}")
        for j in range(1, n - i):
            # Generate combinations for the first list
            for combo1 in itertools.combinations(big_list, i):
                if sum(combo1) == one_third:
                    equal_weight_combinations.append(combo1)
        if len(equal_weight_combinations) > 0:
            break
    return equal_weight_combinations

def get_presents_from_file(file_name):
    """
    Function to load file into a list
    """
    with open(file_name,'r',encoding='utf-8') as file:
        return [int(line) for line in file.read().rstrip().split('\n')]

if __name__ == "__main__":
    presents = get_presents_from_file(sys.argv[1])
    shortest_combos = find_shortest_combinations(presents,3)
    heap = []
    for list1 in shortest_combos:
        quantum_entanglement=math.prod(list1)
        leg_room=len(list1)
        heappush(heap,(leg_room,quantum_entanglement,list1))
    print(f"Part 1: {heap[0][1]}")

    shortest_combos = find_shortest_combinations(presents,4)
    heap = []
    for list1 in shortest_combos:
        quantum_entanglement=math.prod(list1)
        leg_room=len(list1)
        heappush(heap,(leg_room,quantum_entanglement,list1))
    print(f"Part 2: {heap[0][1]}")