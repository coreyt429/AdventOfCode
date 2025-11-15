"""
Advent Of Code 2017 day 7

"""

# import system modules
import time
import re

# import my modules
import aoc  # pylint: disable=import-error


class Program:
    """
    Class to define program
    """

    def __init__(self, input_string):
        """
        init Program()
        """
        # parse imput_string
        match = re.match(r"(\w+) .(\d+).(.*)", input_string)
        if match:
            # program name
            self.name = match.group(1)
            # program weight
            self.weight = int(match.group(2))
            # store children string, we'll parse it later
            children = match.group(3)
            # init children as empty list
            self.children = []
            # init parent
            self.parent = None
            # parse children
            if children:
                # remove arrow
                children = children.replace(" -> ", "")
                # store children names, we'll find the objects later
                self.children = children.split(", ")

    def __str__(self):
        """String"""
        if self.children:
            return f"{self.name} of weight {self.weight} has children: {self.children}"
        return f"{self.name} of weight {self.weight} has no children"

    def __bool__(self):
        """Boolean"""
        return True


def init_programs(lines):
    """
    Function to initialize programs based on input
    Args:
        lines: list() of str()
    Returns:
        program_map: dict() of Program() keyed on Program.name
    """
    # init program_map
    program_map = {}
    # walk liines
    for line in lines:
        # init program
        program = Program(line)
        # store in map
        program_map[program.name] = program
    return program_map


def link_children(program_map):
    """
    Function to link children to parents
    Args:
        program_name: dict()
    """
    # walk programs
    for program in program_map.values():
        # if it has childen
        if program.children:
            # get children names
            children_names = program.children
            # empty children
            program.children = []
            # for child_name in children_names
            for child_name in children_names:
                # add child object
                program.children.append(program_map[child_name])
                # link program as childs parent
                program_map[child_name].parent = program


def find_bottom(program_map):
    """
    Find the bottom of the tower
    Args:
        program_map: dict()
    Returns:
        program: Program()
    """
    # walk programs
    for program in program_map.values():
        # only one shouldn't have a parent
        if not program.parent:
            # return bottom
            return program
    # this shouldn't be possible, but it makes pylint happy to have it.
    return None


def tower_weight(program):
    """
    Function to calculate weight of a sub tower
    Args:
        program: Program()
    Returns:
        weight: int() weight of tower
    """
    # init weight as program weight
    weight = program.weight
    # walk children
    for child in program.children:
        # recurse each child and add its tower weight
        weight += tower_weight(child)
    return weight


def find_imbalance(program):
    """
    Function to find imbalance in the tower
    Args:
        program: Program() to start with
    Returns:
        imbalance or program: Program()
    """
    # if no children, stop recursion
    if not program.children:
        return program
    # init weight and wieght_map
    weight_map = {}
    weights = []
    # walk children
    for child in program.children:
        # add child weight to map and weights
        weight_map[child.name] = tower_weight(child)
        weights.append(weight_map[child.name])
    # walk children again
    for child in program.children:
        # if this is the only child with its weight, then it is out of balance
        if weights.count(weight_map[child.name]) == 1:
            # recurse child
            imbalance = find_imbalance(child)
            # if imbalance exists, return it
            if imbalance:
                return imbalance
    # hmm, this must be the imbalanced program, not its children
    return program


def solve(lines, part):
    """
    Function to solve puzzle
    """
    # init map
    my_map = init_programs(lines)
    # link children
    link_children(my_map)
    # get bottom
    bottom = find_bottom(my_map)
    # part 2, return bottom name
    if part == 1:
        return bottom.name
    # find imbalance
    imbalance = find_imbalance(bottom)
    # get parent
    parent = imbalance.parent
    # init weights
    weights = []
    # store child weights
    for child in parent.children:
        weights.append(tower_weight(child))
    # get tower weight of non imbalance children
    for child in parent.children:
        weight = tower_weight(child)
        if weights.count(weight) > 1:
            break
    # calculate aout of balance
    out_of_balance = weight - tower_weight(imbalance)
    # ajust weight and return part 2 answer
    adjusted = imbalance.weight + out_of_balance
    return adjusted


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017, 7)
    # input_text = my_aoc.load_text()
    # print(input_text)
    input_lines = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
