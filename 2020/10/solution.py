"""
Advent Of Code 2020 day 10

Part 1 was easy. Part 2, I came up with a couple solutions that might
work given infinite time and resources.

I found the final version by studying the solution from u/rune_kg

With some explanation from ChatGPT, it was clear how it worked and I was
able to write a simliar solution with minimal looking back at the original.


"""
# import system modules
import time
from collections import defaultdict
from itertools import combinations
from heapq import heappop, heappush
# import my modules
import aoc # pylint: disable=import-error

def find_jolt_differences(numbers):
    """
    Function to find the jolt differences in an adapter chain
    """
    sorted_numbers = sorted(numbers + [0])
    sorted_numbers.append(sorted_numbers[-1]+3)
    jolt_differences = defaultdict(int)
    for idx, num in enumerate(sorted_numbers):
        if num == sorted_numbers[-1]:
            continue
        diff = sorted_numbers[idx + 1] - num
        jolt_differences[diff] += 1
    # What is the number of 1-jolt differences multiplied by the number of 3-jolt differences?
    return jolt_differences[1] * jolt_differences[3]

def count_adapter_combinations_failed(numbers):
    """
    Function to count the combinations of adapters
    """
    print(f"{len(numbers)} numbers")
    # outlet = 0
    device = max(numbers) + 3
    valid = 0
    # print statement to find minumum number of adapters: 53
    # print(f"{min(numbers)} - {max(numbers)} {(max(numbers) - min(numbers)) // 3}")
    for length in range(50, len(numbers) + 1):
        combos = list(combinations(numbers, length))
        print(f"length: {length}, combos: {len(combos)}")
        for combo in combos:
            if combo[0] > 3:
                continue
            if device - combo[-1] > 3:
                continue
            last = 0
            invalid = False
            for num in combo:
                if num - last > 3:
                    invalid = True
                    break
                last = num
            if not invalid:
                valid += 1
    return valid

def count_adapter_combinations(numbers):
    """
    Failed attempt
    """
    heap = []
    valid = set()
    target = max(numbers) + 3
    heappush(heap, (0, (0,)))
    counter = 0
    while heap:
        length, adapters = heappop(heap)
        counter += 1
        if counter % 10000 == 0:
            print(len(heap), length, adapters)

        if adapters[-1] + 3 >= target:
            valid.add(adapters)

        for num in numbers:
            if adapters[-1] < num <= adapters[-1] + 3:
                tmp_list = list(adapters)
                tmp_list.append(num)
                heappush(heap, (length + 1, tuple(tmp_list)))
    return len(valid)

def depth_first_counter(dag, current_jolt, memoization):
    """
    function to count possible paths
    """
    # path already seen
    if current_jolt in memoization:
        return memoization[current_jolt]
    # new path
    if dag[current_jolt]:
        memoization[current_jolt] = sum(
            depth_first_counter(dag, next_jolt, memoization) for next_jolt in dag[current_jolt]
        )
        return memoization[current_jolt]
    # no further paths
    return 1

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    numbers = [int(num) for num in input_value]
    if part == 1:
        return find_jolt_differences(numbers)
    # Part 2
    sorted_numbers = sorted(numbers + [0])
    sorted_numbers.append(sorted_numbers[-1]+3)
    # Directed Acyclic Graph (DAG)
    dag = {
            next_node:
                {
                    next_dest for next_dest in range(
                        next_node + 1,
                        next_node + 4
                    ) if next_dest in sorted_numbers
                }
             for next_node in sorted_numbers
    }
    return depth_first_counter(dag, 0, {})
    # return count_adapter_combinations(numbers)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020,10)
    input_lines = my_aoc.load_lines()
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
        1: 2170,
        2: 24803586664192
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
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
