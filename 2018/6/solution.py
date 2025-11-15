"""
Advent Of Code 2018 day 6

"""

# import system modules
import time
import re
import itertools

# import my modules
import aoc  # pylint: disable=import-error
from grid import manhattan_distance  # pylint: disable=import-error

labels = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]

X = 0
Y = 1


def get_points(lines):
    """
    Function to extract points from input data
    """
    # init points
    points = {}
    # walk lines
    for idx, line in enumerate(lines):
        # extract numbers
        matches = re.findall(r"(\d+)", line)
        # build point
        points[tuple(int(match) for match in matches)] = labels[idx]
    return points


def find_range_size(points, part):
    """
    Function to find rage size
    """
    # get max values
    max_x = max(point[X] for point in points.keys())
    max_y = max(point[Y] for point in points.keys())
    # init dicts
    distances = {}
    sizes = {}
    # init sizes
    for point, label in points.items():
        sizes[label] = 1

    # walk row/col combinations
    # I need to remember this, it is faster than for x in range, for y in range
    # also keeping current_point in a tuple, seemed to be faster than (col, row)
    for current_point in itertools.product(range(max_x + 1), range(max_y + 1)):
        # in part 1 skip if in points
        if current_point in points and part == 1:
            continue
        # init vars
        min_distance = float("infinity")
        count = 0
        distances[current_point] = 0
        # iterate over points
        for point, label in points.items():
            # get manhattan distance
            distance = manhattan_distance(current_point, point)
            # add to distances
            distances[current_point] += distance
            # if we match distance increment
            if distance == min_distance:
                count += 1
            # new min distance
            elif distance < min_distance:
                count = 1
                min_label = label
                min_distance = distance
        # if only one matches
        if count == 1:
            # increment size
            sizes[min_label] += 1
            # if we are at an edge, set size tin infinity
            if current_point[Y] in (0, max_y) or current_point[X] in (0, max_x):
                sizes[min_label] = float("infinity")
    # init max_size
    max_size = 0
    # iterate over sizes
    for size in sizes.values():
        # if not inf, but bigger than max
        if size != float("inf") and size > max_size:
            # update max_size
            max_size = size
    return max_size, distances


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # if part == 2:
    #    return answer[2]
    my_points = get_points(input_value)
    my_size, my_distances = find_range_size(my_points, part)
    for distance in my_distances.values():
        # too high: 46561
        # too low:  46514
        if part == 2:
            if distance < 10000:
                answer[2] += 1
    if part == 2:
        return answer[2]
    return my_size


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018, 6)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: 0}
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
