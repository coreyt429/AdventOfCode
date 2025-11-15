"""
Advent Of Code 2022 day 12

Struggled on this one with a simple miss.  We can only go up one level, but we
can apparently go down more. Which was stated in the rules, I just misunderstood.

I was thinking my input was bad, because I got the right anser by changing 1 character.
Until I ran my input through the solution from u/themanushiya, and found that it worked.
reviewing I saw that solution was just checking for the next step to be less than current + 1.

I made that change in my code, and it worked.

part 2 takes longer than I would like, but I'll likely leave it for now.
Maybe not, I forgot I did the work to make Grid hashable, so lru_cache worked for get_next()

"""

# import system modules
import time
from heapq import heappop, heappush
from functools import lru_cache
from string import ascii_lowercase

# import my modules
import aoc  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error


@lru_cache(maxsize=None)
def calc_values():
    """Function to calculate height values"""
    base = ord("a") - 1
    values = {char: ord(char) - base for char in ascii_lowercase}
    values["S"] = values["a"]
    values["E"] = values["z"]
    return values


@lru_cache(maxsize=None)
def get_next(grid, current):
    """Function to get next points to try"""
    current_height = grid.get_point(current)
    values = calc_values()
    neighbors = grid.get_neighbors(point=current, directions=["n", "s", "e", "w"])
    next_points = []
    for neighbor in neighbors.values():
        if values[grid.get_point(neighbor)] <= values[current_height] + 1:
            next_points.append(neighbor)
    return next_points


@lru_cache(maxsize=None)
def shortest_path(grid, start, goal):
    """Function to calculate shortest path"""
    heap = []
    heappush(heap, (0, start))
    min_path = float("infinity")
    visited = set()
    while heap:
        steps, current = heappop(heap)

        # print(len(heap), steps, current, grid.get_point(current))
        if current == goal:
            # print(f"reached goal in {steps}")
            min_path = min(min_path, steps)
            return min_path
        if current in visited:
            # print("already been here, discarding")
            continue
        visited.add(current)
        for next_point in get_next(grid, current):
            heappush(heap, (steps + 1, next_point))
    return min_path


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid(input_value, use_overrides=False)
    start = None
    goal = None
    low_points = set()
    for point in grid:
        char = grid.get_point(point)
        if char == "S":
            start = point
            low_points.add(point)
        if char == "E":
            goal = point
        if char == "a":
            low_points.add(point)
    if part == 1:
        return shortest_path(grid, start, goal)
    # part 2, iterate over lowest points to find the shortest path
    shortest = float("infinity")
    for point in low_points:
        shortest = min(shortest, shortest_path(grid, point, goal))
    return shortest


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2022, 12)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 520, 2: 508}
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
