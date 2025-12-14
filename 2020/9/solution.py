"""
Advent Of Code 2020 day 9

itertools.combinations made part 1 easy.

Part 2, I just used for loops set the window.
This works, and I'm sure there is probably a more elegant way.

Trying a sliding window solution as well to expand my knowledge.
Okay, that worked, and quite impressively.  reduced part2 from
0.09 seconds to 0.0
"""

# import system modules
import logging
import argparse
from itertools import combinations

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

# dict to store answers
answer = {1: None, 2: None}


def find_first_invalid(numbers, preamble_size):
    """
    Function to find first number that is not
    the sum of two numbers within preamble_size
    before it.
    """
    for idx in range(preamble_size, len(numbers) + 1):
        match_found = False
        for combo in combinations(numbers[idx - preamble_size : idx], 2):
            if sum(combo) == numbers[idx]:
                match_found = True
                break  # combo for loop
        if match_found:
            continue  # next idx

        return numbers[idx]
    return None


def find_matching_group_orig(numbers, target):
    """
    Function to find a group of consecutive numbers that add up to the target.
    This is my original version
    """
    # find a contiguous set of at least two numbers
    for idx in range(len(numbers) + 1):
        for idx2 in range(idx + 2, len(numbers) + 2):
            value = sum(numbers[idx:idx2])
            if value > target:
                break  # for idx2
            # find a contiguous set of at least two numbers in your list which
            # sum to the invalid number from step 1.
            if value == target:
                min_val = min(numbers[idx:idx2])
                max_val = max(numbers[idx:idx2])
                # To find the encryption weakness, add together the smallest and
                # largest number in this contiguous range;
                return min_val + max_val
    return None


def find_matching_group(numbers, target):
    """
    Function to find a group of consecutive numbers that add up to the target.
    Sliding window version.
    """
    start, end, current_sum = 0, 0, numbers[0]
    # find a contiguous set of at least two numbers in your list which
    # sum to the invalid number from step 1.
    while current_sum != target:
        if current_sum < target:
            end += 1
            current_sum += numbers[end]
        if current_sum > target:
            current_sum -= numbers[start]
            start += 1
    # To find the encryption weakness, add together the smallest and
    # largest number in this contiguous range;
    min_val = min(numbers[start : end + 1])
    max_val = max(numbers[start : end + 1])
    return min_val + max_val


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # XMAS starts by transmitting a preamble of 25 numbers
    preamble_size = 25
    numbers = [int(num) for num in input_value]
    first_invalid = find_first_invalid(numbers, preamble_size)
    if part == 1:
        # What is the first number that does not have this property?
        return first_invalid
    # part 2:
    # which sum to the invalid number from step 1.
    return find_matching_group(numbers, first_invalid)


YEAR = 2020
DAY = 9
input_format = {
    1: "lines",
    2: "lines",
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
