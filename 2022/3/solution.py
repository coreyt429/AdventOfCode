"""
Advent Of Code 2022 day 3

set() and string slicing made this one fairly easy.

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def item_priority(item):
    """Function to calculate item priority"""
    if item.islower():
        # Lowercase item types a through z have priorities 1 through 26.
        return ord(item) - ord('a') + 1
    # Uppercase item types A through Z have priorities 27 through 52.
    return ord(item) - ord('A') + 1 + 26

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    total = 0
    if part == 1:
        for line in input_value:
            half = int(len(line) / 2)
            set_a = set(line[:half])
            set_b = set(line[half:])
            # Find the item type that appears in both compartments of each rucksack.
            total += item_priority(set_a.intersection(set_b).pop())
        # What is the sum of the priorities of those item types?
        return total
    # part 2
    while input_value:
        # Find the item type that corresponds to the badges of each three-Elf group.
        # Every set of three lines in your list corresponds to a single group
        common_set = set(input_value.pop(0))
        common_set.intersection_update(input_value.pop(0))
        common_set.intersection_update(input_value.pop(0))
        total += item_priority(common_set.pop())
    # What is the sum of the priorities of those item types?
    return total

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2022,3)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
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
        1: 8039,
        2: 2510
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
