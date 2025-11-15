"""
Advent Of Code 2022 day 18

Part 1 was pretty easy.  Part 2, I got the answer no problem, but couldn't
get my shortest path solution to run any faster than 180 seconds.

Looking around, it looks like everyone else realized it was faster
to fill the outside space and cound the cube faces it comes into contact with.

That worked and only took 2.9 seconds.

I'm leaving the framework of my shortest path solution as well, for educational
purposes. (mine mainly)
"""

# import system modules
import time
from functools import lru_cache
from heapq import heappop, heappush

# import my modules
import aoc  # pylint: disable=import-error


@lru_cache(maxsize=None)
def min_max_vals(cubes):
    """Function to get the min and max values for a set of cubes"""
    min_vals = [float("infinity"), float("infinity"), float("infinity")]
    max_vals = [0, 0, 0]
    for cube in cubes:
        for dim, val in enumerate(cube):
            min_vals[dim] = min(min_vals[dim], val)
            max_vals[dim] = max(max_vals[dim], val)
    return tuple(min_vals), tuple(max_vals)


@lru_cache()
def is_oob(cube, min_vals, max_vals):
    """Function to check if a cube position is out of bounds"""
    for dim, val in enumerate(cube):
        if val < min_vals[dim] - 1:
            return True
        if val > max_vals[dim] + 1:
            return True
    return False


def shortest_path(start, cubes, goal=(0, 0, 0)):
    """shortest path back to origin"""
    # print(f"shortest_path({start}, {cubes}, {goal})")
    heap = []
    heappush(heap, (0, start, ()))
    min_vals, max_vals = min_max_vals(cubes)
    seen = set()
    outside.add(goal)
    # counter = 0
    while heap:
        # counter += 1
        steps, position, history = heappop(heap)

        if position in seen:
            continue
        seen.add(position)

        if is_oob(position, min_vals, max_vals) or position in outside:
            outside.update(set(list(history) + [position]))
            return steps
        for neighbor in get_neighbors(position):
            # print(f"neighbor: {neighbor}")
            if neighbor in outside or is_oob(neighbor, min_vals, max_vals):
                outside.update(set(list(history) + [position, neighbor]))
                return steps
            # add empty space
            if neighbor not in cubes and neighbor not in seen:
                # print(f"queueing: {neighbor}")
                new_history = tuple(list(history) + [neighbor])
                heappush(heap, (steps + 1, neighbor, new_history))
    # print(f"returning None")
    return None


def fill_outside(cubes):
    """funciton to pre populate outside"""
    heap = [(0, 0, 0)]
    min_vals, max_vals = min_max_vals(cubes)
    seen = set()
    counter = 0
    while heap:
        position = heap.pop(0)
        if position in seen:
            continue
        seen.add(position)
        if position in cubes:
            continue
        if is_oob(position, min_vals, max_vals):
            continue
        outside.add(position)
        for neighbor in get_neighbors(position):
            if neighbor in cubes:
                counter += 1
            if neighbor not in heap and neighbor not in seen:
                heap.append(neighbor)
    return counter


def parse_input(lines):
    """Function to parse input data"""
    points = []
    for line in lines:
        vals = [int(val) for val in line.split(",")]
        points.append(tuple(vals))
    return tuple(points)


@lru_cache(maxsize=None)
def get_neighbors(cube):
    """Function to calculate neighbors"""
    x_val, y_val, z_val = cube
    offsets = [
        (1, 0, 0),
        (-1, 0, 0),  # Neighbors along the x-axis
        (0, 1, 0),
        (0, -1, 0),  # Neighbors along the y-axis
        (0, 0, 1),
        (0, 0, -1),  # Neighbors along the z-axis
    ]
    # Using a list comprehension for better performance
    return [(x_val + dx, y_val + dy, z_val + dz) for dx, dy, dz in offsets]


outside = set()


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    cubes = parse_input(input_value)
    sides = 0
    empty = set()
    for cube in cubes:
        sides += 6
        for neighbor in get_neighbors(cube):
            if neighbor in cubes:
                sides -= 1
            else:
                empty.add(neighbor)
    if part == 2:
        return fill_outside(cubes)
        # for cube in empty:
        #     count = 0
        #     for neighbor in get_neighbors(cube):
        #         if neighbor in cubes:
        #             count += 1
        #     path = shortest_path(cube, cubes)
        #     if path is None:
        #         sides -= count
    return sides


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2022, 18)
    input_data = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 4548, 2: 2588}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
