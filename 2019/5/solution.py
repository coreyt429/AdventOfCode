"""
Advent Of Code 2019 day 5

I took time to build classes for OpCode and IntCodeComputer
since we are likely to need this again for a couple more puzzles.

In theory, we should just need to modify this to add OpCodes and
any new concepts thrown in.

It might be fun to retrofit 2019.2 with this as well, but I'll save
that for another day.

"""

# import system modules
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from intcode import IntCodeComputer  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)
# class OpCode():
#     """
#     Class to represent an operation
#     """
#     # parameter modes, more a reminder for me, not sure this will get used
#     parameter_modes = {
#         0: 'position',
#         1: 'immediate'
#     }

#     def __init__(self, op_code, parent):
#         """init method"""
#         # set op_code
#         self.op_code = op_code
#         # set parmeter_count, I'm not sure this should be passed here
#         # since everything else about the function is defined here
#         # so should the parameter_count
#         parameter_counts = [0, 3, 3, 1, 1, 2, 2, 3, 3]
#         self.parameter_count = parameter_counts[self.op_code]
#         # set parent, needed to access program memory
#         self.parent = parent

#         # function map of known operations
#         self.opcode_func_map = {
#             1: self.add_and_store,
#             2: self.multiply_and_store,
#             3: self.input_and_store,
#             4: self.retrieve_and_output,
#             5: self.jump_if_true,
#             6: self.jump_if_false,
#             7: self.is_less_than,
#             8: self.is_equals
#         }
#         self.execute = self.opcode_func_map[self.op_code]

#     def get_param_values(self, param_modes, params):
#         """
#         Method to get param values
#         """
#         # init values
#         values = []
#         # get program from parent
#         program = self.parent.program
#         # walk modes to set param values
#         for idx, mode in enumerate(param_modes):
#             # position mode
#             if mode == 0:
#                 # get value from program
#                 values.append(program[params[idx]])
#             # immediate
#             elif mode == 1:
#                 # set value from param
#                 values.append(params[idx])
#             else:
#                 # we shouldn't see this
#                 raise IndexError(f'Invalid parameter mode: {mode}')
#         # return value list
#         return values

#     def add_and_store(self, param_modes, params):
#         """
#         Opcode 1 adds together numbers read from two positions and stores the result in a third
#         position. The three integers immediately after the opcode tell you these three positions
#         - the first two indicate the positions from which you should read the input values, and
#         the third indicates the position at which the output should be stored.
#         """
#         program = self.parent.program
#         values = self.get_param_values(param_modes, params)
#         program[params[2]] = sum(values[:2])

#     def multiply_and_store(self, param_modes, params):
#         """
#         Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of
#         adding them. Again, the three integers after the opcode indicate where the inputs and
#         outputs are, not their values.
#         """
#         program = self.parent.program
#         values = self.get_param_values(param_modes, params)
#         program[params[2]] = math.prod(values[:2])

#     def input_and_store(self, param_modes, params):
#         """
#         Opcode 3 takes a single integer as input and saves it to the position
#         given by its only parameter.
#         """
#         # useless action to keep pylint happy
#         type(param_modes)
#         program = self.parent.program
#         program[params[0]] = self.parent.input

#     def retrieve_and_output(self, param_modes, params):
#         """
#         Opcode 4 outputs the value of its only parameter.
#         """
#         # useless action to keep pylint happy
#         type(param_modes)
#         program = self.parent.program
#         return program[params[0]]

#     def jump_if_true(self, param_modes, params):
#         """
#         Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction
#         pointer to the value from the second parameter. Otherwise, it does nothing.
#         """
#         values = self.get_param_values(param_modes, params)
#         if values[0]:
#             # print(True, values[1])
#             self.parent.jump = values[1]

#     def jump_if_false(self, param_modes, params):
#         """
#         Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction
#         pointer to the value from the second parameter. Otherwise, it does nothing.
#         """
#         values = self.get_param_values(param_modes, params)
#         if not values[0]:
#             self.parent.jump = values[1]

#     def is_less_than(self, param_modes, params):
#         """
#         Opcode 7 is less than: if the first parameter is less than the second parameter,
#         it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
#         """
#         program = self.parent.program
#         values = self.get_param_values(param_modes, params)
#         if values[0] < values[1]:
#             program[params[2]] = 1
#         else:
#             program[params[2]] = 0

#     def is_equals(self, param_modes, params):
#         """
#         Opcode 8 is equals: if the first parameter is equal to the second parameter,
#         it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
#         """
#         program = self.parent.program
#         values = self.get_param_values(param_modes, params)
#         if values[0] == values[1]:
#             program[params[2]] = 1
#         else:
#             program[params[2]] = 0

# class IntCodeComputer():
#     """
#     Class to simulate an IntCode Computer
#     """
#     def __init__(self, program, input_val=(1), output=None):
#         """init method"""
#         # parse program
#         self.program = [int(num) for num in program.split(',')]
#         # init pointer
#         self.ptr = 0
#         # init input
#         self.input = input_val
#         self.output = output
#         if not self.output:
#             self.output = self.default_output
#         # init operations
#         self.operations = {}
#         # define operations
#         for op_code in range(1, 8 + 1):
#             self.operations[op_code] = OpCode(op_code, self)
#         # init jump
#         self.jump = None

#     def default_output(self, value):
#         """
#         default output function
#         """
#         print(f'Output: {value}')

#     def run(self, input_val=None):
#         """
#         Method to run program
#         """
#         # set input if passed
#         if not input_val is None:
#             self.input = input_val
#         # init ptr
#         self.ptr = 0
#         # init last_resut
#         last_output = None
#         # loop until break
#         while True:
#             # run next step
#             output = self.step()
#             # check for result
#             if not output is None:
#                 # check for break(99)
#                 if output == 99:
#                     break
#                 # save output
#                 last_output = output
#         # return last output
#         return last_output

#     def step(self):
#         """
#         Method to step into program one step
#         """
#         # get current intstruction string
#         instruction_text = str(self.program[self.ptr])
#         # the opcode is the rightmost two digits of the first value in an instruction.
#         op_code = int(instruction_text[-2:])
#         if op_code == 99:
#             #99 means that the program is finished and should immediately halt
#             return 99
#         # get operation
#         try:
#             operation = self.operations[op_code]
#         except KeyError:
#             print(f"Invalid op_code {op_code} at ptr {self.ptr}")
#             return 99
#         # Parameter modes are single digits, one per parameter, read right-to-left from the opcode
#         param_modes = list(reversed([int(num) for num in instruction_text[:-2]]))
#         # Any missing modes are 0
#         while len(param_modes) < operation.parameter_count:
#             param_modes.append(0)
#         # init params
#         params = []
#         # get a param for each parameter_count
#         for _ in range(operation.parameter_count):
#             # increment ptr
#             self.ptr += 1
#             # get next param
#             params.append(self.program[self.ptr])
#         # execute operation
#         result = operation.execute(param_modes, params)
#         # if operation set jump, then we jump
#         if self.jump:
#             # move ptr to jump value
#             self.ptr = self.jump
#             # clear jump value
#             self.jump = None
#         else:
#             # increment ptr to next instruction
#             self.ptr += 1
#         return result


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    icc = IntCodeComputer(program=input_value)
    if part == 1:
        return icc.run(1)
    return icc.run(5)


YEAR = 2019
DAY = 5
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
