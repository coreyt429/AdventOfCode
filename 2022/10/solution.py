"""
Advent Of Code 2022 day 10

This one was mostly about reading the instructions and getting the timing right.

Added screen reader that was improved in 2021.13 to get part 2 result in a useable
manner.


"""

# import system modules
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def check_cycle(cycle, register, part=1):
    """Function to check cycle state"""
    if part == 2:
        # I initially missed that cycle 1 correlated to pixel 0, so subtract 1
        # then reset for each line so cycle 41, pixel = 0
        pixel = (cycle - 1) % 40
        char = "."
        # light pixel if it is within 3 spaces centered on register
        if abs(pixel - register) < 2:
            char = "#"
        return char
    if cycle in [20, 60, 100, 140, 180, 220]:
        return cycle * register
    return 0


def read_screen(pixels):
    """
    Function to print lcd screen
    sourced from 2016.8, 2021.13
    """
    message = ""
    line_size = 40
    for i in range(0, len(pixels), line_size):
        message += pixels[i : i + line_size] + "\n"
    message = message.replace(".", " ")
    # Split the string into lines
    lines = message.splitlines()
    # pulling the data from grid, did not space pad the end of the last
    # letter. This caused it to not match char_map
    for idx, _ in enumerate(lines):
        lines[idx] += " "

    # Define the width and height of each character
    char_width = 5
    char_height = 6  # Including the space between rows

    # Calculate the number of characters in the message
    # had to update with the +1 2016.8 must have had an even
    # number of characters
    # 2022.10 has an even number of characters, and this didn't break it
    # so it looks like this is the way!
    num_chars = (len(lines[0]) + 1) // char_width

    # Initialize the result string
    result = ""
    char_map = {
        " ##  #  # #  # #### #  # #  # ": "A",
        "#### #    ###  #    #    #### ": "E",
        " ##  #  # #    # ## #  #  ### ": "G",
        "#  # #  # #### #  # #  # #  # ": "H",
        "#    #    #    #    #    #### ": "L",
        " ##  #  # #  # #  # #  #  ##  ": "O",
        "###  #  # #  # ###  #    #    ": "P",
        "###  #  # #  # ###  # #  #  # ": "R",
        "#  # #  # #  # #  # #  #  ##  ": "U",
        "#   ##   # # #   #    #    #  ": "Y",
        "#### #    ###  #    #    #    ": "F",
        "  ##    #    #    # #  #  ##  ": "J",
    }
    # Iterate through each character
    for i in range(num_chars):
        # Extract the 5x5 grid for this character
        char_grid = [line[i * char_width : (i + 1) * char_width] for line in lines]
        # Convert the grid to a single string for easier comparison
        char_string = "".join(char_grid)
        # the last O was missing a couple spaces
        while len(char_string) < char_height * char_width:
            char_string += " "
        # match to char_map
        result += char_map.get(char_string, "?")
        # 2022.10 added printing of missing characters to aid in updating
        if result[-1] == "?":
            print(f"{char_string} == ?")
    return result


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    register_x = 1
    cycles = 0
    result = 0
    if part == 2:
        result = ""
    for line in input_value:
        cycles += 1
        if line == "noop":
            result += check_cycle(cycles, register_x, part)
            continue
        result += check_cycle(cycles, register_x, part)
        num = int(line.split(" ")[1])
        cycles += 1
        result += check_cycle(cycles, register_x, part)
        register_x += num
    if part == 2:
        result = read_screen(result)
    return result


YEAR = 2022
DAY = 10
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
