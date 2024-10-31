"""
Advent Of Code 2020 day 18

Part 1 was smooth.  Part 2, I had a small hitch in string replacements, noted below.

"""
# import system modules
import time
import re
import operator

# import my modules
import aoc # pylint: disable=import-error

pattern_group = re.compile(r'\(([^\(\)]*)\)')
pattern_addition = re.compile(r'(\d+ \+ \d+)')
pattern_digits = re.compile(r'\d+')

def simplify_addition(exp_string, part):
    """
    Function to simplify addition strings
    """
    # print(f"simplify_addition({exp_string}, {part})")
    matches = pattern_addition.fullmatch(exp_string)
    if matches:
        digits = pattern_digits.findall(exp_string)
        exp_string = str(sum((int(digit) for digit in digits)))
    else:
        matches = pattern_addition.findall(exp_string)
        if matches:
            for match in matches:
                # print(f"match: {match}")
                replacement = simplify_expression(match, part)
                # print(f"replacement: {replacement}")
                exp_string = exp_string.replace(f"{match}", replacement)
                # print(f"exp_string: {exp_string}")
                # break here to only process one.
                # when processing all, there is one case in my input file
                # that causes a condition where the string replace fails
                # simplify_addition(8 + 9 + 7 + 7, 2, 2)
                # match: 8 + 9
                # simplify_expression(8 + 9, 2)
                # simplify_addition(8 + 9, 2)
                # replacement: 17
                # exp_string: 17 + 7 + 7, 2
                # match: 7 + 7
                # simplify_expression(7 + 7, 2)
                # simplify_addition(7 + 7, 2)
                # replacement: 14
                # exp_string: 114 + 7, 2     <---- bad juju
                break
    return exp_string

def replace_parentheses(exp_string, part=1):
    """
    Function to simplify parehthese statements"""
    # print(f"replace_parentheses({exp_string}, {part})")
    while '(' in exp_string:
        matches = pattern_group.findall(exp_string)
        if matches:
            for match in matches:
                exp_string = exp_string.replace(f"({match})", simplify_expression(match, part))
    return exp_string

def simplify_expression(exp_string, part=1):
    """
    Function to simplify expression string
    """
    # print(f"simplify_expression({exp_string}, {part})")
    while '+' in exp_string or '*' in exp_string:
        exp_string = replace_parentheses(exp_string, part)
        if part == 2 and '+' in exp_string:
            exp_string = simplify_addition(exp_string, part)
            continue
        total = 0
        operand=''
        operators = {
            '+': operator.iadd,
            '*': operator.imul
        }
        oper = None
        char = None
        for char in exp_string:
            # print(f"char: {char}, total: {total}, operand: {operand}, oper {oper}")
            if char.isdigit():
                operand += char
            elif char in operators:
                if total == 0:
                    total = int(operand)
                else:
                    total = operators[oper](total, int(operand))
                oper = char
                operand=''
            elif char == ' ':
                pass
            else:
                pass
        if oper in operators:
            if total == 0:
                total = int(operand)
            else:
                # print(f"test: {total}{oper}{operand}={operators[oper](total, int(operand))}")
                total = operators[oper](total, int(operand))
                oper = char
        exp_string = str(total)
    return exp_string

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    total = 0
    for expression in input_value:
        # if part == 2:
        #     print(f"{expression} = {simplify_expression(expression, part)}")
        total += int(simplify_expression(expression, part))
    # part 2 attempts
    # 1: 201376568795611 too high
    # 2: 201376568795521
    return total

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020,18)
    input_lines = my_aoc.load_lines()
    # parts dict to looper
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
        1: 29839238838303,
        2: 201376568795521
    }
    # dict to map functions
    funcs = {
        1: solve,
        2: solve
    }
    # looper parts
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
