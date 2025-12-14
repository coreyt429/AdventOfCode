"""
Advent Of Code 2020 day 8

This one was fun.  Based on previous years experience, my assumption
is we will see this code again.  So I made it a class I can move to
another module when we do.

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


class GameConsole:
    """Class to represent a handheld game console"""

    def __init__(self, program):
        """init method"""
        self.program = self.load_program(program)
        self.ptr = 0
        self.accumulator = 0
        self.function_map = {"nop": self.nop, "acc": self.acc, "jmp": self.jmp}

    def load_program(self, program):
        """method to load program instructions"""
        self.program = []
        # convert to list if string
        if isinstance(program, str):
            program = program.splitlines()
        for line in program:
            instruction, value = line.split(" ")
            self.program.append({"instruction": instruction, "value": int(value)})
        return self.program

    def nop(self, value):
        """nop: no op method"""
        isinstance(value, int)
        self.ptr += 1

    def acc(self, value):
        """acc: accumulator method"""
        self.accumulator += value
        self.ptr += 1

    def jmp(self, value):
        """jmp: jump method"""
        self.ptr += value

    def step(self):
        """method to execute a program step"""
        instruction = self.program[self.ptr]["instruction"]
        value = self.program[self.ptr]["value"]
        self.function_map[instruction](value)


def test_loop(program):
    """Function to test a program for infinite loops"""
    hgc = GameConsole(program)
    seen = set()
    # the program terminates by attempting to run the instruction below
    # the last instruction in the file.
    while 0 <= hgc.ptr < len(hgc.program):
        # print(f"{hgc.ptr} {hgc.accumulator}")
        if hgc.ptr in seen:
            return False
        seen.add(hgc.ptr)
        hgc.step()
    # print("Program exited")
    # What is the value of the accumulator after the program terminates?
    return hgc.accumulator


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        hgc = GameConsole(input_value)
        seen = set()
        while True:
            # Immediately before any instruction is executed a second time,
            if hgc.ptr in seen:
                # what value is in the accumulator?
                return hgc.accumulator
            seen.add(hgc.ptr)
            hgc.step()
    # part 2
    for idx, line in enumerate(input_value):
        # No acc instructions were harmed in the corruption of this boot code.
        if "acc" in line:
            continue
        test_program = list(input_value)
        # By changing exactly one jmp or nop, you can repair the boot code and
        # make it terminate correctly.
        if "nop" in line:
            test_program[idx] = test_program[idx].replace("nop", "jmp")
        else:
            test_program[idx] = test_program[idx].replace("jmp", "nop")
        result = test_loop(test_program)
        if result:
            # What is the value of the accumulator after the program terminates?
            return result
    # this shouldn't be possible, but needed to make pylint happy
    return part


YEAR = 2020
DAY = 8
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
