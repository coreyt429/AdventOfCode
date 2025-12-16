"""
Advent Of Code 2023 day 20

"""

# import system modules
import logging
import argparse
from collections import defaultdict
import math

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_input(lines: list[str]) -> dict:
    """parse input into data structure"""
    machine = {}
    for line in lines:
        src, dst = line.split(" -> ")
        dst = dst.split(", ")

        if src == "broadcaster":
            node_type = None
        else:
            node_type = src[0]
            src = src[1:]

        assert src not in machine
        machine[src] = (node_type, dst)
    return machine


def set_input_map(data: dict) -> dict:
    """Set input map"""
    input_map = defaultdict(list)

    for node, (_, dests) in data.items():
        for d in dests:
            input_map[d].append(node)
    return input_map


def set_memory(data: dict, input_map: dict) -> dict:
    """Set initial memory"""
    memory = {}

    for node, (t, _) in data.items():
        if t is None:
            continue
        if t == "%":
            memory[node] = False
        if t == "&":
            memory[node] = {d: False for d in input_map[node]}
    return memory


def process_node(src, node, is_high_pulse, data, memory):
    """Process a single node"""
    info = data.get(node)
    if info is None:
        return []
    t, dests = info
    if t == "%":
        if is_high_pulse:
            return []
        state = memory[node]
        memory[node] = not state
        return [(node, d, not state) for d in dests]
    if t == "&":
        state = memory[node]
        state[src] = is_high_pulse
        # All are high, send a low pulse
        to_send = not sum(state.values()) == len(state)
        return [(node, d, to_send) for d in dests]

    if t is None:
        return [(node, d, is_high_pulse) for d in dests]
    assert False


def part1(data: dict) -> int:
    """solve part 1"""
    counters = defaultdict(int)
    input_map = set_input_map(data)
    memory = set_memory(data, input_map)
    for _ in range(1000):
        todo = [(None, "broadcaster", False)]
        while todo:
            new_todo = []
            for src, node, is_high_pulse in todo:
                counters[is_high_pulse] += 1
                new_todo.extend(process_node(src, node, is_high_pulse, data, memory))
            todo = new_todo
    return math.prod(counters.values())


def part2(data: dict) -> int:
    """solve part 2"""
    counters = defaultdict(int)
    input_map = set_input_map(data)
    memory = set_memory(data, input_map)
    assert len(input_map["rx"]) == 1
    single = input_map["rx"][0]
    assert data[single][0] == "&"
    sources = input_map[single]
    assert all(data[s][0] == "&" for s in sources)
    # Assume that there are n sub-trees and they each have their own cycle
    low_counts = {}
    cycle = 0
    while len(low_counts) < len(sources):
        cycle += 1
        todo = [(None, "broadcaster", False)]

        while todo:
            new_todo = []

            for src, node, is_high_pulse in todo:
                if all([node in sources, not is_high_pulse, node not in low_counts]):
                    logger.debug("Node %s low at cycle %d", node, cycle)
                    low_counts[node] = cycle

                if node == "rx" and not is_high_pulse:
                    rx_count += 1
                counters[is_high_pulse] += 1
                new_todo.extend(process_node(src, node, is_high_pulse, data, memory))
            todo = new_todo

    return math.lcm(*low_counts.values())


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    machine = parse_input(input_value)
    logging.debug("Parsed machine with %d nodes", len(machine))
    if part == 1:
        return part1(machine)
    return part2(machine)


YEAR = 2023
DAY = 20
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
