"""
Advent Of Code 2016 day 15

This one is not 100% in my current style, but it does produce the same output.
It is structually in the same spirit, so moving on.

"""

import re
import time
import aoc  # pylint: disable=import-error

disks = []


def parse_input(input_string):
    """
    Function to parse input
    """
    # get numbers from input_string
    match = re.findall(r"\d+", input_string)
    if match:
        # add to disks
        disks.append(tuple(int(data) for data in match))


def solve():
    """
    Function to solve puzzle
    """
    # initialize delay and drops
    delay = 0
    drops = {}
    # walk disks
    for disk in disks:
        # increment delay for each disk
        delay += 1
        # identify first clock tick of first slot
        first_slot = disk[1] - disk[3]
        # initialize drops
        drops[disk] = set()
        # This works, but causes some disks to start negative
        current_drop = first_slot - delay
        # this worked, but there has to be a better way to loop this
        # I tried a few more elegant solutions, but they were too slow
        # see jupyter notebook for other trials
        # collect the first 1100000 drop times for the disk
        while len(drops[disk]) < 1100000:
            drops[disk].add(current_drop)
            current_drop += disk[1]
    # initialize common drops, to store drops that are common to all disks
    # used the first disk as the initial common
    common_drops = drops[disks[0]]
    # walk disks again
    for disk in disks:
        # reduce common_drops to the intersection of iteself and the current disk
        common_drops = common_drops.intersection(drops[disk])
    # return the lowest value in common_drops
    return sorted(list(common_drops))[0]


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2016, 15)
    # test data
    test_data = [
        "Disc #1 has 5 positions; at time=0, it is at position 4.",
        "Disc #2 has 2 positions; at time=0, it is at position 1.",
    ]
    # load live data
    lines = my_aoc.load_lines()
    # using test data for now, comment out for live
    # lines = test_data

    for part in [1, 2]:
        # initialize disk list
        disks = []
        # parse input
        for line in lines:
            parse_input(line)
        # part 2 add disk
        if part == 2:
            disks.append((7, 11, 0, 0))
        start = time.time()
        answer = solve()
        end = time.time()
        print(f"Part {part}: {answer}, took {end - start} seconds")
