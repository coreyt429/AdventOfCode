"""
Advent Of Code 2021 day 18

"""

# import system modules
import time
import re

# import my modules
import aoc  # pylint: disable=import-error


pattern_digit = re.compile(r"(\d+)")
pattern_pair = re.compile(r"\[(\d+),(\d+)\]")


def add_snail_numbers(left, right):
    """Function to add two snail numbers"""
    return f"[{left},{right}]"


def can_explode(string):
    """Function to identify the exploding pair if any"""
    max_depth = 0
    depth = 0
    for idx, char in enumerate(string):
        if char == "[":
            depth += 1
            max_depth = max(depth, max_depth)
            if max_depth > 4:
                return True, idx
            continue
        if char == "]":
            depth -= 1
    return False, 0


def add_explode_num(string, num, left=False):
    """Function to replace the first digit"""
    nums = pattern_digit.findall(string)
    if not nums:
        return string
    target_num = nums[0]
    if left:
        target_num = nums[-1]
    new_num = str(int(target_num) + int(num))
    new_string = string.replace(target_num, new_num, 1)
    if left:
        last_index = string.rfind(target_num)
        if last_index != -1:
            new_string = (
                string[:last_index] + new_num + string[last_index + len(target_num) :]
            )
    return new_string


def explode_snail_number(string, idx):
    """Function to exlode a pair"""
    left = string[:idx]
    right = string[idx:]
    exp_pair = right[: right.index("]") + 1]
    right = right[len(exp_pair) :]
    exp_pair = [int(num) for num in pattern_digit.findall(exp_pair)]
    # the pair's left value is added to the first regular number to the
    # left of the exploding pair (if any)
    left = add_explode_num(left, exp_pair[0], True)
    right = add_explode_num(right, exp_pair[1])
    return left + "0" + right


def can_split(string):
    """Function to determine if a snail number can be split"""
    # If any regular number is 10 or greater, the leftmost such regular number splits.
    nums = [int(num) for num in pattern_digit.findall(string)]
    for num in nums:
        if num > 9:
            return True, str(num)
    return False, -1


def split_snail_number(string, num):
    """Function to split a snail number"""
    # To split a regular number, replace it with a pair; the left element of
    # the pair should be the regular number divided by two and rounded down,
    # while the right element of the pair should be the regular number divided
    # by two and rounded up. For example, 10": [5,5], 11": [5,6],
    # 12": [6,6], and so on.
    idx = string.index(num)
    left = string[:idx]
    right = string[idx + len(num) :]
    num = int(num)
    middle = f"[{num // 2},{num - (num // 2)}]"
    return left + middle + right


def reduce_snail_number(string):
    """Function to reduce a snail number"""
    working_string = string
    changed = True
    while changed:
        changed = False
        do_explode, idx = can_explode(working_string)
        if do_explode:
            working_string = explode_snail_number(working_string, idx)
            changed = True
            continue
        do_split, num = can_split(working_string)
        if do_split:
            working_string = split_snail_number(working_string, num)
            changed = True
            continue
    return working_string


def calc_magnitude(string):
    """Function to calculate magnitude"""
    working_string = string
    match = pattern_pair.search(working_string)
    magnitude = 0
    while match:
        span = match.span()
        left = working_string[: span[0]]
        right = working_string[span[1] :]
        pair = [int(num) for num in match.groups()]
        magnitude = pair[0] * 3 + pair[1] * 2
        working_string = left + str(magnitude) + right
        match = pattern_pair.search(working_string)
    return int(working_string)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    snail_numbers = list(input_value)
    if part == 2:
        max_magnitude = 0
        for num_1 in snail_numbers:
            for num_2 in snail_numbers:
                if num_1 == num_2:
                    continue
                working_number = add_snail_numbers(num_1, num_2)
                working_number = reduce_snail_number(working_number)
                max_magnitude = max(calc_magnitude(working_number), max_magnitude)
        return max_magnitude
    working_number = snail_numbers.pop(0)
    while snail_numbers:
        new_number = snail_numbers.pop(0)
        working_number = add_snail_numbers(working_number, new_number)
        working_number = reduce_snail_number(working_number)
    return calc_magnitude(working_number)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021, 18)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 4433, 2: 4559}
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
