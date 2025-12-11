"""
Advent Of Code 2017 day 7

"""

# import system modules
from __future__ import annotations
import logging
import argparse
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)


class Program:
    """
    Class to define program
    """

    def __init__(self, input_string):
        """
        init Program()
        """
        match = re.match(r"(\w+) .(\d+).(.*)", input_string)
        if match:
            self.name = match.group(1)
            self.weight = int(match.group(2))
            children = match.group(3)
            self.children = []
            self.parent = None
            if children:
                children = children.replace(" -> ", "")
                self.children = children.split(", ")

    def __str__(self):
        if self.children:
            return f"{self.name} of weight {self.weight} has children: {self.children}"
        return f"{self.name} of weight {self.weight} has no children"

    def __bool__(self):
        return True


def init_programs(lines):
    """
    Function to initialize programs based on input
    """
    program_map = {}
    for line in lines:
        program = Program(line)
        program_map[program.name] = program
    return program_map


def link_children(program_map):
    """
    Function to link children to parents
    """
    for program in program_map.values():
        if program.children:
            children_names = program.children
            program.children = []
            for child_name in children_names:
                program.children.append(program_map[child_name])
                program_map[child_name].parent = program


def find_bottom(program_map):
    """
    Find the bottom of the tower
    """
    for program in program_map.values():
        if not program.parent:
            return program
    return None


def tower_weight(program):
    """
    Function to calculate weight of a sub tower
    """
    weight = program.weight
    for child in program.children:
        weight += tower_weight(child)
    return weight


def find_imbalance(program):
    """
    Function to find imbalance in the tower
    """
    if not program.children:
        return program
    weight_map = {}
    weights = []
    for child in program.children:
        weight_map[child.name] = tower_weight(child)
        weights.append(weight_map[child.name])
    for child in program.children:
        if weights.count(weight_map[child.name]) == 1:
            imbalance = find_imbalance(child)
            if imbalance:
                return imbalance
    return program


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    program_map = init_programs(input_value)
    link_children(program_map)
    bottom = find_bottom(program_map)
    if part == 1:
        return bottom.name
    imbalance = find_imbalance(bottom)
    parent = imbalance.parent
    weights = []
    for child in parent.children:
        weights.append(tower_weight(child))
    for child in parent.children:
        weight = tower_weight(child)
        if weights.count(weight) > 1:
            break
    out_of_balance = weight - tower_weight(imbalance)
    adjusted = imbalance.weight + out_of_balance
    return adjusted


YEAR = 2017
DAY = 7
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
