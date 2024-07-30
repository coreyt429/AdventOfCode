"""
Advent Of Code 2015 day 18

"""
# import system modules
import time
from copy import deepcopy


# import my modules
import aoc # pylint: disable=import-error

# contstants for x and y
X=0
Y=0
TARGET=100

def get_neighbors(grid, point):
    """
    Function to get valid neighbors
    """
    max_x = len(grid[0])
    max_y = len(grid)
    neighbors = set()
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for offset in offsets:
        neighbor = (point[X] + offset[X], point[Y] + offset[Y])
        if 0 <= neighbor[X] < max_x and 0 <= neighbor[Y] < max_y:
            neighbors.add(neighbor)
    return neighbors

def get_neighbor_coordinates(row, col):
    """
    Function to return possible neighbors
    """
    neighbors = (
        (row-1, col-1), (row-1, col), (row-1, col+1),
        (row, col-1), (row, col+1),
        (row+1, col-1), (row+1, col), (row+1, col+1),
    )
    return neighbors

def next_lights(lights, stuck_on=()):
    """
    Function to determine next light states
    """
    retval = deepcopy(lights)
    for row, light_row in enumerate(lights):
        for col, _ in enumerate(light_row):
            #print(row,col)
            on_counter = 0
            #neighbors = get_neighbors(lights, (row, col))
            for neighbor in get_neighbor_coordinates(row, col):
                # neighbor is not off the top or bottom
                if 0 <= neighbor[0] < len(lights) and 0 <= neighbor[1] < len(lights[row]):
                    if lights[neighbor[0]][neighbor[1]] == '#':
                        on_counter += 1
            #print(on_counter)
            if lights[row][col] == '#': # currently on
                # A light which is on stays on when 2 or 3 neighbors are on, or turns off
                if not on_counter in [2,3]:
                    retval[row][col] = '.'
            else: # currently off
                # A light which is off turns on if exactly 3 neighbors are on, or stays off
                if on_counter == 3:
                    retval[row][col] = '#'
    if stuck_on:
        for point in stuck_on:
            retval[point[0]][point[1]] = '#'
    return retval

def on_count(lights):
    """
    Function to count lights that are on
    """
    count = 0
    for row in lights:
        for char in row:
            if char == '#':
                count += 1
    return count

def solve(grid, part):
    """
    Function to solve puzzle
    """
    last_lights = grid
    # part 1, stuck_on is empty
    stuck_on = ()
    if part == 2:
        # corners are stuck_on
        stuck_on =tuple(
                [
                    (0, 0),
                    (0, len(last_lights[0]) - 1),
                    (len(last_lights) - 1, 0),
                    (len(last_lights) - 1, len(last_lights[0]) - 1)
                ]
            )
        for point in stuck_on:
            last_lights[point[0]][point[1]] = '#'
    for _ in range(TARGET):
        new_lights=next_lights(last_lights, stuck_on)
        last_lights = new_lights
    return on_count(last_lights)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015,18)
    #input_text = my_aoc.load_text()
    #print(input_text)
    input_grid = my_aoc.load_grid()
    #print(input_grid)
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
        answer[my_part] = funcs[my_part](input_grid, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
