"""
Advent Of Code 2024 day 17

Part 1 was easy once, I read all the instructions.
Part 2 was going to take forever, so I looked a couple of solutions,
and found one that I liked.  It didn't quite work for me, so I had to
adjust it a bit.

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def parse_input(input_text):
    """
    Function to parse the input text
    """
    input_text = input_text.split('\n')
    registers = {}
    for line in input_text:
        if line.startswith('Register'):
            line = line.split()
            registers[line[1][0]] = int(line[2])
        elif line.startswith('Program'):
            program = []
            for instr in line.split(': ')[1].split(','):
                program.append(*list(map(int, instr.split())))
    return registers, program

def combo_operand_value(operand, registers):
    """
    Function to get the value of a combo operand
    """
    # The value of a combo operand can be found as follows:
    # Combo operands 0 through 3 represent literal values 0 through 3.
    if operand < 4:
        return operand
    # Combo operand 4 represents the value of register A.
    if operand == 4:
        return registers['A']
    # Combo operand 5 represents the value of register B.
    if operand == 5:
        return registers['B']
    # Combo operand 6 represents the value of register C.
    if operand == 6:
        return registers['C']
    # Combo operand 7 is reserved and will not appear in valid programs.
    return None

def run_program(input_text, register_a=None):
    """
    Function to run the program
    """
    registers, program = parse_input(input_text)
    if register_a is not None:
        registers['A'] = register_a
    ptr = 0
    outputs = []
    while ptr < len(program):
        instr = program[ptr:ptr+2]
        literal_operand = instr[1]
        combo_operand = combo_operand_value(literal_operand, registers)
        if instr[0] == 0:
            registers['A'] = operations[0](registers['A'], combo_operand)
        elif instr[0] == 1:
            registers['B'] = operations[1](registers['B'], literal_operand, 0, 0)
        elif instr[0] == 2:
            registers['B'] = operations[2](registers['B'], 0, 0, combo_operand)
        elif instr[0] == 3:
            if registers['A'] != 0:
                ptr = literal_operand
                continue
        elif instr[0] == 4:
            registers['B'] = operations[4](registers['B'], registers['C'], 0, 0)
        elif instr[0] == 5:
            outputs.append(operations[5](0, 0, 0, combo_operand))
        elif instr[0] == 6:
            registers['B'] = operations[6](
                registers['A'],
                registers['B'],
                registers['C'],
                combo_operand
            )
        elif instr[0] == 7:
            registers['C'] = operations[7](
                registers['A'],
                registers['B'],
                registers['C'],
                combo_operand
            )
        ptr += 2
    return outputs

operations = {}
op_names = {}
# The eight instructions are as follows:
# The adv instruction (opcode 0) performs division. The numerator is the value in the A register.
# The denominator is found by raising 2 to the power of the instruction's combo operand.
# (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
# The result of the division operation is truncated to an integer and then written to the
# A register.
operations[0] = lambda a, operand: a // (2 ** operand)
op_names[0] = 'adv'
# The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's
# literal operand, then stores the result in register B.
operations[1] = lambda b, operand, _, __: b ^ operand
op_names[1] = 'bxl'
# The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
# (thereby keeping only its lowest 3 bits),then writes that value to the B register.
operations[2] = lambda b, _, __, operand: operand % 8
op_names[2] = 'bst'
# The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register
# is not zero, it jumps by setting the instruction pointer to the value of its literal operand;
# if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
# operations[3] = lambda a, operand: operand if a != 0 else None
# this operation not needed handled in if statement instead
op_names[3] = 'jnz'
# The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C,
# then stores the result in register B. (For legacy reasons, this instruction reads an operand
# but ignores it.)
operations[4] = lambda b, c, _, __: b ^ c
op_names[4] = 'bxc'

# The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs
# that value. (If a program outputs multiple values, they are separated by commas.)
operations[5] = lambda _, __, ___, operand: operand % 8
op_names[5] = 'out'
# The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is
# stored in the B register. (The numerator is still read from the A register.)
operations[6] = lambda a, b, c, operand: a // (2 ** operand)
op_names[6] = 'bdv'
# The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is
# stored in the C register. (The numerator is still read from the A register.)
operations[7] = lambda a, b, c, operand: a // (2 ** operand)
op_names[7] = 'cdv'

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        return ','.join(map(str,run_program(input_value)))
    _, program = parse_input(input_value)
    result = ''

    # start at 0, starting closer to the answer worked for the sample data
    # and did not work for my puzzle input
    register_a_attempt = 0
    while True:
        result = run_program(input_value, register_a_attempt)
        # check if the output is too long
        if len(result) > len(program):
            print(f"result: {result}, program: {program}")
            raise ValueError("The output is too long")

        # check if the output is correct
        if result == program:
            break

        last = register_a_attempt
        # check each program value to see if it is correct
        for i in range(len(result) - 1, -1, -1):
            if result[i] != program[i]:
                # add 8^i to the register value
                add = 8**i
                # slow down for the last digit
                # In the sample data, incrementing by 8 on position 1,
                # skipped the correct answer
                if add < 9:
                    add = 1
                register_a_attempt += add
                break
        # if the register value did not change, increment by 1
        # this happens when the result matches, except that it is too short
        if register_a_attempt == last:
            register_a_attempt += 1

    # 4398046511103 too low, as expected
    # 35184372088831 too low, as expected
    return register_a_attempt

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2024,17)
    input_data = my_aoc.load_text()
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
        1: '7,6,5,3,6,5,7,0,4',
        2: 190615597431823
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
