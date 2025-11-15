"""
Advent Of Code 2017 day 2

easy peasy, and pylint ran clean the first time.  Maybe I'm learning!

"""

# import system modules
import time
import re

# import my modules
import aoc  # pylint: disable=import-error


def solve(lines, part):
    """
    Function to solve puzzle
    """
    # init checksums
    checksum = 0
    checksum2 = 0
    # walk lines
    for line in lines:
        # get ints from lines
        nums = [int(num) for num in re.findall(r"(\d+)", line)]
        # checksum 1: For each row, determine the difference between the largest value
        # and the smallest value; the checksum is the sum of all of these differences
        checksum += max(nums) - min(nums)
        found = False
        # part 2: It sounds like the goal is to find the only two numbers in each row
        # where one evenly divides the other - that is, where the result of the division
        # operation is a whole number. They would like you to find those numbers on each line,
        # divide them, and add up each line's result.
        if part == 2:
            # walk numbers
            for idx_1, num_1 in enumerate(nums):
                # walk numbers
                for idx_2, num_2 in enumerate(nums):
                    # lets not divide the same num
                    if idx_1 == idx_2:
                        continue
                    # is divisible?
                    if num_1 % num_2 == 0:
                        # yes add to checksum
                        checksum2 += num_1 / num_2
                        # mark found
                        found = True
                        break
                # break outer loop if found
                if found:
                    break
    if part == 2:
        # return part 2, cast as int so it doesn't return xxx.0
        return int(checksum2)
    # return part 1
    return checksum


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017, 2)
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
