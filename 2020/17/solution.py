"""
Advent Of Code 2020 day 17

For part 1, I opted to not try to make Grid() do 3 dimensional, though
logically it would though somethings might be wonky.  I just went with
a similiar dict(tuple) approach, which worked well for part 1.

Part 2, I thought the hypercube was going to complicate things.  I started
with just adding the optional 2 dimension first to the functions that
broke down the point (get_neighbors and load_state).  I ran just to see
what it would do, expecting it to either take a long time or ge tthe wrong
answer.  It ran in 4 seconds, and the answer was correct.

To make it more flexible, I played with swapping out get_neighbors with
get_neighbors_itertools. It is nice that it works with arbitrary
dimensions, and it also takes twice as long to run part 2. So leaving
it here for educational value, but not using it.  I did add lru_cache
on both to bring the times down.

get_neighbors_itertools no cache: 9 seconds
get_neighbors_itertools lru_cache: 4 seconds
get_neighbors no cache: 4 seconds
get_neighbors lru_cache: 2 seconds

"""

# import system modules
import time
from itertools import product
from functools import lru_cache

# import my modules
import aoc  # pylint: disable=import-error


@lru_cache(maxsize=None)
def get_offsets(size):
    """
    Function to get the neighbor offsets for a point dimension size
    """
    return tuple(product([-1, 0, 1], repeat=size))


@lru_cache(maxsize=None)
def get_neighbors_itertools(point):
    """
    Function to calculate neighbors of a point of arbitrary dimension
    """
    neighbors = []
    for offset in get_offsets(len(point)):
        # Add each offset to the original t:
        neighbor = tuple((value + offset[idx] for idx, value in enumerate(point)))
        # for idx, value in enumerate(point):
        #     neighbor.append(value + offset[idx])
        if neighbor != point:
            neighbors.append(neighbor)
    return neighbors


@lru_cache(maxsize=None)
def get_neighbors(point, part=1):
    """
    Function to get the neighbors of a point in 3d or 4d space
    """
    neighbors = []
    for x_val in range(point[0] - 1, point[0] + 2):
        for y_val in range(point[1] - 1, point[1] + 2):
            for z_val in range(point[2] - 1, point[2] + 2):
                if part == 1:
                    neighbor = (x_val, y_val, z_val)
                    if neighbor != point:
                        neighbors.append(neighbor)
                    continue
                for w_val in range(point[3] - 1, point[3] + 2):
                    neighbor = (x_val, y_val, z_val, w_val)
                    if neighbor != point:
                        neighbors.append(neighbor)
    return neighbors


def load_state(lines, part=1):
    """
    Function to load 3d/4d state from 2d text input
    """
    state = {}
    z_val = 0
    w_val = 0
    for y_val, line in enumerate(lines):
        for x_val, char in enumerate(line):
            if part == 1:
                state[(x_val, y_val, z_val)] = char
            else:
                state[(x_val, y_val, z_val, w_val)] = char
    return state


def next_state(current_state, part=1):
    """
    Function to calculate next state
    """
    new_state = {}
    for point, value in current_state.items():
        new_state[point] = str(value)
        for neighbor in get_neighbors(point, part):
            # for neighbor in get_neighbors_itertools(point):
            if neighbor not in new_state:
                new_state[neighbor] = "."
    for point in new_state:
        active_count = 0
        # print(f"Checking point {point}")
        for neighbor in get_neighbors(point, part):
            # for neighbor in get_neighbors_itertools(point):
            # print(f"neighbor {neighbor}: {current_state.get(neighbor, '.')}")
            if current_state.get(neighbor, ".") == "#":
                active_count += 1
        # print(f"{point}, {current_state.get(point, '.')} active_count: {active_count}")
        # If a cube is active and exactly 2 or 3 of its neighbors are also active,
        # the cube remains active. Otherwise, the cube becomes inactive.
        if current_state.get(point, ".") == "#" and active_count not in [2, 3]:
            # print(f"flipping {point} inactive")
            new_state[point] = "."
        # If a cube is inactive but exactly 3 of its neighbors are active, the cube
        # becomes active. Otherwise, the cube remains inactive.
        if current_state.get(point, ".") == "." and active_count == 3:
            # print(f"flipping {point} active")
            new_state[point] = "#"
    return new_state


def count_active(state):
    """
    Function to count active cubes
    """
    active_count = 0
    total = 0
    for value in state.values():
        total += 1
        if value == "#":
            active_count += 1
    # print(f"{active_count}/{total} are active")
    return active_count


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    state = load_state(input_value, part)
    for _ in range(6):
        state = next_state(state, part)
    return count_active(state)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020, 17)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 209, 2: 1492}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
