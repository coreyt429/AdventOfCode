"""
Advent Of Code 2018 day 25

"""
# import system modules
import time
from collections import deque

# import my modules
import aoc # pylint: disable=import-error
from grid import manhattan_distance # pylint: disable=import-error

def parse_data(lines):
    """parse input data"""
    points = []
    for line in lines:
        data = [int(num) for num in line.split(',')]
        points.append(tuple(data))
    return points

def group_points(points, distance_threshold=3):
    """
    Function to group points into constellations
    """
    # init visited and groups
    visited = set()
    groups = []

    def bfs(start_point):
        """breadth first search"""
        # init queue and group
        queue = deque([start_point])
        group = []
        # process queue
        while queue:
            # get next point
            point = queue.popleft()
            # check visited
            if point in visited:
                continue
            # add to visited and group
            visited.add(point)
            group.append(point)

            # Check all other points to see if they are within the threshold distance
            for neighbor in points:
                if (neighbor not in visited and
                    manhattan_distance(point, neighbor) <= distance_threshold):
                    queue.append(neighbor)
        return group

    # walk points
    for point in points:
        # if not visited
        if point not in visited:
            # get group
            group = bfs(point)
            # append group
            groups.append(group)

    return groups

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return part
    constellations = group_points(parse_data(input_value))
    return len(constellations)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018,25)
    input_lines = my_aoc.load_lines()
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
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
