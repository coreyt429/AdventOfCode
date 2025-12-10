"""
Advent Of Code 2025 day 10

"""

# import system modules
import logging
import re
from dataclasses import dataclass
from typing import List, Tuple
import argparse
from heapq import heappop, heappush
import pulp


# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

patterns = {
    "line": re.compile(r"\[(.*)\] (.*) \{(.*)\}"),
}


@dataclass
class ButtonProblem:
    """Problem class for ILP solving"""

    buttons: List[Tuple[int, ...]]
    targets: List[int]

    def solve_min_presses(self):
        """Solve for minimum button presses using ILP"""
        n_counters = len(self.targets)
        n_buttons = len(self.buttons)

        # Build 0/1 matrix a[i][j] = 1 if button j touches counter i
        a = [[0] * n_buttons for _ in range(n_counters)]
        for j, btn in enumerate(self.buttons):
            for i in btn:
                a[i][j] = 1
        # Define ILP problem
        prob = pulp.LpProblem("ButtonMinPresses", pulp.LpMinimize)

        # Decision variables: x_j >= 0 integer
        x = [
            pulp.LpVariable(f"x_{j}", lowBound=0, cat="Integer")
            for j in range(n_buttons)
        ]

        # Objective: minimize total presses
        prob += pulp.lpSum(x), "TotalPresses"

        # Constraints: for each counter i,
        # sum_j a[i][j] * x_j == targets[i]
        for i in range(n_counters):
            prob += (
                pulp.lpSum(a[i][j] * x[j] for j in range(n_buttons)) == self.targets[i],
                f"counter_{i}",
            )

        # Solve
        status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
        if pulp.LpStatus[status] != "Optimal":
            raise RuntimeError(
                f"No optimal solution found, status={pulp.LpStatus[status]}"
            )

        presses = [int(v.value()) for v in x]
        total_presses = sum(presses)
        return total_presses


def parse_input(input_value):
    """
    Function to parse input
    """
    machines = []
    for line in input_value:
        light_str, button_str, joltage_str = patterns["line"].match(line).groups()
        logger.debug("Parsed line: %s, %s, %s", light_str, button_str, joltage_str)
        buttons = []
        button_strings = button_str.replace("(", "").replace(")", "").split(" ")
        for btn_str in button_strings:
            buttons.append(tuple(int(n) for n in btn_str.split(",")))
        machines.append(
            {
                "lights": tuple(char == "#" for char in light_str),
                "buttons": tuple(buttons),
                "joltages": tuple(int(x) for x in joltage_str.split(",")),
            }
        )
    return machines


def fewest_button_presses_joltage(target_joltages, buttons):
    """
    Find fewest button presses to turn on correct lights
    works for example, too slow for real input
    """
    initial_state = tuple([0] * len(target_joltages))
    heap = []
    heappush(heap, (0, initial_state))
    visited = set()

    while heap:
        current_presses, current_state = heappop(heap)
        logger.debug(
            "Target: %s, Visiting state: %s with presses: %d, heap size: %d",
            target_joltages,
            current_state,
            current_presses,
            len(heap),
        )
        if current_state == target_joltages:
            return current_presses

        if current_state in visited:
            continue
        visited.add(current_state)

        invalid = False
        for idx, val in enumerate(current_state):
            if val > target_joltages[idx]:
                invalid = True
                break
        if invalid:
            continue

        for button in buttons:
            new_state = list(current_state)
            for light_idx in button:
                new_state[light_idx] += 1
            heappush(heap, (current_presses + 1, tuple(new_state)))
    return float("inf")


def fewest_button_presses(target_lights, buttons):
    """
    Find fewest button presses to turn on correct lights
    """

    initial_state = tuple([False] * len(target_lights))
    heap = []
    heappush(heap, (0, initial_state))
    visited = set()

    while heap:
        current_presses, current_state = heappop(heap)
        if current_state == target_lights:
            return current_presses

        if current_state in visited:
            continue
        visited.add(current_state)

        for button in buttons:
            new_state = list(current_state)
            for light_idx in button:
                new_state[light_idx] = not new_state[light_idx]
            heappush(heap, (current_presses + 1, tuple(new_state)))
    return float("inf")


def count_button_presses(machines, part):
    """
    Count total button presses needed to turn on all lights
    """
    total_presses = 0
    for machine in machines:
        if part == 1:
            total_presses += fewest_button_presses(
                machine["lights"], machine["buttons"]
            )
            continue
        problem = ButtonProblem(machine["buttons"], machine["joltages"])
        total_presses += problem.solve_min_presses()
        # total_presses += fewest_button_presses_joltage(machine["joltages"], machine["buttons"])
    return total_presses


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    machines = parse_input(input_value)
    return count_button_presses(machines, part)


YEAR = 2025
DAY = 10
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
