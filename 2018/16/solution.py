"""
Advent Of Code 2018 day 16

"""

# import system modules
import time
import re
from copy import deepcopy

# import my modules
import aoc  # pylint: disable=import-error


def parse_input(input_value):
    """
    Function to parse input data
    """
    sample_text, prog_text = input_value.split("\n\n\n\n")
    lines = sample_text.splitlines()
    tests = []
    program = []
    for line in lines:
        # print(line)
        if "Before" in line:
            test_regs = {"before": [], "after": [], "instruction": [], "test_case": []}
            list_text = line.split(": ")[1]
            test_regs["before"] = [int(num) for num in re.findall(r"\d+", list_text)]
        elif "After" in line:
            list_text = line.split(": ")[1]
            test_regs["after"] = [int(num) for num in re.findall(r"\d+", list_text)]
            tests.append(test_regs)
        elif " " in line:
            test_regs["instruction"] = [int(num) for num in line.split(" ")]
    for line in prog_text.splitlines():
        program.append([int(num) for num in line.split(" ")])
    return tests, program


def map_ops(ops_list):
    """
    Map ops to op_id
    """
    ops_map = {}
    while ops_list:
        deletes = []
        for idx, op_dat in enumerate(ops_list):
            op_id, op_names = op_dat
            for op_name in ops_map.values():
                if op_name in op_names:
                    op_names.remove(op_name)
                    ops_list[idx] = (op_id, op_names)
            if len(op_names) == 1:
                ops_map[op_id] = op_names[0]
                deletes.append(op_id)
        ops_list = [
            (op_id, op_names) for op_id, op_names in ops_list if op_id not in deletes
        ]
    return ops_map


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    registers = [0, 0, 0, 0]
    ops_map = {}
    ops = {
        "addr": lambda a, b: registers[a] + registers[b],
        "addi": lambda a, b: registers[a] + b,
        "mulr": lambda a, b: registers[a] * registers[b],
        "muli": lambda a, b: registers[a] * b,
        "banr": lambda a, b: registers[a] & registers[b],
        "bani": lambda a, b: registers[a] & b,
        "borr": lambda a, b: registers[a] | registers[b],
        "bori": lambda a, b: registers[a] | b,
        "setr": lambda a, b: registers[a],
        "seti": lambda a, b: a,
        "gtir": lambda a, b: 1 if a > registers[b] else 0,
        "gtri": lambda a, b: 1 if registers[a] > b else 0,
        "gtrr": lambda a, b: 1 if registers[a] > registers[b] else 0,
        "eqir": lambda a, b: 1 if a == registers[b] else 0,
        "eqri": lambda a, b: 1 if registers[a] == b else 0,
        "eqrr": lambda a, b: 1 if registers[a] == registers[b] else 0,
    }
    samples, program = parse_input(input_value)

    total = 0
    ops_list = []
    for sample in samples:
        count = 0
        # print(test_regs)
        valid_ops = []
        for key, curr_op in ops.items():
            instruct = sample["instruction"]
            registers = deepcopy(sample["before"])
            registers[instruct[3]] = curr_op(instruct[1], instruct[2])
            if registers == sample["after"]:
                valid_ops.append(key)
                count += 1
        ops_list.append((instruct[0], valid_ops))
        if count >= 3:
            total += 1
    ops_map = map_ops(ops_list)
    if part == 2:
        registers = [0, 0, 0, 0]
        for instruct in program:
            registers[instruct[3]] = ops[ops_map[instruct[0]]](instruct[1], instruct[2])
        return registers[0]
    return total


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018, 16)
    input_lines = my_aoc.load_text()
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
