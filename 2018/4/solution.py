"""
Advent Of Code 2018 day 4

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


def parse_input(lines):
    """
    Parse input
    Assumptions based on review of input_data:
    Each entry is three (or more sleep/wake can repeat) lines like:
    [1518-11-01 00:00] Guard #10 begins shift
    [1518-11-01 00:05] falls asleep
    [1518-11-01 00:25] wakes up
    """
    # init guards, and guard_id
    guards = {}
    guard_id = None
    # walk lines
    for line in lines:
        # split data by spaces, no need for a regex here
        data = line.split(" ")
        # if length is 6, we have a new guard on duty
        if len(data) == 6:
            # fetch guard_id
            guard_id = int(data[3].replace("#", ""))
            # if we haven't seen this guard, init the guard
            if guard_id not in guards:
                guards[guard_id] = {"log": [], "minutes": 0}
        # falling asleep
        elif data[2] == "falls":
            # store sleep time
            sleep = (data[0].replace("[]", ""), data[1].replace("]", ""))
        # waking up
        elif data[2] == "wakes":
            # store wakt time
            wake = (data[0].replace("[]", ""), data[1].replace("]", ""))
            # append to guards log
            guards[guard_id]["log"].append((wake, sleep))
            # add to sleep minutes for guard
            guards[guard_id]["minutes"] += int(wake[1].split(":")[1]) - int(
                sleep[1].split(":")[1]
            )
            # I thought about getting the most frequent minute here,
            # but we would be calculating multiple times, so instead
            # we just calculate twice for each guard in solve()
        else:
            print(f"Unhandled: {line}")
    return guards


def sleepiest(guards):
    """
    Function to find the guard who sleeps the most minutes
    """
    # init sleepy
    sleepy = None
    # get the max of minutes
    max_minutes = max(guard["minutes"] for guard in guards.values())
    # find the guard that had the max
    for guard_id, guard in guards.items():
        if guard["minutes"] == max_minutes:
            sleepy = guard_id
            # go ahead and return to cut the loop short
            return sleepy
    return sleepy


def most_frequent_minute(guard):
    """
    Function to find the most frequent sleepy minute for a guard
    """
    # init minutes
    minutes = {}
    # pull log
    log = guard["log"]
    # important check, there is a guard that doesn't sleep, which
    # will throw an exception when we pass an empty list to max
    if log:
        # walk log entries
        for data in log:
            # (('[1518-11-01', '00:25'), ('[1518-11-01', '00:05'))
            # pull sleep and wake minutes from log entry
            sleep = int(data[1][1].split(":")[1])
            wake = int(data[0][1].split(":")[1])
            # for each minute from sleep to wake
            for minute in range(sleep, wake):
                # init if needed
                if minute not in minutes:
                    minutes[minute] = 0
                # increment
                minutes[minute] += 1
        # get max
        max_count = max(minutes.values())
        # find the minute that matches max
        for minute, count in minutes.items():
            if count == max_count:
                return minute, count
    return 0, 0


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # init results
    result = None
    # parse guard data
    guards = parse_input(input_value)
    if part == 1:
        # Strategy 1: Find the guard that has the most minutes asleep.
        # What minute does that guard spend asleep the most?
        # get sleepiest
        sleepy = sleepiest(guards)
        # get most frequent minute of sleepiest
        minute, _ = most_frequent_minute(guards[sleepy])
        # calculate and return
        result = sleepy * minute
        return result
    # Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?
    # What is the ID of the guard you chose multiplied by the minute you chose?
    # init max values
    max_count = 0
    max_guard_id = None
    max_minute = None
    # walk guards
    for guard_id, guard in guards.items():
        # get most frequent minute for guard
        minute, count = most_frequent_minute(guard)
        # if new max, update, max variables
        if count > max_count:
            max_count = count
            max_minute = minute
            max_guard_id = guard_id
    # calculate and return
    result = max_guard_id * max_minute
    return result


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018, 4)
    # input_text = my_aoc.load_text()
    # print(input_text)
    input_lines = sorted(my_aoc.load_lines())
    # for line in input_lines:
    #    print(line)
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
