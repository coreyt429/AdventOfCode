"""
Advent Of Code 2020 day 23

Part 1 was fairly easy.  Part 2 I had two cycle through a few different approaches.

Initially I was working with deque to make rotating the circle easy.  Worked well for Part 1,
was too slow for even short runs on the part 2 cups.

Next I converted that code to use numpy.array().  This was 10 times faster, and still would
have taken a really long time.

The Next iteration was linked lists using list().  This was significantly faster, and would
have worked in walk away and come back later time (20-30 minutes maybe).

So I converted the lists to numpy.array(), which again significantly sped up the operation.
I don't like 5-10 minute solutions, though. So I profiled it to see where the bottlenecks were.
replaced the pickedup set with a numpy.array() of booleans.  This was got it closer, but
initializing it on each pass was still taking time.  So I moved it to the outside of the loop
and added = False statements at the end of the loop to reset the flags after they were used.

I'm at a consistent < 40 seconds now, and I'm happy with that for this one.

"""

# import system modules
import logging
import argparse
import numpy as np

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def move_cups_numpy(cups, current_cup):
    """Functions to move cups 1 turn"""
    # The crab picks up the three cups that are immediately clockwise of the current cup.
    # They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.
    idx = np.where(cups == current_cup)[0][0] + 1
    cups = np.roll(cups, -1 * idx)
    pickup = cups[:3]
    cups = cups[3:]
    cups = np.roll(cups, idx)
    # destination: 2""")
    # The crab selects a destination cup: the cup with a label equal to the current cup's label
    # minus one.
    # If this would select one of the cups that was just picked up, the crab will keep subtracting
    # one until it finds a cup that wasn't just picked up.
    destination = current_cup - 1
    while destination in pickup:
        destination -= 1
    # If at any point in this process the value goes below the lowest value on any cup's label,
    # it wraps around to the highest value on any cup's label instead.
    if destination not in cups:
        destination = max(cups)
    # The crab places the cups it just picked up so that they are immediately clockwise of the
    # destination cup.
    # They keep the same order as when they were picked up.
    idx = np.where(cups == destination)[0][0] + 1
    cups = np.roll(cups, -1 * idx)
    cups = np.concatenate((cups, pickup))
    cups = np.roll(cups, idx + 3)
    # The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
    idx = np.where(cups == current_cup)[0][0] + 1
    current_cup = cups[(idx) % len(cups)]
    return current_cup, cups


def move_cups_linked_list(cups, moves):
    """Functions to move cups 1 turn"""
    max_cup = max(cups)
    linked_list = np.zeros(max_cup + 1, dtype=np.int32)
    for idx in range(len(cups) - 1):
        linked_list[cups[idx]] = cups[idx + 1]
    linked_list[cups[-1]] = cups[0]  # Circular link
    current_cup = cups[0]
    # last_time = time.time()
    pickup_flags = np.zeros(max_cup + 1, dtype=bool)
    for _ in range(moves):
        # The crab picks up the three cups that are immediately clockwise of the current cup.
        # They are removed from the circle; cup spacing is adjusted as necessary to maintain
        # the circle.
        pickup1 = linked_list[current_cup]
        pickup2 = linked_list[pickup1]
        pickup3 = linked_list[pickup2]
        pickup_flags[[pickup1, pickup2, pickup3]] = True
        # Close the gap
        linked_list[current_cup] = linked_list[pickup3]
        # The crab selects a destination cup: the cup with a label equal to the current cup's
        # label minus one.
        # If this would select one of the cups that was just picked up, the crab will keep
        # subtracting one until it finds a cup that wasn't just picked up.
        destination = current_cup - 1
        while pickup_flags[destination] or destination < 1:
            destination -= 1
            # If at any point in this process the value goes below the lowest value on any
            # cup's label, it wraps around to the highest value on any cup's label instead.
            if destination < 1:
                destination = max_cup
        # The crab places the cups it just picked up so that they are immediately clockwise
        # of the destination cup.
        # They keep the same order as when they were picked up.
        linked_list[pickup3] = linked_list[destination]
        linked_list[destination] = pickup1
        # The crab selects a new current cup: the cup which is immediately clockwise of the
        # current cup.
        current_cup = linked_list[current_cup]
        # reset pickup flags
        pickup_flags[[pickup1, pickup2, pickup3]] = False
    return linked_list


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # my_cups = [int(num) for num in input_value[0]]
    my_cups = np.array([int(num) for num in input_value[0]])
    moves = 100

    if part == 2:
        # Due to what you can only assume is a mistranslation (you're not exactly fluent in Crab),
        # you are quite surprised when the crab starts arranging many cups in a circle on your raft
        # - one million (1000000) in total.
        # Your labeling is still correct for the first few cups; after that, the remaining cups are
        # just numbered in an increasing fashion starting from the number after the highest number
        # in your list and proceeding one by one until one million is reached.
        # my_cups = my_cups + list(range(max(my_cups) + 1, 1000000 + 1))
        my_cups = np.concatenate((my_cups, np.arange(max(my_cups) + 1, 1000001)))
        # After discovering where you made the mistake in translating Crab Numbers, you realize the
        # small crab isn't going to do merely 100 moves; the crab is going to do
        # ten million (10000000) moves!
        moves = 10000000
        # moves = 1000000
    linked_list = move_cups_linked_list(my_cups, moves)
    cup = 1
    if part == 1:
        # What are the labels on the cups after cup 1
        cup_string = ""
        for _ in range(len(my_cups)):
            cup_string += f"{cup}"
            cup = linked_list[cup]
        return int(cup_string.replace("1", ""))

    nums = []
    # Determine which two cups will end up immediately clockwise of cup 1.
    for _ in (1, 2):
        cup = linked_list[cup]
        nums.append(cup)
    # What do you get if you multiply their labels together?
    return np.prod(nums, dtype=object)


YEAR = 2020
DAY = 23
input_format = {
    1: "lines",
    2: "lines",
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
