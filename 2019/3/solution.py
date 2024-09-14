"""
Advent Of Code 2019 day 3

At first I thought this was going to be a fun grid puzzle.
The grid module did make building the wires easy, and gave me visual
validation of the first test wires.

building the wires was the most expensive operation in the puzzle,
so I changed to passing the strings instead of list, so I could use
lru_cache to minimize wait time.  

"""
# import system modules
import time
import functools

# import my modules
import aoc # pylint: disable=import-error
from grid import Grid, manhattan_distance # pylint: disable=import-error

@functools.lru_cache
def build_wires(wire_description_1, wire_description_2):
    """
    Function to build wires from input data

    Args:
        wire_description_1: str()
        wire_description_2: str()
    
    Returns:
        wires: list() of tuple(x, y)
    """
    # init grid
    grid = Grid([], type="infinite", coordinate_system="cartesian")
    # init wires
    wires = []
    # for each wire description
    for wire_text in [wire_description_1, wire_description_2]:
        # reduce to lower_case
        lower_case = wire_text.lower()
        # init wire
        wire = []
        # set grid to origin
        grid.pos = (0, 0)
        # walk instructions
        for instruction in lower_case.split(','):
            # get direction from instruction
            direction = instruction[0]
            # get steps from instruction
            steps = int(instruction[1:])
            # for each setp
            for _ in range(steps):
                # move grid pointer in direction
                grid.move(direction)
                # store grid pointer position
                wire.append(grid.pos)
        # add finished wire to list
        wires.append(wire)
    # return wire list
    return wires

def find_intersections(wires):
    """
    Function to find intersecting points in two wires

    Args:
        wires: list() of list() of tuple(x, y)
    
    Returns:
        unnamed: set() of tuple(x, y)
    """
    # get unique points of first wire
    points_a = set(wires[0])
    # get unique points of second wire
    points_b = set(wires[1])
    # return intersction of the two sets
    return points_a.intersection(points_b)

def closest_intersection(wires):
    """
    Function to find closes intersection to origin
    
    Args:
        wires: list() of list() of tuple(x, y)
    
    Returns:
        unnamed: int()
    """
    # init origin
    origin = (0, 0)
    # get intersetion points
    intersections = find_intersections(wires)
    # get distances of points from origin
    distances = [manhattan_distance(origin, point) for point in intersections]
    # return shortest distance
    return min(distances)

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        # find closest_intersection
        return closest_intersection(build_wires(*input_value))
    # build wires
    wires = build_wires(*input_value)
    # find intersections
    intersections = find_intersections(wires)
    # init map
    inx_map = {}
    # walk intersections
    for point in intersections:
        # init inx_map for intersection
        inx_map[point] = []
        # walk wires
        for wire in wires:
            # append index of firt occurence + 1
            inx_map[point].append(wire.index(point) + 1)
    # init min_steps
    min_steps = float('infinity')
    # walk map values
    for steps in inx_map.values():
        # update min_steps
        min_steps = min(sum(steps), min_steps)
    # return smallest value
    return min_steps

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019,3)
    #input_text = my_aoc.load_text()
    #print(input_text)
    input_lines = my_aoc.load_lines()
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
