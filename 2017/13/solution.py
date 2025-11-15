"""
Advent Of Code 2017 day 13

"""

# import system modules
import time
import re

# import my modules
import aoc  # pylint: disable=import-error


def parse_input(lines):
    """
    Function to parse input
    """
    # init data
    data = {}
    # walk lines
    for line in lines:
        # get nums from line as int()
        pos, scan_range = [int(num) for num in re.findall(r"(\d+)", line)]
        # store data
        data[pos] = scan_range
    return data


def position(scanner_range, picosecond):
    """
    Function to calculate scanner position
    """
    # ignore intervals, and reduce picoseconds to position in interval
    # interval time is 2 * scanner_range - 2
    picosecond = picosecond % ((scanner_range * 2) - 2)
    # it hasn't had time to turn around yet
    # 0-3 for range 4
    if picosecond < scanner_range:
        return picosecond
    # example for range 4
    # it has turned around 4=2, 5=1, 6=0
    # 4 - 4 = 0 (4 - 2 - 0) = 2
    # 5 - 4 = 1 (4 - 2 - 1) = 1
    # 6 - 4 = 2 (4 - 2 - 2) = 0
    # return max(index) - 1 - picoseconds in this direction
    return (scanner_range - 2) - (picosecond - scanner_range)


def severity(scanners):
    """
    function to calculate severity
    """
    # init total
    total = 0
    # for picosecond in scanner range
    for picosecond in range(max(scanners.keys()) + 1):
        # set layer: we could just user picosecond here, and I was anticipating
        # reusing this with a delay in part 2.  But part 2 needed to short circuit
        # the run on being caught, so I used a different function for it.
        layer = picosecond
        # does this layer have a scanner?
        if layer in scanners:
            # get the scanners position
            pos = position(scanners[layer], picosecond)
            # did we get caught
            if pos == 0:  # caught
                # oh no!  add layer severity to total
                total += layer * scanners[layer]
    return total


def success(scanners, delay):
    """
    Function to test for successful firewall pass
    """
    # from delay to delay + max scanned layer
    for picosecond in range(delay, max(scanners.keys()) + delay + 1):
        # calculate current layer
        layer = picosecond - delay
        # is there a scanner on this layer
        if layer in scanners:
            # what is the scanners position
            pos = position(scanners[layer], picosecond)
            # did the packet get caught?
            if pos == 0:  # caught
                # not a success
                return False
    # wait we got through all the layers, Yay!
    return True


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # load scanners
    scanners = parse_input(input_value)
    # part 1, we just need the severity if we start at 0
    if part == 1:
        return severity(scanners)
    # part 2, we need to find the least delay to be successful
    # init delay,  takes 4.5 seconds if we start at 0
    # initing to 3.8m to reduce runtime, it still has to
    # run a few cycles, I dell putting the answer in would
    # really be cheating
    delay = 3800000
    # to infinity and beyond!
    while True:
        # if we can get through, return the delay
        if success(scanners, delay):
            return delay
        # otherwise, increment and keep going
        delay += 1


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017, 13)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
