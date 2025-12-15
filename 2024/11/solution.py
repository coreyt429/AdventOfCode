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
import logging
import argparse
from functools import lru_cache

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


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
    if stone == 0:
        return [1]
    can_split, split_stones = split_stone(stone)
    if can_split:
        return split_stones
    return [stone * 2024]


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    stones = {}
    for stone in (int(num) for num in input_value.split(" ")):
        stones[stone] = stones.get(stone, 0) + 1
    blinks = 25
    if part == 2:
        blinks = 75
    for _ in range(blinks):
        new_stones = {}
        for stone, count in stones.items():
            if count > 0:
                new_stones[stone] = new_stones.get(stone, 0)
                for new_stone in change_stone(stone):
                    new_stones[new_stone] = new_stones.get(new_stone, 0) + count
        for key, value in new_stones.items():
            stones[key] = value
    return sum(stones.values())


YEAR = 2024
DAY = 11
input_format = {
    1: "text",
    2: "text",
}

funcs = {
    1: solve,
    2: solve,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    aoc = AdventOfCode(
        year=YEAR,
        day=DAY,
        input_formats=input_format,
        funcs=funcs,
        test_mode=args.test,
    )
    aoc.run(submit=args.submit)
