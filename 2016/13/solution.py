"""
Advent Of Code 2016 day 13

"""
import time
from heapq import heappop, heappush
import aoc # pylint: disable=import-error

def is_wall(point,seed):
    """
    Function to determine if a point is a wall or open space
    Find x*x + 3*x + 2*x*y + y + y*y.
    Add the office designer's favorite number (seed).
    Find the binary representation of that sum; count the number of bits that are 1.
    If the number of bits that are 1 is even, it's an open space.
    If the number of bits that are 1 is odd, it's a wall.
    """
    point_x,point_y = point
    int_value = point_x**2 + 3*point_x + 2*point_x*point_y + point_y + point_y**2
    int_value +=seed
    one_count = bin(int_value)[2:].count('1')
    return one_count % 2 == 1

def neighbors(point,seed):
    """
    Funcition to return valid neighbors for a point
    """
    set_neighbors = set()
    for p_x in [point[0]+1,point[0]-1]:
        if p_x >= 0:
            if not is_wall((p_x,point[1]),seed):
                set_neighbors.add((p_x,point[1]))

        for p_y in [point[1]+1,point[1]-1]:
            if p_y >= 0:
                if not is_wall((point[0],p_y),seed):
                    set_neighbors.add((point[0],p_y))
    return set_neighbors

def solve(seed, part):
    """
    Function to solve puzzle
    For part == 1, we are doing a bfs to find the minimum steps to get to (31, 39)
    For part == 2, we run our bfs, but we are only interested in the count of
    locations we can reach in 50 steps or less.
    """
    start = (1, 1)
    target = (31, 39)
    visited = set()
    heap = []
    heappush(heap,(0,start,()))
    min_steps = float('infinity')
    while heap:
        steps, point, path = heappop(heap)
        # How many locations (distinct x,y coordinates, including your starting location)
        # can you reach in at most 50 steps?
        if part == 2 and steps > 50:
            continue
        visited.add(point)
        if point == target:
            if steps < min_steps:
                min_steps = steps
        else:
            new_path = tuple(list(path) + [point])
            for neighbor in neighbors(point, seed):
                if neighbor not in visited:
                    heappush(heap,(steps+1, neighbor, new_path))
    if part == 1:
        return min_steps
    # part 2
    return len(visited)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2016,13)
    input_text = my_aoc.load_text()
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
        answer[my_part] = funcs[my_part](int(input_text), my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
