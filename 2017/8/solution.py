"""
Advent Of Code 2017 day 8

This one was pretty straight forward.  I had to research the conditional operators.
When I found my answer it looked really familiar, so I think I may have used this
method before.

"""

# import system modules
import time
import re
import operator

# import my modules
import aoc  # pylint: disable=import-error

# dict to store answers
answer = {1: None, 2: None}

# Dictionary mapping conditionals to functions
conditional_operators = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
    # Add more operators as needed
}

# define global registers, no values yet, we will discover the registers
# as we parse the input
registers = {}


def check_value(value):
    """
    Function to convert numbers to ints, or set registers for variables
    """
    # try convertint to int first
    try:
        return int(value)
    except ValueError:
        # failing that set the register and return the string
        registers[value] = 0
        return value


def parse_instructions(instructions):
    """
    Function to parse instructions
    """
    # init commands
    commands = []
    input_pattern = re.compile(r"(\w+) (\w{3}) (\S+) if (\S+) (\S+) (\S+)")
    # walk instructions
    for instruction in instructions:
        # regex match?
        match = input_pattern.match(instruction)
        if match:
            # init command
            command = {"condition": {}}
            # populate command values
            command["register"] = match.group(1)
            registers[command["register"]] = 0
            command["action"] = match.group(2)
            command["value"] = check_value(match.group(3))
            command["condition"]["v_1"] = check_value(match.group(4))
            command["condition"]["conditional"] = match.group(5)
            command["condition"]["v_2"] = check_value(match.group(6))
            # add to commands
            commands.append(command)
    return commands


def execute_instruction(instruction):
    """
    Function to execute instructions
    """
    # if decrement
    if instruction["action"] == "dec":
        # we can handle register vs int with resiters.get()
        registers[instruction["register"]] -= registers.get(
            instruction["value"], instruction["value"]
        )
    else:  # increment
        registers[instruction["register"]] += registers.get(
            instruction["value"], instruction["value"]
        )


def evaluate_condition(condition):
    """
    Function to evaluate conditions
    """
    # get variables, check to see if they are registers, if not get their values
    # Check if the conditional operator is valid
    if condition["conditional"] in conditional_operators:
        # return condition, again handle register vs value with registers.get()
        return conditional_operators[condition["conditional"]](
            registers.get(condition["v_1"], condition["v_1"]),
            registers.get(condition["v_2"], condition["v_2"]),
        )
    # This shouldn't be possible, and I didn't fully read the input, so account
    # for it anyway.
    raise ValueError(f"Unknown conditional operator: {condition['conditional']}")


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # if part 2, we have already done the calculations
    # this way we don't have to execute twice.
    if part == 2:
        return answer[2]
    # init max_value for part 2
    max_value = 0
    # parse input
    program = parse_instructions(input_value)
    # run program instructions
    for code in program:
        # if condition is true
        if evaluate_condition(code["condition"]):
            # increment or decrement
            execute_instruction(code)
            # check max value, and update if needed
            max_value = max(max_value, *registers.values())
    # for part 2, just store the value for now:
    answer[2] = max_value
    # if part 1, return current max register value
    return max(registers.values())


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017, 8)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
