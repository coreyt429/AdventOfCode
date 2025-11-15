"""
Advent Of Code 2021 day 2

Pylint 10.00/10 without making changes, I think that is a first.

For part two, h_val doesn't change. So we just need to calculate
the depth differently.

Added answer[2] storing to short circuit the second pass.  What's
a minutes work to shave milliseconds :)
"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


def parse_data(lines):
    """function to parse data"""
    course = []
    for line in lines:
        command, value = line.split(" ")
        course.append(tuple([command, int(value)]))
    return tuple(course)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return answer[2]
    course = parse_data(input_value)
    h_val = 0
    depth = {1: 0, 2: 0}
    aim = 0
    for step in course:
        command, value = step
        # forward X increases the horizontal position by X units.
        # forward X does two things:
        #     It increases your horizontal position by X units.
        #     It increases your depth by your aim multiplied by X.
        if command == "forward":
            h_val += value
            depth[2] += aim * value
        # down X increases the depth by X units.
        # down X increases your aim by X units.
        elif command == "down":
            depth[1] += value
            aim += value
        # up X decreases the depth by X units.
        # up X decreases your aim by X units.
        elif command == "up":
            depth[1] -= value
            aim -= value
        answer[2] = h_val * depth[2]
    return h_val * depth[part]


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021, 2)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 2070300, 2: 2078985210}
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
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
