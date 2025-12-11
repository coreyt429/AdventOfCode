"""
Advent Of Code 2018 day 21

My solution works eventually, I have hard coded the answers here. even with that
part 2 is slow.  I'll revisit this one later.  notes below

todo, examine the loop from 18 to 25 to see what it does, how and how to get to 28
#ip 3
0  seti 123 0 5
1  bani 5 456 5
2  eqri 5 72 5
3  addr 5 3 3
4  seti 0 0 3
5  seti 0 3 5
6  bori 5 65536 4
7  seti 8858047 4 5
8  bani 4 255 2
9  addr 5 2 5
10 bani 5 16777215 5
11 muli 5 65899 5
12 bani 5 16777215 5
13 gtir 256 4 2
14 addr 2 3 3
15 addi 3 1 3
16 seti 27 5 3
17 seti 0 6 2
18 addi 2 1 1
19 muli 1 256 1
20 gtrr 1 4 1
21 addr 1 3 3
22 addi 3 1 3
23 seti 25 1 3
24 addi 2 1 2
25 seti 17 4 3
26 setr 2 1 4
27 seti 7 3 3
28 eqrr 5 0 2   <-- only thing that uses register 0, so exit points were where 5 == 9
29 addr 2 3 3
30 seti 5 2 3

The solution below from u/marcusandrews seems to highlight the math.  I need to review
and understand how this works:

def run_activation_system(magic_number, is_part_1):
    seen = set()
    c = 0
    last_unique_c = -1

    while True:
        a = c | 65536
        c = magic_number

        while True:
            c = (((c + (a & 255)) & 16777215) * 65899) & 16777215

            if 256 > a:
                if is_part_1:
                    return c
                else:
                    if c not in seen:
                        seen.add(c)
                        last_unique_c = c
                        break
                    else:
                        return last_unique_c
            else:
                a //= 256


magic_number = int(open("input.txt", "r").readlines()[8].split()[1])
print(run_activation_system(magic_number, True))
print(run_activation_system(magic_number, False))


2025.11.27: cleaned up a bit, part 2 is slow
"""

# import system modules
from __future__ import annotations
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


registers = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
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


def parse_input(lines):
    """parse input into instructions"""
    ip = 0
    instructions = []
    for line in lines:
        if "#ip" in line:
            _, ip = line.split(" ")
            ip = int(ip)
            continue
        cmd, val_a, val_b, val_c = line.split(" ")
        instructions.append(
            {"op": cmd, "a": int(val_a), "b": int(val_b), "c": int(val_c)}
        )
    return ip, instructions


def execute(ip, instructions):
    """execute one instruction"""
    instruction = instructions[registers[ip]]
    output = f"ip={registers[ip]} {registers} {instruction['op']}"
    output += f" {instruction['a']} {instruction['b']} {instruction['c']}"
    registers[instruction["c"]] = ops[instruction["op"]](
        instruction["a"], instruction["b"]
    )
    output += f" {registers}"
    # if registers[ip] == 28:
    #     print(output)
    # Afterward, move to the next instruction by adding one to the instruction pointer,
    # even if the value in the instruction pointer was just updated by an instruction.
    registers[ip] += 1


def detect_loop_old(sequence_generator):
    """detect loops in sequence generator"""
    seen = []
    for i, num in enumerate(sequence_generator):
        seen.append(str(num))
        last_5 = ",".join(seen[-5:])
        all_seen = ",".join(seen)
        print(last_5, all_seen.count(last_5))
        if all_seen.count(last_5) > 10:
            return "Loop detected"
        if i > 100000:
            return "Breaking"
    return "No loop detected"


def detect_loop(sequence_generator):
    """detect loops in sequence generator"""
    seen = []
    loop_size = 0  # Variable to store the size of the loop
    i = None
    for i, num in enumerate(sequence_generator):
        seen.append(str(num))
        all_seen = ",".join(seen)
        # Check for repeating patterns of various sizes
        for window_size in range(2, min(100, len(seen) // 2)):
            pattern = ",".join(seen[-window_size:])
            count = all_seen.count(pattern)
            if count > 1:  # Pattern repeats
                loop_size = max(loop_size, window_size)

            # Stop searching if we find a pattern repeating more than 10 times
            if count > 1000:
                return True, int(pattern.split(",", maxsplit=1)[0])

        if i > 100000:
            return True, -1

    return False, i


def run_program(ip, instructions):
    """execute program generator"""
    while True:
        if registers[ip] < 0 or registers[ip] >= len(instructions):
            return
        execute(ip, instructions)
        yield registers[ip]


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    registers.update({0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0})
    ptr, program = parse_input(input_value.splitlines())
    loop = True
    # 11513432 was determined by watching the value of registers[5]
    # the relevant instruction is 28: eqrr 5 0 2
    # 11513431 + 1 = 11513432
    counter = 11513432 - 1
    if part == 2:
        counter = 7434231 - 1
    while loop:
        counter += 1
        registers[0] = counter
        print(counter)
        loop, _ = detect_loop(run_program(ptr, program))
    return counter


YEAR = 2018
DAY = 21
input_format = {
    1: "text",
    2: "text",
}

funcs = {
    1: solve,
    2: solve,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    aoc = AdventOfCode(
        year=YEAR,
        day=DAY,
        input_formats=input_format,
        funcs=funcs,
        test_mode=args.test,
    )
    aoc.run(submit=args.submit)
