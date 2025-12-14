"""
Advent Of Code 2020 day 11

This one works, and it is slow.

Grid() made this one easy to code, but the overhead is killing me on this one.

16 seconds per part.  Taking a quick look at it, the optimizations that would help
here could break other code.  If I look to optimize this one later, it might
be better to decouple it from Grid().

Alternatively,  here are the optimization points in Grid() to look at:

1) get_neighbors() the check for directions at the end, would be more efficient if we
could assume that directions is a list, and iterate over it instead of checking each
direction against directions.  This however would break code that passes directions
as a string.

2) get_neighbors() caching results would help in this case, but could break in dynamic
grids

3) in_bounds() caching  results would help in this case, but could break in dynamic
grids

Okay, changing the response from next_seat to the coordinates instead of the value
allowed me to cache the coordinates, reducing to 6 seconds per part.

Replaced waiting_area.get_point with waiting_area.map.get and further reduced to 3
seconds per part

"""

# import system modules
import logging
import argparse
from collections import defaultdict

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def next_seat_orig(waiting_area, seat, direction, part):
    """
    Function to find the value of the next seat in sight
    """
    neighbors = waiting_area.get_neighbors(point=seat, directions=[direction])
    if not neighbors:
        return "."
    state = waiting_area.get_point(neighbors[direction])
    if state in "L#":
        return state
    if part == 1:
        return "."
    return next_seat(waiting_area, neighbors[direction], direction, part)


def next_seat(waiting_area, seat, direction, part):
    """
    Function to find the value of the next seat in sight
    """
    neighbors = waiting_area.get_neighbors(point=seat, directions=[direction])
    if not neighbors:
        return seat
    # state = waiting_area.get_point(neighbors[direction])
    state = waiting_area.map.get(neighbors[direction], ".")
    if state in "L#":
        return neighbors[direction]
    if part == 1:
        return neighbors[direction]
    return next_seat(waiting_area, neighbors[direction], direction, part)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    waiting_area = Grid(input_value, use_overrides=False)
    last = str(waiting_area)
    threshold = 4
    if part == 2:
        threshold = 5
    seat_cache = defaultdict(dict)
    while True:
        tmp_dict = {}
        for seat in waiting_area:
            neighbor_string = ""
            for direction in ["n", "s", "e", "w", "ne", "nw", "se", "sw"]:
                if direction not in seat_cache[seat]:
                    seat_cache[seat][direction] = next_seat(
                        waiting_area, seat, direction, part
                    )
                neighbor = seat_cache[seat][direction]
                if neighbor == seat:
                    continue
                # neighbor_string += waiting_area.get_point(neighbor)
                neighbor_string += waiting_area.map.get(neighbor, ".")
            # If a seat is empty (L) and there are no occupied seats adjacent to it,
            # the seat becomes occupied.
            if waiting_area.map.get(seat) == "L" and neighbor_string.count("#") == 0:
                tmp_dict[seat] = "#"
                continue
            # If a seat is occupied (#) and four or more seats adjacent to it are
            # also occupied, the seat becomes empty.
            if (
                waiting_area.map.get(seat) == "#"
                and neighbor_string.count("#") >= threshold
            ):
                tmp_dict[seat] = "L"
                continue
            # Otherwise, the seat's state does not change.
        for seat, state in tmp_dict.items():
            waiting_area.set_point(seat, state)
        if last == str(waiting_area):
            break
        last = str(waiting_area)
    return str(waiting_area).count("#")


YEAR = 2020
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
