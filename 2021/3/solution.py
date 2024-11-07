"""
Advent Of Code 2021 day 3



"""
# import system modules
import time
from collections import Counter

# import my modules
import aoc # pylint: disable=import-error

def rotate_clockwise(matrix):
    """function to rotate a grid clockwise"""
    return [list(row) for row in zip(*matrix[::-1])]

def common_element(values, tie_breaker, mode='most'):
    """
    Function to return the most or least common element in a list with a tie breaker.
    
    Parameters:
        values (list): The input list.
        tie_breaker: The preferred element in case of a tie.
        mode (str): 'most' for most common, 'least' for least common.
    
    Returns:
        The most or least common element based on the mode.
    """
    # print(f"common_element(values, {tie_breaker}, {mode})")
    count = Counter(values)
    target_count = max(count.values()) if mode == 'most' else min(count.values())
    candidates = [item for item, cnt in count.items() if cnt == target_count]

    if tie_breaker in candidates:
        return tie_breaker
    return candidates[0]  # Default to the first candidate in case of a tie without tie_breaker

def most_common(values, tie_breaker=0):
    """Function to return the most common element in a list"""
    return common_element(values, tie_breaker, mode='most')

def least_common(values, tie_breaker=0):
    """Function to return the least common element in a list"""
    return common_element(values, tie_breaker, mode='least')

def parse_input(lines):
    """Function to parse input data"""
    report = []
    for line in lines:
        report.append(tuple((char for char in line)))
    return tuple(report)

def calc_gamma_rate(report):
    """Function to calculate gamma rate"""
    matrix = rotate_clockwise(report)
    result = ''
    for row in matrix:
        result += most_common(row)
    return int(result, 2)

def calc_epsilon_rate(report):
    """Function to calculate epsilon rate"""
    matrix = rotate_clockwise(report)
    result = ''
    for row in matrix:
        result += least_common(row)
    return int(result, 2)

def calc_power_consumption(report):
    """Function to calculate power consumption"""
    gamma_rate = calc_gamma_rate(report)
    epsilon_rate = calc_epsilon_rate(report)
    power_consumption = gamma_rate * epsilon_rate
    return power_consumption

def filter_report(report, mode, default_value):
    """
    Function to filter a report for least or most common values
    """
    func = {
        'most': most_common,
        'least': least_common
    }
    numbers = [list(line) for line in report]
    idx = 0
    while len(numbers) > 1:
        # matrix = rotate_clockwise(numbers)
        matching_numbers = []
        idx_nums = [num[idx] for num in numbers]
        # idx_nums = matrix[idx]
        match_char = func[mode](idx_nums, default_value)
        for num in numbers:
            if num[idx] == match_char:
                matching_numbers.append(num)
        numbers = matching_numbers
        if len(numbers) == 1:
            break
        idx += 1
        if idx > len(numbers[0]):
            return None
    return int(''.join(numbers[0]), 2)

def calc_oxygen_generator_rating(report):
    """
    Function to calculate oxygen generator rating
    """
    # To find oxygen generator rating, determine the most common value (0 or 1)
    # in the current bit position, and keep only numbers with that bit in that
    # position. If 0 and 1 are equally common, keep values with a 1 in the position
    # being considered.
    return filter_report(report, 'most', '1')

def calc_co2_scrubber_rating(report):
    """Function to calculate CO2 scrubber rating"""
    # To find CO2 scrubber rating, determine the least common value (0 or 1) in the
    # current bit position, and keep only numbers with that bit in that position.
    # If 0 and 1 are equally common, keep values with a 0 in the position being considered.
    return filter_report(report, 'least', '0')

def calc_life_support_rating(report):
    """
    Function to calculate life support rating:
        multiply the oxygen generator rating by the CO2 scrubber rating
    """
    return calc_oxygen_generator_rating(report) * calc_co2_scrubber_rating(report)

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    diagnostic_report = parse_input(input_value)
    if part == 1:
        return calc_power_consumption(diagnostic_report)
    return calc_life_support_rating(diagnostic_report)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021,3)
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
        1: 3895776,
        2: 7928162
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
