"""
Advent Of Code 2015 day 23

This one was already really fast, I just needed to clean it up.

I still think it is ugly, and I like my 2016 assembunny solutions better.
I just don't feel like refactoring this one that much right now.

"""

# import system modules
import logging
import argparse
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

PATTERN_INSTRUCTION = re.compile(
    r"(jmp|jio|inc|tpl|jie|hlf) *([ab])?(?:, )?([\+-]?\d+)?"
)
PATTERN_JUMP_VALUE = re.compile(r"([+-])(\d+)")
REGISTERS = {"a": 0, "b": 0}

INSTRUCTIONS = ["hlf", "tpl", "inc", "jmp", "jie", "jio"]
PROGRAM = []


def parse_input(input_text):
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
    for line in input_text.strip().splitlines():
        if not line:
            continue
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


def solve(program, part):
    """
    Function to solve puzzle
    """
    PROGRAM.clear()
    PROGRAM.extend(program)
    if part == 1:
        REGISTERS["a"] = 0
    else:
        REGISTERS["a"] = 1
    REGISTERS["b"] = 0
    run_progam()
    return REGISTERS["b"]


YEAR = 2015
DAY = 23
input_format = {
    1: parse_input,
    2: parse_input,
}

funcs = {
    1: solve,
    2: solve,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    aoc = AdventOfCode(
        year=YEAR,
        day=DAY,
        input_formats=input_format,
        funcs=funcs,
        test_mode=args.test,
    )
    aoc.run(submit=args.submit)
