"""
Advent Of Code 2024 day 18

Part 1 was a simple pathfinding problem. I used the Grid class to solve it.
I created a grid of 71x71 and marked the corrupted points with a wall.
Then I used the shortest_paths method from the grid class to find the shortest
path from the start to the end.
The answer was the length of the shortest path minus 1.

Part 2 was going to take a while to solve, so I decided to use a binary search.
I started with the whole list of corrupted points and checked if the path was
blocked. If it was, I moved the unsafe point closer to the safe point.
If the path was not blocked, I moved the safe point to the unsafe point.
I kept doing this until the difference between the safe and unsafe points was 1.
Then I returned the point that was the unsafe point.

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error


def parse_input(lines):
    """Function to parse input"""
    return [tuple(map(int, line.split(","))) for line in lines]


def corrupt_range(grid, corrupted, start, end):
    """Function to corrupt a range of points"""
    for point in corrupted[start:end]:
        grid.set_point(point, "#")


def clear_range(grid, corrupted, start, end):
    """Function to corrupt a range of points"""
    for point in corrupted[start:end]:
        grid.set_point(point, ".")


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid_array = [["."] * 71 for _ in range(71)]
    grid = Grid(grid_array, use_overrides=False)
    corrupted = parse_input(input_value)
    corrupt_range(grid, corrupted, 0, 1024)
    start = (0, 0)
    goal = (70, 70)
    shortest_path = grid.shortest_paths(start, goal)
    if part == 1:
        return len(shortest_path[0]) - 1
    safe = 1024
    unsafe = len(corrupted) + 1
    while unsafe - safe > 1:
        clear_range(grid, corrupted, safe, len(corrupted) + 1)
        corrupt_range(grid, corrupted, safe, unsafe)
        shortest_path = grid.shortest_paths(start, goal)
        if len(shortest_path) < 1:
            # path is blocked, so move closer to safe
            unsafe = safe + (unsafe - safe) // 2
            continue
        # path is not blocked, so move safe
        safe = unsafe
        # and push unsafe closer to the end
        unsafe += (len(corrupted) + 1 - unsafe) // 2
    return ",".join(map(str, corrupted[unsafe]))


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2024, 18)
    input_data = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 360, 2: "58,62"}
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
