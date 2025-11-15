"""
Advent Of Code 2017 day 24

"""

# import system modules
import time
import re

# import my modules
import aoc  # pylint: disable=import-error


def parse_input(lines):
    """
    read component data from input
    """
    # init components
    components = []
    # regex to extract numbers
    pattern = re.compile(r"(\d+)")
    # walk lines
    for line in lines:
        # get int values from line for ports
        ports = [int(port) for port in pattern.findall(line)]
        # add component
        components.append(tuple(ports))
    return components


def build_bridges(bridge, components):
    """
    recursively build possible bridges
    """
    # print(f"build_bridges({bridge}, {components})")
    bridges = []
    # copy bridge and components
    bridge = list(bridge)
    components = list(components)
    # first component find
    if len(bridge) == 0:
        # to start, look for 0
        next_port = 0
    elif len(bridge) == 1:
        bridges.append(bridge)
        # second poort, look for not 0 (unless both are 0)
        next_port = sorted(bridge[0])[1]
    else:
        bridges.append(bridge)
        # compare the last two components to find next_port
        component_a = sorted(bridge[-2])
        component_b = sorted(bridge[-1])
        # get component a port that is in component b
        if component_a[0] in component_b:
            previous_port = component_a[0]
        else:
            previous_port = component_a[1]
        # get component b port that was not used to connect to component a
        if component_b[0] == previous_port:
            next_port = component_b[1]
        else:
            next_port = component_b[0]
    # print(f"next_port: {next_port}")
    # walk components
    for component in components:
        # print(f"{next_port} in {component}: {next_port in component}")
        # does it have the right port?
        if next_port in component:
            # clone bridge and components
            new_bridge = list(bridge)
            new_components = list(components)
            # move component from components to bridge
            new_bridge.append(new_components.pop(new_components.index(component)))
            # add results of recursive build
            bridges.extend(build_bridges(new_bridge, new_components))
    # print(f"bridges: {bridges}")
    # return results
    return bridges


def bridge_strength(bridge):
    """
    Calculate bridge strength
    """
    # init strength
    strength = 0
    # walk components of bridge
    for component in bridge:
        # add sum of ports
        strength += sum(component)
    return strength


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # part 2, we have already calculated, just return
    if part == 2:
        return answer[2]
    # parse data
    components = parse_input(input_value)
    # build possible bridge compbinations
    bridges = build_bridges((), components)
    # init max and longest
    max_strength = 0
    # max_bridge = None
    longest_bridge = []
    longest_strength = 0
    # walk bridges
    for bridge in bridges:
        # get strength
        strength = bridge_strength(bridge)
        # new max?
        if strength > max_strength:
            # max_bridge = bridge
            max_strength = strength
        # new longest?
        if len(bridge) > len(longest_bridge) or (
            len(bridge) == len(longest_bridge) and strength > longest_strength
        ):
            longest_bridge = bridge
            longest_strength = strength
        # print(f"{strength, bridge}")
    # print(f"{max_strength, max_bridge}")
    # store part 2 answer for next pass
    answer[2] = longest_strength
    # return part 1 answer
    return max_strength


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017, 24)
    # fetch input
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
