"""
Advent Of Code 2017 day 4

This one was fairly straight forward. I did trip up in version two, I didn't 
initially test to make sure I wasn't comparing the first passphrase to itself 
and ended up with 0.  I didn't think that would be the answer, and submitted it
anyway.  I was right.  Found the issue and added enumerates and an if statement
to compare indexes.

"""
# import system modules
import time
import re

# import my modules
import aoc # pylint: disable=import-error

# define pattern for reuse
pattern_words = re.compile(r'(\w+)')


def check_passphrase(input_string, version=1):
    """
    Function to check passphrases
    Args:
        passphrase:  string
        version: integer
    Returns:
        boolean: True means valid
    """
    # convert string to list
    pp_list = pattern_words.findall(input_string)
    # walk list to check each word in the pass phrase
    for idx, passphrase in enumerate(pp_list):
        # if a the word appears more than once, then the passphrase is invalid
        # for both versions 1 and 2.  aa is an anagram for aa.
        if pp_list.count(passphrase) > 1:
            return False
        # additional version 2 check
        if version == 2:
            # walk passphrases again
            for idx2, passphrase2 in enumerate(pp_list):
                # lets not compare passphrase to itself
                if idx == idx2:
                    continue
                # compare sorted passphrases
                if sorted(passphrase) == sorted(passphrase2):
                    return False
    return True

def solve(lines, part):
    """
    Function to solve puzzle
    """
    counter = 0
    for line in lines:
        if check_passphrase(line, part):
            counter += 1
    return counter

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017,4)
    input_lines = my_aoc.load_lines()
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
