"""
Advent Of Code 2015 day 8

"""
# import system modules
import time
import re


# import my modules
import aoc # pylint: disable=import-error

def part1(parsed_data):
    """
    Function to dolve part 1
    """
    re_hex=r'(\\x[0-9a-f]{2})'
    retval = 0
    sum1 = 0
    sum2 = 0
    for line in parsed_data:
        size1 = len(line)
        line2 = line.replace('\\\\', '#')
        line2 = line2.replace(r'\"', '#')
        line2 = line2.replace('"','')
        sum1+=size1
        line2 = re.sub(re_hex,'#',line2)
        whitespace_chars = " \t\n\r"  # Space, tab, newline, carriage return
        for char in whitespace_chars:
            line2 = line2.replace(char, "")
        size2 = len(line2)
        sum2 += size2
    retval = sum1 - sum2
    return retval

def part2(parsed_data):
    """
    Function to solve part 2
    """
    re_hex=r'(\\x[0-9a-f]{2})'
    retval = 0
    sum1 = 0
    sum2 = 0
    for line in parsed_data:
        size1 = len(line)
        line2 = line.replace('\\\\', '#')
        line2 = line2.replace('\"', '%')
        line2 = line2.replace('"','\\"')
        line2 = line2.replace('#','\\\\\\\\')
        line2 = line2.replace('%','"\\"')
        sum1+=size1
        line2 = re.sub(re_hex,"\\\\\\\\xNN",line2)
        whitespace_chars = " \t\n\r"  # Space, tab, newline, carriage return
        for char in whitespace_chars:
            line2 = line2.replace(char, "")
        size2 = len(line2)
        sum2 += size2
    retval = sum2 - sum1
    return retval

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015,8)
    #input_text = my_aoc.load_text()
    #print(input_text)
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
        1: part1,
        2: part2
    }
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_lines)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
