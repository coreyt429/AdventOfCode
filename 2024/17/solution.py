"""
Advent Of Code 2024 day 17

Part 1 was easy once, I read all the instructions.
Part 2 was going to take forever, so I looked a couple of solutions,
and found one that I liked.  It didn't quite work for me, so I had to
adjust it a bit.

"""

# import system modules
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_input(input_text):
    """
    Function to parse the input text
    """
    input_text = input_text.split("\n")
    registers = {}
    for line in input_text:
        if line.startswith("Register"):
            line = line.split()
            registers[line[1][0]] = int(line[2])
        elif line.startswith("Program"):
            program = []
            for instr in line.split(": ")[1].split(","):
                program.append(*list(map(int, instr.split())))
    return registers, program


def combo_operand_value(operand, registers):
    """
    Function to get the value of a combo operand
    """
    if operand < 4:
        return operand
    if operand == 4:
        return registers["A"]
    if operand == 5:
        return registers["B"]
    if operand == 6:
        return registers["C"]
    return None


def run_program(input_text, register_a=None):
    """
    Function to run the program
    """
    registers, program = parse_input(input_text)
    if register_a is not None:
        registers["A"] = register_a
    ptr = 0
    outputs = []
    while ptr < len(program):
        instr = program[ptr : ptr + 2]
        literal_operand = instr[1]
        combo_operand = combo_operand_value(literal_operand, registers)
        if instr[0] == 0:
            registers["A"] = operations[0](registers["A"], combo_operand)
        elif instr[0] == 1:
            registers["B"] = operations[1](registers["B"], literal_operand, 0, 0)
        elif instr[0] == 2:
            registers["B"] = operations[2](registers["B"], 0, 0, combo_operand)
        elif instr[0] == 3:
            if registers["A"] != 0:
                ptr = literal_operand
                continue
        elif instr[0] == 4:
            registers["B"] = operations[4](registers["B"], registers["C"], 0, 0)
        elif instr[0] == 5:
            outputs.append(operations[5](0, 0, 0, combo_operand))
        elif instr[0] == 6:
            registers["B"] = operations[6](
                registers["A"], registers["B"], registers["C"], combo_operand
            )
        elif instr[0] == 7:
            registers["C"] = operations[7](
                registers["A"], registers["B"], registers["C"], combo_operand
            )
        ptr += 2
    return outputs


operations = {}
op_names = {}
operations[0] = lambda a, operand: a // (2**operand)
op_names[0] = "adv"
operations[1] = lambda b, operand, _, __: b ^ operand
op_names[1] = "bxl"
operations[2] = lambda b, _, __, operand: operand % 8
op_names[2] = "bst"
op_names[3] = "jnz"
operations[4] = lambda b, c, _, __: b ^ c
op_names[4] = "bxc"
operations[5] = lambda _, __, ___, operand: operand % 8
op_names[5] = "out"
operations[6] = lambda a, b, c, operand: a // (2**operand)
op_names[6] = "bdv"
operations[7] = lambda a, b, c, operand: a // (2**operand)
op_names[7] = "cdv"


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        return ",".join(map(str, run_program(input_value)))
    _, program = parse_input(input_value)
    result = ""
    register_a_attempt = 0
    while True:
        result = run_program(input_value, register_a_attempt)
        if len(result) > len(program):
            print(f"result: {result}, program: {program}")
            raise ValueError("The output is too long")

        if result == program:
            break

        last = register_a_attempt
        for i in range(len(result) - 1, -1, -1):
            if result[i] != program[i]:
                add = 8**i
                if add < 9:
                    add = 1
                register_a_attempt += add
                break
        if register_a_attempt == last:
            register_a_attempt += 1

    return register_a_attempt


YEAR = 2024
DAY = 17
input_format = {
    1: "text",
    2: "text",
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
