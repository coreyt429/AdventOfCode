"""
Advent Of Code 2022 day 5

Fun with stacks :)

"""

# import system modules
import time
from collections import defaultdict

# import my modules
import aoc  # pylint: disable=import-error


def parse_input(input_value):
    """Function to parse input text into columns and moves"""
    stacks, instructions = input_value.split("\n\n")
    # reverse stacks, so we can build from the boottom up
    stacks = list(reversed(stacks.splitlines()))
    labels = stacks.pop(0)
    positions = {}
    columns = defaultdict(list)
    # identify column positions
    for idx, char in enumerate(labels):
        if char != " ":
            positions[idx] = int(char)
    # process remaining rows to build columns
    while stacks:
        line = stacks.pop(0)
        for idx, char in enumerate(line):
            if idx in positions and char != " ":
                columns[positions[idx]].append(char)
    # process instructions:
    moves = []
    for line in instructions.splitlines():
        data = line.split(" ")
        moves.append((int(data[1]), int(data[3]), int(data[5])))
    return moves, columns


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    moves, columns = parse_input(input_value)
    for move in moves:
        qty, source, destination = move
        if part == 1:
            # Crates are moved one at a time
            for _ in range(qty):
                columns[destination].append(columns[source].pop())
        else:
            # The CrateMover 9001 is notable for many new and exciting features: air conditioning,
            # leather seats, an extra cup holder, and the ability to pick up and move multiple
            # crates at once.
            columns[destination].extend(columns[source][-qty:])
            columns[source] = columns[source][:-qty]
    return "".join([column[-1] for column in columns.values()])


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2022, 5)
    input_data = my_aoc.load_text()
    # print(input_text)
    # input_data = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: "TPGVQPFDH", 2: "DMRDFRHHH"}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
