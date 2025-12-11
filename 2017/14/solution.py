"""
Advent Of Code 2017 day 14

"""

# import system modules
from __future__ import annotations
import logging
import argparse
from collections import deque
from functools import reduce
from heapq import heappop, heappush

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

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


def knot_hash(input_value):
    """
    Function to create knot hash
    """
    queue = deque(range(256))
    skip = 0
    total_rotate = 0
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


def hex_to_bits(hex_string):
    """convert hex to bit string"""
    return "".join(format(int(c, 16), "04b") for c in hex_string)


def map_region(grid, position):
    """
    Map a region based on a start string
    """
    logger.debug("mapping region from position %s", position)
    region = set()
    heap = []
    heappush(heap, position)
    while heap:
        logger.debug("processing heap, current size: %d", len(heap))
        current = heappop(heap)
        if current in region:
            continue
        region.add(current)
        for neighbor in grid.get_neighbors(
            point=current, directions=["n", "s", "e", "w"]
        ).values():
            logger.debug("checking neighbor: %s", neighbor)
            if grid.map.get(neighbor) == "#":
                heappush(heap, neighbor)
    logger.debug("region mapped: %s", region)
    return region


def find_regions(grid_map):
    """
    Function to find regions
    """
    regions = []
    already_seen = set()
    grid = Grid(grid_map=grid_map)
    for position in grid:
        char = grid.map.get(position)
        logger.debug("char at position %s: %s", position, char)
        if char == "#":
            if position not in already_seen:
                logger.debug("mapping new region from position %s", position)
                new_region = map_region(grid, position)
                regions.append(new_region)
                already_seen.update(new_region)
    logger.debug("regions found: %s", regions)
    return len(regions)


def print_grid(grid, text="Grid"):
    """
    Function to print grid
    """
    print(f"{text}:")
    for row in grid:
        print("".join(row))
    print()


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    total = 0
    drive = []
    for idx in range(128):
        data = hex_to_bits(knot_hash(f"{input_value}-{idx}"))
        data = data.replace("1", "#").replace("0", ".")
        total += data.count("#")
        drive.append(list(data))
    if part == 2:
        logger.debug("Finding regions")
        return find_regions(drive)
    return total


YEAR = 2017
DAY = 14
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
