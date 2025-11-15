"""
Advent Of Code 2015 day 23

This one was already really fast, I just needed to clean it up.

I still think it is ugly, and I like my 2016 assembunny solutions better.
I just don't feel like refactoring this one that much right now.

"""

# import system modules
import time
import re

# import my modules
import aoc  # pylint: disable=import-error

PATTERN_INSTRUCTION = re.compile(
    r"(jmp|jio|inc|tpl|jie|hlf) *([ab])?(?:, )?([\+-]?\d+)?"
)
PATTERN_JUMP_VALUE = re.compile(r"([+-])(\d+)")
REGISTERS = {"a": 0, "b": 0}

INSTRUCTIONS = ["hlf", "tpl", "inc", "jmp", "jie", "jio"]
PROGRAM = []

def parse_input(lines):
    """
    Function to read filename and parse the program instructions

    parameters:
        file_name: string name of file to load

    returns:
        program: list of dict, program instructions
    """
    # init program
    program = []
    # walk lines
    for line in lines:
        # regex match
        matches = PATTERN_INSTRUCTION.match(line)
        if matches:
            # get instruction
            instruction = matches.group(1)
            if instruction in ["hlf", "tpl", "inc"]:
                register = matches.group(2)
                program.append({"instruction": instruction, "register": register})
            elif instruction in ["jio", "jie"]:
                register = matches.group(2)
                value = matches.group(3)
                matches2 = PATTERN_JUMP_VALUE.match(value)
                program.append(
                    {
                        "instruction": instruction,
                        "register": register,
                        "direction": matches2.group(1),
                        "value": int(matches2.group(2)),
                    }
                )
            elif instruction in ["jmp"]:
                value = matches.group(3)
                matches2 = PATTERN_JUMP_VALUE.match(value)
                program.append(
                    {
                        "instruction": instruction,
                        "direction": matches2.group(1),
                        "value": int(matches2.group(2)),
                    }
                )
            else:
                print(f"unkown instruction in: {line}")
        else:
            print(f"unkown instruction in: {line}")

    return program


def do_inc(register):
    """
    INC instruction
    """
    REGISTERS[register] += 1


def do_tpl(register):
    """
    TPL instruction
    """
    REGISTERS[register] *= 3


def do_hlf(register):
    """
    HLF instruction
    """
    REGISTERS[register] = int(REGISTERS[register] / 2)


def run_progam():
    """
    Executes the program instructions in PROGRAM
    """
    pointer = 0
    func_map = {"inc": do_inc, "tpl": do_tpl, "hlf": do_hlf}
    while 0 <= pointer < len(PROGRAM):
        current_line = PROGRAM[pointer]
        if current_line["instruction"] in ["inc", "tpl", "hlf"]:
            func_map[current_line["instruction"]](current_line["register"])
        elif current_line["instruction"] == "jmp":
            direction = 1
            if current_line["direction"] == "-":
                direction = -1
            pointer += current_line["value"] * direction
            continue
        elif current_line["instruction"] == "jie":
            if REGISTERS[current_line["register"]] % 2 == 0:
                direction = 1
                if current_line["direction"] == "-":
                    direction = -1
                pointer += current_line["value"] * direction
                continue
        elif current_line["instruction"] == "jio":
            if REGISTERS[current_line["register"]] == 1:
                direction = 1
                if current_line["direction"] == "-":
                    direction = -1
                pointer += current_line["value"] * direction
                continue
        pointer += 1


def solve(part):
    """
    Function to solve puzzle
    """
    if part == 1:
        run_progam()
        return REGISTERS["b"]
    REGISTERS["a"] = 1
    REGISTERS["b"] = 0
    run_progam()
    return REGISTERS["b"]


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015, 23)
    # input_text = my_aoc.load_text()
    # print(input_text)
    input_lines = my_aoc.load_lines()
    PROGRAM.clear()
    PROGRAM.extend(parse_input(input_lines))
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
