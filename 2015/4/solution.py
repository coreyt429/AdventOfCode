"""
Advent Of Code 2015 day 4

"""

# import system modules
import time
import hashlib
import re

# import my modules
import aoc  # pylint: disable=import-error


def part1(my_key):
    """
    Function to solve part1
    """
    my_num = 0
    # Create an MD5 hash object
    hash_object = hashlib.md5()
    hex_md5 = ""
    while not re.match("^00000", hex_md5):
        my_num += 1
        # Create a new MD5 hash object for each iteration
        hash_object = hashlib.md5()
        hash_object.update(f"{my_key}{my_num}".encode())
        hex_md5 = hash_object.hexdigest()
    return my_num


def part2(my_key):
    """
    Function to solve part 2
    """
    my_num = 0
    # Create an MD5 hash object
    hash_object = hashlib.md5()
    hex_md5 = ""
    while not re.match("^000000", hex_md5):
        my_num += 1
        # Create a new MD5 hash object for each iteration
        hash_object = hashlib.md5()
        hash_object.update(f"{my_key}{my_num}".encode())
        hex_md5 = hash_object.hexdigest()
    return my_num


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015, 4)
    input_text = my_aoc.load_text()
    print(input_text)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # dict to map functions
    funcs = {1: part1, 2: part2}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_text)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
