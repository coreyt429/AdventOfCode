"""
Advent Of Code 2017 day 25

"""
# import system modules
import time
import re
from collections import deque

# import my modules
import aoc # pylint: disable=import-error

# regex patterns
pattern_begin      = re.compile(r'Begin in state (\w)\.')
pattern_diagnostic = re.compile(r'Perform a diagnostic checksum after (\d+) steps\.')
pattern_new_state  = re.compile(r'In state (\w):')
pattern_condition  = re.compile(r'\s+If the current value is (\d):')
pattern_write      = re.compile(r'\s+- Write the value (\d).')
pattern_move       = re.compile(r'\s+- Move one slot to the (\w+).')
pattern_next       = re.compile(r'\s+- Continue with state (\w).')

def parse_input(lines):
    """
    Functino to parse input data
    """
    movement = {
        "right": 1,
        "left": -1
    }
    machine = {"init_state": "", "checksum_steps": "", "states": {}}
    for line in lines:
        match = pattern_begin.match(line)
        if match:
            machine['init_state'] = match.group(1)
        match = pattern_diagnostic.match(line)
        if match:
            machine['checksum_steps'] = int(match.group(1))
        match = pattern_new_state.match(line)
        if match:
            current_state = match.group(1)
            machine['states'][current_state] = {}
        match = pattern_condition.match(line)
        if match:
            condition = int(match.group(1))
            machine['states'][current_state][condition] = {}
        match = pattern_write.match(line)
        if match:
            machine['states'][current_state][condition]['write'] = int(match.group(1))
        match = pattern_move.match(line)
        if match:
            machine['states'][current_state][condition]['movement'] = movement[match.group(1)]
        match = pattern_next.match(line)
        if match:
            machine['states'][current_state][condition]['next'] = match.group(1)
    return machine

def run_machine(turing_machine):
    """
    Function to run turing machine and provide checksum
    """
    current_state = turing_machine['init_state']
    states = turing_machine['states']
    steps = turing_machine['checksum_steps']
    cursor = 0
    tape = deque([0])
    #print(steps, state, cursor, tape, tape[cursor])
    for _ in range(steps):
        # get current state
        state = states[current_state]
        # get current condition
        conditional = tape[cursor]
        #print(step, state)
        # write new value
        tape[cursor] = state[conditional]['write']
        # move cursor
        cursor += state[conditional]['movement']
        # extend left if needed
        if cursor == -1:
            cursor = 0
            tape.appendleft(0)
        # extend right if needed
        if cursor > len(tape) - 1:
            tape.append(0)
        # set next condition
        current_state = state[conditional]['next']
        #print(tape)
    return sum(tape)

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return "Reboot the printer"
    turing_machine = parse_input(input_value)
    #print(turing_machine)
    checksum = run_machine(turing_machine)
    return checksum

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017,25)
    #input_text = my_aoc.load_text()
    #print(input_text)
    input_lines = my_aoc.load_lines()
    #print(input_lines)
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
