"""
Advent Of Code 2020 day 5



"""

# import system modules
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def id_seat(code):
    """
    Function to convert elf binary seat notation to row/col tuple
    """
    row = {"min": 0, "max": 127}
    col = {"min": 0, "max": 7}
    for char in code:
        if char == "F":
            diff = row["max"] - row["min"]
            row["max"] -= diff // 2 + 1
        if char == "B":
            diff = row["max"] - row["min"]
            row["min"] += diff // 2 + 1
        if char == "L":
            diff = col["max"] - col["min"]
            col["max"] -= diff // 2 + 1
        if char == "R":
            diff = col["max"] - col["min"]
            col["min"] += diff // 2 + 1
    # print(row, col)
    # likely unnecessary checks to be sure we found an answer
    if row["min"] != row["max"]:
        return None
    if col["min"] != col["max"]:
        return None
    return (row["min"], col["min"])


def calc_seat_id(seat):
    """Function to calculate seat ids"""
    row, col = seat
    # Every seat also has a unique seat ID:
    # multiply the row by 8, then add the column.
    return (row * 8) + col


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = Grid(".", use_overrides=False, default_value=".")
    max_seat_id = 0
    for seat_code in input_value:
        seat = id_seat(seat_code)
        grid.set_point(point=seat, value="#")
        seat_id = calc_seat_id(seat)
        max_seat_id = max(max_seat_id, seat_id)
    grid.update()
    # uncomment to visualize
    # print(grid)
    if part == 2:
        for seat in grid:
            if grid.get_point(seat, ".") == ".":
                # Your seat wasn't at the very front or back, though;
                # the seats with IDs +1 and -1 from yours will be in your list.
                # I actually got lucky here, since I visualized my seat with Grid()
                # first, I knew it was not on an end, so I didn't have to check that case
                # so we are just looking for a '.' that has '#' north and south of it
                # this may not work for other inputs
                neighbors = grid.get_neighbors(point=seat, directions="ns")
                if len(neighbors) != 2:
                    continue
                neighbor_seats = "".join(
                    [grid.get_point(neighbor, ".") for neighbor in neighbors.values()]
                )
                if "." not in neighbor_seats:
                    # What is the ID of your seat?
                    return calc_seat_id(seat)
    # What is the highest seat ID on a boarding pass?
    return max_seat_id


YEAR = 2020
DAY = 5
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
