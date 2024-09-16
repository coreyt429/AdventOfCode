"""
Advent Of Code 2019 day 7

This one was pretty straight forward.  The previous work on the
OpCode and IntCodeComputer classes paid dividends here.

All I really had to do was change the input handling, and add
a wait state for input operations when there is no input.

Other than that, I couldn't use .run() since I needed to run in
parallel, the run_sequence function was born for this case to
make all 5 step throught their programs together.

"""
# import system modules
import time
import math
from  itertools import permutations

# import my modules
import aoc # pylint: disable=import-error

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
        parameter_counts = [0, 3, 3, 1, 1, 2, 2, 3, 3]
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
            8: self.is_equals
        }
        self.execute = self.opcode_func_map[self.op_code]

    def get_param_values(self, param_modes, params):
        """
        Method to get param values
        """
        # init values
        values = []
        # get program from parent
        program = self.parent.program
        # walk modes to set param values
        for idx, mode in enumerate(param_modes):
            # position mode
            if mode == 0:
                # get value from program
                values.append(program[params[idx]])
            # immediate
            elif mode == 1:
                # set value from param
                values.append(params[idx])
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
        program[params[2]] = sum(values[:2])

    def multiply_and_store(self, param_modes, params):
        """
        Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of
        adding them. Again, the three integers after the opcode indicate where the inputs and
        outputs are, not their values.
        """
        program = self.parent.program
        values = self.get_param_values(param_modes, params)
        program[params[2]] = math.prod(values[:2])

    def input_and_store(self, param_modes, params):
        """
        Opcode 3 takes a single integer as input and saves it to the position
        given by its only parameter.
        """
        # useless action to keep pylint happy
        type(param_modes)
        program = self.parent.program
        # print(f"input_and_store: {self.parent.inputs}")
        program[params[0]] = self.parent.inputs.pop(0)

    def retrieve_and_output(self, param_modes, params):
        """
        Opcode 4 outputs the value of its only parameter.
        """
        # useless action to keep pylint happy
        type(param_modes)
        parent = self.parent
        program = parent.program
        parent.last_output = program[params[0]]
        parent.output.append(program[params[0]])
        return program[params[0]]

    def jump_if_true(self, param_modes, params):
        """
        Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction
        pointer to the value from the second parameter. Otherwise, it does nothing.
        """
        values = self.get_param_values(param_modes, params)
        if values[0]:
            # print(True, values[1])
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
        if values[0] < values[1]:
            program[params[2]] = 1
        else:
            program[params[2]] = 0

    def is_equals(self, param_modes, params):
        """
        Opcode 8 is equals: if the first parameter is equal to the second parameter,
        it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        """
        program = self.parent.program
        values = self.get_param_values(param_modes, params)
        if values[0] == values[1]:
            program[params[2]] = 1
        else:
            program[params[2]] = 0

class IntCodeComputer():
    """
    Class to simulate an IntCode Computer
    """
    def __init__(self, program, input_val=None):
        """init method"""
        # parse program
        self.program = [int(num) for num in program.split(',')]
        # init pointer
        self.ptr = 0
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
        for op_code in range(1, 8 + 1):
            self.operations[op_code] = OpCode(op_code, self)
        # init jump
        self.jump = None

    def set_output(self, other):
        """Method to connect output to input"""
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

    def step(self):
        """
        Method to step into program one step
        """
        # get current intstruction string
        instruction_text = str(self.program[self.ptr])
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
        if self.jump:
            # move ptr to jump value
            self.ptr = self.jump
            # clear jump value
            self.jump = None
        else:
            # increment ptr to next instruction
            self.ptr += 1
        return result

def run_sequence(program, sequence):
    """
    Function to run a sequence
    """
    # init amp_ids
    amp_ids = ['A', 'B', 'C', 'D', 'E']
    # init amps
    amps = {}
    # walk amp_ids
    for idx, amp_id in enumerate(amp_ids):
        # init amp
        amps[amp_id] = IntCodeComputer(program, sequence[idx])

    # walk amps
    for idx, amp_id in enumerate(amp_ids):
        # connect inputs and outputs
        amps[amp_id].set_output(amps[amp_ids[(idx + 1) % len(amp_ids)]])
    # The first amplifier's input value is 0
    amps['A'].inputs.append(0)
    # init counter
    counter = 0
    # while icc's are still running
    while any((amp.ptr != -1 for amp in amps.values())):
        # increment counter
        counter += 1
        # safety valve
        if counter > 1000:
            # dump data and break loop
            for amp_id, amp in amps.items():
                print(f"amp: {amp_id}, ptr: {amp.ptr} {amp.program[amp.ptr]}, inputs: {amp.inputs}")
            break
        # walk amps
        for amp in amps.values():
            # if still running
            if amp.ptr != -1:
                # execute step
                amp.step()
    # return last output
    return amps['E'].last_output

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        sequences = permutations(range(5))
    if part == 2:
        sequences = permutations(range(5, 10))
    # inint max_output
    max_output = 0
    # iterate over possible sequences
    for sequence in sequences:
        # init output
        output = run_sequence(program=input_value, sequence=sequence)
        if output is not None:
            # check final output againse max_output
            max_output = max(max_output, output)
    # return largest value
    return max_output

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019,7)
    input_text = my_aoc.load_text()
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
    # correct answers to validate changes
    correct = {
        1: 21000,
        2: 61379886
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
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
        assert answer[my_part] == correct[my_part]