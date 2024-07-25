"""
Advent Of Code YEAR day DAY

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    return part

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(YEAR,DAY)
    #input_text = my_aoc.load_text()
    #print(input_text)
    input_lines = my_aoc.load_lines()
    print(input_lines)
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
    for part in parts:
        # log start time
        start = time.time()
        # get answer
        answer[part] = funcs[part](input_lines, part)
        # log end time
        end = time.time()
        # print results
        print(f"Part {part}: {answer[part]}, took {end-start} seconds")