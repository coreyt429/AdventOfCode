"""
Advent Of Code 2017 day 18

I struggled too much with this one.

My initial implementation wasn't working, it may have worked if I had found the bug,
but after reviewing a few other implementations, I realized mathcing instruction
for instruction was going to be inefficient.  So I changed the processing to batch
processing for each computer.  So now each computer runs the program until it terminates
or is io blocked.  That still led me to a loop, that I was struggling with. My logic
flow looked like others, and I was getting to the same state in about the same time,
I was just looping past the answer.  Stepping back through the instruction handlers,
I found that I had coded jgz to jump on non-zero values instead of greater than zero
values.  Changed that condition, and it worked like magic.
"""

# import system modules
import time

# uncomment the next line to turn on sound for part 1
# import winsound
from collections import deque


# import my modules
import aoc  # pylint: disable=import-error


# having fun with this one, in case this makes a song
class SoundPlayer:
    """
    Class SoundPlayer,  this turned out to be pretty useless,
    but a was still fun.  Just commenting out the slow parts now
    """

    def __init__(self):
        """
        init player
        """
        self.history = []

    def last(self):
        """
        return last played frequency
        """
        return self.history[-1]

    def play(self, frequency):
        """
        play sound and update history
        """
        if 37 <= frequency <= 32767:
            # leaving because it was fun
            # commenting out because it slowed us down
            # winsound.Beep(frequency, 500)
            pass
        # print(f"Play {frequency}")
        self.history.append(frequency)


class Computer:
    """
    Class to represent a computer
    """

    # cmd handler function table

    def __init__(self, program=None, comp_id=None):
        """
        init computer
        """
        self.handlers = {
            "snd": self.do_snd,
            "set": self.do_set,
            "add": self.do_add,
            "mul": self.do_mul,
            "mod": self.do_mod,
            "rcv": self.do_rcv,
            "jgz": self.do_jgz,
        }
        self.registers = {
            "pointer": 0,
            "sent": 0,
            "received": 0,
            "recover": None,
            "iowait": False,
        }
        self.program = []
        self.player = SoundPlayer()
        self.partner = None
        self.buffer = deque([])
        self.comp_id = comp_id
        if program:
            self.load_program(program)
        if self.comp_id:
            self.registers["p"] = self.comp_id

    def __str__(self):
        """
        string representation, primarily used in debugging
        """
        my_string = f"{self.comp_id}: running {self.running()}, "
        my_string = f"iowait: {self.registers['iowait']}, "
        my_string += f"pointer: {self.registers['pointer']}/{len(self.program)}, "
        my_string += f"sent: {self.registers['sent']}, buffer: {len(self.buffer)}, "
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
            return self.handlers[instruction](current)
        return self.running()

    def run_program(self):
        """
        run program loop
        """
        # self.registers['pointer'] = 0
        while self.run_next_instruction():
            pass
        return self.running()

    def do_send(self, instruction):
        """
        handler for instruction snd part 2
        """
        self.partner.buffer.append(self.value(instruction["x"]))
        self.partner.registers["iowait"] = False
        self.registers["pointer"] += 1
        self.registers["sent"] += 1
        return True

    def do_receive(self, instruction):
        """
        handler for instruction rcv part 2
        """
        if len(self.buffer) == 0:
            self.registers["iowait"] = True
            return False
        self.registers["iowait"] = False
        self.registers[instruction["x"]] = self.buffer.popleft()
        self.registers["pointer"] += 1
        return True

    def do_snd(self, instruction):
        """
        handler for instruction snd part 1
        """
        frequency = self.value(instruction["x"])
        self.registers["sent"] += 1
        self.player.play(frequency)
        self.registers["pointer"] += 1
        return True

    def do_set(self, instruction):
        """
        handler for instruction set
        """
        self.registers[instruction["x"]] = self.value(instruction["y"])
        self.registers["pointer"] += 1
        return True

    def do_add(self, instruction):
        """
        handler for instruction add
        """
        self.registers[instruction["x"]] += self.value(instruction["y"])
        self.registers["pointer"] += 1
        return True

    def do_mul(self, instruction):
        """
        handler for instruction mul
        """
        self.registers[instruction["x"]] *= self.value(instruction["y"])
        self.registers["pointer"] += 1
        return True

    def do_mod(self, instruction):
        """
        handler for instruction mod
        """
        self.registers[instruction["x"]] %= self.value(instruction["y"])
        self.registers["pointer"] += 1
        return True

    def do_rcv(self, instruction):
        """
        handler for instruction rcv
        """
        value = self.value(instruction["x"])
        if value:
            self.registers["recover"] = self.player.last()
            # at least for part 1, we want to end here
            self.registers["pointer"] += len(self.program)
        self.registers["pointer"] += 1
        return True

    def do_jgz(self, instruction):
        """
        handler for instruction jgz
        """
        # hmm, here lies the bug that tripped be up.  I was this to be non-zero
        # it needs to be non-zero and positive
        if self.value(instruction["x"]) > 0:
            self.registers["pointer"] += self.value(instruction["y"])
        else:
            self.registers["pointer"] += 1
        return True


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        computer = Computer(input_value)
        computer.run_program()
        return computer.registers["recover"]
    # init computers
    computers = {0: Computer(input_value, 0), 1: Computer(input_value, 1)}

    # establish relationship
    computers[0].partner = computers[1]
    computers[1].partner = computers[0]

    # override snd and rcv
    for comp in computers.values():
        comp.handlers["snd"] = comp.do_send
        comp.handlers["rcv"] = comp.do_receive

    while True:
        running = False
        for comp in computers.values():
            if not comp.running():
                break
            running = True
            comp.run_program()

        if not running:
            break
        if all(comp.registers["iowait"] for comp in computers.values()):
            break
    return computers[1].registers["sent"]


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017, 18)
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
