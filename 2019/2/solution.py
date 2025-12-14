"""
Advent Of Code 2019 day 2

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


def parse_input(in_text):
    """parse inpute data"""
    return [int(num) for num in in_text.strip().split(",")]


def execute_program(intcode):
    """execute intcode"""
    operations = {1: lambda a, b: a + b, 2: lambda a, b: a * b}
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
    base_program = input_value[:]
    if part == 2:
        target = 19690720
        for noun in range(100):
            for verb in range(100):
                program = base_program[:]
                program[1] = noun
                program[2] = verb
                result = execute_program(program)
                if result[0] == target:
                    return 100 * noun + verb
    program = base_program[:]
    program[1] = 12
    program[2] = 2
    result = execute_program(program)
    return result[0]


YEAR = 2019
DAY = 2
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
