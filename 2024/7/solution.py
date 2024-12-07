"""
Advent Of Code 2024 day 7

"""
# import system modules
import time
import math
from heapq import heappop, heappush

# import my modules
import aoc # pylint: disable=import-error

def parse_input(lines):
    """Function to parse puzzle input"""
    inputs = []
    for line in lines:
        value_text, nums_text = line.split(': ')
        value = int(value_text)
        nums = [int(num) for num in nums_text.split(' ')]
        inputs.append((value, tuple(nums)))
    return tuple(inputs)

def can_solve(target, nums, operators, next_op='None', value=None):
    """Function to determine if equation is solveable"""
    heap = []
    heappush(heap, (len(nums), nums, 'None', None))

    while heap:
        _, nums, next_op, value = heappop(heap)
        nums = list(nums)
        if not nums:
            if value == target:
                return True
            continue
        if value is None:
            value = nums.pop(0)
        if next_op == 'None':
            for try_op in operators.keys():
                heappush(heap, (len(nums), tuple(nums), try_op, value))
        else:
            value = operators[next_op](value, nums.pop(0))
            heappush(heap, (len(nums), tuple(nums), 'None', value))
    if not nums and value == target:
        return True
    return False

def concat(num_1, num_2):
    """function to concatenate two numbers"""
    if num_2 == 0:
        return num_1 * 10
    # return int(str(num_1) + str(num_2))
    return num_2 + (num_1 * 10 ** math.ceil(math.log10(num_2) + 1e-7))

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    operators = {
        '+': lambda a,b: a + b,
        '*': lambda a,b: a * b
    }
    if part == 2:
        operators['||'] = concat
    total = 0
    equations = parse_input(input_value)
    for equation in equations:
        if can_solve(equation[0], equation[1], operators):
            total += equation[0]
    return total

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2024,7)
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
        1: 1708857123053,
        2: 189207836795655
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
