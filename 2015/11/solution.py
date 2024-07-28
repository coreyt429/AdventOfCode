"""
Advent Of Code 2015 day 11

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def next_char(char):
    """
    Function to get next character
    """
    # get int vslue of char
    int_char = ord(char)
    # increment by 1
    int_char += 1
    # loop around if past last valid character
    if int_char > 122:
        int_char = 97
    # increment if banned letter
    if int_char in [105, 108, 111]: # banned letters i, l, and o
        int_char += 1
    # return new character
    return chr(int_char)

def next_password(input_string):
    """
    Function to calculate next password
    """
    # convert to list
    password = list(input_string)
    # walk list backwards
    for idx in range(len(password)-1, 0, -1):
        # replace current character with net character
        password[idx] = next_char(password[idx])
        # break if not 'a' (only increment up to the
        # least significant position that needs to increment
        if password[idx] != 'a':
            break
    # return joined list
    return ''.join(password)

def three_consecutive(ints):
    """
    Function to test for three consecutive incrementing chars
    Passwords must include one increasing straight of at least three letters,
    like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.
    """
    # walk first n-2 characters
    for idx in range(len(ints) - 2):
        # if idx, idx+1, and idx2 are consecutive
        if ints[idx + 1] == ints[idx] + 1 and ints[idx + 2] == ints[idx + 1] + 1:
            return True
    return False

def two_matched_pairs(ints):
    """
    Function to test for two matched pairs
    Passwords must contain at least two different, non-overlapping pairs of letters,
    like aa, bb, or zz.
    """
    # two matched pairs
    # reset to False
    pairs = set()
    for idx in range(len(ints) - 1):
        if ints[idx + 1] == ints[idx]:
            pair = (ints[idx], ints[idx + 1])
            if not pair in pairs:
                pairs.add(pair)
                if len(pairs) == 2:
                    return True
    return False

def is_valid(password):
    """
    Function to check a passwords validty
    """
    # get int values for chars in password
    ints = [ord(char) for char in password]

    # 3 consecutive letters
    if not three_consecutive(ints):
        return False

    # 2 matched pairs
    if not two_matched_pairs(ints):
        return False

    # banned letters i, o, l
    # Passwords may not contain the letters i, o, or l, as these letters can be mistaken
    # for other characters and are therefore confusing.
    if any(char in password for char in ['i', 'o', 'l']):
        return False
    return True

def solve(password):
    """
    Function to solve puzzle
    """
    # get next password
    password = next_password(password)
    # if not valid, loop until valid
    while not is_valid(password):
        password = next_password(password)
    # return password
    return password

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015,11)
    input_text = my_aoc.load_text()
    #print(input_text)
    # parts dict to loop
    parts = {
        1: 1,
        2: 2
    }
    # dict to store answers
    # set to input_text so part 1 runs on the input,
    # part 2 will them run on the password from part1
    answer = {
        1: input_text, # set to input_text so part 1 runs on the input
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
        answer[my_part] = funcs[my_part](answer[1])
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
