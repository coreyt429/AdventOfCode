import sys
import re
import math
from functools import reduce


def parse_input(data):
    retval = {}
    # Split the data into lines
    parts = data.strip().split('\n\n')

    retval['instructions'] = parts[0]

    map = {}
    mapRegEx = r'(...) = \((...), (...)\)'
    for line in parts[1].split('\n'):
        #print(line)
        coordinates = re.findall(mapRegEx,line)
        #print(coordinates)
        map[coordinates[0][0]] = {'L': coordinates[0][1], 'R': coordinates[0][2]}
    retval['map'] = map
    return retval

def part1(parsed_data):
    steps=0;
    position='AAA'
    while not position == 'ZZZ':
        for LR in parsed_data['instructions']:
            steps+=1
            position = parsed_data['map'][position][LR]
            if position == 'ZZZ':
                break
    return steps

def lcm_of_list(numbers):
    return reduce(lambda x, y: math.lcm(x, y), numbers)

def part2(parsed_data):
    positions = [];
    map = parsed_data['map']
    for currpos in map.keys():
        if currpos[2] == 'A':
            positions.append(currpos)
    results = []
    for startposition in positions:
        steps=0
        position = startposition
        while position[2] != 'Z':
            for LR in parsed_data['instructions']:
                steps+=1
                position = parsed_data['map'][position][LR]
                if position[2] == 'Z':
                    break
        results.append(steps)
    return lcm_of_list(results)

def part2_brute_force(parsed_data):
    steps = 0;
    positions = [];
    map = parsed_data['map']
    for currpos in map.keys():
        if currpos[2] == 'A':
            positions.append(currpos)
    proceed = True
    while proceed:
        for LR in parsed_data['instructions']:
            steps+=1
            print(f'Step {steps}')
            proceed = False
            for position in positions:
                position = parsed_data['map'][position][LR]
                print(position[2])
                if position[2] != 'Z':
                    proceed = True
            if not proceed:
                break
    return steps

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())
    #print(parsed_data)

    #print("Part 1")
    answer1 = part1(parsed_data)
    
    #print("Part 2")
    answer2 = part2(parsed_data)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    