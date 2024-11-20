"""
Advent Of Code 2022 day 1

Easy start.  This was fun.

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    elf_text = input_value.split("\n\n")
    elves = []
    max_calories = 0
    for elf in elf_text:
        elves.append([int(num) for num in elf.splitlines()])
        max_calories = max(max_calories, sum(elves[-1]))
    if part == 2:
        return sum(sorted((sum(elf) for elf in elves))[-3:])
    return max_calories

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2022,1)
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
        1: 71780,
        2: 212489
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
