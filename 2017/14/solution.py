"""
Advent Of Code 2017 day 14

"""
# import system modules
import time
from collections import deque
from functools import reduce
from heapq import heappop, heappush

# import my modules
import aoc # pylint: disable=import-error

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
    for idx in range(0,256,16):
        sparse_hashes.append(sparse_hash[idx:idx+16])
    # use bitwise XOR to create dense_hash values
    dense_hash = []
    for sparse_hash in sparse_hashes:
        dense_hash.append(reduce(lambda x, y: x ^ y, sparse_hash))
    # get hex values of dense_hash for hex hash
    my_hash = ''
    for num in dense_hash:
        my_hash += str(hex(num))[-2:].replace('x','0')
    # return hex hash
    return my_hash

def hex_to_bits(hex_string):
    """convert hex to bit string"""
    return ''.join(format(int(c, 16), '04b') for c in hex_string)

def map_region(grid, position):
    """
    Map a region based on a start string
    """
    # init region
    region = set()
    # init heap with start position
    heap = []
    heappush(heap, position)
    # process heap
    while heap:
        # get current
        current = heappop(heap)
        # already in region? next
        if current in region:
            continue
        # add to region
        region.add(current)
        # get n, e, s, and w neighbors (diagonals not allowed!)
        for neighbor in my_aoc.get_neighbors(grid, current, directions=['n','s','e','w']):
            # if neighbor is filled
            if grid[neighbor[0]][neighbor[1]] == '#':
                # add neighbor to heap
                heappush(heap, neighbor)
    # return region when all possibilities have been exhausted
    return region

def find_regions(grid):
    """
    Function to find regions
    """
    # init regions and already_seen
    regions = []
    already_seen = set()
    # counter was used as part of a visiual when I was getting a wrong answer
    # see note above to not include diagonals
    #counter = 0
    # walk rows
    for idx, row in enumerate(grid):
        # walk columns (chars)
        for idx2, char in enumerate(row):
            # if slot is filled
            if char == '#':
                # init position
                position = (idx, idx2)
                # if not already seen, lets check it out
                if not position in already_seen:
                    # map the region
                    new_region = map_region(grid, position)
                    # append new_region to regions
                    regions.append(new_region)
                    # update already_seen with region, so we can skip them
                    already_seen.update(new_region)
                    # This commented section was to update the individual regions
                    # to different characters to see how they were mapped
                    #for position in new_region:
                    #    grid[position[0]][position[1]] = chr(counter + 32)
                    #counter += 1
    # return the count of regions
    return len(regions)

def print_grid(grid, text='Grid'):
    """
    Function to print grid
    """
    # label
    print(f'{text}:')
    # walk rows
    for row in grid:
        # print row
        print(''.join(row))
    # new line
    print()

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # short circuit for part 2
    if part == 2:
        # we already calculated this in part 1
        return answer[2]
    total = 0
    drive = []
    for idx in range(128):
        data = hex_to_bits(knot_hash(f"{input_value}-{idx}"))
        data = data.replace('1', '#').replace('0', '.')
        total += data.count('#')
        drive.append(list(data))
    answer[2] = find_regions(drive)
    return total


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017,14)
    input_text = my_aoc.load_text()
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
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
