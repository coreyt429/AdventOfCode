"""
Advent Of Code 2024 day 8

Part 1, it took a few iterations to detemine if I should int() or round() in a couple
of places.

Part 2, was made easy by my approach to part 1.  I already had all the points that
were rounded to the line.  I just had to check them to be sure they were "exactly"
collinnear.  Luckily I already had a function in my grid module for that.

"""
# import system modules
import time
from collections import defaultdict
from itertools import combinations

# import my modules
import aoc # pylint: disable=import-error
from grid import Grid, linear_distance, are_collinear # pylint: disable=import-error

def get_line(p_1, p_2, grid):
    """Function to get the points colinear to two points"""
    # calculate slope
    d_x = p_2[0] - p_1[0]
    d_y = p_2[1] - p_1[1]
    slope = d_y/d_x
    # calculate intercept
    intercept = p_1[1] - slope * p_1[0]
    x_range = (grid.cfg['min'][0], grid.cfg['max'][0])
    y_range = (grid.cfg['min'][1], grid.cfg['max'][1])
    points = []
    # iterate over range of x_values in grid
    for x_val in range(x_range[0], x_range[1] + 1):
        # calculate y
        y_val = slope * x_val + intercept
        # not rounding here broke the test data
        # this round is also what I think caused the need for the
        # extra collinear check in part 2
        y_val = round(y_val)
        # check y if y is in the grid
        if y_range[0] <= y_val <= y_range[1]:
            points.append((x_val, y_val))
    return points

def is_antinode(point, pair):
    """Function to check if a point is an antinode for a pair"""
    # points in our pair can't be antinodes, and letting it go further
    # will result in a division by zero error
    if point in pair:
        return False
    distances = []
    for node in pair:
        distances.append(linear_distance(point, node))
    distances.sort()
    return abs(distances[1]/distances[0]) == 2

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid(input_value, use_overrides=False)
    signal_points = defaultdict(set)
    # get the points emitting each signal
    for point, char in grid.items():
        if char != '.':
            signal_points[char].add(point)

    antinodes = set()
    # iterate over the point sets for each signal frequency
    for points in signal_points.values():
        # iterate over possible pairs of points for this signal frequency
        for pair in combinations(points, 2):
            for point in get_line(*pair, grid):
                if is_antinode(point, pair):
                    antinodes.add(point)
                # After updating your model, it turns out that an antinode occurs at any
                # grid position exactly in line with at least two antennas of the same
                # frequency, regardless of distance.
                if part == 2 and are_collinear(point, *pair):
                    antinodes.add(point)
                    # 2256 too high, "exactly" was the missing word, added the are_collinear
                    # check and it worked
    return len(antinodes)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2024,8)
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
        1: 252,
        2: 839
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
