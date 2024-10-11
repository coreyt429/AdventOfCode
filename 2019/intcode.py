"""
intcode module used by multiple 2019 solutions.

When making changed be sure to rerun previous puzzles be sure
we don't break anything:
    python -m 2019.2.solution # doesn't use this yet, but should
    python -m 2019.5.solution
    python -m 2019.7.solution
    python -m 2019.9.solution
    python -m 2019.11.solution
    python -m 2019.13.solution
    python -m 2019.15.solution
    python -m 2019.17.solution

Man, I wish I had understood what "It will perform a series of checks
on each opcode, output any opcodes (and the associated parameter modes)
that seem to be functioning incorrectly" meant on the previous puzzles.
It was much easier debugging once I realized the output was telling me
where the problem was.

"""

import math
from copy import deepcopy

class OpCode():
    """
    Class to represent an operation
    """
    # parameter modes, more a reminder for me, not sure this will get used
    parameter_modes = {
        0: 'position',
        1: 'immediate'
    }

    def __init__(self, op_code, parent):
        """init method"""
        # set op_code
        self.op_code = op_code
        # set parmeter_count, I'm not sure this should be passed here
        # since everything else about the function is defined here
        # so should the parameter_count
        parameter_counts = [0, 3, 3, 1, 1, 2, 2, 3, 3, 1]
        self.parameter_count = parameter_counts[self.op_code]
        # set parent, needed to access program memory
        self.parent = parent

        # function map of known operations
        self.opcode_func_map = {
            1: self.add_and_store,
            2: self.multiply_and_store,
            3: self.input_and_store,
            4: self.retrieve_and_output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.is_less_than,
            8: self.is_equals,
            9: self.adjust_relative_base
        }
        self.execute = self.opcode_func_map[self.op_code]

    def get_param_values(self, param_modes, params):
        """
        Method to get param values
        """
        # init values
        values = []
        # get program from parent
        parent = self.parent
        program = parent.program
        # walk modes to set param values
        for idx, mode in enumerate(param_modes):
            # position mode
            if mode == 0:
                # get value from program
                values.append(program.get(params[idx], 0))
            # immediate
            elif mode == 1:
                # set value from param
                values.append(params[idx])
            # relative
            elif mode == 2:
                offset = parent.relative_base
                # get value from program with relative base
                # The important difference is that relative mode parameters don't count from
                # address 0. Instead, they count from a value called the relative base. The
                # relative base starts at 0.
                values.append(program.get(params[idx] + offset, 0))
            else:
                # we shouldn't see this
                raise IndexError(f'Invalid parameter mode: {mode}')
        # return value list
        return values

    def add_and_store(self, param_modes, params):
        """
        Opcode 1 adds together numbers read from two positions and stores the result in a third
        position. The three integers immediately after the opcode tell you these three positions
        - the first two indicate the positions from which you should read the input values, and
        the third indicates the position at which the output should be stored.
        """
        program = self.parent.program
        values = self.get_param_values(param_modes, params)
        param = params[2]
        if param_modes[2] == 2:
            param += self.parent.relative_base
        program[param] = sum(values[:2])

    def multiply_and_store(self, param_modes, params):
        """
        Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of
        adding them. Again, the three integers after the opcode indicate where the inputs and
        outputs are, not their values.
        """
        program = self.parent.program
        values = self.get_param_values(param_modes, params)
        param = params[2]
        if param_modes[2] == 2:
            param += self.parent.relative_base
        program[param] = math.prod(values[:2])

    def input_and_store(self, param_modes, params):
        """
        Opcode 3 takes a single integer as input and saves it to the position
        given by its only parameter.
        """
        program = self.parent.program
        # values = self.get_param_values(param_modes, params)
        # this shouldn't be, but for days 5 and 7, param_mode 0 didn't used params, not values
        # logically, that should just be for mode 0
        if param_modes[0] == 2:
            program[params[0] + self.parent.relative_base] = self.parent.inputs.pop(0)
            return
        program[params[0]] = self.parent.inputs.pop(0)

    def retrieve_and_output(self, param_modes, params):
        """
        Opcode 4 outputs the value of its only parameter.
        """
        values = self.get_param_values(param_modes, params)
        parent = self.parent
        parent.last_output = values[0]
        # check for connected output
        if isinstance(parent.output, list):
            parent.output.append(values[0])
        else:
            parent.output = values[0]
        return values[0]

    def jump_if_true(self, param_modes, params):
        """
        Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction
        pointer to the value from the second parameter. Otherwise, it does nothing.
        """
        values = self.get_param_values(param_modes, params)
        if values[0]:
            self.parent.jump = values[1]

    def jump_if_false(self, param_modes, params):
        """
        Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction
        pointer to the value from the second parameter. Otherwise, it does nothing.
        """
        values = self.get_param_values(param_modes, params)
        if not values[0]:
            self.parent.jump = values[1]

    def is_less_than(self, param_modes, params):
        """
        Opcode 7 is less than: if the first parameter is less than the second parameter,
        it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        """
        program = self.parent.program
        values = self.get_param_values(param_modes, params)
        param = params[2]
        if param_modes[2] == 2:
            param += self.parent.relative_base
        if values[0] < values[1]:
            program[param] = 1
        else:
            program[param] = 0

    def is_equals(self, param_modes, params):
        """
        Opcode 8 is equals: if the first parameter is equal to the second parameter,
        it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        """
        program = self.parent.program
        values = self.get_param_values(param_modes, params)
        param = params[2]
        if param_modes[2] == 2:
            param += self.parent.relative_base
        if values[0] == values[1]:
            program[param] = 1
        else:
            program[param] = 0
    def adjust_relative_base(self, param_modes, params):
        """
        Opcode 9 adjusts the relative base by the value of its only parameter. The relative
        base increases (or decreases, if the value is negative) by the value of the parameter.
        """
        parent = self.parent
        # program = self.parent.program
        values = self.get_param_values(param_modes, params)
        parent.relative_base += values[0]

class IntCodeComputer():
    """
    Class to simulate an IntCode Computer
    intcode.py:195:0: R0902: Too many instance attributes (9/7) (too-many-instance-attributes)
    combine some into a cfg dict
    """
    def __init__(self, program, input_val=None, relative_base=0):
        """init method"""
        # parse program
        self.source = program
        # self.program = dict(zip(enumerate(int(num) for num in program.split(','))))
        self.program = {
            key:int(value) for key, value in enumerate(program.split(','))
            }
        self.program_backup = deepcopy(self.program)
        # init pointer
        self.ptr = 0
        #
        # relative_base
        self.relative_base = relative_base
        # init running
        # I originally used a boolean for this, but pylint doesn't
        # like too many class properties, so I changed it to
        # set ptr to -1 instead and check for that condition.
        # original .running handling is mostly intact in comments
        # self.running = True
        # init input
        self.inputs = []
        if input_val is not None:
            self.inputs.append(input_val)
        # init output
        self.output = None
        # init last_output
        self.last_output = None
        # init operations
        self.operations = {}
        # define operations
        for op_code in range(1, 9 + 1):
            self.operations[op_code] = OpCode(op_code, self)
        # init jump
        self.jump = None

    def backup(self):
        """Method to backup program state"""
        self.program_backup = deepcopy(self.program)

    def restore(self):
        """Method to restore backup"""
        self.program = deepcopy(self.program_backup)
        self.ptr = 0

    def set_output(self, other):
        """Method to connect output to input"""
        if isinstance(other, list):
            self.output = other
            return
        self.output = other.inputs

    def run(self, input_val=None):
        """
        Method to run program
        """
        # set input if passed
        if not input_val is None:
            self.inputs.append(input_val)
        # init ptr
        self.ptr = 0
        # init last_resut
        last_output = None
        # loop until break
        while True:
            # print(self)
            # run next step
            output = self.step()
            # check for result
            if not output is None:
                # check for break(99)
                if output == 99:
                    break
                # save output
                last_output = output
        # return last output
        return last_output

    def next_op_code(self):
        """
        Method to get the next op_code
        """
        instruction_text = str(self.program[self.ptr])
        # the opcode is the rightmost two digits of the first value in an instruction.
        return int(instruction_text[-2:])

    def step(self):
        """
        Method to step into program one step
        """
        # get current intstruction string
        instruction_text = str(self.program[self.ptr])
        # print(f"instruction_text: {instruction_text}")
        # the opcode is the rightmost two digits of the first value in an instruction.
        op_code = int(instruction_text[-2:])
        if op_code == 99:
            self.ptr = -1
            # self.running = False
            #99 means that the program is finished and should immediately halt
            return 99
        # waiting on input
        if op_code == 3 and len(self.inputs) == 0:
            # return without moving ptr
            return -1
        # get operation
        try:
            operation = self.operations[op_code]
        except KeyError:
            print(f"Invalid op_code {op_code} at ptr {self.ptr}")
            print(f"op_codes: {self.operations.keys()}")
            return 99
        # Parameter modes are single digits, one per parameter, read right-to-left from the opcode
        param_modes = list(reversed([int(num) for num in instruction_text[:-2]]))
        # Any missing modes are 0
        while len(param_modes) < operation.parameter_count:
            param_modes.append(0)
        # init params
        params = []
        # get a param for each parameter_count
        for _ in range(operation.parameter_count):
            # increment ptr
            self.ptr += 1
            # get next param
            params.append(self.program[self.ptr])
        # execute operation
        result = operation.execute(param_modes, params)
        # if operation set jump, then we jump
        if self.jump is not None:
            # move ptr to jump value
            self.ptr = self.jump
            # clear jump value
            self.jump = None
        else:
            # increment ptr to next instruction
            self.ptr += 1
        return result

    def __str__(self) -> str:
        """string"""
        # my_string = f"program: {self.source}\n"
        memory = ', '.join((f"{key}:{value}" for key, value in self.program.items()))
        my_string = f"ptr: {self.ptr}, relative: {self.relative_base},"
        my_string += f"inputs: {self.inputs}, outputs: {self.output}, mem: {memory}"
        # my_string += f"Memory:\n"
        # for key, value in self.program.items():
        #     my_string += f"    {key:4}: {value}\n"
        return my_string
