"""
Advent Of Code 2017 day 10

This one was fun, and I learned a few things in python that I don't usually use.
Yeah, had to google a bit, ash chatGPT vague questions, and play in the scratchpad.

"""

# import system modules
from __future__ import annotations
import logging
import argparse
from collections import deque
from functools import reduce

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)


def hash_list(some_list, queue, skip, total_rotate=0):
    """
    Function to hash a list
    """
    input_list = list(some_list)
    while input_list:
        length = input_list.pop(0)
        knot = list(queue)[:length][::-1]
        queue = deque(knot + list(queue)[length:])
        rotate = length + skip
        total_rotate += rotate
        queue.rotate(-1 * rotate)
        skip += 1
    return queue, skip, total_rotate


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    queue = deque(range(256))
    skip = 0
    total_rotate = 0
    if part == 1:
        queue, skip, total_rotate = hash_list(
            [int(num) for num in input_value.split(",")], queue, skip, total_rotate
        )
        queue.rotate(total_rotate)
        return queue[0] * queue[1]
    num_list = [ord(char) for char in input_value] + [17, 31, 73, 47, 23]
    for _ in range(64):
        queue, skip, total_rotate = hash_list(num_list, queue, skip, total_rotate)
    queue.rotate(total_rotate)
    sparse_hash = list(queue)
    sparse_hashes = []
    for idx in range(0, 256, 16):
        sparse_hashes.append(sparse_hash[idx : idx + 16])
    dense_hash = []
    for sparse in sparse_hashes:
        dense_hash.append(reduce(lambda x, y: x ^ y, sparse))
    my_hash = ""
    for num in dense_hash:
        my_hash += str(hex(num))[-2:].replace("x", "0")
    return my_hash


YEAR = 2017
DAY = 10
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
