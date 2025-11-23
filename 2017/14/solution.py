"""
Advent Of Code 2017 day 14

"""

# import system modules
# import system modules
import sys
import logging

from collections import deque
from functools import reduce
from heapq import heappop, heappush

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

# import my modules
import aoc  # pylint: disable=import-error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def hash_list(some_list, queue, skip, total_rotate=0):
    """
    Function to hash a list
    """
    # copy input
    input_list = list(some_list)
    # init rotate
    rotate = 0
    # repeat until we've exhausted the list
    while input_list:
        # next length to twist
        length = input_list.pop(0)
        # Reverse the first length entries in the deque
        knot = list(queue)[:length][::-1]  # take first length, reverse them
        # Reinsert the reversed values back into the deque
        queue = deque(knot + list(queue)[length:])
        # rotate deque instead of skipping and keeping up with position
        rotate = length + skip
        # yeah, I see I have to keep up with total rotations instead
        total_rotate += rotate
        # rotate left, to simulate skipping right
        queue.rotate(-1 * rotate)
        # increment skip
        skip += 1
    # return 1, skp, and total_rotate to be passed back next pass
    return queue, skip, total_rotate


def knot_hash(input_value):
    """
    Function to solve puzzle
    """
    # init queue with numbers 0=255
    queue = range(256)
    queue = deque(queue)
    # init skipq
    skip = 0
    # init total_rotate
    total_rotate = 0
    num_list = [ord(char) for char in input_value] + [17, 31, 73, 47, 23]
    # run hash_list 64 times
    for _ in range(64):
        queue, skip, total_rotate = hash_list(num_list, queue, skip, total_rotate)
    queue.rotate(total_rotate)
    # split into groups of 16
    sparse_hash = list(queue)
    sparse_hashes = []
    for idx in range(0, 256, 16):
        sparse_hashes.append(sparse_hash[idx : idx + 16])
    # use bitwise XOR to create dense_hash values
    dense_hash = []
    for sparse_hash in sparse_hashes:
        dense_hash.append(reduce(lambda x, y: x ^ y, sparse_hash))
    # get hex values of dense_hash for hex hash
    my_hash = ""
    for num in dense_hash:
        my_hash += str(hex(num))[-2:].replace("x", "0")
    # return hex hash
    return my_hash


def hex_to_bits(hex_string):
    """convert hex to bit string"""
    return "".join(format(int(c, 16), "04b") for c in hex_string)


def map_region(grid, position):
    """
    Map a region based on a start string
    """
    logger.debug("mapping region from position %s", position)
    # init region
    region = set()
    # init heap with start position
    heap = []
    heappush(heap, position)
    # process heap
    while heap:
        logger.debug("processing heap, current size: %d", len(heap))
        # get current
        current = heappop(heap)
        # already in region? next
        if current in region:
            continue
        # add to region
        region.add(current)
        # get n, e, s, and w neighbors (diagonals not allowed!)
        for neighbor in grid.get_neighbors(
            point=current, directions=["n", "s", "e", "w"]
        ).values():
            logger.debug("checking neighbor: %s", neighbor)
            # if neighbor is filled
            if grid.map.get(neighbor) == "#":
                # add neighbor to heap
                heappush(heap, neighbor)
    # return region when all possibilities have been exhausted
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
        # if slot is filled
        logger.debug("char at position %s: %s", position, char)
        if char == "#":
            # if not already seen, lets check it out
            if not position in already_seen:
                logger.debug("mapping new region from position %s", position)
                # map the region
                new_region = map_region(grid, position)
                # append new_region to regions
                regions.append(new_region)
                # update already_seen with region, so we can skip them
                already_seen.update(new_region)
                # This commented section was to update the individual regions
                # to different characters to see how they were mapped
                # for position in new_region:
                #    grid[position[0]][position[1]] = chr(counter + 32)
                # counter += 1
    # return the count of regions
    logger.debug("regions found: %s", regions)
    return len(regions)


def print_grid(grid, text="Grid"):
    """
    Function to print grid
    """
    # label
    print(f"{text}:")
    # walk rows
    for row in grid:
        # print row
        print("".join(row))
    # new line
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

SUBMIT = False

if len(sys.argv) > 1 and sys.argv[1].lower() == "submit":
    SUBMIT = True

if __name__ == "__main__":
    aoc = AdventOfCode(year=YEAR, day=DAY, input_formats=input_format, funcs=funcs)
    aoc.run(submit=SUBMIT)
