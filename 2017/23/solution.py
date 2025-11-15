"""
Advent Of Code 2017 day 23

Part 1 was easy, part 2, I was getting there trying to short circuit, and
ran out of time.  Looked at solutions, and implemented one.  I want to
revisit this at some point, and use that logic to fix my short circuits instead.

"""

# import system modules
import time
import sympy

# import my modules
import aoc  # pylint: disable=import-error


class Computer:
    """
    Class to represent a computer
    """

    # cmd handler function table

    def __init__(self, program=None, comp_id=0):
        """
        init computer
        """
        self.comp_id = comp_id
        self.handlers = {
            "set": self.do_set,
            "sub": self.do_sub,
            "mul": self.do_mul,
            "jnz": self.do_jnz,
        }
        # init register with pointer for position in the program
        self.registers = {"pointer": 0}
        if self.comp_id == 1:
            # set registers for instructions to server as counters
            for instruction in self.handlers:
                self.registers[instruction] = 0
        for register in "abcdefgh":
            self.registers[register] = 0
        self.program = []
        self.partner = None
        if program:
            self.load_program(program)

    def __str__(self):
        """
        string representation, primarily used in debugging
        """
        my_string = f"{self.comp_id}: running {self.running()}, "
        my_string += f"registers: {self.registers}"
        return my_string

    def load_program(self, program):
        """
        parse program instructions
        """
        if isinstance(program, str):
            program = program.split("\n")
        self.program = []
        for line in program:
            inputs = line.split(" ")
            instruction = {"instruction": inputs[0]}
            try:
                instruction["x"] = int(inputs[1])
            except ValueError:
                instruction["x"] = inputs[1]
                self.registers[inputs[1]] = 0
            try:
                instruction["y"] = int(inputs[2])
            except ValueError:
                instruction["y"] = inputs[2]
                self.registers[inputs[2]] = 0
            except IndexError:
                pass
            self.program.append(instruction)

    def value(self, test_value):
        """
        utility function to normalize values
        """
        if isinstance(test_value, int):
            return test_value
        return self.registers[test_value]

    def running(self):
        """
        is the program still running?
        """
        return 0 <= self.registers["pointer"] < len(self.program)

    def run_next_instruction(self):
        """
        execute instruction
        """
        if self.running():
            current = self.program[self.registers["pointer"]]
            # print(self.comp_id, current)
            instruction = current["instruction"]
            if self.comp_id == 1:
                self.registers[instruction] += 1
            return self.handlers[instruction](current)
        return self.running()

    def run_program(self):
        """
        run program loop
        """
        sentinel = 0
        while self.run_next_instruction():
            # print(self)
            sentinel += 1
            if sentinel == 5000000:
                print("Breaking Loop")
                break
        return self.running()

    def do_sub(self, instruction):
        """
        handler for instruction sub
        decreases register X by the value of Y.
        """
        self.registers[instruction["x"]] -= self.value(instruction["y"])
        self.registers["pointer"] += 1
        return True

    def do_set(self, instruction):
        """
        handler for instruction set
        sets register X to the value of Y
        """
        self.registers[instruction["x"]] = self.value(instruction["y"])
        self.registers["pointer"] += 1
        return True

    def do_mul(self, instruction):
        """
        handler for instruction mul
        sets register X to the result of multiplying the value contained in register X
        by the value of Y
        """
        self.registers[instruction["x"]] *= self.value(instruction["y"])
        self.registers["pointer"] += 1
        return True

    def do_jnz(self, instruction):
        """
        handler for instruction jnz
        jumps with an offset of the value of Y, but only if the value of X is not zero.
        (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous
        instruction, and so on.)
        """
        # hmm, here lies the bug that tripped be up.  I was this to be non-zero
        # it needs to be non-zero and positive
        if self.value(instruction["x"]) != 0:
            self.registers["pointer"] += self.value(instruction["y"])
        else:
            self.registers["pointer"] += 1
        return True


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        registers = {"b": 109900, "c": 126900, "h": 0}
        # borrowed logic, thanks u/dario_p1
        for test_b in range(registers["b"], registers["c"] + 1, 17):
            if not sympy.isprime(test_b):
                registers["h"] += 1
        return registers["h"]
    computer = Computer(input_value, part)
    if part == 2:
        # wishlist: use the part 2 logic above to create short circuits
        # to actually fix the program
        computer.registers["a"] = 1
    computer.run_program()
    if part == 2:
        return computer.registers["h"]
    return computer.registers["mul"]


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017, 23)
    # fetch input
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
