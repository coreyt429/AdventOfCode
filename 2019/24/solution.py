"""
Advent Of Code 2019 day 24

part 1 is working

part 2, gets 94 instead of 99 on the test data, and 2050 which is too high
on the puzzle data

Review rules, to be sure we are handling neighbors in the next level correctly
Issue has to be with neighbor rules, I'm certain.

Okay, I had tripped myself up with a couple typos in the neighbor rules. After
clearing those up and prepopulating the -1 and 1 layers as empty, I now
get the correct answer.  I believe the issue with not prepopulating the next layers
is that in the first generation the neighbors that exist in -1 and 1 are not getting
evaluated.  After that, the defaultdict should be creating the neighbor points before
they could possibly be infested.

I started off using Grid() for this which worked for part 1.  For part 2, the
added neighbor rules made Grid() over complicated, so I just went with a
defaultdict (note, Grid() should probably be converted to user defaultdict as well).

This would have gone smoothly if it weren't for a few misses in my code.  The method
was sound, I just had incorrect values for some of the points due to copy/paste without
followup edit.

"""

# import system modules
import logging
import argparse
from collections import defaultdict

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def get_outer_neighbors(point, part):
    """
    Function to get neighbors from outer level grid for edge squares
    """
    x_val, y_val, z_val = point
    neighbors = []
    if part == 2:
        if x_val == 0:  # left
            neighbors.append((1, 2, z_val - 1))
        elif x_val == 4:  # right
            neighbors.append((3, 2, z_val - 1))
        if y_val == 0:  # top
            neighbors.append((2, 1, z_val - 1))
        elif y_val == 4:  # bottom
            neighbors.append((2, 3, z_val - 1))
    return neighbors


def get_inner_neighbors(point, part=1):
    """
    Funtion to get neighbors from inner grid
    """
    x_val, y_val, z_val = point
    neighbors = []
    if part == 2:
        # get outside edge of next layer down
        # (1,2) left
        if x_val == 1 and y_val == 2:
            new_x = 0
            for new_y in range(5):
                neighbors.append((new_x, new_y, z_val + 1))
        # (3,2) right
        if x_val == 3 and y_val == 2:
            new_x = 4
            for new_y in range(5):
                neighbors.append((new_x, new_y, z_val + 1))
        # (2,1) top
        if x_val == 2 and y_val == 1:
            new_y = 0
            for new_x in range(5):
                neighbors.append((new_x, new_y, z_val + 1))
        # (2,3) bottom
        if x_val == 2 and y_val == 3:
            new_y = 4
            for new_x in range(5):
                neighbors.append((new_x, new_y, z_val + 1))
    return neighbors


def get_neighbors(point, part=1):
    """
    Function to get points neighboring a specified point
    """
    # print(f"get_neighbors({point},{part})")
    x_val, y_val, z_val = point
    neighbors = []
    # if z_val != 0 and outside edge
    if part == 2:
        neighbors.extend(get_outer_neighbors(point, part))
    for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x = x_val + offset[0]
        new_y = y_val + offset[1]
        if 0 <= new_x < 5 and 0 <= new_y < 5:
            # if neighbor is (2, 2, ?)
            if part == 2 and new_x == 2 and new_y == 2:
                neighbors.extend(get_inner_neighbors(point, part))
            else:
                neighbors.append((new_x, new_y, z_val))
    # print(f"get_neighbors3({point},{part}): {len(neighbors)} {neighbors}")
    return neighbors


def load_data(lines):
    """
    Function to load input data
    into a defaultdict keyed on tuple(x,y,z)
    """
    grid = defaultdict(lambda: ".")
    z_val = 0
    for y_val, line in enumerate(lines):
        for x_val, char in enumerate(line):
            grid[(x_val, y_val, z_val)] = char
    return grid


def next_generation(grid, part):
    """
    Function to build next generation of bugs
    """
    new_grid = defaultdict(lambda: ".")
    sorted_keys = sorted(grid.keys(), key=lambda k: (k[2], k[1], k[0]))
    for point in sorted_keys:
        # print(f"Checking point {point}: {grid[point]}")
        if part == 2:
            x_val, y_val, _ = point
            if x_val == y_val == 2:
                # print(f"  {point}: middle '?'")
                new_grid[point] = "?"
                continue
        value = grid[point]
        neighbors = get_neighbors(point, part)
        # print(f"  neighbors: {neighbors}")
        count = 0
        for neighbor in neighbors:
            if part == 2:
                x_val, y_val, _ = neighbor
                if x_val == y_val == 2:
                    new_grid[neighbor] = "?"
                    continue
            if neighbor not in grid:
                new_grid[neighbor] = "."
            # print(f"  neighbor: {neighbor} {grid[neighbor]}")
            if grid[neighbor] == "#":
                count += 1
        # print(f"  count: {count}")
        new_value = "."
        # A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
        if value == "#" and count == 1:
            new_value = "#"
        # An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
        if value in ".?" and count in (1, 2):
            new_value = "#"
        # print(f"  new_value: {new_value}")
        new_grid[point] = new_value
    return new_grid


def print_grid(grid):
    """
    Function to print 3d layered grids for part 2
    """
    sorted_keys = sorted(grid.keys(), key=lambda k: (k[2], k[1], k[0]))
    boundaries = {}
    for axis in "xyz":
        boundaries[axis] = {"min": float("infinity"), "max": 0}
    for point in sorted_keys:
        for idx, axis in enumerate("xyz"):
            boundaries[axis]["min"] = min(boundaries[axis]["min"], point[idx])
            boundaries[axis]["max"] = max(boundaries[axis]["max"], point[idx])
    # print(boundaries)
    for z_val in range(boundaries["z"]["min"], boundaries["z"]["max"] + 1):
        print(f"Depth {z_val}:")
        for y_val in range(boundaries["y"]["min"], boundaries["y"]["max"] + 1):
            for x_val in range(boundaries["x"]["min"], boundaries["x"]["max"] + 1):
                print(grid[(x_val, y_val, z_val)], end="")
            print()
        print()


def grid_string(grid):
    """
    String representation of grid dict
    """
    new_string = ""
    sorted_keys = sorted(grid.keys(), key=lambda k: (k[2], k[1], k[0]))
    for point in sorted_keys:
        new_string += grid[point]
    return new_string


def calculate_biodiversity(grid_text):
    """
    Function to calculate biodiveristy
    """
    line = grid_text.replace("\n", "")
    # print(line)
    idx = 0
    biodiversity = 0
    while idx < len(line):
        try:
            idx = line.index("#", idx)
        except ValueError:
            break
        biodiversity += 2**idx
        idx += 1
        # print(idx, biodiversity)
    return biodiversity


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    grid = load_data(input_value)
    if part == 1:
        seen = set()
        seen.add(grid_string(grid))
        while True:
            grid = next_generation(grid, part)
            grid_text = grid_string(grid)
            if grid_text in seen:
                # print(f"First repeat:\n{grid_text}\n")
                break
            seen.add(grid_text)
            # print(f"After {minute} minutes:\n{grid}\n")
        return calculate_biodiversity(grid_text)
    # Part 2
    # prepopulate layers -1 and 1
    # with the test data, not doing this, caused the bugs
    # to never spread past layer 0.
    # puzzle data doesn't seem to do this, and adding to see
    # if it corrects the issue we are seeing for some other reason
    # yes, this was the missing piece.  Without prepopulating these
    # layers I was getting an answer of 2001, with them prepopulated
    # I get the correct answer of 1928
    for z_val in [-1, 1]:
        for y_val in range(5):
            for x_val in range(5):
                grid[(x_val, y_val, z_val)] = "?"
    for _ in range(200):
        grid = next_generation(grid, part)
    sorted_keys = sorted(grid.keys(), key=lambda k: (k[2], k[1], k[0]))
    count = 0
    for point in sorted_keys:
        if grid[point] == "#":
            count += 1
        # print(f"{point}: {grid[point]}")
    # 2050 is too high
    # 2001 is too high
    return count


YEAR = 2019
DAY = 24
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
