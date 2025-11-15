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


"""

import time
import logging
import re
from queue import PriorityQueue
import itertools
import sys
from functools import lru_cache
import aoc  # pylint: disable=import-error


class Node:
    """
    Node class for scoring positions
    """

    def __init__(self, floor, floors, g_score, h_score):
        """
        Init node
        """
        self.floor = floor
        self.floors = floors
        self.anonymized = anonymize(floors)
        self.g_score = g_score
        self.h_score = h_score
        self.f_score = g_score + h_score
        self.threshold = float("infinity")

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
        my_string += f"f_score: {self.f_score}, threshold: {self.threshold}\n"
        floor_num = 4
        for floor in reversed(self.floors):
            my_string += f"{floor_num}:" + " ".join(floor) + "\n"
            floor_num -= 1
        my_string += "\n"
        return my_string


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


def parse_notes(input_string):
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


def anonymize_old(floors):
    """
    Function to anonymize items so symmetrical states are equal
    """
    # find the unique elements in the building from the top down
    elements_seen = []
    for floor_num in range(3, -1, -1):
        floor = floors[floor_num]
        for item in list(floor):
            if not item[:-1] in elements_seen:
                elements_seen.append(item[:-1])
    # convert tuples or sets to list so we can work with them
    list_floors = [list(floor) for floor in floors]
    # walk all the items and replace the element with its index
    # ex:  HG -> 0G, LiM -> 1M
    for floor in list_floors:
        # floor_summary = ' '.join(floor)
        for item, label in enumerate(floor):
            for idx, element in enumerate(elements_seen):
                # if floor_summary.count(element) > 1:
                if element in label:
                    # print(f"{floor[item]} replace {element} with {str(idx)}")
                    floor[item] = label.replace(element, str(idx))
    return tuple(tuple(list(floor)) for floor in list_floors)


@lru_cache(maxsize=None)
def is_valid(floor):
    """
    Function to test validity of a floor configuration
    """
    # sets to classify generators and micro_chips
    generators = []
    micro_chips = []
    # walk the items in the floor
    for item in floor:
        # if item end in G add it's element to generators
        if item[-1] == "G":
            generators.append(item[:-1])
        else:  # add to micro_chips instead
            micro_chips.append(item[:-1])
    # if there are any generators, lets look at the microchips
    if len(generators) > 0:
        # walk micro_chips
        for micro_chip in micro_chips:
            # if micro_chip doesn't have a matching generator, it is not safe
            if not micro_chip in generators:
                return False
    return True


@lru_cache(maxsize=None)
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


def next_floors(current):
    """
    Function to return next floors to try
    """
    print(f"current: {current}")
    next_floor_list = []
    for floor in [current["floor"] + 1, current["floor"] - 1]:
        # check that floor exists
        if floor < 0 or floor > 3:
            continue
        # check so that we don't go down below all the other items
        if floor == current["floor"] - 1:
            empty = True
            # in each floor, if its length is not 0, set false
            for lower_floor in range(current["floor"] - 1, -1, -1):
                if len(current["floors"][lower_floor]) > 0:
                    empty = False
                    break
            # if all the floors below are empty move on, don't process
            if empty:
                continue
        next_floor_list.append(floor)
    return next_floor_list


@lru_cache(maxsize=None)
def try_move(current_node, items, new_floor):
    """
    Function to try moves and return new heap entries
    """
    # lets try not going up with an empty slot
    # this cut part 1 time in half :)
    if None in items and new_floor > current_node.floor:
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
    floors_tuple = tuple(tuple(floor) for floor in new_floors)
    # if both floors are still valid
    if is_valid(floors_tuple[current_node.floor]) and is_valid(floors_tuple[new_floor]):
        # add to new_nodes
        # def __init__(self, floor, floors, g_score, h_score):
        new_nodes.append(
            Node(
                new_floor,
                floors_tuple,
                current_node.g_score + 1,
                calc_h_score(
                    floors_tuple, current_node.g_score, current_node.threshold
                ),
            )
        )
    return new_nodes


# preserving failed h_score routines for future review
def h_score_works_slow(floors, stops, threshold):
    """
    Function to calculate hscore
    gives one point for each item for each move it must make to get to 4
    boosts score if stops //2 + score > threshold (min_solved)
    decreases (prioritizes) score if lower floors are empty
    """
    # score = min_stops_remaining(floors)
    score = 0
    for idx, floor in enumerate(floors):
        score += (3 - idx) * len(floor)
    # if it will take more elevator stops to complete than we have left
    # before min_solved, then we aren't on the right track, so lets bump
    # score up to deprioritize this route
    if stops // 2 + score > threshold:
        score += 100
    if len(floors[0]) == 0:
        score -= 10
        if len(floors[1]) == 0:
            score -= 20
    return score


def h_score_simple(floors, stops, threshold):
    """
    Function to calculate hscore
    gives one point for each item for each move it must make to get to 4
    """
    print(stops, threshold)
    score = 0
    for idx, floor in enumerate(floors):
        score += (3 - idx) * len(floor)
    return score


@lru_cache(maxsize=None)
def calc_h_score(floors, stops, threshold):
    """
    Function to calculate hscore
    gives one point for each item for each move it must make to get to 4
    penalizes if we can't reach solution before min_solved
    rewards empty lower floors and 4th floor more loaded than third

    """
    score = min_stops_remaining(floors)
    # if it will take more elevator stops to complete than we have left
    # before min_solved, then we aren't on the right track, so lets bump
    # score up to deprioritize this route
    if stops // 2 + score > threshold:
        score *= 1000
    else:
        score *= 100

    if len(floors[0]) == 0:
        score -= 1000
        if len(floors[1]) == 0:
            score -= 2000
            if len(floors[3]) > len(floors[2]):
                score -= 3000
    return score


@lru_cache(maxsize=None)
def min_stops_remaining(floors):
    """
    Calculate the stops needed to get all elements to the top
    if we could move them at will
    """
    score = 0
    for idx, floor in enumerate(floors):
        score += (3 - idx) * len(floor)
    return score // 2


def h_score_percentage(floors, stops, threshold):
    """
    Function to calculate h_score based on percentage completion
    rewards for lower floors being empty
    """
    print(stops, threshold)
    max_items = sum(len(floor) for floor in floors)
    # max_items * (4-1) since the highest floor gives the maximum multiplier
    max_score = max_items * 3
    score = min_stops_remaining(floors)
    percentage_complete = score / max_score if max_score > 0 else 1
    score = 1 - percentage_complete

    if len(floors[0]) == 0:
        score -= 0.5
        if len(floors[1]) == 0:
            score -= 1
    return score


@lru_cache(maxsize=None)
def init_goal(floors):
    """
    Function to initialize goal
    I ended up not using, this, bur preseving for now
    """
    goal = 0
    # sum items as goal
    for floor in floors:
        goal += len(floor)
    goal = calc_h_score(([], [], [], [range(goal)]), 0, float("infinity"))
    return goal


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
    Function to solve puzzle using A* algorithm
    """
    # multiply by floor 3
    # min_solved = float('infinity')
    # educated guess
    min_solved = 100
    start_node = Node(
        0,
        tuple(tuple(list(floor)) for floor in floors),
        0,
        calc_h_score(tuple(tuple(list(floor)) for floor in floors), 0, min_solved),
    )
    # initialize PriorityQueue
    open_set = PriorityQueue()
    # add start_node to priority_queue (f_score, node)
    open_set.put((start_node.f_score, start_node))
    # initialize closed set
    closed_set = {}

    # process open set
    counter = 0
    while not open_set.empty():
        counter += 1
        # get current node
        current_node = open_set.get()[1]
        # useless check for min_solved that isn't gettign updated
        if current_node.g_score >= min_solved:
            continue
        # is this state in closed_set?
        # update closed set if we re in closed set, but fewer steps we'll process
        # otherwise continue
        if current_node.g_score > closed_set.get(
            current_node.anonymized, float("infinity")
        ):
            continue
        closed_set[current_node.anonymized] = current_node.g_score
        # check for solution first
        if is_solved(current_node.floor, current_node.floors):
            return current_node.g_score
            # if current_node.g_score < min_solved:
            #    print(f"Took {counter} tries {current_node.g_score}")
            #    print(f"Found win in {current_node.g_score} stops: {current_node.floors}")
            #    print(current_node)
            #    min_solved = current_node.g_score
            #    # just returning first solution to save time
            #    # this is optimized for this input, we would just need to continue if
            #    # we were solving for general solutions
            #    return min_solved
            # continue
        # is it possible to beat current score?
        if min_stops_remaining(current_node.floors) + current_node.g_score > min_solved:
            continue
        # update threshold so children calculate h_score accordingly
        current_node.threshold = min_solved
        for new_node in a_star_next_nodes(current_node):
            # skip if already seen, unless it is a lower step count.
            if new_node.g_score < closed_set.get(
                new_node.anonymized, float("infinity")
            ):
                open_set.put((new_node.f_score, new_node))
    return None


if __name__ == "__main__":
    # sample data
    test_data = [
        "The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.",  # pylint: disable=line-too-long
        "The second floor contains a hydrogen generator.",
        "The third floor contains a lithium generator.",
        "The fourth floor contains nothing relevant.",
    ]
    logging.basicConfig(level=logging.WARNING)
    my_aoc = aoc.AdventOfCode(2016, 11)
    lines = my_aoc.load_lines()
    building = [[], [], [], []]
    # print(sys.argv,len(sys.argv))
    if len(sys.argv) > 1:
        lines = test_data
    for note in lines:
        parse_notes(note)

    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers for validation
    correct = {1: 47, 2: 71}
    # dict to map functions
    funcs = {1: solve_a_star, 2: solve_a_star}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        if my_part == 2:
            for item_element in "ED":
                for item_type in "MG":
                    building[0].append(f"{item_element}{item_type}")
        # get answer
        answer[my_part] = funcs[my_part](building)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
