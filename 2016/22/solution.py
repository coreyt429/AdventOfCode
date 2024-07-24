"""
Advent Of Code 2016 day 22

"""
import time
import re
import aoc # pylint: disable=import-error

# regex for matching grid data
pattern_df = re.compile(r'.*x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%')

def parse_input(lines):
    """
    Function to parse input
    """
    # not sure what the best data structure is yet, so starting with dict of 
    #dicts
    # changed my mind already, dict with position tuple as key is where I
    # want to start
    nodes = {}
    # walk linies
    for line in lines:
        # check if this is a node line
        match = pattern_df.match(line)
        if match:
            # get data from regex match
            # Filesystem              Size  Used  Avail  Use%
            # /dev/grid/node-x0-y0     85T   64T    21T   75%
            position[0], position[1], size, used, avail, percent = match.groups()
            # build position[0]/position[1]
            nodes[(position[0],position[1])] = {
                'size': size,
                'used': used,
                'avail': avail,
                'percent': percent
            }
    # return data
    return nodes

def get_range(nodes):
    """
    Function to get range of x/y values
    Not needed for part 1, anticipating part 2
    """

    # initialize min/max values
    minimum = {}
    maximum = {}
    minimum[0] = float('infinity')
    maximum[0] = 0
    minimum[1] = float('infinity')
    maximum[1] = 0
    # walk nodes
    for position in nodes:
        for x_y in [0,1]:
            # if new min or max, save
            if position[x_y] < minimum[x_y]:
                minimum[x_y] = position[x_y]
            elif position[x_y] > maximum[x_y]:
                maximum[x_y] = position[x_y]
    # return min/max values
    return minimum, maximum
  
def get_neighbors(nodes, position):
    """
    Function to get neighbors of a node
    It doesn't looke like I need this for part 1
    """
    minimum, maximum = get_range(nodes)
    found_neighbors = set()
    if position[1] > minimum[1]:
        found_neighbors.add((position[0], position[1]-1))
    if position[1] <  maximum[1]:
        found_neighbors.add((position[0], position[1]+1))
    if position[0] > minimum[0]:
        found_neighbors.add((position[0]-1, position[1]))
    if position[0] <  maximum[0]:
        found_neighbors.add((position[0]+1, position[1]))
    return found_neighbors

def solve(nodes, part):
    node_positions = set()
    pairs = set()
    for node_a, node_a_data in nodes.items():
        for node_b, node_b_data in nodes.items():
            #Node A is not empty (its Used is not zero).
            #Nodes A and B are not the same node.
            #The data on node A (its Used) would fit on node B (its Avail).
    return part

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
        start = time.time()
        answer[part] = solve(storage_nodes, part)
        end = time.time()
        print(f"Part {part}: {answer[part]}, took {end-start} seconds")