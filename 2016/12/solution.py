"""
Advent Of Code 2016 12

This was reminiscent of 2015 day 23, so I was able to borrow some code there.

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

instructions = []
instructions.append("inc")
instructions.append("dec")
instructions.append("cpy")
instructions.append("jnz")

pattern_instruction = re.compile(r"(\w+) (\S+) *(\S+)?")
pattern_jump_value = re.compile(r"([+-])?(\d+)")


def decode_program(lines):
    """
    Function to parse text block the program instructions

    parameters:
        lines: list of strings

    returns:
        program: list of dict, program instructions
    """
    program = []

    # process each line
    for line in lines:
        # instruction regex r'(\w+) (\S+) *(\S+)?'
        matches = pattern_instruction.match(line)
        if matches:
            instruction = matches.group(1)
            # simple instructions inc, and dec,
            #   just store instruction and register
            if instruction in ["inc", "dec"]:
                register = matches.group(2)
                program.append({"instruction": instruction, "register": register})
            # copy is more comples, source can be an int or register
            elif instruction in ["cpy"]:
                source = matches.group(2)
                # is it a number, if so convert to int?
                if source.isdigit():
                    source = int(source)
                # target should be a register
                register = matches.group(3)
                program.append(
                    {"instruction": instruction, "source": source, "register": register}
                )
            # jnz, also uses int or register
            elif instruction in ["jnz"]:
                val_x = matches.group(2)
                # int? convert it
                if val_x.isdigit():
                    val_x = int(val_x)
                # split val_y with jump regex r'([+-])?(\d+)'
                val_y = matches.group(3)
                matches2 = pattern_jump_value.match(val_y)
                direction = matches2.group(1) or "+"
                val_y = int(matches2.group(2))
                # if direction is - convert val_y to negative
                if direction == "-":
                    val_y *= -1
                program.append({"instruction": instruction, "x": val_x, "y": val_y})
    return program


def run_program(program, registers):
    """
    Executes the program instructions in PROGRAM
    """
    # pointer for current program location
    pointer = 0
    # while pointer is valid, keep processing
    while 0 <= pointer < len(program):
        current_line = program[pointer]
        # increase by one, and move pointer +1
        if current_line["instruction"] == "inc":
            registers[current_line["register"]] += 1
            pointer += 1
        # decrease by 1 and move pointe +1
        elif current_line["instruction"] == "dec":
            registers[current_line["register"]] -= 1
            pointer += 1
        # copy source to target, and move pointer +1
        elif current_line["instruction"] == "cpy":
            # is int?
            if isinstance(current_line["source"], int):
                # yes, use source value
                registers[current_line["register"]] = current_line["source"]
            elif current_line["source"] in registers:
                # no, get register value
                registers[current_line["register"]] = registers[current_line["source"]]
            pointer += 1
        # jnz jumps value instructions if value is not 0
        elif current_line["instruction"] == "jnz":
            x_value = current_line["x"]
            # is int?
            if not isinstance(current_line["x"], int):
                # no, get value from register
                x_value = registers[current_line["x"]]
            # is zero?
            if x_value != 0:
                # No, jump
                pointer += current_line["y"]
            else:
                # Yes, move forward 1
                pointer += 1
    return registers


def solve(lines, part):
    """
    Function to solve puzzle
    """
    registers = {"a": 0, "b": 0, "c": 0, "d": 0}
    if part == 2:
        registers["c"] = 1

    # get program from text
    my_program = decode_program(lines)
    # execute program
    run_program(my_program, registers)
    return registers["a"]


YEAR = 2016
DAY = 12
input_format = {
    1: "lines",
    2: "lines",
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
