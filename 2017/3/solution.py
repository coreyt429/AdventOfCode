"""
Advent Of Code 2017 day 3

This one was a bit more fun.  I went with a more mathematical solution for part 1,
and that didn't work well for part 2. So I tried building a traversal routine to
make the grid, but that was too slow for part 1.  So taking different approaches
for each part.

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error

# x/y constants
X = 0
Y = 1


def get_target_coordinates(target):
    """
    Part 1 solution.  Calculates values instead of building large grid
    """
    # init total, n and new
    total = 1
    counter = 1
    new = 0
    # loop until we find our target
    while total < target:
        # step n up by 2
        counter += 2
        # count of items for this layer
        new = (counter - 1) * 4
        # total count
        total += new
    # find lower right hand corner
    corner = counter // 2
    point = [corner, -1 * corner]
    # get difference between lower right hand corner and target
    diff = total - target
    # if diff is < counter, then target is on the bottom row
    if diff < counter:
        offset = diff
        point[X] -= offset
    # if diff is in the next counter-2 then target is on the left side
    elif diff < counter + (counter - 2):
        offset = diff - counter
        point[X] -= counter - 1
        point[Y] += offset + 1
    # if diff is in the next counter, then target is on the top row
    elif diff < counter * 2 + (counter - 2):
        offset = diff - (counter + (counter - 2))
        point[X] -= counter - 1
        point[X] += offset
        point[Y] *= -1
    # target must be on the right side
    else:
        offset = diff - (counter * 2 + (counter - 2))
        point[Y] += (counter - 2) - offset
    # return target point
    return tuple(point)


def traverse(target):
    """
    Part 2 solultions, builds out grid so we can evaluate neighbors
    """
    # directions to identify position in neighbors
    directions = {"up": 4, "left": 1, "right": 6, "down": 3}
    # init start and mem_map
    start = complex(0, 0)
    mem_map = {start: 1}
    # get neighbors of start
    neighbors = my_aoc.get_neighbors(mem_map, start, type="infinite")
    # init counter
    counter = 1
    # loop indefinitely
    while True:
        # increment counter by 2 (odd numbers)
        counter += 2
        # move current to the right
        current = neighbors[directions["right"]]
        # get neighbors of current
        neighbors = my_aoc.get_neighbors(mem_map, current, type="infinite")
        # initialize entry for current
        mem_map[current] = 0
        # add preexisting neighbor values to current
        for neighbor in neighbors:
            if neighbor in mem_map:
                mem_map[current] += mem_map[neighbor]
        # if current > target, return current value
        if mem_map[current] > target:
            return mem_map[current]
        # make loop up, left, down right
        for direction in ["up", "left", "down", "right"]:
            # start at step 1
            steps = 1
            # unless we are going up, we will have one less step
            if direction == "up":
                steps = 2
            # loop from steps to counter
            for _ in range(steps, counter):
                # get new current
                current = neighbors[directions[direction]]
                # init new current
                mem_map[current] = 0
                # get new neighbors
                neighbors = my_aoc.get_neighbors(mem_map, current, type="infinite")
                # add existing neighbor values
                for neighbor in neighbors:
                    if neighbor in mem_map:
                        mem_map[current] += mem_map[neighbor]
                # if we current > target return value
                if mem_map[current] > target:
                    return mem_map[current]


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        # get target point
        point = get_target_coordinates(int(input_value))
        # return manhattan distance to the center
        return my_aoc.manhattan_distance(point, (0, 0))
    # return mem_map traversal
    return traverse(int(input_value))


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017, 3)
    input_text = my_aoc.load_text()
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
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
