"""
Advent Of Code 2021 day 12

Part 1, I tripped on not building reverse maps for the caves.
Other than that, fairly simple heapq implementation to build the
path list.

Part 2, Counter() made this easy.  Just count the .islower()
nodes in the path.  If it is > 1 skip the small cave.

"""
# import system modules
import time
from heapq import heappop, heappush
from collections import defaultdict, Counter

# import my modules
import aoc # pylint: disable=import-error

def find_paths(cave_map, mode=1):
    """Function to identify valid paths through the cave system"""
    paths = []
    heap = []
    heappush(heap, (0, 'start', ''))
    while heap:
        step, node, path = heappop(heap)
        new_path = f"{path},{node}".replace(',start','start')
        if node == 'end':
            paths.append(new_path)
            continue
        # It would be a waste of time to visit any small cave more than once
        if node.islower():
            # print(f"node: {node} is lowercase")
            if node in path and mode == 1:
                # print(f"node: {node} is in {path}")
                continue

            if node in path and mode == 2:
                # print(f"node: {node} is in {path}")
                # After reviewing the available paths, you realize you might
                # have time to visit a single small cave twice.
                if node in ['start', 'end']:
                    # However, the caves named start and end can only be visited exactly
                    # once each: once you leave the start cave, you may not return to it,
                    # and once you reach the end cave, the path must end immediately.
                    continue
                # Specifically, big caves can be visited any number of times, a single small
                # cave can be visited at most twice, and the remaining small caves
                # can be visited at most once.
                counter = Counter([tmp_node for tmp_node in path.split(',') if tmp_node.islower()])
                # print(f"max counter: {counter.values()}")
                if max(counter.values()) > 1:
                    # print(f"not adding {node} to {path}")
                    continue
        # add possible next steps
        for next_node in cave_map[node]:
            # print(f"node: {node}, next_node: {next_node}")
            heappush(heap, (step + 1, next_node, new_path))
    return paths

def build_cave_map(lines):
    """Function to build cave map from text input"""
    cave_map = defaultdict(list)
    for line in lines:
        node, path = line.split('-')
        cave_map[node].append(path)
        # add reverse mapping as well
        cave_map[path].append(node)
    return cave_map

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    cave_map = build_cave_map(input_value)
    paths = find_paths(cave_map, part)
    path_count = len(paths)
    return path_count

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021,12)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
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
        1: 3576,
        2: 84271
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
