"""
Advent Of Code 2022 day 21

"""

# import system modules
import json
import logging
import argparse
from dataclasses import dataclass
from typing import Literal

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


Operator = Literal["+", "-", "*", "/", "="]


@dataclass(frozen=True)
class Constant:
    """Represents a constant value in the expression graph."""

    value: int


@dataclass(frozen=True)
class Operation:
    """Represents an operation in the expression graph."""

    left: str
    operator: Operator
    right: str


Node = Constant | Operation


def evaluate(name: str, graph: dict[str, Node]) -> int:
    """Evaluates the value of the node with the given name in the expression graph."""
    node = graph[name]
    if isinstance(node, Constant):
        return node.value
    if isinstance(node, Operation):
        left_val = evaluate(node.left, graph)
        right_val = evaluate(node.right, graph)
        if node.operator == "+":
            return left_val + right_val
        if node.operator == "-":
            return left_val - right_val
        if node.operator == "*":
            return left_val * right_val
        if node.operator == "/":
            return left_val // right_val
        if node.operator == "=":
            return int(left_val == right_val)
        raise ValueError(f"Unknown operator: {node.operator}")
    raise ValueError(f"Unknown node type: {node}")


def parse_input(input_value):
    """Parses the input into an expression graph."""
    graph: dict[str, Node] = {}
    for line in input_value:
        name, expr = line.split(": ")
        if expr.isdigit():
            graph[name] = Constant(int(expr))
        else:
            left, operator, right = expr.split(" ")
            graph[name] = Operation(left, operator, right)
    return graph


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    graph = parse_input(input_value)
    logger.debug(json.dumps(graph, default=lambda o: o.__dict__))
    if part == 1:
        return evaluate("root", graph)
    graph["root"] = Operation(graph["root"].left, "=", graph["root"].right)
    graph["humn"] = Constant(1)
    range_start = 0
    range_end = 9999999999999999
    initial_diff = None
    while not evaluate("root", graph):
        difference = evaluate(graph["root"].left, graph) - evaluate(
            graph["root"].right, graph
        )
        if initial_diff is None:
            initial_diff = difference
            logger.debug("Initial difference: %s", initial_diff)
        if initial_diff is not None and (difference > 0) != (initial_diff > 0):
            range_end = graph["humn"].value
            logger.debug("Sign change detected, breaking loop")
            break
        logger.debug(
            "Trying humn = %s, difference = %s", graph["humn"].value, difference
        )
        range_start = graph["humn"].value
        graph["humn"] = Constant(graph["humn"].value * 2)
    logger.debug("humn range: %s - %s", range_start, range_end)
    while range_start + 10 < range_end:
        mid = (range_start + range_end) // 2
        graph["humn"] = Constant(mid)
        difference = evaluate(graph["root"].left, graph) - evaluate(
            graph["root"].right, graph
        )
        logger.debug(
            "Trying mid %s of range %s-%s, difference: %s",
            mid,
            range_start,
            range_end,
            difference,
        )
        # if difference == 0:
        #     range_start = range_end = mid
        #     break
        if (difference > 0) != (initial_diff > 0):
            range_end = mid
        else:
            range_start = mid
    logger.debug("final humn range: %s - %s", range_start, range_end)
    for humn_value in range(range_start, range_end + 1):
        graph["humn"] = Constant(humn_value)
        difference = evaluate(graph["root"].left, graph) - evaluate(
            graph["root"].right, graph
        )
        logger.debug(
            "Trying humn = %s, difference = %s", graph["humn"].value, difference
        )
        if evaluate("root", graph):
            break
    return graph["humn"].value


YEAR = 2022
DAY = 21
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
