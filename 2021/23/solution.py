"""
Advent Of Code 2021 day 23

Shortest path problem. My biggest struggles were tripping on missed rules, and
not checking my if conditions correctly.

"""

# import system modules
import logging
import argparse
import itertools
from heapq import heappop, heappush
from functools import lru_cache

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

cost = {"A": 1, "B": 10, "C": 100, "D": 1000}

destination = {"A": 0, "B": 1, "C": 2, "D": 3}


def unfold_rooms(rooms):
    """Function to unfold rooms in part 2"""
    # Between the first and second lines of text that contain amphipod starting positions,
    # insert the following lines:
    # #D#C#B#A#
    # #D#B#A#C#
    # rooms = ((rooms[0][0], 'D', 'D', rooms[0][1]), etc)
    additions = (("D", "D"), ("C", "B"), ("B", "A"), ("A", "C"))
    new_rooms = []
    for idx, room in enumerate(rooms):
        new_rooms.append((room[0], additions[idx][0], additions[idx][1], room[1]))
    return tuple(new_rooms)


@lru_cache(maxsize=None)
def get_room_clear(occupant, max_slot=1):
    """Function to generate room clear tuple"""
    # Generate combinations with replacement
    combinations = itertools.combinations_with_replacement(
        (occupant, "."), max_slot + 1
    )
    # Generate all unique permutations for each combination
    all_permutations = set(itertools.permutations(comb) for comb in combinations)
    # Flatten the results from the permutations sets
    flattened_permutations = set(itertools.chain.from_iterable(all_permutations))
    # Return sorted, unique results as a tuple
    return tuple(sorted(flattened_permutations))


def is_blocked(idx, entry, hallway):
    """Function to check for impediments between idx and entry"""
    start, end = min(idx, entry), max(idx, entry)
    for step in range(start, end + 1):
        if step == idx:
            continue
        if hallway[step] != ".":
            return True
    return False


def process_hallway(heap, energy_spent, hallway, rooms, max_slot):
    """Function to process hallway positions to add movements to the heap"""
    # hallway next_steps
    for idx, occupant in enumerate(hallway):
        # skip empty
        if occupant == ".":
            continue
        # Once an amphipod stops moving in the hallway, it will stay in that spot until it
        # can move into a room. (That is, once any amphipod starts moving, any other amphipods
        # currently in the hallway are locked in place and will not move again until they can
        # move fully into a room.)
        # for now, just not moving in the hallway if room is not open
        # I think this is going to be too simplistic, and we need to track each Amphipod to
        # allow it to continue to move in the hallway until it doesn't. which we could easily
        # simulate by just queue all the possible destinations when it moves from a room to
        # the hallway.  I think this is going to be the case otherwise, you would never reach
        # either end of the hallway, so why do they exist?
        room_id = destination[occupant]
        entry = (room_id + 1) * 2
        if rooms[room_id] not in get_room_clear(occupant, max_slot):
            continue

        if idx != entry:
            if is_blocked(idx, entry, hallway):
                # print(f"Path from {idx} to {entry} is blocked")
                continue

        slot = max_slot
        while rooms[room_id][slot] != ".":
            slot -= 1
        # print(f"slot: {slot}")
        tmp_hallway = list(hallway)
        tmp_hallway[idx] = "."
        tmp_rooms = [list(room) for room in rooms]
        tmp_rooms[room_id][slot] = occupant
        heappush(
            heap,
            (
                energy_spent + (cost[occupant] * (abs(idx - entry) + slot + 1)),
                tuple(tmp_hallway),
                tuple(tuple(room) for room in tmp_rooms),
            ),
        )


def process_rooms(heap, energy_spent, hallway, rooms, max_slot):
    """Function to process rooms for next moves"""
    # room next steps
    for room_id, room in enumerate(rooms):
        slot = 0
        while slot < max_slot + 1 and room[slot] == ".":
            slot += 1
        if slot > max_slot:
            continue
        occupant = rooms[room_id][slot]
        # let's not leave our target room
        if room_id == destination[occupant] and room in get_room_clear(occupant):
            continue
        entry = (room_id + 1) * 2
        # walk down the hallway until you run into another aphipod
        valid = (0, 1, 3, 5, 7, 9, 10)
        targets = set()
        for idx in range(entry, -1, -1):
            if idx in valid:
                if hallway[idx] != ".":
                    break
                targets.add(idx)
        for idx in range(entry, 11):
            if idx in valid:
                if hallway[idx] != ".":
                    break
                targets.add(idx)
        for idx in targets:
            tmp_hallway = list(hallway)
            tmp_hallway[idx] = occupant
            tmp_rooms = [list(room) for room in rooms]
            tmp_rooms[room_id][slot] = "."
            heappush(
                heap,
                (
                    energy_spent + (cost[occupant] * ((slot + 1) + abs(entry - idx))),
                    tuple(tmp_hallway),
                    tuple(tuple(room) for room in tmp_rooms),
                ),
            )


def find_min_energy(hallway, rooms, part=1):
    """Function to find the minimum energy needed to rehome the amphipods"""
    max_slot = 1
    if part == 2:
        # unfold rooms:
        rooms = unfold_rooms(rooms)
        # update slot references to go from 0 - 3
        max_slot = 3
    solution_state = tuple((char,) * (max_slot + 1) for char in "ABCD")
    heap = []
    heappush(heap, (0, hallway, rooms))
    visited = {}
    min_energy_spent = float("infinity")
    while heap:
        energy_spent, hallway, rooms = heappop(heap)
        # I don't think we will want to see the same state twice
        # okay, we might if we get there at a lower cost
        if (hallway, rooms) in visited and energy_spent >= visited[(hallway, rooms)]:
            continue
        visited[(hallway, rooms)] = energy_spent

        # solve condition
        if rooms == solution_state:
            min_energy_spent = min(energy_spent, min_energy_spent)
            continue

        # using more energy than previous solution
        if energy_spent > min_energy_spent:
            continue

        # next state logic
        process_hallway(heap, energy_spent, hallway, rooms, max_slot)
        process_rooms(heap, energy_spent, hallway, rooms, max_slot)
    return min_energy_spent


def parse_input(lines):
    """Function to parse input"""
    hallway = tuple(["."] * 11)
    rooms = (
        (lines[2][3], lines[3][3]),
        (lines[2][5], lines[3][5]),
        (lines[2][7], lines[3][7]),
        (lines[2][9], lines[3][9]),
    )
    return hallway, rooms


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # if part == 2:
    #     return part
    hallway, rooms = parse_input(input_value)
    return find_min_energy(hallway, rooms, part)


YEAR = 2021
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
