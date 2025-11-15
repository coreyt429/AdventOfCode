"""
Advent Of Code 2022 day 14

The work on Grid() paid off here.  I did tweak get_point and in_bounds a bit
to shave 0.5 seconds off of part 2.  Trying functools with clear_cache in update() to speed it up.

That trimmed another 1 second.

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error


def expand_line(start, end):
    """Function to get the points in a line"""
    min_x = min(start[0], end[0])
    max_x = max(start[0], end[0])
    min_y = min(start[1], end[1])
    max_y = max(start[1], end[1])
    points = set()
    for x_val in range(min_x, max_x + 1):
        for y_val in range(min_y, max_y + 1):
            points.add(tuple((x_val, y_val)))
    return points


def expand_points(point_strings):
    """Function to expand a point string"""
    end_points = []
    points = set()
    for point_string in point_strings:
        vals = [int(num) for num in point_string.split(",")]
        end_points.append(tuple(vals))
    for idx in range(len(end_points) - 1):
        points.update(expand_line(end_points[idx], end_points[idx + 1]))
    return points


def parse_input(lines):
    """Function to parse input data into grid"""
    grid = Grid(
        {(500, 0): "+"}, use_overrides=False, type="infinite", ob_default_value="."
    )
    for line in lines:
        points = line.split(" -> ")
        for point in expand_points(points):
            grid.set_point(point, "#")
    grid.update()
    return grid


def drop_sand(grid, floor, part=1):
    """Function to simulate dropping sand"""
    settled = False
    sand = (500, 0)
    sentinel = 0
    while not settled:
        sentinel += 1
        if sentinel > 1000:
            print("breaking loop")
            break
        if part == 2 and sand[1] == floor - 1:
            settled = True
            break
        # did we fall off the bottom?
        if sand[1] > floor:
            return False
        neighbors = grid.get_neighbors(point=sand, directions=["s", "sw", "se"])
        values = [grid.get_point(neighbor, ".") for neighbor in neighbors.values()]
        # settled position
        if "." not in values:
            # print(f"settling at {sand}, neighbors: {values}")
            grid.set_point(sand, "o")
            return True

        for next_point in [neighbors["s"], neighbors["sw"], neighbors["se"]]:
            value = grid.get_point(next_point, ".")
            # still falling?
            if value == ".":
                sand = next_point
                break  # for loop
    if settled:
        grid.set_point(sand, "o")
    return settled


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = parse_input(input_value)
    max_y = grid.cfg["max"][1]
    counter = 0
    if part == 1:
        while drop_sand(grid, max_y, part):
            counter += 1
            if counter > 100000:
                print("breaking loop 2")
                break
            continue
        return str(grid).count("o")
    while grid.get_point((500, 0)) != "o":
        drop_sand(grid, max_y + 2, part=2)
        counter += 1
        if counter > 100000:
            print("breaking loop 2")
            break
        continue
    grid.update()
    return str(grid).count("o")


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2022, 14)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: None, 2: None}
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
