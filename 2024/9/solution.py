"""
Advent Of Code 2024 day 9

Part 1, I was able to solve with simple logic, and I wasn't happy with the time.
I rewrote compress_filesystem to map out all the spaces first instead of looking up
the next space each time.  That dropped it from 24 seconds to 0.024 seconds.

Part 2, I missed one simple check, or I would have had it the first time.
My initial version did not check to see if space['idx'] was to the left of
file['idx'], which at least caused file 17 to move to the right (likely others).
Fixing this for file 17 got the right answer, and it runs in 2.2 seconds.  So,
I;m happy for now.

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


def read_file_map(file_map):
    """Function to read file_map"""
    filesystem = []
    file_id = 0
    counter = 0
    for char in file_map:
        value = int(char)
        for _ in range(value):
            if counter % 2 == 0:
                filesystem.append(file_id)
            else:
                filesystem.append(".")
        if counter % 2 == 0:
            file_id += 1
        counter += 1
    return filesystem


def compress_filesystem(filesystem):
    """Function to compress the filesystem, improved"""
    space_indexes = [i for i, value in enumerate(filesystem) if value == "."]
    space_idx = 0

    for idx in range(len(filesystem) - 1, -1, -1):
        if isinstance(filesystem[idx], int) and space_indexes[space_idx] < idx:
            filesystem[space_indexes[space_idx]] = filesystem[idx]
            filesystem[idx] = "."
            space_idx += 1
            if not space_idx < len(space_indexes):
                space_indexes = [
                    i for i, value in enumerate(filesystem) if value == "."
                ]
    return filesystem


def map_filesystem(filesystem):
    """Function to map filesystem into spaces and files"""
    spaces = []
    files = []
    last = "."
    for idx, value in enumerate(filesystem):
        if isinstance(value, int):
            if last != value:
                current = {"idx": idx, "length": 1, "id": value}
                files.append(current)
            else:
                current["length"] += 1
            last = value
        else:
            if isinstance(last, int):
                current = {"idx": idx, "length": 1}
                spaces.append(current)
            else:
                current["length"] += 1
            last = "."
    return spaces, files


def compress_filesystem_2(filesystem):
    """Function to compress filesystem by moving files instead of blocks"""
    spaces, files = map_filesystem(filesystem)
    for file in reversed(files):
        for space in spaces:
            if space["idx"] > file["idx"]:
                continue
            if space["length"] >= file["length"]:
                for idx in range(space["idx"], space["idx"] + file["length"]):
                    filesystem[idx] = file["id"]
                for idx in range(file["idx"], file["idx"] + file["length"]):
                    filesystem[idx] = ""
                file["idx"] = space["idx"]
                space["length"] -= file["length"]
                space["idx"] += file["length"]
                break
    return filesystem


def checksum_filesystem(filesystem):
    """function to calculate filesystem checksum"""
    total = 0
    for idx, value in enumerate(filesystem):
        if isinstance(value, int):
            total += idx * value
    return total


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    files = read_file_map(input_value)
    if part == 1:
        files = compress_filesystem(files)
    else:
        files = compress_filesystem_2(files)
    checksum = checksum_filesystem(files)
    return checksum


YEAR = 2024
DAY = 9
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
