"""
Advent Of Code 2015 day 9

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


def parse_input(input_text):
    """
    Function to parse line data
    """
    routes = []
    for line in input_text.strip().splitlines():
        if not line:
            continue
        tmp = line.split(" ")
        route = {
            "start": tmp[0],
            "end": tmp[2],
            "distance": int(tmp[4]),
        }
        routes.append(route)
    return routes


def goto(parsed_data, routes, locations, current_loc, already):
    """
    Recursive function to map route
    """
    # print(f'map,locations,{current_loc},{already}')
    visited = already + (current_loc,)
    for next_loc in locations:
        if next_loc not in visited:
            goto(parsed_data, routes, locations, next_loc, visited)
    all_visited = True
    for location in locations:
        if location not in visited:
            all_visited = False
    if all_visited:
        routes.append(list(visited))


def get_distance(mapdata, start, end):
    """
    Function to get calcultate distance
    """
    retval = -1
    for entry in mapdata:
        if entry["start"] == start and entry["end"] == end:
            retval = entry["distance"]
        elif entry["start"] == end and entry["end"] == start:
            retval = entry["distance"]
    return retval


def part1(parsed_data, _part=None):
    """
    Function to solve part 1
    """
    retval = -1

    locations = set()
    routes = []
    for route in parsed_data:
        locations.add(route["start"])
        locations.add(route["end"])
    # print(locations)
    for start in locations:
        goto(parsed_data, routes, locations, start, ())
    for route in routes:
        distance = 0
        for idx in range(len(route) - 1):
            distance += get_distance(parsed_data, route[idx], route[idx + 1])
        if retval < 0 < distance:
            retval = distance
        elif distance < retval:
            retval = distance
        # print(route,distance)
    return retval


def part2(parsed_data, _part=None):
    """
    Function to solve part 2
    """
    retval = -1

    locations = set()
    routes = []
    for route in parsed_data:
        locations.add(route["start"])
        locations.add(route["end"])
    # print(locations)
    for start in locations:
        goto(parsed_data, routes, locations, start, ())
    for route in routes:
        distance = 0
        for idx in range(len(route) - 1):
            distance += get_distance(parsed_data, route[idx], route[idx + 1])
        retval = max(retval, distance)
    return retval


YEAR = 2015
DAY = 9
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
