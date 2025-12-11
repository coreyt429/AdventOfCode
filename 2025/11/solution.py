"""
Advent Of Code 2025 day 11

"""

# import system modules
from __future__ import annotations
import logging
import argparse
from dataclasses import dataclass

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class Device:
    """class to represent a device"""

    parent: "ServerRack"
    name: str
    children: list
    path_counts: dict = None
    counter: int = 0

    def find_paths(self, target: str):
        """return paths from this device to its children"""
        self.counter += 1
        if self.path_counts is not None:
            logger.debug(
                "Using cached paths from %s to %s: %s paths found",
                self.name,
                target,
                self.path_counts,
            )
            return self.path_counts
        self.path_counts = {
            target: 0,
            "dac": 0,
            "fft": 0,
            "both": 0,
        }
        logger.debug(
            "Finding paths from device %s to target %s: call count %s",
            self.name,
            target,
            self.counter,
        )
        if self.name == target:
            self.path_counts[target] = 1
        for child in self.children:
            child_paths = self.parent.devices[child].find_paths(target)
            if self.name in ["dac", "fft"]:
                other = "fft" if self.name == "dac" else "dac"
                self.path_counts[self.name] += child_paths[target]
                self.path_counts["both"] += child_paths[other]
            for k, v in child_paths.items():
                self.path_counts[k] += v
        logger.debug(
            "Paths from device %s to target %s: %s", self.name, target, self.path_counts
        )
        return self.path_counts


class ServerRack:
    """class to represent a server rack"""

    def __init__(self):
        self.devices = {}
        self.paths = set()
        self.visited = set()
        self.dag_paths = {}

    def add_device(self, input_line: str):
        """Add a device to the rack"""
        device_name, children_str = input_line.split(": ")
        children = children_str.split(" ") if children_str else []
        if device_name not in self.devices:
            device = Device(parent=self, name=device_name, children=children)
            self.devices[device_name] = device
        else:
            self.devices[device_name].children.extend(children)

    def find_path(self, start: str, target: str):
        """
        Wrapper to find path from start to target device
        """
        logger.debug("Finding path from %s to %s", start, target)
        child = self.devices.get(start)
        logger.debug("Starting device: %s", child)
        return child.find_paths(target=target)

    def find_path_dfs(self, current: str, target: str, path=None):
        """
        Find path from current to target device
        Worked for part 1, part 2 is too complex
        """
        logger.debug(
            "Finding path from %s to %s with current path: %s", current, target, path
        )
        if path is None:
            self.visited = set()
            self.paths = set()
            path = tuple()
        path = path + (current,)
        logger.debug("current: %s, target: %s, path: %s", current, target, path)
        if current == target:
            logger.debug("Found path to target %s: %s", target, tuple(path))
            self.paths.add(tuple(path))
            return
        if current not in self.devices:
            logger.warning("Device %s not found in rack", current)
            return
        logger.debug(
            "Current device %s has children: %s",
            current,
            self.devices[current].children,
        )
        for child in self.devices[current].children:
            if child in path:
                logger.warning(
                    "Cycle detected: %s, skipping child %s", path + (child,), child
                )
                continue
            logger.debug("Exploring child %s of %s", child, current)
            if tuple(path + (child,)) not in self.visited:
                self.visited.add(tuple(path + (child,)))
                self.find_path_dfs(child, target, path)
            else:
                logger.warning(
                    "Already visited %s, skipping to avoid cycle", path + (child,)
                )
        return

    def __str__(self):
        ret_str = f"ServerRack with devices: {list(self.devices.keys())}"
        for k, v in self.devices.items():
            ret_str += f"\n  Device {k} with children: {v.children}"
        return ret_str


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    rack = ServerRack()
    rack.add_device("out: ")
    rack.add_device("you: ")

    for line in input_value:
        rack.add_device(line)
    logger.debug("Rack: %s", rack)
    if part == 2:
        paths = rack.find_path("svr", "out")
        for k, v in paths.items():
            logger.debug("Paths from svr to %s: %s", k, v)
        return paths["both"]
    paths = rack.find_path("you", "out")
    logger.debug("Paths found: %s", paths["out"])
    return paths["out"]


YEAR = 2025
DAY = 11
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
