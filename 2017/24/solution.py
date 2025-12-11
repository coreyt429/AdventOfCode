"""
Advent Of Code 2017 day 24

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


def parse_input(lines):
    """
    read component data from input
    """
    components = []
    pattern = re.compile(r"(\d+)")
    for line in lines:
        ports = [int(port) for port in pattern.findall(line)]
        components.append(tuple(ports))
    return components


def build_bridges(bridge, components):
    """
    recursively build possible bridges
    """
    bridges = []
    bridge = list(bridge)
    components = list(components)
    if len(bridge) == 0:
        next_port = 0
    elif len(bridge) == 1:
        bridges.append(bridge)
        next_port = sorted(bridge[0])[1]
    else:
        bridges.append(bridge)
        component_a = sorted(bridge[-2])
        component_b = sorted(bridge[-1])
        if component_a[0] in component_b:
            previous_port = component_a[0]
        else:
            previous_port = component_a[1]
        if component_b[0] == previous_port:
            next_port = component_b[1]
        else:
            next_port = component_b[0]
    for component in components:
        if next_port in component:
            new_bridge = list(bridge)
            new_components = list(components)
            new_bridge.append(new_components.pop(new_components.index(component)))
            bridges.extend(build_bridges(new_bridge, new_components))
    return bridges


def bridge_strength(bridge):
    """
    Calculate bridge strength
    """
    strength = 0
    for component in bridge:
        strength += sum(component)
    return strength


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    components = parse_input(input_value)
    bridges = build_bridges((), components)
    max_strength = 0
    longest_bridge = []
    longest_strength = 0
    for bridge in bridges:
        strength = bridge_strength(bridge)
        max_strength = max(strength, max_strength)
        if len(bridge) > len(longest_bridge) or (
            len(bridge) == len(longest_bridge) and strength > longest_strength
        ):
            longest_bridge = bridge
            longest_strength = strength
    if part == 1:
        return max_strength
    return longest_strength


YEAR = 2017
DAY = 24
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
