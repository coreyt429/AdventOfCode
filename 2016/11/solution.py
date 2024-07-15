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
"""
import time
import logging
import re
import copy
from heapq import heappop, heappush
import itertools
import sys

import aoc #pylint: disable=import-error

# overkill for the puzzle, but chatGPT was more than happy to generate this,
# and it was faster than me looking up a few elements I didn't know
elements = {
    'hydrogen': 'H',
    'helium': 'He',
    'lithium': 'Li',
    'beryllium': 'Be',
    'boron': 'B',
    'carbon': 'C',
    'nitrogen': 'N',
    'oxygen': 'O',
    'fluorine': 'F',
    'neon': 'Ne',
    'sodium': 'Na',
    'magnesium': 'Mg',
    'aluminum': 'Al',
    'silicon': 'Si',
    'phosphorus': 'P',
    'sulfur': 'S',
    'chlorine': 'Cl',
    'argon': 'Ar',
    'potassium': 'K',
    'calcium': 'Ca',
    'scandium': 'Sc',
    'titanium': 'Ti',
    'vanadium': 'V',
    'chromium': 'Cr',
    'manganese': 'Mn',
    'iron': 'Fe',
    'cobalt': 'Co',
    'nickel': 'Ni',
    'copper': 'Cu',
    'zinc': 'Zn',
    'gallium': 'Ga',
    'germanium': 'Ge',
    'arsenic': 'As',
    'selenium': 'Se',
    'bromine': 'Br',
    'krypton': 'Kr',
    'rubidium': 'Rb',
    'strontium': 'Sr',
    'yttrium': 'Y',
    'zirconium': 'Zr',
    'niobium': 'Nb',
    'molybdenum': 'Mo',
    'technetium': 'Tc',
    'ruthenium': 'Ru',
    'rhodium': 'Rh',
    'palladium': 'Pd',
    'silver': 'Ag',
    'cadmium': 'Cd',
    'indium': 'In',
    'tin': 'Sn',
    'antimony': 'Sb',
    'tellurium': 'Te',
    'iodine': 'I',
    'xenon': 'Xe',
    'cesium': 'Cs',
    'barium': 'Ba',
    'lanthanum': 'La',
    'cerium': 'Ce',
    'praseodymium': 'Pr',
    'neodymium': 'Nd',
    'promethium': 'Pm',
    'samarium': 'Sm',
    'europium': 'Eu',
    'gadolinium': 'Gd',
    'terbium': 'Tb',
    'dysprosium': 'Dy',
    'holmium': 'Ho',
    'erbium': 'Er',
    'thulium': 'Tm',
    'ytterbium': 'Yb',
    'lutetium': 'Lu',
    'hafnium': 'Hf',
    'tantalum': 'Ta',
    'tungsten': 'W',
    'rhenium': 'Re',
    'osmium': 'Os',
    'iridium': 'Ir',
    'platinum': 'Pt',
    'gold': 'Au',
    'mercury': 'Hg',
    'thallium': 'Tl',
    'lead': 'Pb',
    'bismuth': 'Bi',
    'polonium': 'Po',
    'astatine': 'At',
    'radon': 'Rn',
    'francium': 'Fr',
    'radium': 'Ra',
    'actinium': 'Ac',
    'thorium': 'Th',
    'protactinium': 'Pa',
    'uranium': 'U',
    'neptunium': 'Np',
    'plutonium': 'Pu',
    'americium': 'Am',
    'curium': 'Cm',
    'berkelium': 'Bk',
    'californium': 'Cf',
    'einsteinium': 'Es',
    'fermium': 'Fm',
    'mendelevium': 'Md',
    'nobelium': 'No',
    'lawrencium': 'Lr',
    'rutherfordium': 'Rf',
    'dubnium': 'Db',
    'seaborgium': 'Sg',
    'bohrium': 'Bh',
    'hassium': 'Hs',
    'meitnerium': 'Mt',
    'darmstadtium': 'Ds',
    'roentgenium': 'Rg',
    'copernicium': 'Cn',
    'nihonium': 'Nh',
    'flerovium': 'Fl',
    'moscovium': 'Mc',
    'livermorium': 'Lv',
    'tennessine': 'Ts',
    'oganesson': 'Og'
}


# regexes we will use for parsing notes
pattern_floor = re.compile(r'The (\w+) floor contains (.*)')
pattern_split = re.compile(r', and | and |, ')
pattern_microchip = re.compile(r'a (\w+)-compatible microchip.*')
pattern_generator = re.compile(r'a (\w+) generator.*')

def parse_notes(input_string):
    """
    Function to parse notes
    """
    floors = {
        'first': 0,
        'second': 1,
        'third': 2,
        'fourth': 3
    }
    match = pattern_floor.match(input_string)
    floor = floors[match.group(1)]
    items = pattern_split.split(match.group(2))
    for item in items:
        match = pattern_microchip.match(item)
        if match:
            building[floor].add(f"{elements[match.group(1)]}M")
        else:
            match = pattern_generator.match(item)
            if match:
                building[floor].add(f"{elements[match.group(1)]}G")
            else:
                pass
def anonymize(floors):
    """
    Function to anonymize items so symmetrical states are equal
    """
    # find the unique elements in the building from the top down
    elements_seen = []
    for floor_num in range(3,-1,-1):
        floor = floors[floor_num]
        for item in floor:
            if not item[:-1] in elements_seen:
                elements_seen.append(item[:-1])
    # convert tuples or sets to list so we can work with them
    if isinstance(floors, list) and isinstance(floors[0], list):
        list_floors = floors
    else:
        list_floors = [list(floor) for floor in floors]
    # walk all the items and replace the element with its index
    # ex:  HG -> 0G, LiM -> 1M
    for floor in list_floors:
        for item, label in enumerate(floor):
            for idx, element in enumerate(elements_seen):
                floor[item] = label.replace(element,str(idx))
    return tuple(tuple(floor) for floor in list_floors)

def is_valid(floor):
    """
    Function to test validity of a floor configuration
    """
    # sets to classify generators and micro_chips
    generators = set()
    micro_chips = set()
    # walk the items in the floor
    for item in floor:
        # if item end in G add it's element to generators
        if item[-1] == 'G':
            generators.add(item[:-1])
        else: # add to micro_chips instead
            micro_chips.add(item[:-1])
    # if there are any generators, lets look at the microchips
    if len(generators) > 0:
        # walk micro_chips
        for micro_chip in micro_chips:
            # if micro_chip doesn't have a matching generator, it is not safe
            if not micro_chip in generators:
                return False
    return True

def is_solved(current):
    """
    Function to test for solved puzzles
    """
    # If we aren't on the top floor, it is not solved
    if current['floor'] != 3:
        return False
    # walk lower floors
    for floor in range(current['floor']-1,-1,-1):
        # if lower floor is not empty, it is not solved
        if len(current['floors'][floor]) > 0:
            return False
    # nothing ruled out, must be solved
    return True

def next_floors(current):
    """
    Function to return next floors to try
    """
    next_floor_list = []
    for floor in [current['floor']+1, current['floor']-1]:
        # check that floor exists
        if floor < 0 or floor > 3:
            continue
        # check so that we don't go down below all the other items
        if floor == current['floor']-1:
            empty = True
            # in each floor, if its length is not 0, set false
            for lower_floor in range(current['floor']-1,-1,-1):
                if len(current['floors'][lower_floor]) > 0:
                    empty = False
                    break
            # if all the floors below are empty move on, don't process
            if empty:
                continue
        next_floor_list.append(floor)
    return next_floor_list

def try_move(stops, items, current, new):
    """
    Function to try moves and return new heap entries
    """
    new_heap=[]
    # clone current['floors']
    new['floors'] = copy.deepcopy(current['floors'])
    # move items from current['floor'] to new['floor']
    for item in items:
        # ignore if None
        if item:
            new['floors'][current['floor']].remove(item)
            new['floors'][new['floor']].add(item)
    # if both floors are still valid
    if (is_valid(new['floors'][current['floor']]) and
        is_valid(new['floors'][new['floor']])):
        # add to heap
        new_heap.append((
            stops + 1,
            new['floor'],
            tuple(tuple(floor) for floor in new['floors'])
            )
        )
    return new_heap

def solve(floors):
    """
    Function to solve part1
    """
    #Initialize heap and add start floor
    heap = []
    # Add first item to heap
    # Heap description:
    #   - stop_count int initialized to 0
    #   - current_floor int initialized to 0 (first floor)
    #   - tuple of tuples to represent the floors and items on them
    heappush(heap,(0,0,tuple(tuple(floor) for floor in floors)))
    # initialize visited as empty set
    visited=set()
    # set min_solved to infinity
    min_solved = float('infinity')
    # process heap
    while heap:
        # get current record from the heap
        current = {}
        stops, current['floor'], floors_as_tuples = heappop(heap)
        # convert floors to list of lists
        current['floors'] = [set(floor) for floor in floors_as_tuples]
        # check to see if we have already been here
        current['state'] = anonymize(current['floors'])
        if (current['floor'],current['state']) in visited:
            # yes, next
            continue
        # no, add to visited states and process
        visited.add((current['floor'],current['state']))

        # is this a solution:
        if is_solved(current):
            # shorter solution?
            if stops < min_solved:
                min_solved = stops
            # move on to next heap item
            continue
        # for valid floors in current_floor +/- 1
        new = {}
        for new['floor'] in next_floors(current):
            # find each possible pairing, including empty (None)
            for items in itertools.combinations(
                list(current['floors'][current['floor']])+[None],
                2
            ):
                # ignore matches
                if items[0] != items[1]:
                    for result in try_move(stops, items, current, new):
                        heappush(heap,result)
    return min_solved

if __name__ == "__main__":
    test_data = [
        "The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.", #pylint: disable=line-too-long
        "The second floor contains a hydrogen generator.",
        "The third floor contains a lithium generator.",
        "The fourth floor contains nothing relevant.",
    ]
    logging.basicConfig(level=logging.WARNING)
    my_aoc = aoc.AdventOfCode(2016,11)
    lines = my_aoc.load_lines()
    building = [
        set(),
        set(),
        set(),
        set()
    ]
    print(sys.argv,len(sys.argv))
    if len(sys.argv) > 1:
        lines = test_data
    for note in lines:
        parse_notes(note)
    print(building)
    start_time = time.time()
    part1 = solve(building)
    end_time = time.time()
    print(f"Part 1: {part1} ({end_time - start_time} seconds)")
    for item_element in 'ED':
        for item_type in 'MG':
            building[0].add(f"{item_element}{item_type}")
    print(building)
    start_time = time.time()
    part2 = solve(building)
    end_time = time.time()
    print(f"Part 2: {part2} ({end_time - start_time} seconds)")
