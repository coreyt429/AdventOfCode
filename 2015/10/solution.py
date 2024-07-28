"""
Advent Of Code 2015 day 10

Part1: 252594
Part2: 3579328

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def look_and_say_mine(sequence):
    """
    Function to perform look and say conversion
    """
    result = ''
    current_digit = sequence[0]
    count = 1

    for digit in sequence[1:]:
        if digit == current_digit:
            count += 1
        else:
            result += str(count) + current_digit
            current_digit = digit
            count = 1
    result += str(count)+current_digit
    return result

def look_and_say(sequence):
    """
    Function to perform look and say conversion
    After completing this, I ran my solution through claude.ai for performance suggestions
    storing result as a list rather than string, shaved 1 second off of part 2
    """
    result = []
    current_digit = sequence[0]
    count = 1

    for digit in sequence[1:]:
        if digit == current_digit:
            count += 1
        else:
            result.extend([str(count), current_digit])
            current_digit = digit
            count = 1

    result.extend([str(count), current_digit])
    return ''.join(result)

def solve(input_string, num_iters):
    """
    Function to solve puzzle
    """
    new_string = input_string
    for _ in range(num_iters):
        new_string = look_and_say(new_string)
    return len(new_string)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015,10)
    INPUT_TEXT = '1113222113'
    # parts dict to loop
    parts = {
        1: 40,
        2: 50
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
    for my_part, start_string in parts.items():
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](INPUT_TEXT, start_string)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
