"""
Advent Of Code 2020 day 8

This one was fun.  Based on previous years experience, my assumption
is we will see this code again.  So I made it a class I can move to
another module when we do.

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

class GameConsole:
    """Class to represent a handheld game console"""

    def __init__(self, program):
        """init method"""
        self.program = self.load_program(program)
        self.ptr = 0
        self.accumulator = 0
        self.function_map = {
            "nop": self.nop,
            "acc": self.acc,
            "jmp": self.jmp
        }

    def load_program(self, program):
        """method to load program instructions"""
        self.program = []
        # convert to list if string
        if isinstance(program, str):
            program = program.splitlines()
        for line in program:
            instruction, value = line.split(' ')
            self.program.append(
                {
                    "instruction": instruction,
                    "value": int(value)
                }
            )
        return self.program

    def nop(self, value):
        """nop: no op method"""
        isinstance(value, int)
        self.ptr += 1

    def acc(self, value):
        """acc: accumulator method"""
        self.accumulator += value
        self.ptr += 1

    def jmp(self, value):
        """jmp: jump method"""
        self.ptr += value

    def step(self):
        """method to execute a program step"""
        instruction = self.program[self.ptr]["instruction"]
        value = self.program[self.ptr]["value"]
        self.function_map[instruction](value)

def test_loop(program):
    """Function to test a program for infinite loops"""
    hgc = GameConsole(program)
    seen = set()
    # the program terminates by attempting to run the instruction below
    # the last instruction in the file.
    while 0 <= hgc.ptr < len(hgc.program):
        # print(f"{hgc.ptr} {hgc.accumulator}")
        if hgc.ptr in seen:
            return False
        seen.add(hgc.ptr)
        hgc.step()
    # print("Program exited")
    # What is the value of the accumulator after the program terminates?
    return hgc.accumulator

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        hgc = GameConsole(input_value)
        seen = set()
        while True:
            # Immediately before any instruction is executed a second time,
            if hgc.ptr in seen:
                # what value is in the accumulator?
                return hgc.accumulator
            seen.add(hgc.ptr)
            hgc.step()
    # part 2
    for idx, line in enumerate(input_value):
        # No acc instructions were harmed in the corruption of this boot code.
        if 'acc' in line:
            continue
        test_program = list(input_value)
        # By changing exactly one jmp or nop, you can repair the boot code and
        # make it terminate correctly.
        if "nop" in line:
            test_program[idx] = test_program[idx].replace('nop', 'jmp')
        else:
            test_program[idx] = test_program[idx].replace('jmp', 'nop')
        result = test_loop(test_program)
        if result:
            # What is the value of the accumulator after the program terminates?
            return result
    # this shouldn't be possible, but needed to make pylint happy
    return part

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020,8)
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
    # correct answers once solved, to validate changes
    correct = {
        1: 1200,
        2: 1023
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
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
