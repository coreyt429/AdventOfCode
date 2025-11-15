"""
Advent Of Code 2022 day 4

This one was fairly quick.  solve_original() is my original infinite list of
if statements.

solve() is the solution from chatGPT optimizing my solution.
"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


def solve_original(input_value, part):
    """
    Function to solve puzzle
    """
    count = 0
    for line in input_value:
        elf_1, elf_2 = line.split(",")
        elf_1 = [int(num) for num in elf_1.split("-")]
        elf_2 = [int(num) for num in elf_2.split("-")]
        if elf_1[0] <= elf_2[0] and elf_1[1] >= elf_2[1]:
            count += 1
            continue
        if elf_2[0] <= elf_1[0] and elf_2[1] >= elf_1[1]:
            count += 1
            continue
        if part == 2:
            if elf_1[0] <= elf_2[0] <= elf_1[1]:
                count += 1
                continue
            if elf_1[0] <= elf_2[1] <= elf_1[1]:
                count += 1
                continue
            if elf_2[0] <= elf_1[0] <= elf_2[1]:
                count += 1
                continue
            if elf_2[0] <= elf_1[1] <= elf_2[1]:
                count += 1
                continue
    return count


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    count = 0
    for line in input_value:
        # Parse input into ranges
        (start1, end1), (start2, end2) = [
            tuple(map(int, elf.split("-"))) for elf in line.split(",")
        ]

        # Check full containment
        if (start1 <= start2 <= end2 <= end1) or (start2 <= start1 <= end1 <= end2):
            count += 1
        elif part == 2:
            # Check partial overlap
            if not (end1 < start2 or end2 < start1):
                count += 1
    return count


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2022, 4)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 487, 2: 849}
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
