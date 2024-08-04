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
"""
import time
import logging
import re
import copy
from heapq import heappop, heappush
from queue import PriorityQueue
import itertools
import sys

import aoc #pylint: disable=import-error

class Node:
    """
    Node class for scoring positions
    """
    def __init__(self, floor, floors, g_score, h_score, parent=None):
        """
        Init node
        """
        self.floor = floor
        self.floors = floors
        self.anonymized = anonymize(floors)
        self.g_score = g_score
        self.h_score = h_score
        self.f_score = g_score + h_score
        self.threshold = float('infinity')
        self.parent = parent

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
        my_string = f"g_score: {self.g_score}, h_score: {self.h_score}, f_score: {self.f_score}, threshold: {self.threshold}\n"
        floor_num = 4
        for floor in reversed(self.floors):
            my_string += f"{floor_num}:" + " ".join(floor) + "\n"
            floor_num -= 1
        my_string += "\n"
        return my_string

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
        for item in sorted(list(floor)):
            if not item[:-1] in elements_seen:
                elements_seen.append(item[:-1])
    #print(elements_seen)
    # convert tuples or sets to list so we can work with them
    list_floors = [sorted(list(floor)) for floor in floors]
    # walk all the items and replace the element with its index
    # ex:  HG -> 0G, LiM -> 1M
    for floor in list_floors:
        for item, label in enumerate(floor):
            for idx, element in enumerate(elements_seen):
                if element in label:
                    #print(f"{floor[item]} replace {element} with {str(idx)}")
                    floor[item] = label.replace(element, str(idx))
            #print(floor[item])
    #exit()
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
            for lower_floor in range(current_node.floor-1,-1,-1):
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

#try_move_a_star(current_node, items, new)
def try_move_a_star(current_node, items, new):
    """
    Function to try moves and return new heap entries
    """
    # lets try not going up with an empty slot
    # this cut part 1 time in half :)
    if None in items:
        if new['floor'] > current_node.floor:
            return []
    new_nodes=[]
    # clone current['floors']
    new['floors'] = []
    for floor in current_node.floors:
        new['floors'].append(set(floor))
    # move items from current['floor'] to new['floor']
    for item in items:
        # ignore if None
        if item:
            new['floors'][current_node.floor].remove(item)
            new['floors'][new['floor']].add(item)
    # if both floors are still valid
    if (is_valid(new['floors'][current_node.floor]) and
        is_valid(new['floors'][new['floor']])):
        # add to new_nodes
        # def __init__(self, floor, floors, g_score, h_score, parent=None):
        new_nodes.append(Node(
            new['floor'],
            tuple(tuple(sorted(list(floor))) for floor in new['floors']),
            current_node.g_score + 1,
            h_score(tuple(tuple(sorted(list(floor))) for floor in new['floors']), current_node.g_score, current_node.threshold),
            current_node
        )
        )
    return new_nodes

def h_score_works_slow(floors, stops, threshold):
    #score = min_steps_remaining(floors)
    score = 0
    for idx, floor in enumerate(floors):
        score += (3-idx) * len(floor)
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
    score = 0
    for idx, floor in enumerate(floors):
        score += (3 - idx) * len(floor)
    return score

def h_score(floors, stops, threshold):
    #print(f"h_score({floors}, {stops}, {threshold})")
    score = min_steps_remaining(floors)
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

def min_steps_remaining(floors):
    score = 0
    for idx, floor in enumerate(floors):
        score += (3 - idx) * len(floor) 
    return score // 2

def h_score_percentage(floors, stops, threshold):
    max_items = sum(len(floor) for floor in floors)
    max_score = max_items * 3  # max_items * (4-1) since the highest floor gives the maximum multiplier
    score = min_steps_remaining(floors)
    percentage_complete = score / max_score if max_score > 0 else 1
    score = 1 - percentage_complete

    #if len(floors[0]) == 0:
    #    score -= 0.5
    #    if len(floors[1]) == 0:
    #        score -= 1
    return score

def solve_a_star(floors):
    goal = 0
    # sum items as goal
    for floor in floors:
        goal += len(floor)
    # multiply by floor 3
    min_solved = float('infinity')
    goal = h_score((set(),set(),set(),set(range(goal))), 0 , min_solved)
    #def a_star(start, goal, maze, heuristics):
    """
    Function to execute A* algorithm to detect shortest solution
    """
    # set start_node  (position, g_score, h_score)
    # def __init__(self, floor, floors, g_score, h_score, parent=None):
    #heappush(heap,(0,0,tuple(tuple(floor) for floor in floors)))
    

    start_node = Node(0, tuple(tuple(sorted(list(floor))) for floor in floors), 0, h_score(tuple(tuple(sorted(list(floor))) for floor in floors), 0, min_solved))
    # initialize PriorityQueue
    open_set = PriorityQueue()
    # add start_node to priority_queue (f_score, node)
    open_set.put((start_node.f_score, start_node))
    # initialize closed set
    closed_set = {}

    # process open set
    last_q = 0
    counter = 0
    while not open_set.empty():
        counter += 1
        # get current node
        current_node = open_set.get()[1]
        #print(current_node)
        if open_set.qsize() // 1000 != last_q:
            last_q = open_set.qsize() // 1000
            #print(f"Counter: {counter} Queue: {open_set.qsize()}. min_solved = {min_solved}")
            #print(current_node)
        #if current_node.g_score in [46, 47]:
        #    print(current_node)
        # add to closed set
        # are we at the goal?
        if current_node.h_score == goal:
            if current_node.g_score < min_solved:
                print(f"Took {counter} tries")
                #print(f"Found win in {current_node.g_score} stops: {current_node.floors}")
                #print(current_node)
                min_solved = current_node.g_score
                # this worked for part1, we were getting the lowest step win first
                # with the current h_score. earlier h_score routines were hitting 
                # longer step count wins first, so this may not work for part 2  
                #if min_solved in [47, 71]:
                #    return min_solved
                #next_node = current_node
                #path = []
                #while next_node:
                #    path.append(next_node)
                #    next_node = next_node.parent
                #for next_node in reversed(path):
                #    print(next_node)
            continue
        # is this state in closed_set?
        if current_node.anonymized in closed_set:
            # update closed set if we re in closed set, but fewer steps we'll process
            # otherwise continue
            if current_node.g_score > closed_set.get(current_node.anonymized, float('infinity')):
                continue
        closed_set[current_node.anonymized] = current_node.g_score
        if current_node.g_score >= min_solved:
            #print(f"Discarding too many steps: {current_node.g_score, current_node.h_score, current_node.f_score}")
            continue
        # is it possible to beat current score?
        if min_steps_remaining(current_node.floors) + current_node.g_score > min_solved:
            continue
        # update threshold so children calculate h_score accordingly
        current_node.threshold = min_solved
        # for valid floors in current_floor +/- 1
        new = {}
        for new['floor'] in next_floors_a_star(current_node):
            # find each possible pairing, including empty (None)
            for items in itertools.combinations(
                sorted(list(current_node.floors[current_node.floor])) + [None],
                2
            ):
                # ignore matches
                if items[0] != items[1]:
                    for new_node in try_move_a_star(current_node, items, new):
                        # skip if already seen, unless it is a lower step count.
                        if new_node.anonymized not in closed_set or new_node.g_score < closed_set[new_node.anonymized]:
                            open_set.put((new_node.f_score, new_node))
    print("Finished processing")
    return min_solved  # No path found


def solve_bfs(floors):
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
        if stops > min_solved:
            continue
        # convert floors to list of lists
        current['floors'] = [set(floor) for floor in floors_as_tuples]
        # is this a solution:
        if is_solved(current):
            # shorter solution?
            if stops < min_solved:
                min_solved = stops
            # move on to next heap item
            continue
        # check to see if we have already been here
        current['state'] = anonymize(current['floors'])
        if (current['floor'], current['state']) in visited:
            # yes, next
            continue
        # no, add to visited states and process
        visited.add((current['floor'],current['state']))

        # for valid floors in current_floor +/- 1
        new = {}
        for new['floor'] in next_floors(current):
            # find each possible pairing, including empty (None)
            for items in itertools.combinations(
                list(current['floors'][current['floor']]) + [None],
                2
            ):
                # ignore matches
                if items[0] != items[1]:
                    for result in try_move(stops, items, current, new):
                        heappush(heap, result)
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
    #print(sys.argv,len(sys.argv))
    if len(sys.argv) > 1:
        lines = test_data
    for note in sorted(lines):
        parse_notes(note)
    
    #print(building)
    start_time = time.time()
    part1 = solve_a_star(building)
    end_time = time.time()
    print(f"Part 1: {part1} ({end_time - start_time} seconds)")
    #exit()
    for item_element in 'ED':
        for item_type in 'MG':
            building[0].add(f"{item_element}{item_type}")
    #print(building)
    start_time = time.time()
    part2 = solve_a_star(building)
    end_time = time.time()
    print(f"Part 2: {part2} ({end_time - start_time} seconds)")
