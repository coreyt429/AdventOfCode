"""
Advent Of Code 2016 day 19

This one needed a creative solution, and more familiarity with collections.deque.

Good learning opportunity for me.

"""
import time
import collections

import aoc # pylint: disable=import-error

def solve(input_value, puzzle_part=1):
    """
    Function to solve puzzle.
    This solves part1 efficiently, and I'm sure it would solve part 2
    eventually.  I'm just not that patient (I found coded, tested, and documented
    another solution while it was running, and still killed it without an answer)
    """
    # Initialize deque with elf indices
    queue = collections.deque(range(1, input_value + 1))
    # loop until we have an answer
    while len(queue) > 1:
        # select elf1 and elf2 based on rules for problem part
        if puzzle_part == 1:
            # first two in the queue
            elf1 = queue.popleft()
            elf2 = queue.popleft()
        else:
            # deque rotation was too slow, see solve_part2
            # Pop elf2 at the middle index
            mid_index = len(queue) // 2
            queue.rotate(-mid_index)
            elf2 = queue.popleft()
            queue.rotate(mid_index)

            # Pop elf1 at the start
            elf1 = queue.popleft()
        # silly call to make pylint happy, and leave code readable
        if elf2:
            pass
        # Put elf1 back at the end
        queue.append(elf1)
    return queue.popleft()



def solve_part2(input_value):
    """
    Function to solve part 2
    part two solution:  thanks to u/aceshades for the idea to split the queue
    the split queue lets us "rotate" the queue by using pop and popleft instead
    of rotate
    """
    # populate left with the first half of the elves
    left = collections.deque(range(1,input_value // 2 + 1))
    # populate right with the second half reversed
    right = collections.deque(range(input_value, input_value // 2, -1))
    # loop until one side is empty
    while left and right:
        # pop from the longer half
        if len(left) > len(right):
            left.pop()
        else:
            right.pop()

        # rotate, moving from the front of the logical queue (front of left)
        # to the end of the logical queue (beginning of right)
        right.appendleft(left.popleft())
        # moving from middle right  of logical queue (end of right) to
        # middle left of logical queue (beginning of left)
        left.append(right.pop())
    # return whichever remains
    return left[0] or right[0]

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2016,19)
    my_input = int(my_aoc.load_text())
    # test input, uncomment to test
    #my_input=5
    # parts structure to loop
    parts = {
        1: 1,
        2: 2
    }
    # answer structure
    answer = {
        1: None,
        2: None
    }
    # functiopn map since we are using seperate functions
    func_map = {
        1: solve,
        2: solve_part2
    }
    # loop parts
    for part in parts:
        # log start time
        start = time.time()
        # collect answer
        answer[part] = func_map[part](my_input)
        # log end time
        end = time.time()
        print(f"Part {part}: {answer[part]}, took {end-start} seconds")
