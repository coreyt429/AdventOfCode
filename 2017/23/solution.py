"""
Advent Of Code 2017 day 23

Part 1 was easy, part 2, I was getting there trying to short circuit, and
ran out of time.  Looked at solutions, and implemented one.  I want to
revisit this at some point, and use that logic to fix my short circuits instead.

"""

# import system modules
from __future__ import annotations
import logging
import argparse
import sympy

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)


class Computer:
    """
    Class to represent a computer
    """

    def __init__(self, program=None, comp_id=0):
        """
        Initialize the coprocessor computer.

        Args:
            program (Iterable[str] | str | None): Assembly source.
            comp_id (int): Identifier used when counting ops in part 1.
        """
        self.comp_id = comp_id
        self.handlers = {
            "set": self.do_set,
            "sub": self.do_sub,
            "mul": self.do_mul,
            "jnz": self.do_jnz,
        }
        self.registers = {"pointer": 0}
        if self.comp_id == 1:
            for instruction in self.handlers:
                self.registers[instruction] = 0
        for register in "abcdefgh":
            self.registers[register] = 0
        self.program = []
        if program:
            self.load_program(program)

    def __str__(self):
        """String representation with register state for debugging."""
        my_string = f"{self.comp_id}: running {self.running()}, "
        my_string += f"registers: {self.registers}"
        return my_string

    def load_program(self, program):
        """
        Parse the textual program into instruction dictionaries.

        Args:
            program (Iterable[str] | str): Assembly instructions.
        """
        if isinstance(program, str):
            program = program.split("\n")
        self.program = []
        for line in program:
            inputs = line.split(" ")
            instruction = {"instruction": inputs[0]}
            try:
                instruction["x"] = int(inputs[1])
            except ValueError:
                instruction["x"] = inputs[1]
                self.registers[inputs[1]] = 0
            try:
                instruction["y"] = int(inputs[2])
            except ValueError:
                instruction["y"] = inputs[2]
                self.registers[inputs[2]] = 0
            except IndexError:
                pass
            self.program.append(instruction)

    def value(self, test_value):
        """
        Resolve a literal or register name to an integer value.
        """
        if isinstance(test_value, int):
            return test_value
        return self.registers[test_value]

    def running(self):
        """Return True while the instruction pointer is in bounds."""
        return 0 <= self.registers["pointer"] < len(self.program)

    def run_next_instruction(self):
        """Execute the next instruction and advance the pointer."""
        if self.running():
            current = self.program[self.registers["pointer"]]
            instruction = current["instruction"]
            if self.comp_id == 1:
                self.registers[instruction] += 1
            return self.handlers[instruction](current)
        return self.running()

    def run_program(self):
        """Run instructions until completion or a safeguard limit."""
        sentinel = 0
        while self.run_next_instruction():
            sentinel += 1
            if sentinel == 5_000_000:
                logger.warning("Breaking Loop")
                break
        return self.running()

    def do_sub(self, instruction):
        """Subtract operand from register."""
        self.registers[instruction["x"]] -= self.value(instruction["y"])
        self.registers["pointer"] += 1
        return True

    def do_set(self, instruction):
        """Set register to operand value."""
        self.registers[instruction["x"]] = self.value(instruction["y"])
        self.registers["pointer"] += 1
        return True

    def do_mul(self, instruction):
        """Multiply register by operand value."""
        self.registers[instruction["x"]] *= self.value(instruction["y"])
        self.registers["pointer"] += 1
        return True

    def do_jnz(self, instruction):
        """Jump relative when the operand is non-zero."""
        if self.value(instruction["x"]) != 0:
            self.registers["pointer"] += self.value(instruction["y"])
        else:
            self.registers["pointer"] += 1
        return True


def solve(input_value, part):
    """
    Solve both parts of the coprocessor puzzle.
    """
    if part == 2:
        registers = {"b": 109900, "c": 126900, "h": 0}
        for test_b in range(registers["b"], registers["c"] + 1, 17):
            if not sympy.isprime(test_b):
                registers["h"] += 1
        return registers["h"]
    computer = Computer(input_value, part)
    computer.run_program()
    return computer.registers["mul"]


YEAR = 2017
DAY = 23
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
