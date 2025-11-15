"""
Advent Of Code 2019 day 16

On this one, I completely failed to see the obvious pattern in part 2.

Credit to u/kwenti for the level2() solution below, and chatGPT for
explaining it until I understood.  I tried to use the idea of the pattern
with my solution, and just couldn't get the speed without processing the
same way.  So my final solution looks very similar to the level2()
function.

"""

# import system modules
import time
from itertools import cycle, accumulate
import numpy as np


# import my modules
import aoc  # pylint: disable=import-error

pattern = [0, 1, 0, -1]
# save pattern_len so we don't calculate it repeatedly
PATTERN_LENGTH = len(pattern)
pattern_cache_base = {}
pattern_cache_full = {}


def calculate_pattern_original(idx, length):
    """
    Function to calculate the pattern to use
    """
    if (idx, length) in pattern_cache_base:
        print(f"Cache hit: {(idx, length)}")
        return pattern_cache_base[(idx, length)]
    print(f"Cache miss: {(idx, length)}")
    # init new_pattern
    new_pattern = []
    # init repeat as one more than idx (counting from 1 instead of 0)
    repeat = idx + 1
    # init idx_2
    idx_2 = 0
    # loop until the new pattern is full
    # while len(new_pattern) < length + 1:
    while idx_2 < len(pattern):
        # iterate over repeat range
        for _ in range(repeat):
            # append pattern value from position of idx_2
            new_pattern.append(pattern[idx_2 % PATTERN_LENGTH])
        # increment idx_2 after repeats
        idx_2 += 1
    # at this point, we have a repeating pattern, so just scale it out to length
    new_pattern2 = []
    while len(new_pattern2) < length + 1:
        new_pattern2.extend(new_pattern)
    # When applying the pattern, skip the very first value exactly once. (In other words,
    # offset the whole pattern left by one.)
    # we solve this by just removing the first element in the pattern
    new_pattern2.pop(0)
    while len(new_pattern2) > length:
        new_pattern2.pop(-1)
    pattern_cache_base[(idx, length)] = list(new_pattern2)
    # return new pattern
    return new_pattern2


def calculate_pattern(idx, length):
    """
    Function to calculate the pattern to use with optimizations
    """
    if (idx, length) in pattern_cache_full:
        return pattern_cache_full[(idx, length)]

    if idx in pattern_cache_base:
        # print(f"Cache hit: {idx}")
        # Cache the base pattern only for the specific idx
        base_pattern = pattern_cache_base[idx]
    else:
        # print(f"Cache miss: {idx}")
        # Generate the base pattern once per idx
        base_pattern = []
        repeat = idx + 1
        for value in pattern:
            base_pattern.extend([value] * repeat)
        pattern_cache_base[idx] = base_pattern
    # Expand the pattern to the desired length, skipping the first element
    full_pattern = (base_pattern * ((length // len(base_pattern)) + 1))[1 : length + 1]
    pattern_cache_full[(idx, length)] = full_pattern
    return full_pattern


def run_phase_original(signal):
    """
    Function to run a single FFT phase
    """
    # init new_signal
    new_signal = []
    # iterate over signal
    for idx, value in enumerate(signal):
        # get new_pattern
        full_pattern = calculate_pattern(idx, len(signal))
        # init new_sum
        new_sum = 0
        # iterate over signal again
        for idx_2, value in enumerate(signal):
            # add value * pattern to new_sum
            # new_sum += (value * base_pattern[(idx_2 + 1) % len(base_pattern)])
            new_sum += value * full_pattern[idx_2]
        # get last digit of new_sum
        # new_val = int(str(new_sum)[-1])
        # not sure why this didn't work, revisit later
        # ah, it was failing because of negative numbers,
        # use absolute value to resolve
        new_val = abs(new_sum) % 10
        # append new_val to new_signal
        new_signal.append(new_val)
    # return new_signal
    return new_signal


def run_phase(signal):
    """
    Function to run a single FFT phase more efficiently using NumPy
    """
    signal = np.array(signal)  # Convert signal to a NumPy array
    new_signal = []
    # Iterate over signal
    for idx in range(len(signal)):
        # get new pattern
        new_pattern = calculate_pattern(idx, len(signal))
        # print(len(signal))
        # Use NumPy's dot product for faster computation
        new_sum = np.dot(signal, new_pattern)
        # Get the last digit of new_sum
        new_val = abs(new_sum) % 10
        new_signal.append(new_val)
    return new_signal


def signal_to_str(signal):
    """
    Function to convert signal list to signal string
    """
    return "".join([str(num) for num in signal])


def level2(input_string):
    """
    Modified from original by u/kwenti

    Used to get explanation from chatGPT, which pointed out what I was missing
    Since the target range is in the second half, our pattern [0, 1, 0, -1] means
    up through offset, the values are multiplied 0, after that they are multiplied by 1
    I'm trying to use this knowledge to optimize my solution first, but also
    getting a better understanding of itertools.cycle and itertools.accumulate used below,
    so I may end up using that as well, if I can't get a decent time otherwise.

    Due to lack of time, running as is.
    """
    # get offset
    offset = int(input_string[:7])
    # get digits
    digits = [int(num) for num in input_string]
    # calcluate target_length
    target_length = 10000 * len(digits) - offset
    iterator = cycle(reversed(digits))
    arr = [next(iterator) for _ in range(target_length)]
    # iterate over phases
    for _ in range(100):
        # update result list
        arr = [n % 10 for n in accumulate(arr)]
    # reverse last 8 digits
    return "".join(str(num) for num in arr[-1:-9:-1])


def run_phase_part_2(signal):
    """
    Attempt to optimize phase run, still slow
    """
    for i in range(len(signal) - 1, -1, -1):
        signal[i] = sum(signal[i:]) % 10
    return signal


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    signal = [int(char) for char in input_value]
    offset = 0
    if part == 1:
        for _ in range(100):
            signal = run_phase(signal)
        return signal_to_str(signal)[offset : offset + 8]
    # part 2
    # The real signal is your puzzle input repeated 10000 times. Treat this new signal as a
    # single input list. Patterns are still calculated as before, and 100 phases of FFT are
    # still applied.
    # offset = int(signal_to_str(signal)[:7])
    # signal = signal*10000
    # signal = signal[offset:]
    # for phase in range(1, 100 + 1):
    #     signal = run_phase_part_2(signal)
    # get offset
    offset = int(input_value[:7])
    # calcluate target_length
    target_length = 10000 * len(signal) - offset
    # create iterator of reversed signal with itertools.cycle()
    iterator = cycle(reversed(signal))
    # load initial reversed signal list
    reversed_signal = [next(iterator) for _ in range(target_length)]
    # iterate over phases
    for _ in range(100):
        # update result list with itertools.accumulate()
        reversed_signal = [n % 10 for n in accumulate(reversed_signal)]
    # reverse last 8 digits
    return "".join(str(num) for num in reversed_signal[-1:-9:-1])


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019, 16)
    input_text = my_aoc.load_text()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: "59281788", 2: "96062868"}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
