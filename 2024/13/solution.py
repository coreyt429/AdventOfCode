"""
Advent Of Code 2024 day 13

Tried BFS/DFS, and was taking too long, using too much memory, etc.

Sat down with pencil and paper to figure out the math, and came up short.

Discussed what I understood of the problem mathematically with ChatGPT, and
came up with a sound math strategy.  Ran that through sympy and solved,
sample data and part 1 with no problem.

Bring on part 2.  oh that's it, just add to prize x/y values.  same solution
same solve time.


"""

# import system modules
import logging
import argparse
import re
from sympy import symbols, solve

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

digit_pattern = re.compile(r"(\d+)")


def parse_input(text, part):
    """Function to parse input"""
    machines = []
    machine_texts = text.split("\n\n")
    add = 0
    if part == 2:
        add = 10000000000000
    for machine_text in machine_texts:
        machine_list = machine_text.splitlines()
        button_a = digit_pattern.findall(machine_list[0])
        button_b = digit_pattern.findall(machine_list[1])
        prize = digit_pattern.findall(machine_list[2])
        machines.append(
            {
                "button_a": tuple(int(num) for num in button_a),
                "button_b": tuple(int(num) for num in button_b),
                "prize": tuple(int(num) + add for num in prize),
            }
        )
    return machines


def solve_two_diophantine(eq1, eq2):
    """
    Solve two simultaneous linear Diophantine equations:
    eq1: c_1 = a_coef1 * a + b_coef1 * b
    eq2: c_2 = a_coef2 * a + b_coef2 * b
    Returns values of (a, b) that satisfy both equations.
    """
    a_coef1, b_coef1, c_1 = eq1
    a_coef2, b_coef2, c_2 = eq2
    sym_a, sym_b = symbols("a b", integer=True)

    solutions = solve(
        [
            a_coef1 * sym_a + b_coef1 * sym_b - c_1,
            a_coef2 * sym_a + b_coef2 * sym_b - c_2,
        ],
        (sym_a, sym_b),
        dict=True,
    )

    if solutions:
        return solutions
    return "No integer solutions exist."


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    machines = parse_input(input_value, part)

    total = 0
    for machine in machines:
        equation1 = (
            machine["button_a"][0],
            machine["button_b"][0],
            machine["prize"][0],
        )
        equation2 = (
            machine["button_a"][1],
            machine["button_b"][1],
            machine["prize"][1],
        )
        result = solve_two_diophantine(equation1, equation2)
        if isinstance(result, list):
            cost = float("infinity")
            for press_data in result:
                presses = tuple(press_data.values())
                cost = min(cost, (presses[0] * 3) + (presses[1] * 1))
            total += cost
    return total


YEAR = 2024
DAY = 13
input_format = {
    1: "text",
    2: "text",
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
