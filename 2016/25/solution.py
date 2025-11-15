"""
Advent Of Code 2016 day 25

Thanks to day 23 struggles, this one was easier.

There are two loops to deal with, but only one saves a significant amount of time.
The 3, 4, 5, 6, 7 loop I solved, so now it completes in 7 seconds
There is another loop at 12, that I haven't worked out yet.

Don't forget that the rules from Day 23 still apply.  The tgl operation,
may impact the out operation.  I'm not 100% certain that this happened,
but I accounted for it in case.  Nevermind, I put a check in for this case,
and it does not seem to occur.  Still worth handling just in case.

"""

# import system modules
import time
import re

# import my modules
import aoc  # pylint: disable=import-error

# define globals to use
registers = {"a": 0, "b": 0, "c": 0, "d": 0}

# instruction list
instructions = []
instructions.append("inc")
instructions.append("dec")
instructions.append("cpy")
instructions.append("jnz")
instructions.append("tgl")
instructions.append("out")

# regex's to parse instructions
pattern_instruction = re.compile(r"(\w+) (\S+) *(\S+)?")
pattern_jump_value = re.compile(r"([+-])?(\S+)")


def decode_program(input_textblock):
    """
    Function to parse text block the program instructions

    parameters:
        uinput_text: string name of data

    returns:
        program: list of dict, program instructions
    """
    program = []
    # split text into lines
    lines = input_textblock.split("\n")

    # process each line
    for line in lines:
        # instruction regex r'(\w+) (\S+) *(\S+)?'
        matches = pattern_instruction.match(line)
        if matches:
            instruction = matches.group(1)
            # simple instructions inc, and dec,
            #   just store instruction and register
            if instruction in ["inc", "dec", "out"]:
                register = matches.group(2)
                program.append({"instruction": instruction, "x": register})
            elif instruction in ["tgl"]:
                register = matches.group(2)
                program.append({"instruction": instruction, "x": register})
            # copy is more comples, source can be an int or register
            elif instruction in ["cpy"]:
                source = matches.group(2)
                # is it a number, if so convert to int?
                if source.isdigit():
                    source = int(source)
                # target should be a register
                register = matches.group(3)
                program.append({"instruction": instruction, "x": source, "y": register})
            # jnz, also uses int or register
            elif instruction in ["jnz"]:
                val_x = matches.group(2)
                # int? convert it
                if val_x.isdigit():
                    val_x = int(val_x)
                # split val_y with jump regex r'([+-])?(\d+)'
                val_y = matches.group(3)
                matches2 = pattern_jump_value.match(val_y)
                direction = matches2.group(1) or "+"
                if matches2.group(2) in registers:
                    val_y = matches2.group(2)
                else:
                    val_y = int(matches2.group(2))
                # if direction is - convert val_y to negative
                if direction == "-":
                    val_y *= -1
                program.append({"instruction": instruction, "x": val_x, "y": val_y})
    return program


def do_inc(**kwargs):
    """
    Function to execute inc instruction
    """
    registers[kwargs["x"]] += 1
    kwargs["pointer"] += 1
    return kwargs["pointer"]


def do_out(**kwargs):
    """
    Function to execute inc instruction
    """
    xmit_value = registers.get(kwargs["x"], kwargs["x"])
    kwargs["pointer"] += 1
    return kwargs["pointer"], str(xmit_value)


def do_dec(**kwargs):
    """
    Function to execute dec instruction
    """
    registers[kwargs["x"]] -= 1
    kwargs["pointer"] += 1
    return kwargs["pointer"]


def do_cpy(**kwargs):
    """
    Function to execute cpy instruction
    """
    if kwargs["x"] in registers:
        # no, get register value
        registers[kwargs["y"]] = registers[kwargs["x"]]
    else:
        # yes, use source value
        registers[kwargs["y"]] = int(kwargs["x"])
    kwargs["pointer"] += 1
    return kwargs["pointer"]


def do_jnz(**kwargs):
    """
    Function to execute jnz instruction
    """
    x_value = kwargs["x"]
    # is int?
    if kwargs["x"] in registers:
        # no, get value from register
        x_value = registers[kwargs["x"]]
    # is zero?
    if x_value != 0:
        # No, jump
        if kwargs["y"] in registers:
            kwargs["pointer"] += registers[kwargs["y"]]
        else:
            kwargs["pointer"] += kwargs["y"]
    else:
        # Yes, move forward 1
        kwargs["pointer"] += 1
    return kwargs["pointer"]


def do_tgl(**kwargs):
    """
    Function to execute tgl instruction
    """
    if kwargs["x"] in registers:
        target_pointer = kwargs["pointer"] + registers[kwargs["x"]]
    else:
        target_pointer = kwargs["pointer"] + int(kwargs["x"])
    kwargs["pointer"] += 1
    if target_pointer < len(kwargs["program"]):
        target = kwargs["program"][target_pointer]
        # For one-argument instructions, inc becomes dec, and all other one-argument
        # instructions become inc.
        if target["instruction"] == "dec":
            target["instruction"] = "inc"
        elif target["instruction"] == ["inc", "out"]:
            target["instruction"] = "dec"
        # If tgl toggles itself (for example, if a is 0, tgl a would target itself and
        # become inc a), the resulting instruction is not executed until the next time
        # it is reached.
        elif target["instruction"] == "tgl":
            target["instruction"] = "inc"
        # For two-argument instructions, jnz becomes cpy, and all other
        # two-instructions become jnz.
        elif target["instruction"] == "jnz":
            target["instruction"] = "cpy"
        elif target["instruction"] == "cpy":
            target["instruction"] = "jnz"
    return kwargs["pointer"]


def run_program(program):
    """
    Executes the program instructions in PROGRAM
    """
    # Function mappings
    func_map = {
        "inc": lambda **kwargs: (do_inc(**kwargs), None),
        "dec": lambda **kwargs: (do_dec(**kwargs), None),
        "cpy": lambda **kwargs: (do_cpy(**kwargs), None),
        "jnz": lambda **kwargs: (do_jnz(**kwargs), None),
        "tgl": lambda **kwargs: (do_tgl(**kwargs), None),
        "out": do_out,  # This one will return both pointer and signal
    }
    # pointer for current program location
    pointer = 0
    # while pointer is valid, keep processing
    signal = ""
    while 0 <= pointer < len(program):
        if len(signal) == 8:
            # break the look when the signal gets to 8 bytes
            break
        if pointer == 3:
            # short circuite the 3, 4, 5, 6loop
            # 3: inc   d     {'a': 3, 'b': 1, 'c': 7, 'd': 367}
            # 4: dec   b     {'a': 3, 'b': 1, 'c': 7, 'd': 368}
            # 5: jnz   b  -2 {'a': 3, 'b': 0, 'c': 7, 'd': 368}
            # 6: dec   c     {'a': 3, 'b': 0, 'c': 7, 'd': 368}
            # 7: jnz   c  -5 {'a': 3, 'b': 0, 'c': 6, 'd': 368}
            registers["d"] = registers["b"] * registers["c"] + registers["a"]
            registers["c"] = 0
            registers["b"] = 0
            pointer = 8
        # there has to be a way to reduce this loop, but I'm commenting it out for now
        # revisit later? maybe
        # if pointer == 12:
        #    # 12: cpy   2   c {'a': 0, 'b': 2730, 'c': 0, 'd': 2730}
        #    # 12: cpy   2   c {'a': 1, 'b': 2728, 'c': 0, 'd': 2730}
        #    # 12: cpy   2   c {'a': 1364, 'b': 2, 'c': 0, 'd': 2730}
        #    # 17: jnz   c  -4 {'a': 1364, 'b': 0, 'c': 0, 'd': 2730}
        #    registers['a'] = registers['b'] // 2
        #    registers['b'] -= 2
        #    registers['c'] = 0
        #    pointer = 19
        current = program[pointer]
        str_current = f"{pointer:2d}: "
        str_current += (
            f"{current['instruction']} {current['x']:>3} {current.get('y', '  '):>3}"
        )
        # print(f"{str_current} {registers}")
        pointer, xmit_signal = func_map[current["instruction"]](
            program=program,
            pointer=pointer,
            x=current.get("x", None),
            y=current.get("y", None),
        )
        if xmit_signal:
            signal += xmit_signal
    return signal


def solve(input_value):
    """
    Function to solve puzzle
    """
    # initial target pattern, I was matching a longer pattern to get the answer
    # target = '010101010101010101010101010101010101'
    # to improve runtime, reduced to the smallest match that guarantees our answer
    target = "01010101"
    seed = -1
    signal = ""
    # loop until we find the target
    while signal != target:
        seed += 1
        # set register a to seed
        registers["a"] = seed
        # decode program (do this on each pass to reset tgl'd instructions)
        program = decode_program(input_value)
        # execute program
        signal = run_program(program)
        # debug print
        # print(f"Seed: {seed} {signal}")

    return seed


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2016, 25)
    input_text = my_aoc.load_text()
    # print(input_text)
    # input_lines = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # dict to map functions
    funcs = {1: solve, 2: lambda ignore_input: ("Click on 'Transmit Signal'")}
    # loop parts
    for part in parts:
        # log start time
        start = time.time()
        # get answer
        answer[part] = funcs[part](input_text)
        # log end time
        end = time.time()
        # print results
        print(f"Part {part}: {answer[part]}, took {end - start} seconds")
