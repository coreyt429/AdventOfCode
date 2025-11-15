"""
Advent Of Code 2019 day 23

IntCodeComputer handled this pretty well.  Part 1, I worked completely in
the scratchpad.

Part 2, converted the part 1 logic into get_next_nat() then the solve() logic
is simply get_next_nat() was y_val is the same as the last return y_val, if not stick it in
iccs[0].inputs

The couple of trip ups I had, in case they help anyone else are:
  - don't move packets from outputs to packet_queue until they are complete
  - don't compare y_val to last_y_val in every pass, only the when inputs_waiting
    is false.

Part 2 was taking 4.4 seconds.  Tried changing the lists to deque to use popleft()
instead of pop(0).  This does not seem to have impacted run time.

profiling shows intcode.py:302(step) as the culprit, but further optimzations there
are not really justified to shave 4.4 seconds down.  As this would require regression
testing against previous puzzles using the code as well.
"""

# import system modules
import time
from collections import deque

# import my modules
from intcode import IntCodeComputer  # pylint: disable=import-error
import aoc  # pylint: disable=import-error


def get_next_nat(iccs, packet_queue):
    """
    Function to execute icc commands until a packet is sent
    to address 255
    """
    keep_running = True
    while keep_running:
        for idx, icc in enumerate(iccs):
            # check to see if output has a complete packet
            while len(icc.output) > 2:
                # move next packet to the queue
                for _ in range(3):
                    packet_queue.append(icc.output.popleft())
        # print(f"Packet Queue: {packet_queue}")
        while packet_queue:
            idx = packet_queue.popleft()
            # print(idx, packet_queue)
            x_val = packet_queue.popleft()
            y_val = packet_queue.popleft()
            # print(f"packet: {idx} {x_val} {y_val}")
            if idx == 255:
                keep_running = False
                return x_val, y_val
            iccs[idx].inputs.append(x_val)
            iccs[idx].inputs.append(y_val)
        if not keep_running:
            break
        for idx, icc in enumerate(iccs):
            if not icc.inputs:
                icc.inputs.append(-1)
            # print(idx, icc.next_op_code(),icc.inputs, icc.output)
            icc.step()
    raise RuntimeError("Should not reach here")


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    iccs = []
    packet_queue = deque()
    for idx in range(50):
        icc = IntCodeComputer(input_value)
        icc.output = deque()
        # print(type(icc.output))
        icc.inputs.append(idx)
        iccs.append(icc)
    if part == 1:
        # What is the Y value of the first packet sent to address 255
        return get_next_nat(iccs, packet_queue)[1]
    last_y_val = None
    while True:
        x_val, y_val = get_next_nat(iccs, packet_queue)
        inputs_waiting = False
        for icc in iccs:
            if icc.inputs and icc.inputs[0] != -1:
                inputs_waiting = True
        if not inputs_waiting:
            # What is the first Y value delivered by the NAT to the computer at address 0
            # twice in a row?
            if y_val == last_y_val:
                return y_val
            iccs[0].inputs.append(x_val)
            iccs[0].inputs.append(y_val)
            last_y_val = y_val


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019, 23)
    input_text = my_aoc.load_text()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 26163, 2: 18733}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
