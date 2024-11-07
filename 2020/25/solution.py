"""
Advent Of Code 2020 day 25

Nice easy finish for the year.

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def transform(value, subject_number=7):
    """function to transform a number"""
    # Set the value to itself multiplied by the subject number.
    value *= subject_number
    # Set the value to the remainder after dividing the value by 20201227.
    return value % 20201227

def transform_loop(value, loops, subject_number=7):
    """function to transform in a loop"""
    for _ in range(loops):
        value = transform(value, subject_number)
    return value

def find_loop(target):
    """function to find loopsize for a public key"""
    value = 1
    counter = 0
    while value != target:
        value = transform(value)
        counter += 1
    return counter

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return "Pay the Deposit"
    public_keys = {
        'door': int(input_value.pop(0)),
        'card': int(input_value.pop(0))
    }
    loop_size = {}
    for key, public_key in public_keys.items():
        loop_size[key] = find_loop(public_key)
    encryption_key = {
        'door': transform_loop(1, loop_size['door'], public_keys['card']),
        'card': transform_loop(1, loop_size['card'], public_keys['door'])
    }
    return encryption_key['door']

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020,25)
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
    # correct answers once solved, to validate changes
    correct = {
        1: 11328376,
        2: "Pay the Deposit"
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
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
