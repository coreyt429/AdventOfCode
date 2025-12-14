"""
Advent Of Code 2016 day 17

This one was pretty quick, this built on the hashing we did in the last few,
and the path finding earlier.

I started with a modified dijkstra to get the shortest path, then after reading
part 2, simply removed the pruning for paths that cannot be shortest, and
added a check for longest.

The original longest and shortest functions are in the jupyter notebook, Here
they are combined into one.

Note, I usually try to either do row/col or x/y coordinates.  This time, I had
it in my head that start was (0,0) and end was (3,3) so it is more like x/-y.

Added Note.  Claude tells me there is a name for this type of coordinates:

It's called a "screen coordinate system" or sometimes "pixel coordinate system."
This system is commonly used in computer graphics, particularly for displaying
images on screens and in game development.
In this coordinate system:

The origin (0,0) is typically at the top-left corner of the screen or canvas.
The x-axis increases from left to right, as in the standard Cartesian system.
The y-axis increases from top to bottom, which is the opposite of the
standard Cartesian system.

"""

import logging
import argparse
from heapq import heappush, heappop
import hashlib
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def get_neighbors(position, seed, path):
    """
    Function to determine valid neighbors for a position
    """
    # map to loop for possible directions
    direction_map = {
        "U": {
            "pos": 0,  # position in the has to check
            "offset": (0, -1),  # x/y offsets
        },
        "D": {
            "pos": 1,
            "offset": (0, 1),
        },
        "L": {
            "pos": 2,
            "offset": (-1, 0),
        },
        "R": {
            "pos": 3,
            "offset": (1, 0),
        },
    }
    # empty set of neighbors
    neighbors = set()
    # md5 hash of seed + path
    my_hash = hashlib.md5(f"{seed}{path}".encode("utf-8")).hexdigest()
    # walk dirction_map
    for direction, info in direction_map.items():
        # check if character position is unlocked
        if my_hash[info["pos"]] in "bcdef":
            # calculate next room from info offsets
            next_room = (
                position[0] + info["offset"][0],
                position[1] + info["offset"][1],
            )
            # is the next_room valid (let's not fall of fthe map)
            if 0 <= next_room[0] <= 3 and 0 <= next_room[1] <= 3:
                # add to neighbors
                neighbors.add((direction, next_room))
    # return set of rooms to go to next
    return neighbors


def min_max_paths(seed):
    """
    Function to return the shortest and longest paths thorught the puzzle
    """
    # initialize start values
    start = (0, 0)
    end = (3, 3)
    heap = []
    min_rooms = float("infinity")
    min_path = ""
    max_rooms = 0
    max_path = ""
    # initialize heap (rooms_visited, path, current_room)
    heappush(heap, (0, "", start))
    # sentinel = 0
    while heap:
        # sentinel += 1
        # if sentinel > 20:
        #    print("Breaking loop!")
        #    break
        room_count, current_path, pos = heappop(heap)
        if pos == end:
            # we're at the vault
            # Is this the longest path
            if room_count > max_rooms:
                max_rooms = room_count
                max_path = current_path
            # is this the shortest path
            if room_count < min_rooms:
                min_rooms = room_count
                min_path = current_path
            continue
        # walk neighbors for current pos
        for neighbor in get_neighbors(pos, seed, current_path):
            heappush(heap, (room_count + 1, current_path + neighbor[0], neighbor[1]))
    # return min and max values
    return min_rooms, min_path, max_rooms, max_path


def solve(seed, part):
    """
    Wrapper that returns the requested answer for part 1 or 2.
    """
    _, min_path, max_rooms, _ = min_max_paths(seed.strip())
    return min_path if part == 1 else max_rooms


YEAR = 2016
DAY = 17
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
