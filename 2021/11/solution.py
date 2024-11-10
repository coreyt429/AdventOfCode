"""
Advent Of Code 2021 day 11

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error
from grid import Grid # pylint: disable=import-error

def convert_to_ints(grid):
    """convert char to int"""
    for point in grid:
        grid.set_point(point, int(grid.get_point(point)))

def run_step(grid):
    """calculate octopus energy for a step"""
    flashed = set()
    can_flash = []
    # First, the energy level of each octopus increases by 1
    for point in grid:
        grid.set_point(point, grid.get_point(point) + 1)

    for point in grid:
        if grid.get_point(point) > 9:
            can_flash.append(point)

    # This process continues as long as new octopuses keep having their energy level
    # increased beyond 9.
    while can_flash:
        point = can_flash.pop(0)
        # (An octopus can only flash at most once per step.)
        if point in flashed:
            continue
        # Then, any octopus with an energy level greater than 9 flashes.
        # This increases the energy level of all adjacent octopuses by 1,
        # including octopuses that are diagonally adjacent.
        # If this causes an octopus to have an energy level greater than 9, it also flashes.
        # This process continues as long as new octopuses keep having their energy level
        # increased beyond 9.
        neighbors = grid.get_neighbors(point=point)
        # print(f"flashing: {point}, neighbors: {neighbors}")
        for neighbor in neighbors.values():
            grid.set_point(neighbor, grid.get_point(neighbor) + 1)
            # If this causes an octopus to have an energy level greater than 9, it also flashes.
            if grid.get_point(neighbor) > 9:
                can_flash.append(neighbor)
        flashed.add(point)
    # Finally, any octopus that flashed during this step has its energy level set to 0,
    #  as it used all of its energy to flash.
    for point in flashed:
        grid.set_point(point, 0)

    return len(flashed)

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid(input_value, use_overrides=False)
    convert_to_ints(grid)
    # print(f"Before any steps:\n{grid}\n")
    total = 0
    step = 0
    while True:
        step += 1
        flashes = run_step(grid)
        if flashes == 100 and part == 2:
            # What is the first step during which all octopuses flash?
            return step
        total += flashes
        if step == 100 and part == 1:
            # How many total flashes are there after 100 steps?
            return total

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021,11)
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
        1: 1632,
        2: 303
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
