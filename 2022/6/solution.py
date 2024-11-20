"""
Advent Of Code 2022 day 6

str() slicing and set() may have made this one too easy.
I was expecting part 2 to be trickier, but I just needed
to replace 4 with length in find_packet_start() and default
length to 4.  

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def find_packet_start(packet, length=4):
    """Function to find start marker in a packet"""
    for marker in range(length, len(packet) + 1):
        test = set(packet[marker - length:marker])
        if len(test) == length:
            return marker
    return None

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        return find_packet_start(input_value[0])
    return find_packet_start(input_value[0], 14)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2022,6)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
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
    # correct answers once solved, to validate changes
    correct = {
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
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
