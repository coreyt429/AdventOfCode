"""
Advent Of Code 2021 day 9

convert_to_ints highlighted a bug in Grid().set_point().  The logic for detecting
an empty value was using "not value" instead of "value is None".  So when I passed
0 to it, I was getting ' ' instead of 0

Part 1, simply iterate through the points and check to see if any neighbors are
lower, if not, then it is a low point.

Part 2, used the loop from Part 1 to detect low points, 

"""
# import system modules
import time
import math
from heapq import heappop, heappush

# import my modules
import aoc # pylint: disable=import-error
from grid import Grid # pylint: disable=import-error

def is_low_point(point, grid):
    """
    Function to check if a point is a low point
    """
    low_point = True
    for neighbor in grid.get_neighbors(point=point, directions=['n','s','e','w']).values():
        value = grid.get_point(point)
        if value >= grid.get_point(neighbor):
            low_point = False
            break
    return low_point

def convert_to_ints(grid):
    """convert character digits to integers for mathing"""
    for point in grid:
        value = grid.get_point(point)
        grid.set_point(point, int(value))

def calculate_basin_size(point, grid):
    """Function to calculate basin_size for a low_point"""
    heap = []
    basin = set()
    directions = ['n', 's', 'e', 'w']
    heappush(heap, (point, list(grid.get_neighbors(point=point, directions=directions).values())))
    while heap:
        current, neighbors = heappop(heap)
        current_value = grid.get_point(current)
        # Locations of height 9 do not count as being in any basin
        if current_value == 9:
            continue
        basin.add(current)
        for neighbor in neighbors:
            if neighbor in basin:
                continue
            neighbor_value = grid.get_point(neighbor)
            # Locations of height 9 do not count as being in any basin
            if neighbor_value == 9:
                continue
            # this condition works with my input, and may be invalid for other inputs
            # my input works if I leave this condition out and just go ahead and
            # push it to the heap from here.
            # I'm leaving it in, because it is dramatically faster with this condition
            # 0.09 seconds vs 1.21 seconds
            if neighbor_value >= current_value:
                heappush(
                    heap,
                    (
                        neighbor,
                        list(grid.get_neighbors(point=neighbor, directions=directions).values())
                    )
                )
    return len(basin)

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid(input_value)
    convert_to_ints(grid)
    total = 0
    basins = {}
    for point in grid:
        if is_low_point(point, grid):
            risk_level = int(grid.get_point(point)) + 1
            total += risk_level
            if part == 2:
                basins[point] = calculate_basin_size(point, grid)
    if part == 2:
        basin_sizes = list(reversed(sorted(basins.values())))
        return math.prod(basin_sizes[:3])
    # 1280 too high  >= not >  this one tripped on 9 not being less than [9, 9, 9, 9]
    return total

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021,9)
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
        1: 480,
        2: 1045660
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
