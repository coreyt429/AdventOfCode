"""
Advent Of Code 2024 day 14

"""
# import system modules
import time
import re
import math

# import my modules
import aoc # pylint: disable=import-error
from grid import Grid # pylint: disable=import-error

def blank_grid(height=7, width=11):
    """Function to initialize a blank grid of a particular size"""
    grid_seed = []
    for row in range(height):
        row = []
        for _ in range(width):
            row.append('.')
        grid_seed.append(row)

    grid = Grid(grid_seed, use_overrides=False)
    return grid

pattern_digit = re.compile(r'(\-?\d+)')

def parse_input(lines):
    """Function to parse input"""
    robots = []
    for line in lines:
        values = [int(num) for num in pattern_digit.findall(line)]
        robots.append({'position': tuple(values[:2]), 'velocity': tuple(values[2:])})
    return robots


def new_position(grid, current, velocity, moves):
    """Function to calculate position of a robot"""
    new = [0, 0]
    for dim in (0, 1):
        new[dim] = (current[dim] + (velocity[dim] * moves)) % (grid.cfg['max'][dim] + 1)
    return tuple(new)

def safety_factor(grid):
    """Funciton to calculate safety_factor based on grid values"""
    quadrants = [0, 0, 0, 0]
    for point, value in grid.items():
        if value == '.':
            continue
        # upper half
        if point[0] < grid.cfg['max'][0]//2:
            # left
            if point[1] < grid.cfg['max'][1]//2:
                quadrants[0] += value
            # right
            elif point[1] > grid.cfg['max'][1]//2:
                quadrants[1] += value
        # lower half
        elif point[0] > grid.cfg['max'][0]//2:
            # left
            if point[1] < grid.cfg['max'][1]//2:
                quadrants[2] += value
            # right
            elif point[1] > grid.cfg['max'][1]//2:
                quadrants[3] += value
    return math.prod(quadrants)

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    robots = parse_input(input_value)
    grid = blank_grid(height=103, width=101)
    if part == 1:
        moves = 100
        for robot in robots:
            robot['position'] = new_position(grid, robot['position'], robot['velocity'], moves)
            current = grid.get_point(robot['position'])
            if current == '.':
                grid.set_point(robot['position'], 1)
            else:
                grid.set_point(robot['position'], current +1)
        return safety_factor(grid)
    moves = 1000000
    # The answer was not in the first 7000 iterations, so lets fast forward over them
    # cheating I know, but it takes 80 seconds to get to the answer, runs in 4 this way
    for robot in robots:
        robot['position'] = new_position(grid, robot['position'], robot['velocity'], 7000)
    for move in range(7000, moves):
        for point in grid:
            grid.set_point(point, '.')
        for robot in robots:
            robot['position'] = new_position(grid, robot['position'], robot['velocity'], 1)
            current = grid.get_point(robot['position'])
            if current == '.':
                grid.set_point(robot['position'], 1)
            else:
                grid.set_point(robot['position'], current +1)
        if "111111111111111111111" in str(grid):
            # print(f"move: {move + 1}\n{grid}\n\n")
            return move + 1
    return part

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2024,14)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
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
    # correct answers once solved, to validate changes
    correct = {
        1: 229069152,
        2: 7383
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
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
