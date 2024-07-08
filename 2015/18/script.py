import sys
import re
from copy import deepcopy
"""
.#.#.#
...##.
#....#
..#...
#.#..#
####..
"""
def get_neighbor_coordinates(row,col):
    neighbors = (
        (row-1, col-1), (row-1, col), (row-1, col+1),
        (row, col-1), (row, col+1),
        (row+1, col-1), (row+1, col), (row+1, col+1),
    )
    return neighbors

def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')
    lights = []
    # loop through lines
    for line in lines:
        lights.append(list(line))
    return lights

def print_lights(lights,label):
    print(f'{label}:')
    for row in lights:
        print(''.join(row))
    print()

def nextLights(lights,stuck_on=()):
    retval = deepcopy(lights)
    for row in range(len(lights)):
        for col in range(len(lights[row])):
            #print(row,col)
            on = 0
            neighbors = get_neighbor_coordinates(row,col)
            #print(neighbors)
            for neighbor in neighbors:
                #print(neighbor)
                if not (neighbor[0] < 0 or neighbor[0] >= len(lights)): # neighbor is not off the top or bottom
                    if not (neighbor[1] < 0 or neighbor[1] >= len(lights[row])): # neighbor is not off the left or right
                        #print(f'{neighbor[0]},{neighbor[1]} = {lights[neighbor[0]]}')
                        if lights[neighbor[0]][neighbor[1]] == '#':
                            on+=1
            #print(on)
            if lights[row][col] == '#': # currently on
                if not on in [2,3]: # A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise
                    retval[row][col] = '.'
            else: # currently off
                if on == 3: # A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
                    retval[row][col] = '#'
    if stuck_on:
        for point in stuck_on:
            retval[point[0]][point[1]] = '#'
    return retval

def on_count(lights):
    count = 0
    for row in lights:
        for char in row:
            if char == '#':
                count += 1
    return count

def part1(parsed_data,target):
    retval = 0;
    #print_lights(parsed_data,'Initial State')
    last_lights = parsed_data
    for n in range(target):
        new_lights=nextLights(last_lights)
        #print_lights(new_lights,f'After {n} step')
        last_lights = new_lights
    #print(last_lights)
    return on_count(last_lights)

def part2(parsed_data,target):
    retval = 0;
    last_lights = parsed_data
    stuck_on =tuple([(0,0),(0,len(last_lights[0])-1),(len(last_lights)-1,0),(len(last_lights)-1,len(last_lights[0])-1)])
    for point in stuck_on:
        last_lights[point[0]][point[1]] = '#'
    #print_lights(last_lights,'Initial State')
    #print(stuck)
    for n in range(target):
        new_lights=nextLights(last_lights,stuck_on)
        #print_lights(new_lights,f'After {n} step')
        last_lights = new_lights
    #print(last_lights)
    return on_count(last_lights)

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())
    #print(parsed_data)
    target = int(sys.argv[2])
    #print("Part 1")
    answer1 = part1(parsed_data,target)
    
    #print("Part 2")
    answer2 = part2(parsed_data,target)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    