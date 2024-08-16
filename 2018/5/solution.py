"""
Advent Of Code 2018 day 5

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def generate_pairs():
    """
    Function to generate unit pairs
    """
    # init new_pairs
    new_pairs = []
    # for range from A - Z
    for idx in range(65, 91):
        # add Aa and aA
        new_pairs.append(f"{chr(idx)}{chr(idx+32)}")
        new_pairs.append(f"{chr(idx+32)}{chr(idx)}")
    return new_pairs

def reduce_string(pairs, start_string):
    """
    Function to reduce polymer string
    """
    # init last_string and current_string
    last_string = ""
    current_string = start_string
    # loop until they are the same (no more reduction)
    while last_string != current_string:
        # update last_string
        last_string = current_string
        # loop pairs
        for pair in pairs:
            # remove from current_string
            current_string = current_string.replace(pair,"")
    # return final current_string
    return current_string

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # init pairs
    pairs = generate_pairs()
    # How many units remain after fully reacting the polymer you scanned?
    if part == 1:
        # reduce initial scanned string
        reduced_string = reduce_string(pairs, input_value)
        # return length (not the string like I did at first)
        return len(reduced_string)
    # part 2:
    # init min string to max size
    min_string = input_value
    # loop pairs
    for idx, pair in enumerate(pairs):
        # we only need to process every other pair
        # aA and Aa are the same for this
        if idx % 2 == 1:
            continue
        # copy input_string
        test_string = input_value
        # replace a and A
        test_string = test_string.replace(pair[0],'')
        test_string = test_string.replace(pair[1],'')
        # reduce the new string
        reduced_string = reduce_string(pairs, test_string)
        # if we have found a new shortest string, save it
        if len(reduced_string) < len(min_string):
            min_string = reduced_string
    # return length of shortest string
    return len(min_string)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018,5)
    input_text = my_aoc.load_text()
    #print(input_text)
    #input_lines = my_aoc.load_lines()
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
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
