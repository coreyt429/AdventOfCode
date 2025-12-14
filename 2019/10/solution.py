"""
Advent Of Code 2019 day 10

Focus today was on the math.  As part of my effort to improve my rusty math skills,
I started with working out on paper how to determine if points were colinear, and calculating
the distance between points.  These were the tools I needed to solve part 1.

Part 2, introduced a bit of trigonometry.  To get the bearing I needed to get the
arctangent of delta(y)/delta(x), then adjust by 90 degrees to be relative the the y axis
instead of the x axis.  This worked well for my test dataset centered on (0, 0).  Running
against the problem test data, I quickly realized that the calculations I was doing were for
cartesian coordinates not screen coordinates.  So I launched down this long rabbit whole of
moving the whole thing to cartesian which worked great.  The answer needs to be in screen :(
Converting the final answer to screen was not working well, so I rethought the whole thing.
Backed out the changes so everything was screen coordinates.  Then reworked the bearing function
to account for screen coordinates.

"""

# import system modules
import logging
import argparse
import math

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid, sort_collinear_points, are_collinear  # pylint: disable=import-error

X = 0
Y = 1

# dict to store answers
answer = {1: None, 2: None}

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def bearing(p_1, p_2):
    """
    Function to calculate bearing of p_2 from p_1, accounting for screen coordinates
    """
    # delta x stays the same
    d_x = p_2[X] - p_1[X]
    # delta y needs to be inverted for screen coordinates
    d_y = -(p_2[Y] - p_1[Y])
    # get arctangent in radians
    radians = math.atan2(d_y, d_x)
    # convert to degrees
    degrees = math.degrees(radians)
    # Adjust for relative to the Y axis (bearing)
    degrees = 90 - degrees
    # Ensure bearing is in 0-360 range
    if degrees < 0:
        degrees += 360
    return degrees


def get_sorted_points(line_list, origin):
    """
    Function to sort the a list of lines by the bearing of the
    first poin in the line from an origin
    """
    lines = []
    for line in line_list:
        lines.append(sort_collinear_points(line + [origin]))
    # init new_lines
    new_lines = []
    # iterate over lines
    for line in lines:
        # if origin is on the front end, just remove it and leave line alone
        if line[0] == origin:
            line.pop(0)
            new_lines.append(line)
            continue
        # if origin is on the back end, remove it, and reverse the line
        if line[-1] == origin:
            line.pop(-1)
            new_lines.append(line[::-1])
            continue
        # Find the index of the origin point in the line
        index = line.index(origin)
        # reverse the line leading to origin
        new_lines.append(line[:index][::-1])
        # add the line after origin
        new_lines.append(line[index + 1 :])

    new_lines.sort(key=lambda line: bearing(origin, line[0]))
    sorted_points = []
    added = True
    while added:
        added = False
        for line in new_lines:
            if not line:
                continue
            sorted_points.append(line.pop(0))
            added = True
    return sorted_points


def find_best_position(grid):
    """
    Function to find the position in the map that can monitor
    the most asteroids

    Args:
        grid: Grid()

    Returns:
        best_position: tuple(x, y) coordinate of the best position
        most_detected: int() number of asteroids monitored
        lines_by_point: list() of list() of tuple(x, y) lines that include point

    """
    # init lines_by_point
    lines_by_point = {}
    # get points of asteroid locations
    points = [point for point in grid if grid.get_point(point) == "#"]
    # iterate over points
    for p_1 in points:
        # init lines list for point
        lines = []
        # iterate over points
        for p_2 in points:
            # don't include self
            if p_1 == p_2:
                continue
            # init found
            found = False
            # iterate over existing lines
            for line in lines:
                # if p_2 is on the same line as p_1 and the first entry in line
                if are_collinear(p_1, p_2, line[0]):
                    # add p_2 to line
                    line.append(p_2)
                    # set found
                    found = True
                    # stop processing lines
                    break
            # if we didn't find a mathing line, create one
            if not found:
                # add new line
                lines.append([p_2])
        # save lines
        lines_by_point[p_1] = lines
    # init most_detected and best_position
    most_detected = 0
    best_position = None
    # iterate over points
    for point in points:
        # add 1 for each line:
        detected = len(lines_by_point[point])
        # iterate over lines
        for line in lines_by_point[point]:
            # if line has more than two points including point
            if len(line) > 1:
                # sort line to determine the position of point
                new_line = sort_collinear_points(line + [point])
                # if point isn't on the end of the line
                if point not in [new_line[0], new_line[-1]]:
                    # add an extra detected, since it can monitor 2 in this line
                    detected += 1
        # do we have a new winner
        if detected > most_detected:
            # set winner
            most_detected = detected
            best_position = point
    # return values
    return best_position, most_detected, lines_by_point


def _compute_answers(input_value):
    """
    Compute and cache both part answers.
    """
    grid = Grid(input_value, use_overrides=False)
    best, count, lines_by_point = find_best_position(grid)
    sorted_points = get_sorted_points(lines_by_point[best], best)
    point = sorted_points[199]
    answer[1] = count
    answer[2] = (100 * point[0]) + point[1]


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if answer[part] is None:
        _compute_answers(input_value)
    return answer[part]


def parse_input(input_text):
    """
    Parse the asteroid map lines.
    """
    return [line.rstrip("\n") for line in input_text.splitlines() if line.strip()]


YEAR = 2019
DAY = 10
input_format = {
    1: parse_input,
    2: parse_input,
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
