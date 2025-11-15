"""
Advent Of Code 2021 day 5

"""

# import system modules
import time
from collections import defaultdict

# import my modules
import aoc  # pylint: disable=import-error


def solve(lines, part):
    """Function to solve puzzle"""
    points = defaultdict(int)
    data = {"p": [], "x": [0, 0], "y": [0, 0]}
    for line in lines:
        data["p"] = line.split(" -> ")
        for idx, value in enumerate(data["p"]):
            data["x"][idx], data["y"][idx] = (int(num) for num in value.split(","))
        # if x's match or y's match, then we have a vertical or horizontal line
        if any([len(set(data["x"])) == 1, len(set(data["y"])) == 1]):
            # Consider only horizontal and vertical lines.
            for x_val in range(min(data["x"]), max(data["x"]) + 1):
                for y_val in range(min(data["y"]), max(data["y"]) + 1):
                    points[(x_val, y_val)] += 1
        elif part == 2:
            # Consider all of the lines.
            d_x = 1
            if data["x"][1] - data["x"][0] < 0:
                d_x = -1
            # d_y = d_x * slope
            d_y = d_x * int(
                (data["y"][1] - data["y"][0]) / (data["x"][1] - data["x"][0])
            )
            x_val = data["x"][0]
            y_val = data["y"][0]
            while x_val != data["x"][1]:
                points[(x_val, y_val)] += 1
                x_val += d_x
                y_val += d_y
            points[(data["x"][1], data["y"][1])] += 1
    # At how many points do at least two lines overlap?
    counter = 0
    for _, count in points.items():
        if count > 1:
            counter += 1
    # 11690 - too low
    return counter


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021, 5)
    input_data = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 6687, 2: 19851}
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
