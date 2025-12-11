"""
Advent Of Code 2017 day 8

This one was pretty straight forward.  I had to research the conditional operators.
When I found my answer it looked really familiar, so I think I may have used this
method before.

"""

# import system modules
from __future__ import annotations
import logging
import argparse
import re
import operator
from collections import defaultdict

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)

conditional_operators = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
}


def parse_instructions(instructions):
    """
    Convert raw text instructions into executable command dictionaries.

    Args:
        instructions (Iterable[str]): Input program lines from the puzzle.

    Returns:
        list[dict]: Parsed command dictionaries containing action metadata
            and conditional clauses.
    """
    commands = []
    input_pattern = re.compile(r"(\w+) (\w{3}) (\S+) if (\S+) (\S+) (\S+)")
    for instruction in instructions:
        match = input_pattern.match(instruction)
        if match:
            command = {"condition": {}}
            command["register"] = match.group(1)
            command["action"] = match.group(2)
            command["value"] = int(match.group(3))
            command["condition"]["left"] = match.group(4)
            command["condition"]["operator"] = match.group(5)
            cond_value = match.group(6)
            try:
                cond_value = int(cond_value)
            except ValueError:
                pass
            command["condition"]["right"] = cond_value
            commands.append(command)
    return commands


def get_value(token, registers):
    """
    Resolve a token into an integer value.

    Args:
        token (int | str): Literal integer or register name.
        registers (Mapping[str, int]): Current machine register state.

    Returns:
        int: Numeric value represented by the token.
    """
    if isinstance(token, int):
        return token
    return registers[token]


def execute_instruction(instruction, registers):
    """
    Apply a parsed instruction to the register state.

    Args:
        instruction (dict): Parsed instruction with `register`, `action`,
            and `value`.
        registers (MutableMapping[str, int]): Register map to mutate.
    """
    value = get_value(instruction["value"], registers)
    if instruction["action"] == "dec":
        registers[instruction["register"]] -= value
    else:
        registers[instruction["register"]] += value


def evaluate_condition(condition, registers):
    """
    Determine whether an instruction's conditional guard passes.

    Args:
        condition (dict): Condition dictionary containing `left`,
            `operator`, and `right`.
        registers (Mapping[str, int]): Current register state.

    Returns:
        bool: True when the condition holds, False otherwise.
    """
    operator_func = conditional_operators.get(condition["operator"])
    if operator_func is None:
        raise ValueError(f"Unknown conditional operator: {condition['operator']}")
    return operator_func(
        registers[condition["left"]],
        get_value(condition["right"], registers),
    )


def run_program(input_value):
    """
    Execute every instruction while tracking register maxima.

    Args:
        input_value (Iterable[str]): Raw instruction lines.

    Returns:
        tuple[int, int]: Final maximum register value and the highest value
            observed at any point during execution.
    """
    program = parse_instructions(input_value)
    registers = defaultdict(int)
    max_value = 0
    for code in program:
        if evaluate_condition(code["condition"], registers):
            execute_instruction(code, registers)
            if registers:
                max_value = max(max_value, registers[code["register"]])
    max_register_value = max(registers.values()) if registers else 0
    return max_register_value, max_value


def solve(input_value, part):
    """
    Evaluate the register program for the requested puzzle part.

    Args:
        input_value (Iterable[str]): Puzzle input lines.
        part (int): Part selector (1 or 2).

    Returns:
        int: Answer for the requested part.
    """
    max_register_value, max_value = run_program(input_value)
    if part == 1:
        return max_register_value
    return max_value


YEAR = 2017
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
