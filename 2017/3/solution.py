"""
Advent Of Code 2017 day 3

This one was a bit more fun.  I went with a more mathematical solution for part 1,
and that didn't work well for part 2. So I tried building a traversal routine to
make the grid, but that was too slow for part 1.  So taking different approaches
for each part.

"""

# import system modules
import logging
import sys

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import manhattan_distance, Grid  # pylint: disable=import-error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# x/y constants
X = 0
Y = 1


def get_target_coordinates(target):
    """
    Part 1 solution.  Calculates values instead of building large grid
    """
    # init total, n and new
    total = 1
    counter = 1
    new = 0
    # loop until we find our target
    while total < target:
        # step n up by 2
        counter += 2
        # count of items for this layer
        new = (counter - 1) * 4
        # total count
        total += new
    # find lower right hand corner
    corner = counter // 2
    point = [corner, -1 * corner]
    # get difference between lower right hand corner and target
    diff = total - target
    # if diff is < counter, then target is on the bottom row
    if diff < counter:
        offset = diff
        point[X] -= offset
    # if diff is in the next counter-2 then target is on the left side
    elif diff < counter + (counter - 2):
        offset = diff - counter
        point[X] -= counter - 1
        point[Y] += offset + 1
    # if diff is in the next counter, then target is on the top row
    elif diff < counter * 2 + (counter - 2):
        offset = diff - (counter + (counter - 2))
        point[X] -= counter - 1
        point[X] += offset
        point[Y] *= -1
    # target must be on the right side
    else:
        offset = diff - (counter * 2 + (counter - 2))
        point[Y] += (counter - 2) - offset
    # return target point
    return tuple(point)


def traverse(target):
    """
    Part 2 solultions, builds out grid so we can evaluate neighbors
    """
    grid = Grid(grid_map=[[1]], type="infinite")
    logger.debug("grid:\n%s", grid)
    current_pos = (0, 0)
    current_value = 1
    while current_value <= target:
        neighbors = grid.get_neighbors(point=current_pos, diagonals=True)
        logger.debug("neighbors: %s", neighbors)
        for k, v in neighbors.items():
            logger.debug("  %s: %s = %s", k, v, grid.map.get(v))
        neighbor_values = {
            k: grid.map.get(v)
            for k, v in neighbors.items()
            if grid.map.get(v) is not None
        }
        logger.debug("neighbor values: %s", neighbor_values)
        if not neighbor_values:
            current_value = 1
            current_pos = neighbors["e"]
            grid.set_point(current_pos, current_value)
            grid.update()
            logger.debug("grid:\n%s", grid)
            continue
        current_value = sum(neighbor_values.values())
        grid.set_point(current_pos, current_value)
        grid.update()
        logger.debug("grid:\n%s", grid)
        key = ".".join(sorted(neighbor_values.keys()))
        logger.debug("key: %s", key)
        if key in ["w", "nw.w", "nw.s.sw.w", "s.sw.w"]:
            current_pos = neighbors["n"]
            continue
        if key in ["s.sw", "e.s.se", "e.s.se.sw"]:
            current_pos = neighbors["w"]
            continue
        if key in ["e.se", "e.n.ne", "e.n.ne.se"]:
            current_pos = neighbors["s"]
            continue
        if key in ["n.ne", "n.ne.nw.w", "n.nw.w"]:
            current_pos = neighbors["e"]
            continue
    return current_value


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        # get target point
        point = get_target_coordinates(int(input_value))
        # return manhattan distance to the center
        return manhattan_distance(point, (0, 0))
    # return mem_map traversal
    return traverse(int(input_value))


YEAR = 2017
DAY = 3
input_format = {
    1: "text",
    2: "text",
}

funcs = {
    1: solve,
    2: solve,
}

SUBMIT = False

if len(sys.argv) > 1 and sys.argv[1].lower() == "submit":
    SUBMIT = True

if __name__ == "__main__":
    aoc = AdventOfCode(year=YEAR, day=DAY, input_formats=input_format, funcs=funcs)
    aoc.run(submit=SUBMIT)
