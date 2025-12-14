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
import logging
import argparse
from itertools import permutations

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from intcode import IntCodeComputer  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def run_sequence(program, sequence):
    """
    Function to run a sequence
    """
    # init amp_ids
    amp_ids = ["A", "B", "C", "D", "E"]
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
    amps["A"].inputs.append(0)
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
                print(
                    f"amp: {amp_id}, ptr: {amp.ptr} {amp.program[amp.ptr]}, inputs: {amp.inputs}"
                )
            break
        # walk amps
        for amp in amps.values():
            # if still running
            if amp.ptr != -1:
                # execute step
                amp.step()
    # return last output
    return amps["E"].last_output


def parse_input(input_text):
    """
    Return stripped program text.
    """
    return input_text.strip()


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    sequences = []
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


YEAR = 2019
DAY = 7
input_format = {
    1: parse_input,
    2: parse_input,
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
