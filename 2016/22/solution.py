"""
Advent Of Code 2016 day 22

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
        minimum, maximum = get_range(self.data)
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
                    retval += f"{symbols[0]}{self.data[pos][USED]:>3d}/{self.data[pos][SIZE]:>3d}{symbols[1]}"
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
    # walk linies
    for line in lines:
        # check if this is a node line
        match = pattern_df.match(line)
        if match:
            # get data from regex match
            # Filesystem              Size  Used  Avail  Use%
            # /dev/grid/node-x0-y0     85T   64T    21T   75%
            position = [0, 0]
            position[0], position[1], size, used, avail, percent = match.groups()
            # useless operation to make pylint happy later
            # I don't think we are actually using percent, so dropping it from data
            # structure.  for that matter, we provbably aren't using size either
            percent = int(percent)
            # build position[0]/position[1]
            nodes[(int(position[0]),int(position[1]))] = tuple(
                [int(size), int(used), int(avail)]
            )
    # return data
    return nodes

def get_range(nodes):
    """
    Function to get range of x/y values
    Not needed for part 1, anticipating part 2
    """
    if not nodes:
        return ({0: 0, 1: 0}, {0: 0, 1: 0})

    x_values, y_values = zip(*nodes)
    
    return (
        {0: min(x_values), 1: min(y_values)},
        {0: max(x_values), 1: max(y_values)}
    )
  
def get_neighbors(nodes, position, preferred='udlr'):
    """
    Function to get neighbors of a node
    It doesn't looke like I need this for part 1
    """
    (minimum, maximum) = get_range(nodes)
    found_neighbors = set()
    if position[1] > minimum[1] and 'u' in preferred:
        found_neighbors.add((position[0], position[1]-1))
    if position[1] <  maximum[1] and 'd' in preferred:
        found_neighbors.add((position[0], position[1]+1))
    if position[0] > minimum[0] and 'l' in preferred:
        found_neighbors.add((position[0]-1, position[1]))
    if position[0] <  maximum[0] and 'r' in preferred:
        found_neighbors.add((position[0]+1, position[1]))
    return found_neighbors

def can_move(nodes, node_a, node_b):
    """
    Function to determine if data can move from node_a to node_b
    """
    # {'size': '85', 'used': '64', 'avail': '21', 'percent': '75'}
    #Nodes A and B are not the same node.
    if node_a == node_b:
        #print(f"node_a == node_b")
        return False
    #Node A is not empty (its Used is not zero).
    if nodes[node_a][USED] == 0:
        #print(f"{nodes[node_a][USED]} == 0")
        return False
    #The data on node A (its Used) would fit on node B (its Avail).
    # note to self <= and >= don't mean the same thing
    if nodes[node_b][AVAIL] >= nodes[node_a][USED]:
        #print(f"{nodes[node_b][AVAIL]} >= {nodes[node_a][USED]}")
        return True
    #print(f"{nodes[node_b][AVAIL]} !>= {nodes[node_a][USED]}")
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

already_seen = set()

def move_empty_to_target(nodes, target_node, current_node = False):
    """
    Function to move empty to target node
    """
    #print(f"move_empty_to_target(nodes, {target_node})")
    heap = []
    heappush(heap,HeapEntry(0, find_empty(nodes), nodes))
    min_steps = float('infinity')
    min_data = None
    while heap:
        #print(len(heap))
        # get next test case
        #steps, current_node, nodes = heappop(heap)
        # node as a HeapEntry object
        current = heappop(heap)
        #print(f"{current.node}: {current.data[current.node]}")
        empty = find_empty(current.data)
        #print(f"Empty: {empty}")
        #print(current)
        # lets not test longer paths
        if current.steps > min_steps:
            #print(f"Too many steps")
            continue
        # solved?
        if empty == target_node:
            #print("Solved")
            if current.steps < min_steps:
                min_steps = current.steps
                min_data = current.data
            continue
        if str(current) in already_seen:
            #print("already_seen")
            continue
        already_seen.add(str(current))
        #print(f"Empty: {empty}, Neighbors: {get_neighbors(current.data, empty)}")
        directions = 'ur'
        if target_node[1] >= empty[1]:
            directions += 'd'
        if empty[1] == 21 and empty[0] > 22:
            directions += 'dl'
        #(27, 0) (29, 1) ur
        # bumping to six to let it go around the wall
        # target_node[1] + 1 >= empty[1] and 
        if target_node[1] + 1 >= empty[1] and target_node[0] - 1 <= empty[0]:
            directions += 'l'
        #print(target_node, empty, directions)
        for neighbor in get_neighbors(current.data, empty, directions):
            if current_node:
                # don't swap with current node
                if current_node == neighbor:
                    #print(f"Don't move free to final target {neighbor}")
                    continue
            # set current to neighbor, and add to heap
            if can_move(current.data, neighbor, empty):
                heappush(heap,HeapEntry(current.steps + 1, neighbor, move_data(current.data, neighbor, empty)))
            #else:
            #    print(f"Can't move free to {neighbor}")
    return min_steps, min_data


def find_shortest_path(nodes, start_node, target_node):
    """
    Function to find shortest path
    """
    # init heap
    heap = []
    # move the empty space next to target first
    steps, nodes = move_empty_to_target(nodes, (23, 19))
    total_steps = steps
    for y_val in range(18,0,-1):
        #print(y_val)
        steps, nodes = move_empty_to_target(nodes, (23, y_val))
        total_steps += steps

    steps, nodes = move_empty_to_target(nodes, (23, 0))
    total_steps += steps
    steps, nodes = move_empty_to_target(nodes, (start_node[0]-1,start_node[1]))
    total_steps += steps
    #print(total_steps, nodes)
    current = HeapEntry(total_steps, start_node, nodes)
    print(current, current.steps)
    while current.node !=  target_node:
        empty = find_empty(current.data)
        current.data = move_data(current.data, current.node, empty)
        current.steps += 1
        current.node = empty
        if current.node == target_node:
            break
        #print(current)
        #print(current.steps)
        steps, nodes = move_empty_to_target(current.data, (current.node[0]-1,current.node[1]), current.node)
        #print(steps, nodes)
        current.data = nodes
        current.steps += steps
    return current.steps
    

def count_pairs(nodes):
    node_positions = set()
    pairs = set()
    for node_a, node_a_data in nodes.items():
        for node_b, node_b_data in nodes.items():
            # can we move from a to b, and is the reverse already saved?
            if can_move(nodes, node_a, node_b):
                if not (node_b, node_a) in pairs:
                    pairs.add((node_a, node_b))
    return len(pairs)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2016,22)
    #input_text = my_aoc.load_text()
    #print(input_text)
    input_lines = my_aoc.load_lines()
    #print(input_lines)
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
            target_node = (0,0)
            source_node = (get_range(storage_nodes)[1][0],0)
            # find shortest path from target to source
            answer[part] = find_shortest_path(storage_nodes, source_node, target_node)
        # log end time
        end = time.time()
        print(f"Part {part}: {answer[part]}, took {end-start} seconds")
