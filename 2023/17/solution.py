"""
Advent Of Code 2023 day 17

This script implements a modified Dijkstra's algorithm with minimum and maximum
forward paths.
"""

# import system modules
import logging
import argparse
from heapq import heappop, heappush

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"


CITY_MAP = []

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def next_position(my_map, current_position, new_direction):
    """
    Function to get next position in a direction.

    parameters:
        my_map: dict heatmap of city blocks
        current_position: tuple (r,c) coordinates
        new_direction: str 'N', 'S', 'E', 'W'

    returns:
        next_pos: tuple (r,c) coordinates
    """
    next_pos = None
    # up
    if new_direction == "N":
        if current_position[0] != 0:
            next_pos = (current_position[0] - 1, current_position[1])
    # down
    elif new_direction == "S":
        if current_position[0] < len(my_map) - 1:
            next_pos = (current_position[0] + 1, current_position[1])
    # left
    elif new_direction == "W":
        if current_position[1] != 0:
            next_pos = (current_position[0], current_position[1] - 1)
    # right
    elif new_direction == "E":
        if current_position[1] < len(my_map[0]) - 1:
            next_pos = (current_position[0], current_position[1] + 1)
    return next_pos


# DIRECTION_MAP dict of possible directions based on ingress direction
DIRECTION_MAP = {
    "N": {"L": "W", "R": "E", "F": "N"},
    "S": {"L": "E", "R": "W", "F": "S"},
    "E": {"L": "N", "R": "S", "F": "E"},
    "W": {"L": "S", "R": "N", "F": "W"},
}


def dijkstra(start_pos, min_forward, max_forward):
    """
    modified dijkstra algorithm

    parameters:
        start_pos: tuple (r,c) coordinagtes
        min_forward: int minimum forward movements allowed per line
        max_forward: int maximum forward movements allowed per line

    returns:
        heat_loss: dict heat_loss scores
        previous_blocks: dict mapping of blocks to their predecessor in this path
    """
    # print(f"dijkstra(CITY_MAP, {start_pos}, {min_forward}, {max_forward})")
    heap = [
        (0, start_pos, 0, "S"),
        (0, start_pos, 0, "E"),
    ]  # (cost, position, forward movements, ingress direction)

    previous_nodes = {}
    heat_loss = {}
    heat_loss[(start_pos, 0, "S")] = 0
    heat_loss[(start_pos, 0, "E")] = 0

    while heap:
        fields = ["heat_loss", "position", "forward_movements", "direction"]
        current = dict(zip(fields, heappop(heap)))
        current_position_key = (
            current["position"],
            current["forward_movements"],
            current["direction"],
        )

        if current_position_key not in previous_nodes:
            previous_nodes[current_position_key] = None

        # Early termination if we've reached the bottom-right corner
        if current["position"] == (len(CITY_MAP) - 1, len(CITY_MAP[0]) - 1):
            break

        for movement in "LRF":
            new = {}
            new["direction"] = DIRECTION_MAP[current["direction"]][movement]
            new["position"] = next_position(
                CITY_MAP, current["position"], new["direction"]
            )
            new["forward_movements"] = (
                current["forward_movements"] + 1 if movement == "F" else 1
            )

            if new["position"]:
                row, col = new["position"]
                new["heat_loss"] = current["heat_loss"] + CITY_MAP[row][col]

                # Check if this movement results in a lower heat loss
                if new["heat_loss"] < heat_loss.get(
                    (new["position"], new["forward_movements"], new["direction"]),
                    float("infinity"),
                ):
                    # Skip forward movement if it exceeds max_forward
                    if movement == "F" and new["forward_movements"] > max_forward:
                        continue
                    # Skip non-forward movement if not enough forward moves
                    if movement != "F" and current["forward_movements"] < min_forward:
                        continue

                    heat_loss[
                        (new["position"], new["forward_movements"], new["direction"])
                    ] = new["heat_loss"]
                    new_position_key = (
                        new["position"],
                        new["forward_movements"],
                        new["direction"],
                    )
                    previous_nodes[new_position_key] = current_position_key
                    heappush(
                        heap,
                        (
                            new["heat_loss"],
                            new["position"],
                            new["forward_movements"],
                            new["direction"],
                        ),
                    )

    return heat_loss, previous_nodes


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if not CITY_MAP:
        for line in input_value:
            CITY_MAP.append([int(x) for x in line.strip()])
    start = (0, 0)
    end = (len(CITY_MAP) - 1, len(CITY_MAP[0]) - 1)
    min_moves, max_moves = (0, 3)
    if part == 2:
        min_moves, max_moves = (4, 10)

    heat_loss_results, _ = dijkstra(start, min_moves, max_moves)
    min_heat_loss_key = None
    for key, path_heat_loss in heat_loss_results.items():
        (position, _, _) = key
        # ((12, 11), 0, 'S'): 131

        if position == end:
            if not min_heat_loss_key:
                min_heat_loss_key = key
            elif path_heat_loss < heat_loss_results[min_heat_loss_key]:
                min_heat_loss_key = key

    return heat_loss_results.get(min_heat_loss_key, None)


YEAR = 2023
DAY = 17
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
