"""
Advent Of Code 2020 day 14

Oddly, I struggled more on part 1 than part 2.  Though not much of a struggle.


# part 1 attempts
    # 1: 8873958978075 too low, wasn't updating the mask. repeat after me, "look at the input"
    # 2: 16817784741555 too high, wasn't trimming values to 36 bits. condition caused by 3
    # 3: 11139573408728 too high, continue was missing on mask condition
    # 4: 9967721333886, bingo
"""

# import system modules
import time
from collections import defaultdict
import re

# import my modules
import aoc  # pylint: disable=import-error


def mask_as_string(mask):
    """
    Function to convert mask back to string
    """
    mask_list = ["X"] * 36
    for idx, value in mask.items():
        mask_list[idx] = value
    return "".join([str(char) for char in mask_list])


def apply_mask(value, mask):
    """
    Function to apply bitmask to an int value
    """
    # print(f"apply_mask({value})")
    value_str = f"{value:036b}"
    # fix for attempt 2, which was caused by issue in attempt 3
    # while len(value_str) > 36:
    #     print(f"trimming {value_str}")
    #     value_str = value_str[1:]
    value_list = list(value_str)
    # print(f"value:   {value_str}  (decimal {value})")
    # print(f"mask:    {mask_as_string(mask)}")
    for idx, mask_value in mask.items():
        value_list[idx] = mask_value
    value_str = "".join([str(num) for num in value_list])
    # print(f"result:  {value_str}  (decimal {int(value_str, 2)})")
    return int(value_str, 2)


def build_mask(mask_str, version=1):
    """
    Funciton to build mask_dict from mask_str"""
    mask_dict = {}
    # convert mask_str to dict of replacement values
    for idx, value in enumerate(mask_str.split(" = ")[1]):
        if value != "X":
            mask_dict[idx] = int(value)
        elif version == 2:
            mask_dict[idx] = value
    return mask_dict


def mask_address(address, mask):
    """
    Function to mask addresses

    If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
    If the bitmask bit is X, the corresponding memory address bit is floating.
    """
    # print(f"mask_address({address}, {mask})")
    address_str = f"{address:036b}"
    # print(address_str)
    # print(f"address: {address_str}  (decimal {address})")
    # print(f"mask:    {mask_as_string(mask)}")
    address_list = list(address_str)
    addresses = [""]
    for idx, value in mask.items():
        # If the bitmask bit is 0, the corresponding memory address bit is unchanged.
        if value == 0:
            continue
        address_list[idx] = str(value)
    # print(f"result:  {''.join([str(val) for val in address_list])}")
    for value in address_list:
        # print(value)
        new_addresses = []
        for new_address in addresses:
            # print(new_address)
            if value == "X":
                new_addresses.append(new_address + "0")
                new_addresses.append(new_address + "1")
            else:
                new_addresses.append(new_address + value)
        addresses = new_addresses
    # for address_str in addresses:
    #     print(address_str)
    return [int(address_str, 2) for address_str in addresses]


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # The entire 36-bit address space begins initialized to the value 0 at every address.
    memory = defaultdict(int)
    # mask = build_mask(input_value[0])
    pattern_instruction = re.compile(r"(\d+)")
    for instruction in input_value:
        if "mask" in instruction:
            mask = build_mask(instruction, part)
            # hey, we shouldn't process any more from here, bad things happen
            continue
        matches = pattern_instruction.findall(instruction)
        address = int(matches.pop(0))
        value = int(matches.pop(0))
        if part == 1:
            memory[address] = apply_mask(value, mask)
            continue
        # part 2
        addresses = mask_address(address, mask)
        for address in addresses:
            memory[address] = value
    # for idx, value in memory.items():
    #     print(idx, value)
    return sum(memory.values())


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020, 14)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 9967721333886, 2: 4355897790573}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
