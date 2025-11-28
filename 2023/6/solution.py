"""
Advent Of Code 2023 6 6

"""

# import system modules
import sys
import logging

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251128"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.debug("Advent of Code Template Version %s", TEMPLATE_VERSION)

def parse_input2(data):
    # Split the data into lines
    lines = data.strip().replace(' ','').split('\n')

    # Split each line by whitespace and remove the first element (the label)
    time_values = [int(value) for value in lines[0].split(':')[1:]]
    distance_values = [int(value) for value in lines[1].split(':')[1:]]

    # Combine the time and distance values into a list of tuples
    time_distance_pairs = list(zip(time_values, distance_values))
    return time_distance_pairs

def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')

    # Split each line by whitespace and remove the first element (the label)
    time_values = [int(value) for value in lines[0].split()[1:]]
    distance_values = [int(value) for value in lines[1].split()[1:]]

    # Combine the time and distance values into a list of tuples
    time_distance_pairs = list(zip(time_values, distance_values))
    return time_distance_pairs


def solve(input_value, _):
    """
    Function to solve puzzle
    """
    retval = 1;
    # foreach pair
    for time, distance in input_value:
        wins=0
        for ms in range(1,time):
            if ms*(time-ms) > distance:
                wins+=1
        retval*=wins
    return retval


YEAR = 2023
DAY = 6
input_format = {
    1: parse_input,
    2: parse_input2,
}

funcs = {
    1: solve,
    2: solve,
}

SUBMIT = False

if len(sys.argv) > 1 and sys.argv[1].lower() == "submit":
    SUBMIT = True

if __name__ == "__main__":
    logger.debug("Starting Advent of Code %d Day %d", YEAR, DAY)
    aoc = AdventOfCode(year=YEAR, day=DAY, input_formats=input_format, funcs=funcs)
    logger.debug("Running Advent of Code %d Day %d", YEAR, DAY)
    aoc.run(submit=SUBMIT)
