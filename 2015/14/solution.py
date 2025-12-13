"""
Advent Of Code 2015 day 14

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

# Dancer can fly 27 km/s for 5 seconds, but then must rest for 132 seconds.

pattern_input = re.compile(
    r"(\w+) .* (\d+) km.*for (\d+) seconds.* rest for (\d+) seconds."
)


def parse_input(input_text):
    """
    Function to parse input
    """
    # dict to store reindeer data
    reindeer = {}
    # loop through lines
    for line in input_text.strip().splitlines():
        if not line:
            continue
        # match regx
        match = pattern_input.match(line)
        if match:
            # get data
            name, speed, duration, rest = match.groups()
            # store data
            reindeer[name] = {
                "speed": int(speed),
                "duration": int(duration),
                "rest": int(rest),
            }
    return reindeer


def distance_traveled(reindeer, seconds):
    """
    Function to calculate distance traveled
    """
    # Distance each reindeer travels per interval is the product of its speed and duration
    distance_per_interval = reindeer["speed"] * reindeer["duration"]
    # Cycle lendth is the sum of the reindeer's travel duration and rest period
    cycle = reindeer["rest"] + reindeer["duration"]
    # the number of intervals is the quotient of total seconds divided by cycle length
    intervals = int(seconds / cycle)
    # remainder is the remainder of total seconds divided by cycle length
    remainder = seconds % cycle
    # initialize distance
    distance = 0
    # if remainder time would be a full speed burst
    if remainder >= reindeer["duration"]:
        # increment intervals
        intervals += 1
    else:
        # increment distance by product of remainder and speed
        distance = remainder * reindeer["speed"]
    # increment distance by the distance traveled in inetervals
    return distance + (intervals * distance_per_interval)


def part1(parsed_data, _part=None):
    """
    Function to solve part 1:
        get maximum distance traveled in 2503 seconds
    """
    # max_distance traveled
    max_distance = 0
    seconds = 2503
    for stats in parsed_data.values():
        distance = distance_traveled(stats, seconds)
        max_distance = max(max_distance, distance)
    return max_distance


def part2(parsed_data, _part=None):
    """
    Function to solve part two:
        Instead, at the end of each second, he awards one point to the
        reindeer currently in the lead. (If there are multiple reindeer tied for the lead,
        they each get one point.)
    """
    seconds = 2503
    # initialize scores
    scores = {}
    for reindeer in parsed_data:
        scores[reindeer] = 0

    # for sec in  1 through 2503
    for sec in range(1, seconds + 1):
        # initialize leaders and high
        leaders = []
        high = 0
        # check each reindeer
        for name, stats in parsed_data.items():
            # get distance
            distance = distance_traveled(stats, sec)
            # if new high
            if distance > high:
                # set high
                high = distance
                # reset leaders
                leaders = [name]
            # if tie
            elif distance == high:
                # add to leaders
                leaders.append(name)
        # add 1 point to each leader
        for leader in leaders:
            scores[leader] += 1
    # return highest score
    return max(scores.values())


YEAR = 2015
DAY = 14
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
