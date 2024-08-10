"""
Advent Of Code 2017 day 12

"""
# import system modules
import time
import re

# import my modules
import aoc # pylint: disable=import-error

def trace_pipe(pipes, current, visited=()):
    """
    Function to trace from one pipe to find connections
    """

    # add current to visited
    visited = (*visited, current)
    # walk connections for current
    for target in pipes[current]:
        # if target hasn't been visited already
        if target not in visited:
            # trace target as well
            visited = trace_pipe(pipes, target, visited)
    # return tuple visited
    return visited

def load_pipes(lines):
    """
    Function to read input and build pipe connections
    """
    # init connections and all_nums
    connections = {}
    all_nums = set()
    # walk lines
    for line in lines:
        # find all numbers in line, and store as ints
        nums = [int(num) for num in re.findall(r'(\d+)', line)]
        # update all_nums set
        all_nums.update(nums)
        # pop current, the rest are connected to current
        current = nums.pop(0)
        # walk remainint numbers
        for num in nums:
            # connect current <-> num
            connections.setdefault(current, set()).add(num)
            connections.setdefault(num, set()).add(current)
    return connections, all_nums

def solve(lines, part):
    """
    Function to solve puzzle
    """
    # parse input data
    pipes, all_programs = load_pipes(lines)
    # trace program 0
    connected = trace_pipe(pipes, 0)
    # get disconnected from all_programs - connected
    disconnected = all_programs.difference(connected)
    if part == 1:
        # part1 return count connected to 0
        return len(connected)
    # part 2, continue
    # add connedcted to groups
    groups = [connected]
    # while we still have disconnected programs
    while disconnected:
        # trace next program in disconnected
        connected = trace_pipe(pipes, disconnected.pop())
        # append new connected set to groups
        groups.append(connected)
        # update disconnected by removing connected
        disconnected.difference_update(connected)
    # return the count of groups
    return len(groups)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017,12)
    # fetch input
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
        1: solve,
        2: solve
    }
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
