"""
Advent Of Code 2015 day 6

"""

# import system modules
import logging
import argparse
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

# constants for x/y
X = 0
Y = 1
# constants for ON and OFF
OFF = 0
ON = 1


def parse_input(input_text):
    """
    Function to parse input
    """
    commands = []
    pattern_parse = re.compile(r"(.*) (\d+),(\d+) through (\d+),(\d+)")
    for line in input_text.strip().splitlines():
        if not line:
            continue
        result = pattern_parse.findall(line)
        row = []
        for item in result[0]:
            if item.isdigit():
                row.append(int(item))
            else:
                row.append(item)
        # pylint: disable=unbalanced-tuple-unpacking
        command, x_start, y_start, x_end, y_end = row
        commands.append(
            {"command": command, "rect": [(x_start, y_start), (x_end, y_end)]}
        )
    return commands


def init_light_grid(height=1000, width=1000):
    """
    Function to initialize the light grid
    """
    return [[0 for _ in range(width)] for _ in range(height)]


def print_lights(lights):
    """
    Function to print light_grid
    """
    for row in lights:
        print("".join([str(num) for num in row]))


def count_lights(lights):
    """
    Function to count lights that are on
    """
    retval = 0
    for row in lights:
        for light in row:
            if light == ON:
                retval += 1
    return retval


def count_brightness(lights):
    """
    Function to count brightness
    """
    retval = 0
    for row in lights:
        for light in row:
            retval += light
    return retval


def toggle_lights(lights, rect):
    """
    Function to toggle lights
    """
    start, end = rect
    for x_val in range(start[X], end[X] + 1):
        for y_val in range(start[Y], end[Y] + 1):
            if lights[x_val][y_val] == ON:
                lights[x_val][y_val] = OFF
            else:
                lights[x_val][y_val] = ON


def set_lights(lights, status, rect):
    """
    Function to set lights
    """
    start, end = rect
    for x_val in range(start[X], end[X] + 1):
        for y_val in range(start[Y], end[Y] + 1):
            lights[x_val][y_val] = status


def adjust_lights(lights, status, rect):
    """
    Function to adjust lights
    """
    start, end = rect
    for x_val in range(start[X], end[X] + 1):
        for y_val in range(start[Y], end[Y] + 1):
            lights[x_val][y_val] += status
            if lights[x_val][y_val] < OFF:
                lights[x_val][y_val] = OFF


def part1(parsed_data, _part=None):
    """
    Function to solve part 1
    """
    lights = init_light_grid()
    for command in parsed_data:
        if command["command"] == "turn on":
            set_lights(lights, ON, command["rect"])
        elif command["command"] == "turn off":
            set_lights(lights, OFF, command["rect"])
        elif command["command"] == "toggle":
            toggle_lights(lights, command["rect"])
    return count_lights(lights)


def part2(parsed_data, _part=None):
    """
    Function to solve part 2
    """
    lights = init_light_grid()
    # print('Before:')
    # print_lights(lights)
    for command in parsed_data:
        if command["command"] == "turn on":
            adjust_lights(lights, 1, command["rect"])
        elif command["command"] == "turn off":
            adjust_lights(lights, -1, command["rect"])
        elif command["command"] == "toggle":
            adjust_lights(lights, 2, command["rect"])
    # print('after:')
    # print_lights(lights)
    return count_brightness(lights)


YEAR = 2015
DAY = 6
input_format = {
    1: parse_input,
    2: parse_input,
}

funcs = {
    1: part1,
    2: part2,
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
