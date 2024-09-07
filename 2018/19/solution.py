"""
Advent Of Code 2018 day 19

I need to revisit this one later, but still not feeling well today.

For both parts, there is an obvious loop between instructions 3-11.
I just don't have the energy to sort it out. 
So using hints from the solutions page, I cheated a bit, and just
found the sum of the divisors of register[4] 10551370

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

registers = [0, 0, 0, 0, 0, 0]

ops = {
    'addr': lambda a, b : registers[a] + registers[b],
    'addi': lambda a, b : registers[a] + b,
    'mulr': lambda a, b : registers[a] * registers[b],
    'muli': lambda a, b : registers[a] * b,
    'banr': lambda a, b : registers[a] & registers[b],
    'bani': lambda a, b : registers[a] & b,
    'borr': lambda a, b : registers[a] | registers[b],
    'bori': lambda a, b : registers[a] | b,
    'setr': lambda a, b : registers[a],
    'seti': lambda a, b : a,
    'gtir': lambda a, b : 1 if a > registers[b] else 0,
    'gtri': lambda a, b : 1 if registers[a] > b else 0,
    'gtrr': lambda a, b : 1 if registers[a] > registers[b] else 0,
    'eqir': lambda a, b : 1 if a == registers[b] else 0,
    'eqri': lambda a, b : 1 if registers[a] == b else 0,
    'eqrr': lambda a, b : 1 if registers[a] == registers[b] else 0
}

def parse_input(lines):
    """
    Parse input file to program instructions
    """
    inst_ptr = 0
    instructions = []
    for line in lines:
        if "#inst_ptr" in line:
            _, inst_ptr = line.split(' ')
            inst_ptr = int(inst_ptr)
            continue
        cmd, val_a, val_b, val_c = line.split(' ')
        instructions.append(
            {
                "op": cmd,
                "a": int(val_a),
                "b": int(val_b),
                "c": int(val_c)
            }
        )
    return inst_ptr, instructions

def execute(inst_ptr, instructions, debug=False):
    """
    Execute the next program instruction
    """
    instruction = instructions[registers[inst_ptr]]
    output = f"ip={registers[inst_ptr]} {registers} {instruction['op']}"
    output += f" {instruction['a']} {instruction['b']} {instruction['c']}"
    # if registers[inst_ptr] == 3:
    #     if registers[5] == 2:
    #         registers[5] = registers[4] + 1
    #         registers[0] += 1
    #         registers[1] = 11
    # if registers[inst_ptr] == 12:
    #     if registers[3] == 2:
    #         registers[3] = registers[4] - 1

    registers[instruction['c']] = ops[instruction['op']](instruction['a'], instruction['b'])
    output += f" {registers}"
    if debug:
        print(output)
    # Afterward, move to the next instruction by adding one to the instruction pointer,
    # even if the value in the instruction pointer was just updated by an instruction.
    registers[inst_ptr] += 1

def find_divisors(num):
    """
    find the divisors of a number
    """
    divisors = []
    for i in range(1, int(num**0.5) + 1):
        if num % i == 0:
            divisors.append(i)
            if i != num // i:
                divisors.append(num // i)
    return sorted(divisors)

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    debug = False
    ptr, program = parse_input(input_value)
    if part == 2:
        registers[0] = 1
        registers[1] = 0
        registers[2] = 0
        registers[3] = 0
        registers[4] = 0
        registers[5] = 0
        debug = False
        for _ in range(17):
            execute(ptr, program, debug)
        return sum(find_divisors(registers[4]))
    while 0 <= registers[ptr] < len(program):
        execute(ptr, program, debug)
    return registers[0]

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018,19)
    #input_text = my_aoc.load_text()
    #print(input_text)
    input_lines = my_aoc.load_lines()
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
