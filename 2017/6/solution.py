"""
Advent Of Code 2017 day 6

"""
# import system modules
import time
import re

# import my modules
import aoc # pylint: disable=import-error

def redistribute(num_tuple):
    """
    Function to redistribute blocks
    """
    # convert to list
    num_list = list(num_tuple)
    # store list length
    num_list_len = len(num_list)
    # store max calue
    max_val = max(num_list)
    # store index of first max value
    idx = num_list.index(max_val)
    # move max_val from first max block to move_blocks
    move_blocks = max_val
    num_list[idx] = 0
    # while blocks remain to move
    while move_blocks:
        # increment idx
        idx += 1
        # roll over if idx is invalid
        if idx >- num_list_len:
            idx = idx % num_list_len
        # move block from move_blocks to num_list[idx]
        num_list[idx] += 1
        move_blocks -= 1
    return tuple(num_list)

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # conver input text to tuple of ints
    start_tuple = tuple(int(num) for num in re.findall(r'(\d+)', input_value))
    # counter to count steps
    counter = 0
    # set of states already seen
    seen = set()
    # current tuple to evaluate
    current_tuple = start_tuple
    # loop counter
    loop_count = 0
    # store first loop tuple, init to None
    loop_tuple = None
    # infinite loop
    while True:
        # if we have already seen this tuple
        if current_tuple in seen:
            # if part 1, we are done, return counter
            if part == 1:
                return counter
            # part 2, and we haven't identified the loop tuple
            if not loop_tuple:
                # set loop_tuple
                loop_tuple = current_tuple
                # store count to get here the first time
                last_counter = counter
        # if part 2, and we are at the loop tuple
        if part == 2 and current_tuple == loop_tuple:
            # increment loop_count, first time goes from 0 to 1
            loop_count += 1
            # if it's not the first time though
            if loop_count > 1:
                # return the difference between this counter and the first instance
                return counter - last_counter
        # add to seen
        seen.add(current_tuple)
        # redistribute to get next state
        current_tuple = redistribute(current_tuple)
        # increment counter
        counter += 1
        # end of loop

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017,6)
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
