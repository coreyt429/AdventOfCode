import sys
import re
from itertools import combinations

def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')
    return [int(x) for x in lines]

combos = []

def part1(parsed_data,target):
    retval = 0;
    result = []
    global combos
    for idx in range(1, len(parsed_data) + 1):
        for combo in combinations(parsed_data, idx):
            if sum(combo) == target:
                combos.append(combo)
                result.append(combo)
    return len(result)

def part2(parsed_data,target):
    global combos
    minimum=None
    min_combos = []
    for combo in combos:
        if minimum is None or len(combo) < minimum:
            minimum = len(combo)
    for combo in combos:
        if len(combo) == minimum:
            min_combos.append(combo)
    return len(min_combos)

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())
    #print(parsed_data)
    target= int(sys.argv[2])
    #print("Part 1")
    answer1 = part1(parsed_data,target)
    
    #print("Part 2")
    answer2 = part2(parsed_data,target)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    