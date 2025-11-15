"""
Advent Of Code 2020 day 15

I played around with data structures on this one.

I started with a big deque for the numbers.  worked great for
test data and part 1.  way to big and slow for part 2.

Converted that to a defaultdict(deque) keyed on the number and
queing its appearances.  Worked, solved the problem, slow.

Optimized deque to only store the last two values.  This got it
down to 22 seconds.

Dropped both, and went with a dict(tuple) keyed on number with
value as a tuple of the last two instances.  time is doen to 13
seconds for part 2, so leaving it at that.

"""

# import system modules
import time
# from collections import deque
# from collections import defaultdict

# import my modules
import aoc  # pylint: disable=import-error


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    numbers = [int(num) for num in input_value[0].split(",")]
    seen = {}
    current = numbers[-1]
    seen = {num: (idx + 1, None) for idx, num in enumerate(numbers)}
    target = 2020 + 1
    if part == 2:
        target = 30000000 + 1
    for turn in range(len(numbers) + 1, target):
        # print(turn, current, seen[current])
        if current not in seen or seen[current][1] is None:
            next_number = 0
        else:
            next_number = seen[current][0] - seen[current][1]
        if next_number in seen:
            seen[next_number] = (turn, seen[next_number][0])
        else:
            seen[next_number] = (turn, None)
        current = next_number
        # if turn % 1000000 == 0:
        # print(f"turn: {turn}, spoken: {current}")
    # attempts:
    # 1: 104 too low
    # 2: 371 got it.  helps if you remember to parse the input
    # part 2:
    # 1: 175594 too high.   ah, input matters, that was using the test input
    # 2: 352, got it.
    return current


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020, 15)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 371, 2: 352}
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
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
