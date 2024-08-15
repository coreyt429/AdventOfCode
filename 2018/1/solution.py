"""
Advent Of Code 2018 day 1

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # Starting with a frequency of zero
    frequency = 0
    if part == 1:
        # what is the resulting frequency after all of the changes in frequency have been applied?
        for change in input_value:
            frequency +=  change
        return frequency
    # part 2:
    # What is the first frequency your device reaches twice?
    # set to track history
    already_seen = set([frequency])
    # Note that your device might need to repeat its list of frequency changes many times before a
    # duplicate frequency is found
    while True:
        # run changes
        for change in input_value:
            # add change to frequency
            frequency +=  change
            # have we seen this frequency?
            if frequency in already_seen:
                # return it
                return frequency
            # add to already seen
            already_seen.add(frequency)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018,1)
    #input_text = my_aoc.load_text()
    #print(input_text)
    input_lines = my_aoc.load_integers()
    #print(input_lines)
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
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
