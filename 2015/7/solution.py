"""
Advent Of Code 2015 day 7

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


def parse_input(input_text):
    """
    Function to parse input
        123 -> x
        456 -> y
        x AND y -> d
        x OR y -> e
        x LSHIFT 2 -> f
        y RSHIFT 2 ->
        NOT x -> h
        NOT y -> i
    """
    # define regex patterns, tested against sample data already
    re_patterns = {
        "init": re.compile(r"^(\d+) -> ([a-z]+)"),
        "not": re.compile(r"(NOT) (.+) -> ([a-z]+)"),
        "andor": re.compile(r"(.+) (AND|OR) ([a-z]+) -> ([a-z]+)"),
        "shift": re.compile(r"([a-z]+) (.SHIFT) (\d+) -> ([a-z]+)"),
        "copy": re.compile(r"^([a-z]+) -> ([a-z]+)"),
    }
    circuit = {}
    # loop through lines
    for line in input_text.strip().splitlines():
        if not line:
            continue
        cmd = {}
        # check each pattern to see if it matches
        for pattern, re_pattern in re_patterns.items():
            match = re_pattern.search(line)
            if match:
                cmd["type"] = pattern
                if pattern == "init":
                    cmd["value"] = int(match.groups(1)[0])
                    cmd["target"] = match.groups(1)[1]
                elif pattern == "andor":
                    cmd["L"] = match.groups(1)[0]
                    cmd["operator"] = match.groups(1)[1]
                    cmd["R"] = match.groups(1)[2]
                    cmd["target"] = match.groups(1)[3]
                    # if 'c' in line:
                    #    print(cmd)
                elif pattern == "shift":
                    cmd["L"] = match.groups(1)[0]
                    cmd["operator"] = match.groups(1)[1]
                    cmd["bits"] = int(match.groups(1)[2])
                    cmd["target"] = match.groups(1)[3]
                elif pattern == "not":
                    cmd["operator"] = match.groups(1)[0]
                    cmd["L"] = match.groups(1)[1]
                    cmd["target"] = match.groups(1)[2]
                elif pattern == "copy":
                    cmd["source"] = match.groups(1)[0]
                    cmd["target"] = match.groups(1)[1]
        if len(cmd) > 0:
            circuit[cmd["target"]] = cmd
    return circuit


def print_circuit(circuit):
    """
    Function to print circuit
    """
    for wire in sorted(circuit.keys()):
        print(f"{wire}: {circuit[wire]}")
    print()


def do_init(**kwargs):
    """
    Function to initialize a wire
    """
    cmd = kwargs["cmd"]
    wires = kwargs["wires"]
    wires[cmd["target"]] = cmd["value"]


def do_andor(**kwargs):
    """
    Function to perform AND OR operation
    """
    cmd = kwargs["cmd"]
    wires = kwargs["wires"]
    circuit = kwargs["circuit"]
    if not cmd["L"] in wires:
        wire_trace(cmd["L"], wires, circuit)
    if not cmd["R"] in wires:
        wire_trace(cmd["R"], wires, circuit)
    if cmd["operator"] == "AND":
        wires[cmd["target"]] = wires[cmd["L"]] & wires[cmd["R"]]
    else:
        wires[cmd["target"]] = wires[cmd["L"]] | wires[cmd["R"]]


def do_not(**kwargs):
    """
    Function to perform NOT operation
    """
    cmd = kwargs["cmd"]
    wires = kwargs["wires"]
    circuit = kwargs["circuit"]
    if not cmd["L"] in wires:
        wire_trace(cmd["L"], wires, circuit)
    # Bitmask for 8-bit
    bitmask = 0xFFFF
    wires[cmd["target"]] = (~wires[cmd["L"]]) & bitmask


def do_copy(**kwargs):
    """
    Function to perform COPY operation
    """
    cmd = kwargs["cmd"]
    wires = kwargs["wires"]
    circuit = kwargs["circuit"]
    if not cmd["source"] in wires:
        wire_trace(cmd["source"], wires, circuit)
    wires[cmd["target"]] = wires[cmd["source"]]


def wire_trace(target, wires, circuit):
    """
    function to trace a wire in a circuit
    """
    cmd = circuit[target]
    func_map = {"init": do_init, "andor": do_andor, "not": do_not, "copy": do_copy}
    if cmd["type"] in func_map:
        func_map[cmd["type"]](cmd=cmd, target=target, wires=wires, circuit=circuit)
    else:
        if not cmd["L"] in wires:
            wire_trace(cmd["L"], wires, circuit)
        if cmd["operator"] == "RSHIFT":
            wires[cmd["target"]] = wires[cmd["L"]] >> cmd["bits"]
        elif cmd["operator"] == "LSHIFT":
            wires[cmd["target"]] = wires[cmd["L"]] << cmd["bits"]
    return wires[target]


def part1(parsed_data, _part=None):
    """
    Function to solve part 1
    """
    wires = {"1": 1}  # hard wire this to handle "1 AND" entries
    wire_trace("a", wires, parsed_data)
    return wires["a"]


def part2(parsed_data, _part=None):
    """
    Function to solve part 2
    """
    wires = {
        "1": 1,  # hard wire this to handle "1 AND" entries
        "b": 956,  # hard wire b to match part1 a
    }
    wire_trace("a", wires, parsed_data)
    return wires["a"]


YEAR = 2015
DAY = 7
input_format = {
    1: parse_input,
    2: parse_input,
}

funcs = {
    1: part1,
    2: part2,
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
