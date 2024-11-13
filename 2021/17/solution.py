"""
Advent Of Code 2021 day 17

When I first read this one, I was tempted to use Grid()
to visualize it.  As I thought about the problem, I realized
it could be solved mathematically instead and I didn't need
the visualization.  The tricky part was narrowing the range
to search.

"""
# import system modules
import time
import re
import math

# import my modules
import aoc # pylint: disable=import-error


def parse_data(text):
    """Function to parse input data"""
    digit_pattern = re.compile(r'(\-*\d+)')
    nums = [int(num) for num in digit_pattern.findall(text)]
    return dict({'x': nums[:2], 'y': nums[2:]})

def find_min_x(target):
    """Function to find the minimum x velocity that can reach the target"""
    x_min = min(target['x'])
    return round(math.sqrt(x_min*2))

def in_target_area(point, target):
    """Function to determine if a point is in the target area"""
    if target['x'][0] <= point[0] <=  target['x'][1]:
        if target['y'][0] <= point[1] <=  target['y'][1]:
            return True
    return False

def missed_target_area(point, target):
    """Function to determine if a point has passed the target area"""
    if point[0] >  max(target['x']):
        return True
    if point[1] <  min(target['y']):
        return True
    return False

def trace_path(velocity, target):
    """Function to trace a path"""
    max_y = 0
    min_y = 0
    x_velocity, y_velocity = velocity
    x_val, y_val = 0, 0
    # points = set([(0,0)])
    while not missed_target_area((x_val, y_val), target):
        # increment position
        x_val += x_velocity
        y_val += y_velocity
        # points.add((x_val, y_val))
        max_y = max(y_val, max_y)
        min_y = min(y_val, min_y)
        # decrement velocities
        y_velocity -= 1
        x_velocity = max(x_velocity - 1, 0)
        if in_target_area((x_val, y_val), target):
            return True, max_y, min_y, (x_val, y_val)
    return False, max_y, min_y, (0, 0)

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    target = parse_data(input_value)
    # minimum x velocity that will get there
    start_x = find_min_x(target)
    # maximum x velocity, that won't overshoot on step 1
    stop_x = max(target['x'])
    # start at the minimum y, any lower and we overshoot
    start_y = min(target['y'])
    # stop at the opposite y value
    stop_y = abs(start_y)
    goal = 0
    successes = set()
    for x_val in range(start_x, stop_x + 1):
        for y_val in range(start_y, stop_y + 1):
            velocity = (x_val, y_val)
            success, max_y, _, _ = trace_path(velocity, target)
            # print(velocity, success, max_y, min_y, point)
            if success:
                successes.add((x_val, y_val))
                goal = max(max_y, goal)
    if part == 2:
        # 2003 too low
        return len(successes)
    # 105 too low
    # doubled stop_y
    # 435 too low
    # set stop_y to abs(min_y)
    # 30628 correct
    return goal

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021,17)
    input_data = my_aoc.load_text()
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
        1: 30628,
        2: 4433
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
