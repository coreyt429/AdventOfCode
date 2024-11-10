"""
Advent Of Code 2021 day 8



"""
# import system modules
import time
from heapq import heappop, heappush

# import my modules
import aoc # pylint: disable=import-error

digits = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg'
}

def parse_input(lines):
    """Function to parse puzzle input"""
    values = []
    for line in lines:
        signal_patterns, output_value = line.split(' | ')
        values.append({
            'signal_patterns': signal_patterns.split(' '),
            'output_value': output_value.split(' '),
            })
    return values

def matching_segments(pattern_a, pattern_b):
    """Count the matching characters in two strings"""
    set_a = set(pattern_a)
    set_b = set(pattern_b)
    return len(set_a.intersection(set_b))

def map_wires(signal_patterns):
    """ Function to map wire signals to values"""
    heap = []
    for pattern in signal_patterns:
        heappush(heap, (0, len(pattern), pattern))

    unique_lengths = {2:1, 3:7, 4:4, 7:8}
    wire_map = {}
    while heap:
        turn, length, pattern = heappop(heap)
        # map unique_length sequences
        if length in unique_lengths:
            wire_map[unique_lengths[length]] = pattern
            continue

        # finish turn 0 before attempting the others
        # this ensures 1, 4,7, and 8 are set first
        if turn < 1:
            heappush(heap, (turn + 1, length, pattern))
            continue
        # how well does it match 1?
        if matching_segments(pattern, wire_map[1]) == 1:
            # how well does it match 4?
            if matching_segments(pattern, wire_map[4]) == 2:
                # 2: 1=1, 4=2, 7=2, 8=5,
                wire_map[2] = pattern
                continue
            # how well does it match 8?
            if matching_segments(pattern, wire_map[8]) == 5:
                # 5: 1=1, 4=3, 7=2, 8=5,
                wire_map[5] = pattern
                continue
            # 6: 1=1, 4=3, 7=2, 8=6,
            wire_map[6] = pattern
            continue
        # how well does it match 4?
        if matching_segments(pattern, wire_map[4]) == 4:
            # 9: 1=2, 4=4, 7=3, 8=6,
            wire_map[9] = pattern
            continue
        # how well does it match 8?
        if matching_segments(pattern, wire_map[8]) == 5:
            # 3: 1=2, 4=3, 7=3, 8=5,
            wire_map[3] = pattern
            continue
        # 0: 1=2, 4=3, 7=3, 8=6,
        wire_map[0] = pattern
        continue

    # add reverse map
    for key, value in list(wire_map.items()):
        wire_map[''.join(sorted(value))] = key

    return wire_map

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    data = parse_input(input_value)
    if part == 2:
        total = 0
        for datum in data:
            wire_map = map_wires(datum['signal_patterns'])
            result_list = [wire_map[''.join(sorted(pattern))] for pattern in datum['output_value']]
            total += int(''.join(map(str, result_list)))
        return total

    target_lengths = [2, 3, 4, 7]
    counter = 0
    for datum in data:
        for value in datum['output_value']:
            if len(value) in target_lengths:
                counter += 1
    return counter

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021,8)
    input_data = my_aoc.load_lines()
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
    # correct answers once solved, to validate changes
    correct = {
        1: 369,
        2: 1031553
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
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
