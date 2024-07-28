"""
Advent Of Code 2015 day 14

"""
# import system modules
import time
import re

# import my modules
import aoc # pylint: disable=import-error

#Dancer can fly 27 km/s for 5 seconds, but then must rest for 132 seconds.

pattern_input = re.compile(r'(\w+) .* (\d+) km.*for (\d+) seconds.* rest for (\d+) seconds.')

def parse_input(lines):
    """
    Function to parse input
    """
    # dict to store reindeer data
    reindeer = {}
    # loop through lines
    for line in lines:
        # match regx
        match = pattern_input.match(line)
        if match:
            # get data
            name, speed, duration, rest = match.groups()
            # store data
            reindeer[name] = {
                'speed': int(speed),
                'duration': int(duration),
                'rest': int(rest)
            }
    return reindeer

def distance_traveled(reindeer, seconds):
    """
    Function to calculate distance traveled
    """
    # Distance each reindeer travels per interval is the product of its speed and duration
    distance_per_interval = reindeer['speed'] * reindeer['duration']
    # Cycle lendth is the sum of the reindeer's travel duration and rest period
    cycle = reindeer['rest'] + reindeer['duration']
    # the number of intervals is the quotient of total seconds divided by cycle length
    intervals = int(seconds / cycle)
    # remainder is the remainder of total seconds divided by cycle length
    remainder  = seconds % cycle
    # initialize distance
    distance = 0
    # if remainder time would be a full speed burst
    if remainder >= reindeer['duration']:
        # increment intervals
        intervals += 1
    else:
        # increment distance by product of remainder and speed
        distance = remainder * reindeer['speed']
    # increment distance by the distance traveled in inetervals
    return distance + (intervals * distance_per_interval)


def part1(parsed_data):
    """
    Function to solve part 1:
        get maximum distance traveled in 2503 seconds
    """
    # max_distance traveled
    max_distance = 0
    seconds = 2503
    for stats in parsed_data.values():
        distance = distance_traveled(stats, seconds)
        if distance > max_distance:
            max_distance = distance
    return max_distance

def part2(parsed_data):
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

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015,14)
    #input_text = my_aoc.load_text()
    #print(input_text)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {
        1: 1,
        2: 2
    }
    # dict to store answers
    answer = {
        1: None,
        2: None
    }
    # dict to map functions
    funcs = {
        1: part1,
        2: part2
    }
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](parse_input(input_lines))
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
