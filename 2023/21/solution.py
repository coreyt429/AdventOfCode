"""
Advent Of Code 2023 day 21

"""

# import system modules
import logging
import argparse
from functools import cache
from itertools import product

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_input(lines: list[str]) -> tuple[list[list[str]], list[list[int]]]:
    """parse input data into two maps, one with characters and one with integers"""
    my_map = []
    my_map2 = []
    my_dict = {"O": 0, ".": 1, "S": 2, "#": 3}

    # Split the data into lines
    for line in lines:
        row = list(line)
        my_map.append(row)
        my_map2.append([my_dict[element] for element in row])
    return my_map, my_map2


@cache
def get_neighbor_coordinates(
    row_max: int, col_max: int, row: int, col: int, include_negative=False
) -> list[tuple[int, int]]:
    """get neighbor coordinates for a given cell"""
    retval = []
    for nr, nc in [(row - 1, col), (row, col - 1), (row, col + 1), (row + 1, col)]:
        if include_negative or (0 <= nr < row_max and 0 <= nc < col_max):
            retval.append((nr, nc))
    return retval


def take_step(my_map: list[list[int]]) -> list[list[int]]:
    """take a step in the map simulation"""
    spaces = set()
    for i, j in product(range(len(my_map)), range(len(my_map[0]))):
        if my_map[i][j] in {0, 2}:  # Using a set for faster membership checking
            spaces.add((i, j))
    for i, j in spaces:
        destinations = get_neighbor_coordinates(len(my_map), len(my_map[0]), i, j)
        my_map[i][j] = 1
        for dr, dc in destinations:
            if my_map[dr][dc] < 3:
                my_map[dr][dc] = 0
    return my_map


def convert_map(
    my_map: list[list[str]],
) -> tuple[dict[complex, str], complex, int, int]:
    """convert map to infinite grid format"""
    # init grid
    grid, start = {}, None
    # original was reading the file, but since I already have it in a
    for y_idx, y_val in enumerate(my_map):
        for x_idx, x_val in enumerate(y_val):
            c = x_val
            if c == "S":
                # store start coordinates as complex number
                start = x_idx + 1j * y_idx
            # store plot value with coordinates as complex number
            grid[x_idx + 1j * y_idx] = c
    # max x and y values
    max_x, max_y = int(max(p.real for p in grid)), int(max(p.imag for p in grid))
    return grid, start, max_x, max_y


def infinite_grid(grid: dict[complex, str], p: complex, max_x: int, max_y: int) -> str:
    """infinite grid lookup"""
    # remainder of x and y if point divided by max X/Y in single grid
    x = p.real % (max_x + 1)
    y = p.imag % (max_y + 1)
    # return corresponding grid value
    return grid[x + y * 1j]


def complex_neighbors(p: complex) -> list[complex]:
    """get 4 neighboring coordinates as complex numbers"""
    return [p - 1j, p - 1, p + 1, p + 1j]


def generate_history(
    grid: dict[complex, str], start: complex, max_x: int, max_y: int, steps: int
) -> tuple[list[int], list[int]]:
    """generate history of reachable points over steps"""
    # initialize empty ods, and evens / queue with start
    odds, evens, queue = set(), {start}, {start}
    # history storage
    odd_history, even_history = [0], [1]
    for i in range(1, steps + 1):
        new_points = set()
        for p in queue:  # initially start, after that new_points
            # foreach neighbor if not already processed
            for n in [
                n for n in complex_neighbors(p) if n not in evens and n not in odds
            ]:
                # if start or empty
                if infinite_grid(grid, n, max_x, max_y) in ".S":
                    new_points.add(n)
        # add to evens or odds
        if i % 2:
            odds |= new_points
        else:
            evens |= new_points
        # add histories
        odd_history.append(len(odds))
        even_history.append(len(evens))
        # set queue for next pass
        queue = new_points
    # return histories
    return odd_history, even_history


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    data = {}

    data["grid"], data["map"] = parse_input(input_value)
    if part == 1:
        retval = 0
        for _ in range(64):
            take_step(data["map"])
        for row in data["map"]:
            for sq in row:
                if sq == 0:
                    retval += 1
        return retval
    # convert map to infinite grid format
    grid, start, max_x, max_y = convert_map(data["grid"])
    # generate history, only save odd history
    history, _ = generate_history(grid, start, max_x, max_y, 3 * 262 + 65)
    # I understand this math, but where did 262 come from to start with?
    steps = 101150  # (26501365 - 65) // 262
    a = history[2 * 262 + 65]
    b = history[2 * 262 + 65] - history[262 + 65]
    c = history[3 * 262 + 65] - 2 * history[2 * 262 + 65] + history[262 + 65]
    retval = a + b * (steps - 2) + c * ((steps - 2) * (steps - 1) // 2)
    return retval


YEAR = 2023
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
