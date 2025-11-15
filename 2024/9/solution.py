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
import time

# import my modules
import aoc  # pylint: disable=import-error


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
        # increment file_id after adding a file
        if counter % 2 == 0:
            file_id += 1
        counter += 1
    return filesystem


def compress_filesystem_original(filesystem):
    """Function to compress the filesystem"""
    for idx in range(len(filesystem) - 1, -1, -1):
        if isinstance(filesystem[idx], int):
            idx_space = filesystem.index(".")
            if idx_space < idx:
                filesystem[idx_space] = filesystem[idx]
                filesystem[idx] = "."
    return filesystem


def compress_filesystem(filesystem):
    """Function to compress the filesystem, improved"""
    # Precompute all space indexes
    space_indexes = [i for i, value in enumerate(filesystem) if value == "."]
    # Pointer to track the next available space
    space_idx = 0

    # Iterate from right to left, moving blocks into available spaces
    for idx in range(len(filesystem) - 1, -1, -1):
        if isinstance(filesystem[idx], int) and space_indexes[space_idx] < idx:
            # Move block to the next available space
            filesystem[space_indexes[space_idx]] = filesystem[idx]
            filesystem[idx] = "."
            # Move to the next space
            space_idx += 1
            # this condition shouldn't happen, but should be accounted for.
            if not space_idx < len(space_indexes):
                # recompute all space indexes
                space_indexes = [
                    i for i, value in enumerate(filesystem) if value == "."
                ]
    return filesystem


def map_filesystem(filesystem):
    """Function to map filesystem into spaces and files"""
    spaces = []
    files = []
    last = "."
    # iterate over filesystem
    for idx, value in enumerate(filesystem):
        # files
        if isinstance(value, int):
            # new file?
            if last != value:
                current = {"idx": idx, "length": 1, "id": value}
                files.append(current)
            else:
                current["length"] += 1
            last = value
        # spaces
        else:
            # new space?
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
    # iterate over files from right to left
    for file in reversed(files):
        # iterate over spaces from left to right
        for space in spaces:
            if space["idx"] > file["idx"]:
                continue
            # if file will fit in space
            if space["length"] >= file["length"]:
                # swap file and space
                for idx in range(space["idx"], space["idx"] + file["length"]):
                    filesystem[idx] = file["id"]
                for idx in range(file["idx"], file["idx"] + file["length"]):
                    filesystem[idx] = ""
                # update file index so we can check it
                file["idx"] = space["idx"]
                # reduce space size by file
                space["length"] -= file["length"]
                # move space pointer forward
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
        # 8491540479687 too high
        # 8491540479686 too high, just guessed off by one, back to examining output
    checksum = checksum_filesystem(files)
    return checksum


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2024, 9)
    input_data = my_aoc.load_text()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 6288707484810, 2: 6311837662089}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
