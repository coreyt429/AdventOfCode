"""
Advent Of Code 2016 day 6

slight modification to get into new format

"""

# import system modules
import time
from heapq import heappush, heappop

# import my modules
import aoc  # pylint: disable=import-error


def solve(lines, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return answer[2]
    messages = {1: "", 2: ""}
    for pos in range(len(lines[0])):
        tmp_str = ""
        for line in lines:
            tmp_str += line[pos]
        letters = set(tmp_str)
        heap = []
        for letter in letters:
            heappush(heap, (-1 * tmp_str.count(letter), letter))
        _, letter = heappop(heap)
        messages[1] += letter
        while heap:
            _, letter = heappop(heap)
        messages[2] += letter
    answer[2] = messages[2]
    return messages[1]


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2016, 6)
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
