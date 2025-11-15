"""
Advent Of Code 2018 day 7

"""

# import system modules
import time
import re

# import my modules
import aoc  # pylint: disable=import-error

# regex for input
pattern_input = re.compile(r"Step (\w).*step (\w).*")


def parse_input(lines):
    """
    Function to parse input
    Args:
        lines: list(str()) input data

    Returns:
        requirements: dict() with prerequisites and next_steps
    """
    # init requirements
    requirements = {}
    # walk lines
    for line in lines:
        # match regex
        match = pattern_input.match(line)
        if match:
            # store step_a and step_b
            step_a = match.group(1)
            step_b = match.group(2)
            # init steps if not already
            if step_b not in requirements:
                requirements[step_b] = {}
                requirements[step_b]["prereqs"] = []
                requirements[step_b]["next"] = []
            if step_a not in requirements:
                requirements[step_a] = {}
                requirements[step_a]["prereqs"] = []
                requirements[step_a]["next"] = []
            # step_a is a requirement of step_b
            requirements[step_b]["prereqs"].append(step_a)
            # step_b is a next step for step_a
            requirements[step_a]["next"].append(step_b)
    return requirements


def dependencies_satisfied(instructions, step, result):
    """
    Function to determine if a step is ready to execute

    Args:
        instructions: dict() instruction list
        step: str() step name
        result: str() steps already set in order

    Returns:
        ready: bool() status
    """
    # init ready, assume True, then disprove
    ready = True
    # get dependencies for step
    dependencies = instructions[step]["prereqs"]
    # are all step's dependencies already in result?
    for prev_step in dependencies:
        if prev_step not in result:
            ready = False
    return ready


def get_order(instructions):
    """
    Function to order instructions

    Args:
        instructions: dict()

    Returns:
        result: str() order of instruction keys
    """
    # init result and available as empty
    result = ""
    available = []
    # until all keys are in result
    # technically, just checking length, and we always
    # check to be sure the new step is not already there
    # so they should be unique
    # maybe sorted(list(result)) != sorted(instructions.keys()) would be better?
    while len(result) < len(instructions.keys()):
        # if there are any availables?
        if len(available) > 0:
            # sort available
            available.sort()
            # add the lowest ranking available to result
            # only one per pass, to allow subsequent processing
            # of next_steps, to be sure we are always adding
            # the lowest available step
            result += available.pop(0)
        # walk instructions
        for step in instructions:
            # skip if we have already placed or queued the step
            if step in list(result) + available:
                continue
            # is the step ready?
            if dependencies_satisfied(instructions, step, result):
                # add to available
                available.append(step)
    return result


def time_per_step(step, seconds):
    """
    Calculate time for step

    Args:
        step: str() name of step (A, B, C, etc)
        seconds: int() seconds offset to add

    Returns:
        int() seconds for step
    """
    # seconds 0 for test, 60 for prod
    # add A=0, B=1, etc (Note A=1, B=2, was causing 1 additional second per step)
    return seconds + ord(step) - ord("A")


def build(instructions, order, worker_count=4, seconds=60):
    """
    Function to simulate building sleigh

    Args:
        instructions: dict()
        order: str() steps in order
        worker_count: int() number of workers default=4
        seconds: int() number of seconds to pad steps default=60

    Returns:
        seconds: int() number of seconds build process will take
    """
    # convert order to list
    order = list(order)
    # init in_pogress and completed
    in_progress = []
    completed = ""
    # build workers:
    workers = []
    for _ in range(worker_count):
        workers.append({"step": None, "time_left": 0})
    # init timer: -1 because we will immediately increment to 0 in the loop
    second = -1
    # loop until completed
    while len(completed) < len(instructions.keys()):
        # increment timer
        second += 1
        # walk workers
        for worker in workers:
            # is worker idle
            if worker["time_left"] == 0:
                # if worker has a step, then it is completed
                if worker["step"]:
                    # add to completed
                    completed += worker["step"]
                    # remove from in_progress
                    in_progress.pop(in_progress.index(worker["step"]))
                    # remove from worker
                    worker["step"] = None
                # worker was either already working on None,or
                # we jsut finished another step
                # find new step to work on
                # walk steps
                for step in order:
                    # if step not completed, or in_progress, and is ready to start:
                    if step not in list(
                        completed
                    ) + in_progress and dependencies_satisfied(
                        instructions, step, completed
                    ):
                        # add step to worker
                        worker["step"] = step
                        # init step timer
                        worker["time_left"] = time_per_step(step, seconds)
                        # add to in_progress
                        in_progress.append(step)
                        # break loop so we don't add more steps
                        break
            # worker is busy
            else:
                # do work
                worker["time_left"] -= 1
    # return to complete all steps
    return second


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    reqs = parse_input(input_value)
    order = get_order(reqs)
    if part == 2:
        return build(reqs, order)
    return order


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018, 7)
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
