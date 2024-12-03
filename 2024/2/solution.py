"""
Advent Of Code 2024 day 2

A bit of simple iteration and recursion makes part 2 work.

This technique runs in 0.01 seconds, so not really looking for a faster method.

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def parse_data(lines):
    """Function to parse input data"""
    reports = []
    for line in lines:
        report = [int(num) for num in line.split(' ')]
        reports.append(tuple(report))
    return tuple(reports)

def dampen_report(report, dampener):
    """Function to dampen reports: Part 2"""
    # part 1?  just return false
    if dampener == 1:
        return False
    # iterate over indexes
    for idx in range(len(report)):
        my_list = list(report)
        # remove current index
        my_list.pop(idx)
        # check is_safe without dampener on the revised report
        if is_safe(tuple(my_list), dampener -1):
            return True
    return False

def is_safe(report, dampener=1):
    """Function to determine if a report is safe"""
    safe = True
    # The levels are either all increasing or all decreasing.
    if report not in [tuple(sorted(report)), tuple(reversed(sorted(report)))]:
        return dampen_report(report, dampener)
    # Any two adjacent levels differ by at least one and at most three
    for idx, num in enumerate(report[:-1]):
        if report[idx + 1] == num:
            return dampen_report(report, dampener)
        if not -4 < report[idx + 1] - num < 4:
            return dampen_report(report, dampener)
    return safe

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    reports = parse_data(input_value)
    counter = 0
    # same logic here for both parts.
    # pass part as dampener to get different behavior
    for report in reports:
        if is_safe(report, part):
            counter += 1
    return counter

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2024,2)
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
        1: 220,
        2: 296
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
