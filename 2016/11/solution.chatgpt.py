import time
import logging
import re
import copy
from heapq import heappop, heappush
from queue import PriorityQueue
import itertools
import sys

import aoc  # pylint: disable=import-error

class Node:
    def __init__(self, floor, floors, g_score, h_score, parent=None):
        self.floor = floor
        self.floors = floors
        self.anonymized = anonymize(floors)
        self.g_score = g_score
        self.h_score = h_score
        self.f_score = g_score + h_score
        self.parent = parent

    def __lt__(self, other):
        if self.f_score == other.f_score:
            return self.h_score < other.h_score
        return self.f_score < other.f_score

    def __str__(self):
        my_string = f"g_score: {self.g_score}, h_score: {self.h_score}, f_score: {self.f_score}\n"
        floor_num = 4
        for floor in reversed(self.floors):
            my_string += f"{floor_num}:" + " ".join(floor) + "\n"
            floor_num -= 1
        my_string += "\n"
        return my_string

elements = {
    'hydrogen': 'H', 'helium': 'He', 'lithium': 'Li', 'beryllium': 'Be', 'boron': 'B',
    'carbon': 'C', 'nitrogen': 'N', 'oxygen': 'O', 'fluorine': 'F', 'neon': 'Ne',
    'sodium': 'Na', 'magnesium': 'Mg', 'aluminum': 'Al', 'silicon': 'Si', 'phosphorus': 'P',
    'sulfur': 'S', 'chlorine': 'Cl', 'argon': 'Ar', 'potassium': 'K', 'calcium': 'Ca',
    'scandium': 'Sc', 'titanium': 'Ti', 'vanadium': 'V', 'chromium': 'Cr', 'manganese': 'Mn',
    'iron': 'Fe', 'cobalt': 'Co', 'nickel': 'Ni', 'copper': 'Cu', 'zinc': 'Zn',
    'gallium': 'Ga', 'germanium': 'Ge', 'arsenic': 'As', 'selenium': 'Se', 'bromine': 'Br',
    'krypton': 'Kr', 'rubidium': 'Rb', 'strontium': 'Sr', 'yttrium': 'Y', 'zirconium': 'Zr',
    'niobium': 'Nb', 'molybdenum': 'Mo', 'technetium': 'Tc', 'ruthenium': 'Ru', 'rhodium': 'Rh',
    'palladium': 'Pd', 'silver': 'Ag', 'cadmium': 'Cd', 'indium': 'In', 'tin': 'Sn',
    'antimony': 'Sb', 'tellurium': 'Te', 'iodine': 'I', 'xenon': 'Xe', 'cesium': 'Cs',
    'barium': 'Ba', 'lanthanum': 'La', 'cerium': 'Ce', 'praseodymium': 'Pr', 'neodymium': 'Nd',
    'promethium': 'Pm', 'samarium': 'Sm', 'europium': 'Eu', 'gadolinium': 'Gd', 'terbium': 'Tb',
    'dysprosium': 'Dy', 'holmium': 'Ho', 'erbium': 'Er', 'thulium': 'Tm', 'ytterbium': 'Yb',
    'lutetium': 'Lu', 'hafnium': 'Hf', 'tantalum': 'Ta', 'tungsten': 'W', 'rhenium': 'Re',
    'osmium': 'Os', 'iridium': 'Ir', 'platinum': 'Pt', 'gold': 'Au', 'mercury': 'Hg',
    'thallium': 'Tl', 'lead': 'Pb', 'bismuth': 'Bi', 'polonium': 'Po', 'astatine': 'At',
    'radon': 'Rn', 'francium': 'Fr', 'radium': 'Ra', 'actinium': 'Ac', 'thorium': 'Th',
    'protactinium': 'Pa', 'uranium': 'U', 'neptunium': 'Np', 'plutonium': 'Pu', 'americium': 'Am',
    'curium': 'Cm', 'berkelium': 'Bk', 'californium': 'Cf', 'einsteinium': 'Es', 'fermium': 'Fm',
    'mendelevium': 'Md', 'nobelium': 'No', 'lawrencium': 'Lr', 'rutherfordium': 'Rf',
    'dubnium': 'Db', 'seaborgium': 'Sg', 'bohrium': 'Bh', 'hassium': 'Hs', 'meitnerium': 'Mt',
    'darmstadtium': 'Ds', 'roentgenium': 'Rg', 'copernicium': 'Cn', 'nihonium': 'Nh',
    'flerovium': 'Fl', 'moscovium': 'Mc', 'livermorium': 'Lv', 'tennessine': 'Ts', 'oganesson': 'Og'
}

pattern_floor = re.compile(r'The (\w+) floor contains (.*)')
pattern_split = re.compile(r', and | and |, ')
pattern_microchip = re.compile(r'a (\w+)-compatible microchip.*')
pattern_generator = re.compile(r'a (\w+) generator.*')

def parse_notes(input_string):
    floors = {'first': 0, 'second': 1, 'third': 2, 'fourth': 3}
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

def anonymize(floors):
    elements_seen = []
    for floor_num in range(3, -1, -1):
        floor = floors[floor_num]
        for item in sorted(list(floor)):
            if item[:-1] not in elements_seen:
                elements_seen.append(item[:-1])
    list_floors = [sorted(list(floor)) for floor in floors]
    for floor in list_floors:
        for item, label in enumerate(floor):
            for idx, element in enumerate(elements_seen):
                if element in label:
                    floor[item] = label.replace(element, str(idx))
    return tuple(tuple(sorted(list(floor))) for floor in list_floors)

def is_valid(floor):
    generators = set()
    micro_chips = set()
    for item in floor:
        if item[-1] == 'G':
            generators.add(item[:-1])
        else:
            micro_chips.add(item[:-1])
    if generators and any(micro_chip not in generators for micro_chip in micro_chips):
        return False
    return True

def is_solved(current):
    if current['floor'] != 3:
        return False
    for floor in range(current['floor'] - 1, -1, -1):
        if len(current['floors'][floor]) > 0:
            return False
    return True

def next_floors_a_star(current_node):
    next_floor_list = []
    for floor in [current_node.floor + 1, current_node.floor - 1]:
        if 0 <= floor <= 3:
            if floor == current_node.floor - 1:
                empty = all(len(current_node.floors[f]) == 0 for f in range(floor, -1, -1))
                if empty:
                    continue
            next_floor_list.append(floor)
    return next_floor_list

def try_move_a_star(current_node, items, new):
    if None in items and new['floor'] > current_node.floor:
        return []
    new_nodes = []
    new['floors'] = [set(floor) for floor in current_node.floors]
    for item in items:
        if item:
            new['floors'][current_node.floor].remove(item)
            new['floors'][new['floor']].add(item)
    if is_valid(new['floors'][current_node.floor]) and is_valid(new['floors'][new['floor']]):
        new_nodes.append(Node(
            new['floor'],
            tuple(tuple(sorted(list(floor))) for floor in new['floors']),
            current_node.g_score + 1,
            h_score(tuple(tuple(sorted(list(floor))) for floor in new['floors'])),
            current_node
        ))
    return new_nodes

def h_score(floors):
    score = 0
    for idx, floor in enumerate(floors):
        score += (3 - idx) * len(floor)
    return score

def solve_a_star(floors):
    start_node = Node(0, tuple(tuple(sorted(list(floor))) for floor in floors), 0, h_score(floors))
    open_set = PriorityQueue()
    open_set.put((start_node.f_score, start_node))
    closed_set = {}

    while not open_set.empty():
        current_node = open_set.get()[1]
        if current_node.anonymized in closed_set and closed_set[current_node.anonymized] <= current_node.g_score:
            continue
        closed_set[current_node.anonymized] = current_node.g_score
        if is_solved({'floor': current_node.floor, 'floors': current_node.floors}):
            return current_node.g_score

        for new_floor in next_floors_a_star(current_node):
            new = {'floor': new_floor}
            for items in itertools.combinations(sorted(list(current_node.floors[current_node.floor])) + [None], 2):
                if items[0] != items[1]:
                    for new_node in try_move_a_star(current_node, items, new):
                        open_set.put((new_node.f_score, new_node))
    return float('infinity')

if __name__ == "__main__":
    test_data = [
        "The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.",
        "The second floor contains a hydrogen generator.",
        "The third floor contains a lithium generator.",
        "The fourth floor contains nothing relevant.",
    ]
    logging.basicConfig(level=logging.WARNING)
    my_aoc = aoc.AdventOfCode(2016, 11)
    lines = my_aoc.load_lines()
    building = [set(), set(), set(), set()]
    if len(sys.argv) > 1:
        lines = test_data
    for note in lines:
        parse_notes(note)
    start_time = time.time()
    part1 = solve_a_star(building)
    end_time = time.time()
    print(f"Part 1: {part1} ({end_time - start_time} seconds)")
    for item_element in 'ED':
        for item_type in 'MG':
            building[0].add(f"{item_element}{item_type}")
    start_time = time.time()
    part2 = solve_a_star(building)
    end_time = time.time()
    print(f"Part 2: {part2} ({end_time - start_time} seconds)")
