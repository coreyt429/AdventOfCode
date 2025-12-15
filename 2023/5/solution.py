"""
Advent Of Code 2023 day 5

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


def parse_input(data):
    """
    parse input
    """
    almanac = {}
    data_list = [section.split(":") for section in data.split("\n\n")]
    for section in data_list:
        almanac[section[0].replace(" map", "")] = [
            line.split(" ") for line in section[1].strip().split("\n")
        ]
    for key, value in almanac.items():
        almanac[key] = [[int(num) for num in sublist] for sublist in value]
    return almanac


def check_map(seed, conversion_map):
    """
    simple brute force method for part1, takes too long for part2
    """
    for line in conversion_map:
        if line[1] <= seed < (line[1] + line[2]):
            return line[0] + (seed - line[1])
    return seed


def conversion_map_to_range(conversion_map):
    """
    Convert the input conversion map into a nested list where each item is a
    list of start, end, and amount to offset if matched, return sorted nested list
    For instance, [50, 98, 2] becomes [98, 99, -48]
    """
    conversion_list = []
    for line in conversion_map:
        conversion_list.append([line[1], (line[1] + line[2] - 1), (line[0] - line[1])])
    return sorted(conversion_list, key=lambda x: x[0])


def convert_seed_range_list(seed_range, conversion_range):
    """
    For part 2, take the seed_range and convert it to a list of ranges based
    on the conversion_range and return sorted nested list
    """
    seed_range_list = []
    curr_value = seed_range[0]
    for curr_range in conversion_range:
        if curr_value < curr_range[0]:
            seed_range_list.append([curr_value, (curr_range[0] - 1)])
            curr_value = curr_range[0]
        if curr_range[0] <= curr_value <= curr_range[1]:
            max_value = (
                curr_range[1] if not seed_range[1] <= curr_range[1] else seed_range[1]
            )
            seed_range_list.append(
                [(curr_value + curr_range[2]), (max_value + curr_range[2])]
            )
            curr_value = max_value + 1
        if curr_value - 1 == seed_range[1]:
            break
    if curr_value < seed_range[1]:
        seed_range_list.append([curr_value, seed_range[1]])
    return sorted(seed_range_list, key=lambda x: x[0])


def part1(parsed_data):
    """
    solve part 1
    """
    minimum = None
    for seed in parsed_data["seeds"][0]:
        current_id = seed
        for conversion_map in parsed_data:
            if conversion_map != "seeds":
                current_id = check_map(current_id, parsed_data[conversion_map])
        if minimum is None or int(current_id) < minimum:
            minimum = int(current_id)
    return minimum


def part2(parsed_data):
    """
    solve part 2
    """
    minimum = None
    seeds = parsed_data["seeds"][0]
    seed_pairs = [
        [seeds[i], (seeds[i] + seeds[i + 1] - 1)] for i in range(0, len(seeds), 2)
    ]
    conversion_maps = [
        conversion_map
        for conversion_map in parsed_data.keys()
        if conversion_map != "seeds"
    ]
    conversion_range_dict = {}
    for conversion_map in conversion_maps:
        conversion_range_dict[conversion_map] = conversion_map_to_range(
            parsed_data[conversion_map]
        )
    for seed_range in seed_pairs:
        curr_seed_range = [seed_range.copy()]
        for curr_conv_map in conversion_range_dict.values():
            curr_output_list = []
            for entry in curr_seed_range:
                output_list = convert_seed_range_list(entry, curr_conv_map)
                curr_output_list.append(output_list)
            curr_output_list = [
                item for sublist in curr_output_list for item in sublist
            ]
            curr_output_list = sorted(curr_output_list, key=lambda x: x[0])
            curr_seed_range = curr_output_list.copy()
        if minimum is None or curr_seed_range[0][0] < minimum:
            minimum = curr_seed_range[0][0]
    return minimum


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    data = parse_input(input_value)
    if part == 1:
        return part1(data)
    return part2(data)


YEAR = 2023
DAY = 5
input_format = {
    1: "text",
    2: "text",
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
