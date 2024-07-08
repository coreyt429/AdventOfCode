import sys
from copy import deepcopy
from functools import cache
from itertools import product

def parse_input(data):
    myMap = []
    myMap2 = []
    myDict = {'O': 0, '.': 1, 'S': 2, '#': 3}

    # Split the data into lines
    lines = data.strip().split('\n')
    for line in lines:
        row = list(line)
        myMap.append(row)
        myMap2.append([myDict[element] for element in row])
    return myMap,myMap2

def print_map(myMap, label): # modified to handle tuple of tuples of ints instead of list of lost of str
    print(f'print_map({myMap})')
    print(f'{label}:')
    char_map = {0: 'O', 1: '.', 2: 'S', 3: '#'}
    for line in myMap:
        print(''.join(char_map[i] for i in line))

    print()

@cache
def get_neighbor_coordinates(row_max, col_max, row, col, include_negative=False):
    retval = []
    for nr, nc in [(row-1, col), (row, col-1), (row, col+1), (row+1, col)]:
        if include_negative or (0 <= nr < row_max and 0 <= nc < col_max):
            retval.append((nr, nc))
    return retval


def take_step(myMap):
    spaces = set()
    for i, j in product(range(len(myMap)), range(len(myMap[0]))):
        if myMap[i][j] in {0, 2}:  # Using a set for faster membership checking
            spaces.add((i, j))
    for i,j in spaces:
        destinations = get_neighbor_coordinates(len(myMap),len(myMap[0]),i,j)
        myMap[i][j] = 1
        for dr, dc in destinations:
            if myMap[dr][dc] < 3:
                myMap[dr][dc] = 0
    return myMap

## # Part 2 is from stole.py.  I like this solution, to the infinite grid problem.  # comments added to improve my understanding
def convert_map(myMap):
    # init grid
    grid, start = {}, None
    # original was reading the file, but since I already have it in a 
    for y in range(len(myMap)):
        for x in range(len(myMap[y])):
            c=myMap[y][x]
            if c == "S":
                # store start coordinates as complex number
                start = x + 1j * y
            # store plot value with coordinates as complex number
            grid[x + 1j * y] = c
    # max x and y values
    maxX, maxY = int(max(p.real for p in grid)), int(max(p.imag for p in grid))            
    return grid, start, maxX, maxY

# simplicity in complexity?
def infinite_grid(grid, p, maxX, maxY):
    # remainder of x and y if point divided by max X/Y in single grid
    x = p.real % (maxX + 1)
    y = p.imag % (maxY + 1)
    # return corresponding grid value
    return grid[x + y * 1j]

def generate_history(grid, start, maxX, maxY, steps):
    # initialize empty ods, and evens / queue with start 
    odds, evens, queue = set(), {start}, {start}
    # quickly generate neighbors, I should probably use lamda like this more.
    n4 = lambda p: [p - 1j, p - 1, p + 1, p + 1j]
    # history storage
    odd_history, even_history = [0], [1]
    for i in range(1,steps+1):
        new_points = set()
        for p in queue: # initially start, after that new_points
            # foreach neighbor if not already processed
            for n in [n for n in n4(p) if n not in evens and n not in odds]:
                # if start or empty
                if infinite_grid(grid, n, maxX, maxY) in ".S":
                    new_points.add(n)
        # add to evens or odds
        if i % 2:
            odds |= new_points
        else:
            evens |= new_points
        # add histories
        odd_history.append(len(odds))
        even_history.append(len(evens))
        # set queue for next pass
        queue = new_points
    # return histories
    return odd_history, even_history


def part1(startMap):
    myMap = deepcopy(startMap)
    retval = 0;
    #print_map(myMap,'Start')
    for idx in range(64):
        #myMap = take_step(myMap)
        take_step(myMap)
        #print_map(myMap,f'Step {idx}')
    for row in myMap:
        for sq in row:
            if sq == 0:
                retval+=1
    #print(f"Part1: {retval}")
    return retval

def part2(parsed_data):
    retval = 0;
    # convert map to infinite grid format
    grid, start, maxX, maxY = convert_map(parsed_data)
    # generate history, only save odd history
    history, _ = generate_history(grid, start, maxX, maxY, 3*262+65)
    # I understand this math, but where did 262 come from to start with?
    steps = 101150 # (26501365 - 65) // 262 
    a = history[2*262+65]
    b = history[2*262+65] - history[262+65]
    c = history[3*262+65] - 2*history[2*262+65] + history[262+65]
    retval = a + b*(steps-2) + c*((steps-2)*(steps-1)//2)
    return retval

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data,myMap = parse_input(f.read())
    #print("Part 1")
    answer1 = part1(myMap)
    
    #print("Part 2")
    answer2 = part2(parsed_data)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    