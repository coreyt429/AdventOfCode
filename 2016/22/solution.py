"""
Advent Of Code 2016 day 22

This one was tougher than it should ahve been. 
I had a simple shortest path search that worked on the sample data.
The input data was too big of a search area.

While it was running, I read a few hints, and realized most people seemed to
sove this one by hand, because the answer is fairly easy to count out if
you look at the data.  Since the leaderboard closed 8 years ago, I don't 
really gain anything from that.  So I tweaked my algorithm to solve
programatically.

Tricks to narrow search space:

- move empty node to the left of the source node first
  - this was still a large search space so I guided it a bit
  - give it a range of y values to go up
  - give it a position to move it around the wall
  - give it a range to take it to the top
- limit left and down moves to where they are necessary
- could probably further narrow by limiting right moves, but that doesn't seem
  necessary

"""
import time
import re
from heapq import heappush, heappop
from copy import deepcopy
import aoc # pylint: disable=import-error

# regex for matching grid data
pattern_df = re.compile(r'.*x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%')

# static globals for tuple deciphering
SIZE=0
USED=1
AVAIL=2
PERCENT=3
X=0
Y=1
MIN=0
MAX=1

class HeapEntry:
    """
    Class heap entry, gives a sortable object for the heap, 
    workaround for heapq not liking dict
    """
    def __init__(self, my_steps, my_node, my_data):
        """
        Initialize HeapEntry
        """
        # store step counter
        self.steps = my_steps
        # store target node
        self.target = (0,0)
        # store current node
        self.node = my_node
        # store node data
        self.data = my_data

    def __lt__(self, other):
        """
        Less than function for heapq sorting
        """
        return (self.steps, self.node) < (other.steps, other.node)


    def __str__(self):
        """
        Function for string handling
        """
        # get range
        _, maximum = get_range(self.data)
        #retval = f"Steps: {self.steps}, Position: ({self.node})\n"
        retval = ""
        for y_val in range(0,maximum[Y]+1):
            for x_val in range(0,maximum[X]+1):
                symbols = '  '
                pos = (x_val, y_val)
                if pos == self.target:
                    symbols = '()'
                if pos == self.node:
                    symbols = '[]'
                if self.data[pos][USED] < 100:
                    retval += f"{symbols[0]}{self.data[pos][USED]:>3d}/"
                    retval += f"{self.data[pos][SIZE]:>3d}{symbols[1]}"
                else:
                    retval += f"{symbols[0]}###/{self.data[pos][SIZE]:>3d}{symbols[1]}"
                if x_val < maximum[X]:
                    retval += " "
            retval += "\n"
        return retval

def parse_input(lines):
    """
    Function to parse input
    """
    # not sure what the best data structure is yet, so starting with dict of
    #dicts
    # changed my mind already, dict of dict with position tuple as key is where I
    # want to start
    # changed to dict of tuples with position tuple as key
    nodes = {}
    # walk lines
    for line in lines:
        # check if this is a node line
        match = pattern_df.match(line)
        if match:
            # get data from regex match
            # Filesystem              Size  Used  Avail  Use%
            # /dev/grid/node-x0-y0     85T   64T    21T   75%
            position = [0, 0]
            position[X], position[Y], size, used, avail, percent = match.groups()
            # useless operation to make pylint happy later
            # I don't think we are actually using percent, so dropping it from data
            # structure.  for that matter, we provbably aren't using size either
            percent = int(percent)
            # build position[0]/position[1]
            nodes[(int(position[X]),int(position[Y]))] = tuple(
                [int(size), int(used), int(avail)]
            )
    # return data
    return nodes

def get_range(nodes):
    """
    Function to get range of x/y values
    Not needed for part 1, anticipating part 2
    """
    # if empty return all zeros
    if not nodes:
        return ({0: 0, 1: 0}, {0: 0, 1: 0})
    # zip node data into x and y values
    x_values, y_values = zip(*nodes)
    # return mins and maxes
    return (
        {X: min(x_values), Y: min(y_values)},
        {X: max(x_values), Y: max(y_values)}
    )

def get_neighbors(nodes, position, preferred='udlr'):
    """
    Function to get neighbors of a node
    It doesn't looke like I need this for part 1
    """
    # get range
    (minimum, maximum) = get_range(nodes)
    # found = empty set
    found_neighbors = set()
    # if up is valid, add up
    if position[Y] > minimum[Y] and 'u' in preferred:
        found_neighbors.add((position[X], position[Y]-1))
    # if down is valid add down
    if position[Y] <  maximum[Y] and 'd' in preferred:
        found_neighbors.add((position[X], position[Y]+1))
    # if left is valid add left
    if position[X] > minimum[X] and 'l' in preferred:
        found_neighbors.add((position[X]-1, position[Y]))
    # if right is valid add right
    if position[X] <  maximum[X] and 'r' in preferred:
        found_neighbors.add((position[X]+1, position[Y]))
    # return found
    return found_neighbors

def can_move(nodes, node_a, node_b):
    """
    Function to determine if data can move from node_a to node_b
    """
    # {'size': '85', 'used': '64', 'avail': '21', 'percent': '75'}
    #Nodes A and B are not the same node.
    if node_a == node_b:
        return False
    #Node A is not empty (its Used is not zero).
    if nodes[node_a][USED] == 0:
        return False
    #The data on node A (its Used) would fit on node B (its Avail).
    # note to self <= and >= don't mean the same thing
    if nodes[node_b][AVAIL] >= nodes[node_a][USED]:
        return True
    return False

def move_data(nodes, node_a, node_b):
    """
    function to move data from node_a to node_b
    """
    #clone nodes
    tmp_nodes = deepcopy(nodes)
    # get lists of node data to manipulate
    node_a_data = list(tmp_nodes[node_a])
    node_b_data = list(tmp_nodes[node_b])
    # add node_a data to node_b
    node_b_data[USED] += node_a_data[USED]
    # relalculate available
    node_b_data[AVAIL] = node_b_data[SIZE] - node_b_data[USED]
    # set node_a data to empty
    node_a_data[USED] = 0
    # recalculate available
    node_a_data[AVAIL] = node_a_data[SIZE] - node_a_data[USED]
    # convert back to tuples
    tmp_nodes[node_a] = tuple(node_a_data)
    tmp_nodes[node_b] = tuple(node_b_data)
    # return new structure
    return tmp_nodes

def find_empty(nodes):
    """
    Function to find the empty data node
    """
    # walk nodes
    for node, data in nodes.items():
        # find empty
        if data[USED] == 0:
            return node
    return None

# set already seen outside move_empty_to_target in case we overlap
already_seen = set()

def move_empty_to_target(nodes, target_node, current_node = False):
    """
    Function to move empty to target node
    """
    # init heap
    heap = []
    # start heap with current empty position
    heappush(heap,HeapEntry(0, find_empty(nodes), nodes))
    min_steps = float('infinity')
    min_data = None
    # process heap
    while heap:
        # get next test case
        # node as a HeapEntry object
        current = heappop(heap)
        # fin empty
        empty = find_empty(current.data)
        # lets not test longer paths
        if current.steps > min_steps:
            continue
        # solved?
        if empty == target_node:
            if current.steps < min_steps:
                min_steps = current.steps
                min_data = current.data
            continue
        # already visited?
        if str(current) in already_seen:
            continue
        # store in already visited
        already_seen.add(str(current))
        # always allow up
        directions = 'u'
        # allow right if within 1 row of target and col is less than target + 1
        # (23,0) (28, 0)
        if target_node[Y] + 1 >= empty[Y] and target_node[X] + 1 >= empty[X]:
            directions += 'r'
        # allow down if we are at target level or higher
        if target_node[Y] >= empty[Y]:
            directions += 'd'
        # allow down and left if we are at the wall
        if empty[Y] == 21 and empty[X] > 22:
            directions += 'dl'
        # allow left if within 1 row of target and col is > target - 1
        if target_node[Y] + 1 >= empty[Y] and target_node[X] - 1 <= empty[X]:
            directions += 'l'
        for neighbor in get_neighbors(current.data, empty, directions):
            if current_node and current_node == neighbor:
                continue
            # set current to neighbor, and add to heap
            if can_move(current.data, neighbor, empty):
                heappush(
                    heap,
                    HeapEntry(
                        current.steps + 1,
                        neighbor,
                        move_data(current.data, neighbor, empty)
                    )
                )
    return min_steps, min_data


def find_shortest_path(nodes, start_node, target_node):
    """
    Function to find shortest path
    """
    # move the empty node up to wall end
    steps, nodes = move_empty_to_target(nodes, (23, 19))
    total_steps = steps
    # move empty node up to top
    for y_val in range(18,0,-1):
        steps, nodes = move_empty_to_target(nodes, (23, y_val))
        total_steps += steps
    # move empty node to left top (should already be there)
    steps, nodes = move_empty_to_target(nodes, (23, 0))
    total_steps += steps
    # move empty node to left of source
    current = HeapEntry(total_steps, start_node, nodes)
    steps, nodes = move_empty_to_target(nodes, (start_node[X]-1,start_node[Y]))
    total_steps += steps
    # build current
    current = HeapEntry(total_steps, start_node, nodes)
    # loop until current.node is target_node
    while current.node !=  target_node:
        # get empty (should be left of current)
        empty = find_empty(current.data)
        # move from current to empty
        current.data = move_data(current.data, current.node, empty)
        current.steps += 1
        current.node = empty
        # break if we are there
        if current.node == target_node:
            break
        # move empty node to left of current
        steps, nodes = move_empty_to_target(
            current.data,
            (current.node[X]-1,current.node[Y]),
            current.node
        )
        current.data = nodes
        current.steps += steps
    # return steps
    return current.steps

def count_pairs(nodes):
    """
    Function to count pairs (part 1)
    """
    # init sets
    pairs = set()
    # walk nodes
    for node_a in nodes.keys():
        #walk nodes
        for node_b in nodes.keys():
            # can we move from a to b, and is the reverse already saved?
            if can_move(nodes, node_a, node_b):
                # if reverse not in pairs already add
                if not (node_b, node_a) in pairs:
                    pairs.add((node_a, node_b))
    #return count
    return len(pairs)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2016,22)
    input_lines = my_aoc.load_lines()
    storage_nodes = parse_input(input_lines)
    # parts structure to loop
    parts = {
        1: 1,
        2: 2
    }
    answer = {
        1: None,
        2: None
    }
    # loop parts
    for part in parts:
        # log start time
        start = time.time()
        # part 1, just run count_pairs
        if part == 1:
            answer[part] = count_pairs(storage_nodes)
        else:
            # part 2, find target and source nodes
            read_node = (0,0)
            source_node = (get_range(storage_nodes)[MAX][X],0)
            # find shortest path from target to source
            answer[part] = find_shortest_path(storage_nodes, source_node, read_node)
        # log end time
        end = time.time()
        print(f"Part {part}: {answer[part]}, took {end-start} seconds")
