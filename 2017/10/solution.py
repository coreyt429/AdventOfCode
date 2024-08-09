"""
Advent Of Code 2017 day 10

This one was fun, and I learned a few things in python that I don't usually use.
Yeah, had to google a bit, ash chatGPT vague questions, and play in the scratchpad.

"""
# import system modules
import time
from collections import deque
from functools import reduce

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

def solve(input_value, part):
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
    if part == 1:
        # for part 1, we simply run hash_list once
        queue, skip, total_rotate = hash_list(
            [int(num) for num in input_value.split(',')], queue, skip, total_rotate
        )
        # rotate back
        queue.rotate(total_rotate)
        # return the product of the first two numbers
        return queue[0]*queue[1]
    # part 2, a few more steps here.
    # first, get the ord() values of the char()s in the input string + extra list
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

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017,10)
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
