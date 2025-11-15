"""
Advent Of Code 2016 day 16
This one was pretty easy.  I worked it out in the jupyter notebook, then just cleaned it up here
"""

import time
import aoc  # pylint: disable=import-error


def dragon_curve(str_a):
    """
    Function to generate dragon curve of string
    """
    # str_b = str_a reveresed, with the '1's replaced with '2's
    str_b = str_a[::-1].replace("1", "2")
    # replace the '0's with '1's
    str_b = str_b.replace("0", "1")
    # replace the '2's with '0's
    str_b = str_b.replace("2", "0")
    # return concatenated string
    return f"{str_a}0{str_b}"


def checksum(input_string):
    """
    Function to generate checksum
    """
    my_checksum = ""
    # walk every other index of the string
    for idx in range(0, len(input_string), 2):
        # if idx matches idx+1
        if input_string[idx] == input_string[idx + 1]:
            my_checksum += "1"
        else:
            my_checksum += "0"
    # if length is odd, return
    if len(my_checksum) % 2 == 1:
        return my_checksum
    # return recursively until we get an odd checksum
    return checksum(my_checksum)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2016, 16)
    # load input string from aoc
    input_data = my_aoc.load_text()
    # target sizes
    size = {1: 272, 2: 35651584}
    for part in [1, 2]:
        start = time.time()
        # get initial dragon curve
        new_string = dragon_curve(input_data)
        while len(new_string) < size[part]:
            # keep regenerating until we reach target size
            new_string = dragon_curve(new_string)
        # truncate string to target size
        new_string = new_string[: size[part]]
        # get checksum
        new_string_checksum = checksum(new_string)
        end = time.time()
        print(f"Part {part}: {new_string_checksum}, took {end - start} seconds")
