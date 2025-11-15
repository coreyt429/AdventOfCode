"""
Advent Of Code 2018 day 23

Part1 was quick and easy.

Part2 Brute force was impractical. Though I did use the opportunity to improve
my manhattan_distance function.

I reveiewed a couple of z3 implementations for this, and thougth that sounded familiar.
Dusted off an older z3 solution I used in the past (technically future since it was a 2023
puzzle).  I had issues running any of these on my current system, and instead focused
on a simple math solution from u/EriiKKo.

This solution I feel may be making assumptions that aren't true for the general case,
but work with the input data and test data. So it works in the context of this puzzle.

My understanding of the logic is to collapse the 3d structure to a line, and identify the
point in that line that is inside the most circles.

"""

# import system modules
import time
import re
from queue import PriorityQueue

# import my modules
import aoc  # pylint: disable=import-error
from grid import manhattan_distance  # pylint: disable=import-error


def parse_input(lines):
    """
    Function to parse input date
    Args:
        lines: list() of str()
    Returns:
        bots: dict() keyed on tuple(x,y,z)
    """
    # regex to parse input
    pattern_input = re.compile(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)")

    bots = {}
    for line in lines:
        match = pattern_input.findall(line)
        if match:
            # convert to integers
            pos_x, pos_y, pos_z, radius = [int(num) for num in match[0]]
            bots[(pos_x, pos_y, pos_z)] = radius
    return bots


def closest_max_intersection(points, origin=(0, 0, 0)):
    """
    Function to calculate the nearest point with the most intersections

    This is adapted from the solution presented by u/EriiKKo, and converted
    to work in my code base.

    Args:
        points: dict() keyed on coordinate tuple() value radius int()
        origin: coordinate tuple()
    """
    # init queue
    queue = PriorityQueue()
    # walk points
    for point, radius in points.items():
        distance = manhattan_distance(origin, point)
        # entry event (distance - radius) or 0 if origin is in the circle
        queue.put((max(0, distance - radius), 1))
        # exit event distance + radius
        queue.put((distance + radius + 1, -1))

    # init variables
    count = 0
    max_count = 0
    result = 0
    # process queue
    while not queue.empty():
        # get distance and event
        distance, event = queue.get()
        # increment/decrement count
        count += event
        # if new max
        if count > max_count:
            # update result and max
            result = distance
            max_count = count
    return result


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    nanobots = parse_input(input_value)
    if part == 1:
        max_signal = max((signal for signal in nanobots.values()))
        max_nanobot = None
        for nanobot, signal in nanobots.items():
            if signal == max_signal:
                max_nanobot = nanobot
        in_range = []
        for nanobot in nanobots:
            if manhattan_distance(max_nanobot, nanobot) <= max_signal:
                in_range.append(nanobot)
        return len(in_range)
    # part 2:
    return closest_max_intersection(nanobots)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018, 23)
    # grab input
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
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
