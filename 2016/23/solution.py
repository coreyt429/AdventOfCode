"""
Advent Of Code 2016 day 23

I struggled a bit with this one. read a few clues, then studied the output to find
the relevant loop.

instructions 5, 6, and 7 loop to calculate egg_count factorial. So I added a
shortcut for that loop to speed it up.

"""

# import system modules
import logging
import argparse
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

# define globals to use
registers = {"a": 0, "b": 0, "c": 0, "d": 0}

# instruction list
instructions = []
instructions.append("inc")
instructions.append("dec")
instructions.append("cpy")
instructions.append("jnz")
instructions.append("tgl")

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
            if instruction in ["inc", "dec"]:
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
        elif target["instruction"] == "inc":
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


# Function mappings
func_map = {"inc": do_inc, "dec": do_dec, "cpy": do_cpy, "jnz": do_jnz, "tgl": do_tgl}


def run_program(program):
    """
    Executes the program instructions in PROGRAM
    """
    # pointer for current program location
    pointer = 0
    # while pointer is valid, keep processing
    while 0 <= pointer < len(program):
        if pointer == 5:
            # short circuite the 5, 6, 7 loop
            # 5: inc   a     -  {'a': 1, 'b': 6, 'c': 5, 'd': 7}
            # 6: dec   c     -  {'a': 2, 'b': 6, 'c': 5, 'd': 7}
            # 7: jnz   c  -2 -  {'a': 2, 'b': 6, 'c': 4, 'd': 7}
            registers["a"] = registers["d"] * registers["b"]
            registers["c"] = 0
            registers["d"] = 1
            pointer = 8
        current = program[pointer]
        str_current = f"{pointer:2d}: "
        str_current += (
            f"{current['instruction']} {current['x']:>3} {current.get('y', '  '):>3}"
        )
        # print(f"{str_current} {registers}")
        pointer = func_map[current["instruction"]](
            program=program,
            pointer=pointer,
            x=current.get("x", None),
            y=current.get("y", None),
        )


def solve(input_value, part=1):
    """
    Function to solve puzzle
    """
    registers["a"] = 7 if part == 1 else 12
    registers["b"] = 0
    registers["c"] = 0
    registers["d"] = 0
    program = decode_program(input_value)
    run_program(program)
    return registers["a"]


YEAR = 2016
DAY = 23
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
