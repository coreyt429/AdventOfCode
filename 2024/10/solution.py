"""
Advent Of Code 2024 day 10

In my failure to read instructions, I essentially solved part 2 before part 1.
After a bit of debugging on the example data, a reread of the instructions
pointed out the problem.  This made part 2, a little bit easy.

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error


def convert_to_int(grid):
    """Function to convert grid values to integers."""
    for point, value in grid.items():
        if isinstance(value, str) and value.isdigit():
            grid.set_point(point, int(value))


def find_trailheads(grid):
    """Function to identifiy trailheads on a map."""
    for point, value in grid.items():
        if value == 0:
            yield point


def count_trails(grid, point, history=()):
    """Function to count trails recursively."""
    paths = set()
    current = grid.get_point(point)
    history += (point,)
    if current == 9:
        return {history}

    neighbors = grid.get_neighbors(point=point, directions=["n", "s", "e", "w"])
    for neighbor in neighbors.values():
        value = grid.get_point(neighbor)
        if value == current + 1:
            paths.update(count_trails(grid, neighbor, history))

    return paths


def solve(input_value, part):
    """
    Function to solve puzzle.
    """
    grid = Grid(input_value, use_overrides=False)
    convert_to_int(grid)
    score = 0
    for point in find_trailheads(grid):
        paths = count_trails(grid, point)
        if part == 1:
            # Assembling more fragments of pages, you establish that a trailhead's
            # score is the number of 9-height positions reachable from that trailhead
            #  via a hiking trail.
            end_points = set()
            for path in paths:
                end_points.add(path[-1])
            score += len(end_points)
        elif part == 2:
            # A trailhead's rating is the number of distinct hiking trails which begin at
            # that trailhead.
            score += len(paths)
    # What is the sum of the scores of all trailheads on your topographic map?
    return score


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2024, 10)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 811, 2: 1794}
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
