"""
Advent Of Code 2019 day 2

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def parse_input(in_text):
    """parse inpute data"""
    return [int(num) for num in in_text.split(',')]

def execute_program(intcode):
    """execute intcode"""
    operations = {
        1: lambda a, b : a + b,
        2: lambda a, b : a * b
    }
    ptr = 0
    while intcode[ptr] != 99:
        op_code = intcode[ptr]
        if op_code not in operations:
            print(f"Error at {ptr}")
            break
        num_a = intcode[intcode[ptr + 1]]
        num_b = intcode[intcode[ptr + 2]]
        target = intcode[ptr + 3]
        intcode[target] = operations[op_code](num_a, num_b)
        ptr += 4
        if ptr >= len(intcode):
            print(f"OOB Error at  {ptr} > {len(intcode)}")
    return intcode

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        target = 19690720
        for noun in range (100):
            for verb in range(100):
                program = parse_input(input_value)
                program[1] = noun
                program[2] = verb
                result = execute_program(program)
                if result[0] == target:
                    return 100 * noun + verb
    program = parse_input(input_value)
    program[1] = 12
    program[2] = 2
    result = execute_program(program)
    return result[0]

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019,2)
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
