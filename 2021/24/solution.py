"""
Advent Of Code 2021 day 24

Okay, I just wanted this one to be done.  Answers were calculated with a borrowed solution.
I understand what it is doing, but my attempts to speed it up were bad.

I like the fake code type puzzles when we can run them and find a solution, maybe short circuit
a few loops.  But I don't have the time to work out this type :(

Putting on the review later list

2025.11.27 - Spreadsheet analysis shows that the answer has to be divisible by 16
   - Trial and error from there indicates 8192 is the magic number


"""

# import system modules
import time
import logging

# import my modules
import aoc  # pylint: disable=import-error

# set logging level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Alu:
    """Class to represent an Alu"""

    # The ALU is a four-dimensional processing unit: it has integer variables w, x, y, and z.

    def __init__(self, program):
        self.registers = {"w": 0, "x": 0, "y": 0, "z": 0}
        self.program = self.load(program)
        self.inputs = []
        # These variables all start with the value 0. The ALU also supports six instructions:
        self.operations = {
            "inp": self.inp,
            "add": self.add,
            "mul": self.mul,
            "div": self.div,
            "mod": self.mod,
            "eql": self.eql,
        }

    def load(self, program):
        """method to load a program into instructions"""
        instructions = []
        for line in program:
            data = line.split(" ")
            params = []
            op = data.pop(0)
            while data:
                datum = data.pop(0)
                try:
                    params.append(int(datum))
                except ValueError:
                    params.append(datum)
            instructions.append((op, tuple(params)))
        return instructions

    def value(self, item):
        """method to get the value of an item"""
        if isinstance(item, int):
            return item
        return self.registers[item]

    def inp(self, *args):
        """inp method - reads input q and loads it to a register"""
        # inp a - Read an input value and write it to variable a.
        register = args[0]
        value = self.inputs.pop(0)
        self.registers[register] = int(value)

    def add(self, a, b):
        """add method - adds b to a"""
        # add a b - Add the value of a to the value of b, then store the result in variable a.
        self.registers[a] += self.value(b)

    def mul(self, a, b):
        """mul method - sets a to the product of a and b"""
        # mul a b - Multiply the value of a by the value of b, then store the result in variable a.
        self.registers[a] *= self.value(b)

    def div(self, a, b):
        """div method - sets a to the integer result of division with b"""
        # div a b - Divide the value of a by the value of b, truncate the result to an integer, then
        # store the result in variable a. (Here, "truncate" means to round the value toward zero.)
        self.registers[a] //= self.value(b)

    def mod(self, a, b):
        """mod method - sets a to the remainder of division with b"""
        # mod a b - Divide the value of a by the value of b, then store the remainder in variable a.
        # (This is also called the modulo operation.)
        self.registers[a] %= self.value(b)

    def eql(self, a, b):
        """eql method - sets a to 1 if a == b, otherwise 0"""
        # eql a b - If the value of a and b are equal, then store the value 1 in variable a.
        # Otherwise, store the value 0 in variable a.
        if self.value(a) == self.value(b):
            self.registers[a] = 1
        else:
            self.registers[a] = 0

    def reset(self, inputs=None):
        """method to reset the Alu"""
        if inputs is None:
            inputs = []
        for key in self.registers:
            self.registers[key] = 0
        self.inputs = inputs

    def run(self, inputs=None):
        """method to run an alu program"""
        if not inputs is None:
            self.inputs = inputs
        for operation, params in self.program:
            logger.debug("input: %s", self.inputs)
            logger.debug("%s %s - %s", operation, params, self.registers)
            self.operations[operation](*params)
            logger.debug("%s %s - %s", operation, params, self.registers)

def get_relevant_adds(puzzle):
    """function to get the relevant add values from the puzzle"""
    div1, div26 = [], []
    for i in range(0, len(puzzle), 18):
        logger.debug("Processing block starting at line %s", puzzle[i + 4])
        if puzzle[i + 4][1][1] == 1:
            div1.append(int(puzzle[i + 15][1][1]))
            div26.append(None)
        else:
            div1.append(None)
            div26.append(int(puzzle[i + 5][1][1]))
    return div1, div26


def get_model_no(div1, div26, part):
    """function to get the model number"""
    model_no = [0] * 14
    stack = []
    start_digit = 9 if part == 1 else 1
    for i, (a, b) in enumerate(zip(div1, div26)):
        if a:
            stack.append((i, a))
        else:
            ia, a = stack.pop()
            diff = a + b
            if part == 1:
                model_no[ia] = min(start_digit, start_digit - diff)
                model_no[i] = min(start_digit, start_digit + diff)
            else:
                model_no[ia] = max(start_digit, start_digit - diff)
                model_no[i] = max(start_digit, start_digit + diff)
    return model_no


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    alu = Alu(input_value)
    # logger.debug("Program: %s", alu.program)
    div1, div26 = get_relevant_adds(alu.program)
    logger.debug("div1: %s", div1)
    logger.debug("div26: %s", div26)
    model_no = get_model_no(div1, div26, part)
    model_str = "".join(str(d) for d in model_no)
    logger.debug("Model number digits: %s", model_str)
    alu.reset()
    alu.run(model_no)
    assert alu.registers["z"] == 0
    logger.debug("Final ALU registers: %s", alu.registers)
    return int(model_str)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2021, 24)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 59692994994998, 2: 16181111641521}
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
