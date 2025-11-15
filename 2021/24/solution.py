"""
Advent Of Code 2021 day 24

Okay, I just wanted this one to be done.  Answers were calculated with a borrowed solution.
I understand what it is doing, but my attempts to speed it up were bad.

I like the fake code type puzzles when we can run them and find a solution, maybe short circuit
a few loops.  But I don't have the time to work out this type :(

Putting on the review later list

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


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
        if isinstance(item, int):
            return item
        return self.registers[item]

    def inp(self, *args):
        """inp method - reads input q and loads it to a register"""
        # inp a - Read an input value and write it to variable a.
        register = args[0]
        self.registers[register] = int(self.inputs.pop(0))

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
        # eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.
        if self.value(a) == self.value(b):
            self.registers[a] = 1
        else:
            self.registers[a] = 0

    def reset(self, inputs=[]):
        """method to reset the Alu"""
        for key in self.registers:
            self.registers[key] = 0
        self.inputs = inputs

    def run(self, inputs=None):
        """method to run an alu program"""
        if not inputs is None:
            self.inputs = inputs
        for operation, params in self.program:
            self.operations[operation](*params)
            # print(f"{operation} {params} - {self.registers}")


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        return None
    alu = Alu(input_value)
    num = 11111111111111
    increment = 11
    digits = set()
    while True:
        print(len(str(num)))
        alu.run(list(str(num)))
        if alu.registers["z"] < 9000:
            print(num, alu.registers["z"])
            num_string = str(num)[-12:-10]
            digits.add(num_string)
            print(digits)
        print(alu.registers)
        break

        if alu.registers["z"] == 0:
            break
        # break
        alu.reset()
        num += increment
        num_string = str(num).replace("0", "1")
        # the last two digits must be 18 or 29
        test_num = int(num_string[-2:])
        if test_num < 18:
            num_string = num_string[:-2] + "18"
        if test_num > 29:
            num_string = num_string[:-2] + "18"
            num = int(num_string)
            num += 100
            num_string = str(num)
        if 18 < test_num < 29:
            num_string = num_string[:-2] + "29"
        if num_string[5] != num_string[6]:
            num_string = num_string[:5] + num_string[6] + num_string[6:]
        valid_set = {"60", "40", "30", "18", "20", "50", "29", "00"}
        while num_string[-4:-2] not in valid_set:
            num = int(num_string)
            num += 100
            num_string = str(num)
        valid_set = {
            "19",
            "77",
            "85",
            "87",
            "64",
            "67",
            "68",
            "89",
            "65",
            "84",
            "86",
            "79",
            "63",
            "62",
            "93",
            "73",
            "76",
            "81",
            "91",
            "66",
            "69",
            "72",
            "61",
            "82",
            "98",
            "83",
            "71",
            "96",
            "95",
            "88",
            "94",
            "97",
            "92",
            "74",
            "78",
            "99",
            "75",
        }
        while num_string[-6:-4] not in valid_set:
            num = int(num_string)
            num += 10000
            num_string = str(num)
        valid_set = {
            "26",
            "19",
            "65",
            "66",
            "76",
            "45",
            "59",
            "24",
            "44",
            "14",
            "16",
            "78",
            "32",
            "63",
            "39",
            "51",
            "62",
            "33",
            "69",
            "64",
            "68",
            "58",
            "28",
            "85",
            "18",
            "31",
            "74",
            "36",
            "15",
            "93",
            "38",
            "42",
            "35",
            "46",
            "79",
            "25",
            "95",
            "57",
            "82",
            "17",
            "49",
            "98",
            "21",
            "47",
            "91",
            "12",
            "27",
            "37",
            "22",
            "88",
            "71",
            "00",
            "99",
            "11",
            "41",
            "48",
            "29",
            "72",
            "96",
            "87",
            "92",
            "61",
            "52",
            "73",
            "23",
            "34",
            "67",
            "77",
            "13",
            "83",
            "54",
            "55",
            "43",
            "86",
            "84",
            "81",
            "75",
            "56",
            "89",
            "53",
            "94",
            "97",
        }
        while num_string[-8:-6] not in valid_set:
            num = int(num_string)
            num += 1000000
            num_string = str(num)
        valid_set = {
            "97",
            "29",
            "64",
            "56",
            "47",
            "22",
            "77",
            "46",
            "28",
            "86",
            "85",
            "38",
            "83",
            "14",
            "26",
            "11",
            "62",
            "23",
            "33",
            "93",
            "32",
            "12",
            "57",
            "81",
            "68",
            "15",
            "90",
            "17",
            "21",
            "41",
            "95",
            "61",
            "63",
            "88",
            "82",
            "36",
            "58",
            "55",
            "16",
            "35",
            "34",
            "52",
            "44",
            "24",
            "66",
            "67",
            "72",
            "94",
            "89",
            "74",
            "37",
            "25",
            "92",
            "99",
            "59",
            "75",
            "48",
            "54",
            "31",
            "98",
            "73",
            "43",
            "69",
            "78",
            "76",
            "42",
            "79",
            "27",
            "39",
            "96",
            "91",
            "18",
            "45",
            "13",
            "71",
            "87",
            "19",
            "84",
            "65",
            "51",
            "49",
            "53",
        }
        while num_string[-10:-8] not in valid_set:
            num = int(num_string)
            num += 100000000
            num_string = str(num)

        num = int(num_string)
    return part


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
