"""
Advent Of Code 2020 day 13

Part 1 was easy.  Part 2, I played with generators some, and could
solve the test data relatively quickly.  Way too slow in the input.

ChatGPT suggested Chinese Remainder Theorem (CRT), and that proved to
be efficient.  Took be a bit to wrap my head around it, and now I
feel like I understand it a bit.  Will I remember this in the future
probably not :(

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


def find_next_departure(input_value):
    """function to solve part 1"""
    start_minute = int(input_value[0])
    busses = [int(bus) for bus in input_value[1].split(",") if bus != "x"]
    min_next_depart = float("infinity")
    min_bus = None
    for bus in busses:
        last_depart = (start_minute // bus) * bus
        next_depart = last_depart + bus
        # is the bus here now?
        if last_depart == start_minute:
            min_next_depart = start_minute
            min_bus = bus
            break
        if next_depart < min_next_depart:
            min_next_depart = next_depart
            min_bus = bus
    return (min_next_depart - start_minute) * min_bus


def find_cascading_departure(bus_string):
    """function to solve part 2"""
    busses = {}
    generators = {}
    current = {}
    for idx, bus in enumerate(bus_string.split(",")):
        if bus.isdigit():
            busses[idx] = int(bus)
            generators[idx] = departure_generator(int(bus))
            current[idx] = 0

    for departure in generators[0]:
        current[0] = departure
        for bus_id, generator in generators.items():
            if bus_id == 0:
                continue
            while current[bus_id] < current[0] + bus_id:
                current[bus_id] = next(generator)
        cascade = True
        for idx, timestamp in current.items():
            if timestamp != current[0] + idx:
                cascade = False
        if cascade:
            return departure
    raise RuntimeError("No cascading departure found")


def departure_generator(bus_id):
    """Generator function for departure times"""
    idx = 0
    while True:
        yield idx * bus_id
        idx += 1


def find_earliest_cascading_departure(bus_string):
    """Function to solve part2 quickly"""
    busses = {}
    for idx, bus in enumerate(bus_string.split(",")):
        if bus.isdigit():
            busses[idx] = int(bus)
    timestamp = 0
    step = 1  # Start with a step size of 1

    for index, frequency in busses.items():
        # Find the next timestamp where (timestamp + index) % frequency == 0
        while (timestamp + index) % frequency != 0:
            timestamp += step  # Increment the timestamp by the current step size

        # Update the step size to be the least common multiple (LCM)
        # of all frequencies encountered so far
        step *= frequency
        # print(index, frequency, step, timestamp)

    return timestamp


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        return find_next_departure(input_value)
    return find_earliest_cascading_departure(input_value[1])


YEAR = 2020
DAY = 13
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
