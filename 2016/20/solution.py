"""
Advent Of Code 2016 day 20

Okay, I tried the brute force method, and it was brutal.

Had to think this one through myself, and didn't resort to looking
at other answers.  Yay!!!

"""
import time
import re
import aoc # pylint: disable=import-error

def solve(lines):
    """
    Function to solve puzzle
    """
    # set max, so we can find any unblocked on the end
    # ironically, this was necessary for the sample data
    # and not for my input data
    max_value=4294967295
    # set smallest and last_smallest
    smallest = 0
    last_smallest = -1
    # regex to match input lines, on second thought, it would be more efficient
    # to parse the input into values once, and pass those to this function
    # but its already running in 0.09445691108703613 seconds so what would I gain
    pattern_range = re.compile(r'(\d+)-(\d+)')
    # clone lines into remainig
    remaining = list(lines)
    # empty allowed ip set
    allowed = set()
    # empty last blocked address
    max_blocked = 0
    # loop while we have entries in remaining
    while remaining:
        # do we have a new smallest?
        if last_smallest == smallest:
            # add it to allowe
            allowed.add(smallest)
            # update last_smallest
            last_smallest = smallest
            # increment smallest
            smallest += 1
        else:
            # update last_smallest
            last_smallest = smallest
        # clone lines from remainig
        lines = list(remaining)
        # reset remaining
        remaining = []
        # walk lines in numeric order
        for line in sorted(lines):
            # line should always match, if not bad input
            match = pattern_range.match(line)
            if match:
                # get start and end
                start = int(match.group(1))
                end = int(match.group(2))
                # is smallest blocked by this rule?
                if start <= smallest <= end:
                    # increment to end of this block + 1
                    smallest = end +1
                # is smallest smaller than the last number blocked
                if smallest < end:
                    # add to remaining for next pass
                    remaining.append(line)
                # does this rule extend the blocked range
                if end > max_blocked:
                    # update max_blocked
                    max_blocked = end
    # lastly, were there any addresses after the last block
    for addr in range(max_blocked+1,max_value+1):
        allowed.add(addr)
    # return the allowed set
    return allowed

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2016,20)
    input_lines = my_aoc.load_lines()
    # note start time
    start_time = time.time()
    # get unblocked set
    unblocked_addresses = solve(input_lines)
    # note end time
    end_time = time.time()
    # the answer to part one is the minum value in the unblocked set
    print(f"Part 1: {min(unblocked_addresses)}, took {end_time-start_time} seconds")
    # the answer to part two is the count of entries in the unblocked set
    print(f"Part 2: {len(unblocked_addresses)}")

    #Part 1: 19449262, took 0.09445691108703613 seconds
    #Part 2: 119
