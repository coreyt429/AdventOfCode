"""
Advent Of Code 2024 day 11

Part 1 no problem. Part 2, thats a lot of numbers.

I initially got hung up on order matters, until I looked at solutions
and realize it didn't.  u/lmasman used a dict to map and count the numbers.
That tripped a memory of similar problems in the past.  One of these days
maybe I'll just remember that technique.  From there I was able to adapt
my code to the new data structure, and solve time is down to 0.04 seconds
for part 2.

"""
# import system modules
import time
from functools import lru_cache
# import my modules
import aoc # pylint: disable=import-error

@lru_cache(maxsize=None)
def split_stone(stone):
    """Function to split even length stones"""
    stone_str = str(stone)
    split_stones = []
    if len(stone_str) % 2 == 0:
        half = len(stone_str) // 2
        split_stones.append(int(stone_str[0:half]))
        split_stones.append(int(stone_str[half:]))
        return True, split_stones
    return False, [stone]

@lru_cache(maxsize=None)
def change_stone(stone):
    """Function to check a stone to see which change it needs to make"""
    # If the stone is engraved with the number 0,
    # it is replaced by a stone engraved with the number 1.
    if stone == 0:
        return [1]
    # If the stone is engraved with a number that has an even number of digits,
    # it is replaced by two stones. The left half of the digits are engraved on the new left stone,
    # and the right half of the digits are engraved on the new right stone.
    # (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
    can_split, split_stones = split_stone(stone)
    if can_split:
        return split_stones
    # If none of the other rules apply, the stone is replaced by a new stone;
    # the old stone's number multiplied by 2024 is engraved on the new stone.
    return [stone * 2024]

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    stones = {}
    for stone in (int(num) for num in input_value.split(' ')):
        stones[stone] = stones.get(stone, 0) + 1
    blinks = 25
    if part == 2:
        blinks = 75
    for _ in range(blinks):
        new_stones = {}
        for stone, count in stones.items():
            if count > 0:
                # stones[stone] -= count
                new_stones[stone] = new_stones.get(stone, 0)
                for new_stone in change_stone(stone):
                    new_stones[new_stone] = new_stones.get(new_stone, 0) + count
        for key, value in new_stones.items():
            stones[key] = value
    return sum(stones.values())

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2024,11)
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
        1: 235850,
        2: 279903140844645
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
