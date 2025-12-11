"""
Advent Of Code 2017 day 25

"""

# import system modules
from __future__ import annotations
import logging
import argparse
import re
from collections import deque

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)

pattern_begin = re.compile(r"Begin in state (\w)\.")
pattern_diagnostic = re.compile(r"Perform a diagnostic checksum after (\d+) steps\.")
pattern_new_state = re.compile(r"In state (\w):")
pattern_condition = re.compile(r"\s+If the current value is (\d):")
pattern_write = re.compile(r"\s+- Write the value (\d).")
pattern_move = re.compile(r"\s+- Move one slot to the (\w+).")
pattern_next = re.compile(r"\s+- Continue with state (\w).")


def parse_input(lines):
    """
    Functino to parse input data
    """
    movement = {"right": 1, "left": -1}
    machine = {"init_state": "", "checksum_steps": "", "states": {}}
    for line in lines:
        match = pattern_begin.match(line)
        if match:
            machine["init_state"] = match.group(1)
        match = pattern_diagnostic.match(line)
        if match:
            machine["checksum_steps"] = int(match.group(1))
        match = pattern_new_state.match(line)
        if match:
            current_state = match.group(1)
            machine["states"][current_state] = {}
        match = pattern_condition.match(line)
        if match:
            condition = int(match.group(1))
            machine["states"][current_state][condition] = {}
        match = pattern_write.match(line)
        if match:
            machine["states"][current_state][condition]["write"] = int(match.group(1))
        match = pattern_move.match(line)
        if match:
            machine["states"][current_state][condition]["movement"] = movement[
                match.group(1)
            ]
        match = pattern_next.match(line)
        if match:
            machine["states"][current_state][condition]["next"] = match.group(1)
    return machine


def run_machine(turing_machine):
    """
    Function to run turing machine and provide checksum
    """
    current_state = turing_machine["init_state"]
    states = turing_machine["states"]
    steps = turing_machine["checksum_steps"]
    cursor = 0
    tape = deque([0])
    for _ in range(steps):
        state = states[current_state]
        conditional = tape[cursor]
        tape[cursor] = state[conditional]["write"]
        cursor += state[conditional]["movement"]
        if cursor == -1:
            cursor = 0
            tape.appendleft(0)
        if cursor > len(tape) - 1:
            tape.append(0)
        current_state = state[conditional]["next"]
    return sum(tape)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return "Reboot the printer"
    turing_machine = parse_input(input_value)
    checksum = run_machine(turing_machine)
    return checksum


YEAR = 2017
DAY = 25
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
