"""
Advent Of Code 2019 day 4

This one was pretty straight forward, not much to say.


"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def check_passcode(int_in, mode=1):
    """
    Function to check a passcode
    Args:
        int_in: int()
    Returns:
        bool()
    """
    # convert to string
    work_str = str(int_in)
    # init rool flags
    has_repeating_digit = False
    no_incrementing_values = True
    # get length
    length = len(work_str)
    # walk characters
    for idx, char in enumerate(work_str):
        # if not the last char
        if idx < length - 1:
            # if the next char is smaller
            if work_str[idx + 1] < char:
                # set flag
                no_incrementing_values = False
                # no need to test this num further
                break
            # if next char is the same
            if char == work_str[idx + 1]:
                # part 2
                if mode == 2:
                    # if the char after next matches, no go
                    if idx < length - 2 and char == work_str[idx + 2]:
                        continue
                    # if the previous character matches, no go
                    if idx > 0 and char == work_str[idx - 1]:
                        continue
                # set flag
                has_repeating_digit = True
    # return true if all conditions met
    return all([has_repeating_digit, no_incrementing_values])

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    start_num, end_num = [int(num) for num in input_value.split('-')]
    num = start_num
    passwords = []
    for num in range(start_num, end_num + 1):
        if check_passcode(num, part):
            passwords.append(num)
    return len(passwords)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019,4)
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
