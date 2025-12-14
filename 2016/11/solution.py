"""
Advent of code 2016 day 11

I might have over designed this one, and it took me a while as a result.
It just felt like a good object oriented excercise. - see jupyter notebook for what
I'm talking about.  Below is rewrite that actually finished in a not so reasonable time.

The solution below scraps my over designed object oriented attempt.  The first worked well,
just slowly.

This attempt uses a simpler data structure:
    # Heap description:
    #   - stop_count int initialized to 0
    #   - current_floor int initialized to 0 (first floor)
    #   - tuple of tuples to represent the floors and items on them
    # Initial structure (for test data):
    #   stops = 0, current_floor = 0, floors_as_tuples = (('HM', 'LiM'), ('HG',), ('LiG',), ())
    heappush(heap,(0,0,tuple(tuple(floor) for floor in floors)))

8/2/2024 revisit.  I broke the old solution out as solve_bfs, and started solve_a_star.  So
far solve_a_star is not faster, and inconsistent in results. possibly need a different h_score
current h_score is the product of the floor index and the count of items on the floor

The current heuristics work, but there is some randomness.  sometimes it answers really quickly,
and sometimes it takes a while.  sometimes it gets the right answer first, sometimes it doesnt.

This version is accurate, but slow on part 2

Randomness has been worked out.  The sets I was using for the floors were causing it.

In this version I changed the sets to lists, and removed all sorting, so original order is
preserved. New items on a floor are appended to the floor.  0.75 sec for part 1, 220 seconds
for part 2.

Next, lets try prepending instead of appending when we move to a floor.
okay, that caused wrong answers to be found first. reverting.

I'm happy with this for now.  It passes pylint, and runs consistently every time.  I wish part 2
was faster, maybe I'll revisit another day:

12/3/2024 revisit.  Profiled the run, and see that memoizing is_valid and anonymize might help.
  part 1: 0.53 seconds
  part 2: 261 seconds

11/27/25 revisit.  converted to heapq, removed lru_cache from functions that don't get cache hits.
  Part 1: 47, took 0.23032712936401367 seconds
  Part 2: 71, took 77.16478490829468 seconds

11/27/25 revisit.  cleaned up a lot, added checks before spawning nodes:
  Part 1: 47, took 0.23984408378601074 seconds
  Part 2: 71, took 13.964895963668823 seconds
"""

import logging
import argparse
import re
from heapq import heappop, heappush
import itertools
from functools import lru_cache
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


class Node:
    """
    Node class for scoring positions
    """

    def __init__(self, floor, floors, g_score):
        """
        Init node
        """
        self.floor = floor
        self.floors = floors
        self.counts = floor_counts(floors)
        self.g_score = g_score
        self.h_score = calc_h_score(self.counts)

    @property
    def f_score(self):
        """
        Return f_score
        """
        return self.g_score + self.h_score

    @property
    def state_key(self):
        """
        Symmetry-aware state key: elevator floor + anonymized floors.
        States that differ only by renaming elements collapse to the same key.
        """
        return (self.floor, anonymize(self.floors))

    def __gt__(self, other):
        """
        Node greater than
        """
        if self.f_score == other.f_score:
            return self.h_score > other.h_score
        return self.f_score > other.f_score

    def __lt__(self, other):
        """
        Node less than
        """
        if self.f_score == other.f_score:
            return self.h_score < other.h_score
        return self.f_score < other.f_score

    def __str__(self):
        my_string = f"g_score: {self.g_score}, h_score: {self.h_score}, "
        my_string += f"f_score: {self.f_score}\n"
        floor_num = 4
        for floor in reversed(self.floors):
            my_string += f"{floor_num}:" + " ".join(floor) + "\n"
            floor_num -= 1
        my_string += "\n"
        return my_string


@lru_cache(maxsize=None)
def floor_counts(floors):
    """
    Return counts of items on each floor
    """
    return tuple(len(floor) for floor in floors)


@lru_cache(maxsize=None)
def calc_h_score(counts):
    """
    Heuristic score function: min_stops_remaining(counts) with
    bonuses for empty lower floors.
    """
    score = min_stops_remaining(counts)
    # reward for empty lower floors
    # if counts[0] == 0:
    #     score -= 2
    #     if counts[1] == 0:
    #         score -= 1
    return max(score, 0)


@lru_cache(maxsize=None)
def min_stops_remaining(counts):
    """
    counts: tuple of ints (number of items on each floor)
    """
    score = 0
    for idx, n in enumerate(counts):
        score += (3 - idx) * n
    return score // 2


# overkill for the puzzle, but chatGPT was more than happy to generate this,
# and it was faster than me looking up a few elements I didn't know
elements = {
    "hydrogen": "H",
    "helium": "He",
    "lithium": "Li",
    "beryllium": "Be",
    "boron": "B",
    "carbon": "C",
    "nitrogen": "N",
    "oxygen": "O",
    "fluorine": "F",
    "neon": "Ne",
    "sodium": "Na",
    "magnesium": "Mg",
    "aluminum": "Al",
    "silicon": "Si",
    "phosphorus": "P",
    "sulfur": "S",
    "chlorine": "Cl",
    "argon": "Ar",
    "potassium": "K",
    "calcium": "Ca",
    "scandium": "Sc",
    "titanium": "Ti",
    "vanadium": "V",
    "chromium": "Cr",
    "manganese": "Mn",
    "iron": "Fe",
    "cobalt": "Co",
    "nickel": "Ni",
    "copper": "Cu",
    "zinc": "Zn",
    "gallium": "Ga",
    "germanium": "Ge",
    "arsenic": "As",
    "selenium": "Se",
    "bromine": "Br",
    "krypton": "Kr",
    "rubidium": "Rb",
    "strontium": "Sr",
    "yttrium": "Y",
    "zirconium": "Zr",
    "niobium": "Nb",
    "molybdenum": "Mo",
    "technetium": "Tc",
    "ruthenium": "Ru",
    "rhodium": "Rh",
    "palladium": "Pd",
    "silver": "Ag",
    "cadmium": "Cd",
    "indium": "In",
    "tin": "Sn",
    "antimony": "Sb",
    "tellurium": "Te",
    "iodine": "I",
    "xenon": "Xe",
    "cesium": "Cs",
    "barium": "Ba",
    "lanthanum": "La",
    "cerium": "Ce",
    "praseodymium": "Pr",
    "neodymium": "Nd",
    "promethium": "Pm",
    "samarium": "Sm",
    "europium": "Eu",
    "gadolinium": "Gd",
    "terbium": "Tb",
    "dysprosium": "Dy",
    "holmium": "Ho",
    "erbium": "Er",
    "thulium": "Tm",
    "ytterbium": "Yb",
    "lutetium": "Lu",
    "hafnium": "Hf",
    "tantalum": "Ta",
    "tungsten": "W",
    "rhenium": "Re",
    "osmium": "Os",
    "iridium": "Ir",
    "platinum": "Pt",
    "gold": "Au",
    "mercury": "Hg",
    "thallium": "Tl",
    "lead": "Pb",
    "bismuth": "Bi",
    "polonium": "Po",
    "astatine": "At",
    "radon": "Rn",
    "francium": "Fr",
    "radium": "Ra",
    "actinium": "Ac",
    "thorium": "Th",
    "protactinium": "Pa",
    "uranium": "U",
    "neptunium": "Np",
    "plutonium": "Pu",
    "americium": "Am",
    "curium": "Cm",
    "berkelium": "Bk",
    "californium": "Cf",
    "einsteinium": "Es",
    "fermium": "Fm",
    "mendelevium": "Md",
    "nobelium": "No",
    "lawrencium": "Lr",
    "rutherfordium": "Rf",
    "dubnium": "Db",
    "seaborgium": "Sg",
    "bohrium": "Bh",
    "hassium": "Hs",
    "meitnerium": "Mt",
    "darmstadtium": "Ds",
    "roentgenium": "Rg",
    "copernicium": "Cn",
    "nihonium": "Nh",
    "flerovium": "Fl",
    "moscovium": "Mc",
    "livermorium": "Lv",
    "tennessine": "Ts",
    "oganesson": "Og",
}


# regexes we will use for parsing notes
pattern_floor = re.compile(r"The (\w+) floor contains (.*)")
pattern_split = re.compile(r", and | and |, ")
pattern_microchip = re.compile(r"a (\w+)-compatible microchip.*")
pattern_generator = re.compile(r"a (\w+) generator.*")


def parse_input(input_text):
    """
    Parse the full puzzle input into a list of floors.
    """
    building = [[], [], [], []]
    for note in input_text.strip().splitlines():
        if not note:
            continue
        parse_notes(building, note)
    return building


def parse_notes(building, input_string):
    """
    Function to parse notes
    """
    floors = {"first": 0, "second": 1, "third": 2, "fourth": 3}
    match = pattern_floor.match(input_string)
    floor = floors[match.group(1)]
    items = pattern_split.split(match.group(2))
    for item in items:
        match = pattern_microchip.match(item)
        if match:
            building[floor].append(f"{elements[match.group(1)]}M")
        else:
            match = pattern_generator.match(item)
            if match:
                building[floor].append(f"{elements[match.group(1)]}G")
            else:
                pass


def normalize_floors(floors):
    """
    Return a canonical floors representation: tuple of sorted tuples.
    """
    return tuple(tuple(sorted(floor)) for floor in floors)


@lru_cache(maxsize=None)
def anonymize(floors):
    """
    Function to anonymize items so symmetrical states are equal.
    """
    # Find the unique elements in the building from the top down
    elements_seen = {}
    next_index = 0

    for floor_num in range(3, -1, -1):
        for item in floors[floor_num]:
            element = item[:-1]
            if element not in elements_seen:
                elements_seen[element] = str(next_index)
                next_index += 1

    # Create a new list for modified floors
    anonymized_floors = []

    for floor in floors:
        anonymized_floor = []
        for item in floor:
            element = item[:-1]
            if element in elements_seen:
                anonymized_floor.append(item.replace(element, elements_seen[element]))
        anonymized_floors.append(anonymized_floor)
    # Convert back to tuples before returning
    return tuple(tuple(floor) for floor in anonymized_floors)


@lru_cache(maxsize=None)
def is_valid(floor):
    """
    A floor is invalid iff:
      - there is at least one generator, AND
      - there exists a microchip whose matching generator is not present.
    """
    # 0 or 1 item: always safe
    if len(floor) <= 1:
        return True

    gens = set()
    chips = set()

    for item in floor:
        element = item[:-1]
        if item[-1] == "G":
            gens.add(element)
        else:  # microchip
            chips.add(element)

    # No generators or no chips → nothing can fry
    if not gens or not chips:
        return True

    # If there's any chip whose generator isn't present, it's unsafe.
    # chips - gens is exactly that set.
    return not chips - gens


# @lru_cache(maxsize=None)
def is_solved(current_floor, floors):
    """
    Function to test for solved puzzles
    """
    # If we aren't on the top floor, it is not solved
    if current_floor != 3:
        return False
    # walk lower floors
    for floor in range(current_floor - 1, -1, -1):
        # if lower floor is not empty, it is not solved
        if len(floors[floor]) > 0:
            return False
    # nothing ruled out, must be solved
    return True


def next_floors_a_star(current_node):
    """
    Function to return next floors to try
    """
    next_floor_list = []
    for floor in [current_node.floor + 1, current_node.floor - 1]:
        # check that floor exists
        if floor < 0 or floor > 3:
            continue
        # check so that we don't go down below all the other items
        if floor == current_node.floor - 1:
            empty = True
            # in each floor, if its length is not 0, set false
            for lower_floor in range(current_node.floor - 1, -1, -1):
                if len(current_node.floors[lower_floor]) > 0:
                    empty = False
                    break
            # if all the floors below are empty move on, don't process
            if empty:
                continue
        next_floor_list.append(floor)
    return next_floor_list


# @lru_cache(maxsize=None)
def try_move(current_node, items, new_floor):
    """
    Function to try moves and return new heap entries
    """
    # lets try not going up with an empty slot
    if None in items and new_floor > current_node.floor:
        return []
    # lets try not going down with both slots full
    if None not in items:
        if new_floor < current_node.floor:
            return []

        if "G" in items[0] and "M" in items[1]:
            if items[0][:-1] == items[1][:-1]:
                return []
        if "G" in items[1] and "M" in items[0]:
            if items[0][:-1] == items[1][:-1]:
                return []
    new_nodes = []
    # clone current['floors']
    new_floors = []
    for floor in current_node.floors:
        new_floors.append(list(floor))
    # move items from current['floor'] to new['floor']
    filtered_items = [item for item in items if item is not None]

    for item in filtered_items:
        new_floors[current_node.floor].remove(item)
        new_floors[new_floor].append(item)
    # floors_tuple = tuple(tuple(floor) for floor in new_floors)
    # print(f"floors_tuple a: {floors_tuple}")
    floors_tuple = normalize_floors(new_floors)
    # print(f"floors_tuple b: {floors_tuple}")

    # if both floors are still valid
    if is_valid(floors_tuple[current_node.floor]) and is_valid(floors_tuple[new_floor]):
        # add to new_nodes
        # def __init__(self, floor, floors, g_score, h_score):
        new_nodes.append(
            Node(
                new_floor,
                floors_tuple,
                current_node.g_score + 1,
            )
        )
    return new_nodes


def a_star_next_nodes(current_node):
    """
    Function to get next nodes to potentially
    add to open_set
    """
    # for valid floors in current_floor +/- 1
    new_nodes = []
    new = {}
    for new["floor"] in next_floors_a_star(current_node):
        # find each possible pairing, including empty (None)
        for items in itertools.combinations(
            list(current_node.floors[current_node.floor]) + [None], 2
        ):
            # ignore matches
            if items[0] == items[1]:
                continue

            for new_node in try_move(current_node, items, new["floor"]):
                new_nodes.append(new_node)
    return new_nodes


def solve_a_star(floors):
    """
    A* search using an admissible heuristic (min_stops_remaining(counts))
    and a conservative closed_set keyed on the exact state (floor, floors).

    This version avoids anonymization in the closed_set to rule out
    over-aggressive state merging as the cause of returning None.
    """
    min_solve = 100
    # Build a canonical start state
    start_floors = normalize_floors(tuple(tuple(list(floor)) for floor in floors))
    start_node = Node(0, start_floors, 0)

    open_set = []
    heappush(open_set, (start_node.f_score, start_node))

    # closed_set maps (floor, floors) -> best g_score seen for that exact state
    closed_set = {}

    while open_set:
        _, current_node = heappop(open_set)
        # logger.debug("Current node: %s", current_node)
        # logger.debug("Open set size: %d", len(open_set))
        key = current_node.state_key
        best_g = closed_set.get(key, float("inf"))
        if current_node.g_score > best_g or current_node.g_score >= min_solve:
            # We've already seen this exact state with a better path
            continue

        # Record / update best g for this state
        closed_set[key] = current_node.g_score

        # Goal check
        if is_solved(current_node.floor, current_node.floors):
            min_solve = min(min_solve, current_node.g_score)
            continue

        if current_node.g_score >= min_solve:
            continue

        # Expand neighbors
        for new_node in a_star_next_nodes(current_node):
            new_key = new_node.state_key
            if new_node.g_score < closed_set.get(new_key, float("inf")):
                heappush(open_set, (new_node.f_score, new_node))

    # If we exhaust the open_set without finding a goal, there's genuinely no solution
    return min_solve


def solve(building, part):
    """
    Wrapper that prepares floors and runs the A* search.
    """
    floors = [list(floor) for floor in building]
    if part == 2:
        for item_element in "ED":
            for item_type in "MG":
                floors[0].append(f"{item_element}{item_type}")
    return solve_a_star(floors)


YEAR = 2016
DAY = 11
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
