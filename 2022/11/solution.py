"""
Advent Of Code 2022 day 11

Part 1 was pretty smooth.

I struggled with part 2, but possibly due to being in a meeting the whole time.

Thanks to u/jaccomoc, your solution pointed out what I was doing wrong in mine.
I was finding the least common multiple of the divisor tests, and was implementing
it wrong in my solution. Doing it the right way made it run a lot faster.

Also probably wasted 30 minutes or so trying to figure out why the test data wasn't
getting the right answer, and it was because 1000 != 10000.  Needed to run the
correct number of loops.

After that, part 2 would have run smoothly, except that I forgot to change the
divisor from 3 to 1. So it quickly got the wrong answer.

"""

# import system modules
import time
import math
import operator
from functools import reduce

# import my modules
import aoc  # pylint: disable=import-error


def lcm(num_a, num_b):
    """Function to find the least common multiple of two numbers"""
    return abs(num_a * num_b) // math.gcd(num_a, num_b)


def lcm_of_list(numbers):
    """Function to find the least common multiple of a list of numbers"""
    return reduce(lcm, numbers)


class Monkey:
    """Class to represent a monkey throwing items"""

    def __init__(self, parent, description):
        """init method"""
        self.parent = parent
        self.inspected = 0
        self.items = []
        self.operation = None
        self.monkey_id = None
        self.test = None
        self.targets = {True: None, False: None}
        self.parse_description(description)

    def parse_description(self, description):
        """method to parse a description"""
        lines = description.splitlines()
        self.monkey_id = int(lines[0].split(" ")[1].replace(":", ""))
        self.items = [int(num) for num in lines[1].split(": ")[1].split(", ")]
        # self.operation = lines[2].split(' = ')[1]
        self.operation = self._parse_operation(lines[2])
        self.test = int(lines[3].split(" ")[-1])
        self.targets = {
            True: int(lines[4].split(" ")[-1]),
            False: int(lines[5].split(" ")[-1]),
        }

    def _parse_operation(self, line):
        """Convert the operation line into a callable function"""
        op_map = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.floordiv,  # Use floordiv for integer division
        }
        _, expression = line.split(" = ")
        left, oper, right = expression.split(" ")
        op_func = op_map[oper]

        def operation(old):
            left_val = old if left == "old" else int(left)
            right_val = old if right == "old" else int(right)
            return op_func(left_val, right_val)

        return operation

    def inspect(self, old):
        """method to inspect an item and modify its value"""
        # string = self.operation
        # new = eval(string.replace('old', str(old)))
        new = self.operation(old) % self.parent.lcm
        # if new % self.parent.lcm == 0:
        #     new /= self.parent.lcm
        self.inspected += 1
        return new

    def throw(self, item):
        """Method to throw an item to the next monkey"""
        # After each monkey inspects an item but before it tests your worry level,
        # your relief that the monkey's inspection didn't damage the item causes
        # your worry level to be divided by three and rounded down to the nearest integer.
        if self.parent.divisor != 1:
            item = item // self.parent.divisor
        target = self.targets[item % self.test == 0]
        # print(f"{self.monkey_id} Throwing {item} to {target}")
        next_monkey = self.parent.get(target)
        next_monkey.items.append(item)

    def play_round(self):
        """Method to play a round"""
        while self.items:
            self.throw(self.inspect(self.items.pop(0)))

    def __str__(self):
        """string method"""
        my_string = f"Monkey {self.monkey_id}: {self.items}"
        return my_string


class Monkeys:
    """collection class for Monkey()"""

    def __init__(self, divisor=3):
        self.monkeys = {}
        self.divisor = divisor
        self.lcm = None

    def add(self, description):
        """add a monkey to the collection based on description"""
        monkey = Monkey(self, description)
        self.monkeys[monkey.monkey_id] = monkey
        self.lcm = lcm_of_list([monkey.test for monkey in self])

    def get(self, monkey_id):
        """method to retrieve a monkey"""
        return self.monkeys.get(monkey_id, None)

    def __iter__(self):
        """Return an iterator over the collection sorted by monkey_id"""
        return iter(
            monkey for _, monkey in sorted(self.monkeys.items(), key=lambda x: x[0])
        )

    def __str__(self):
        """string method"""
        my_string = "Monkeys:\n"
        my_string += "\n".join(monkey for monkey in self)
        return my_string


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    monkeys = Monkeys()
    rounds = 20
    if part == 2:
        monkeys.divisor = 1
        rounds = 10000
    for description in input_value.split("\n\n"):
        monkeys.add(description)
    for _ in range(rounds):
        for monkey in monkeys:
            monkey.play_round()
    inspected = sorted([monkey.inspected for monkey in monkeys])
    # part 2
    # 16162291125 too high, forgot to change monkeys.divisor
    # 15048718170 - correct
    return math.prod(inspected[-2:])


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2022, 11)
    input_data = my_aoc.load_text()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 58056, 2: 15048718170}
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
