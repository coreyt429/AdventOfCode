import sys
from copy import deepcopy
from functools import cache

def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')
    myMap=[]
    for line in lines:
        myMap.append(list(line))    
    return tuple(tuple(line) for line in myMap)

def print_map(myMap,label):
    print(f'{label}:')
    for line in myMap:
        print(''.join(line))
    print()

@cache
def tilt_north(myMap):
    # Convert the tuple of tuples to a list of lists for easier manipulation
    mutable_map = [list(row) for row in myMap]

    for col in range(len(mutable_map[0])):
        for row in range(len(mutable_map)):
            if mutable_map[row][col] == '.':
                for row2 in range(row + 1, len(mutable_map)):
                    if mutable_map[row2][col] == '.':
                        continue
                    elif mutable_map[row2][col] == 'O':
                        mutable_map[row][col] = 'O'
                        mutable_map[row2][col] = '.'
                        break
                    else:
                        break
    
    # Convert the list of lists back to a tuple of tuples before returning
    return tuple(tuple(row) for row in mutable_map)

# FIXME:  rotation should be cw not ccw
@cache
def rotate_ccw(myMap):
    retval = []
    for row in range(len(myMap)):
        new_row = []
        for col in range(len(myMap[row])):
            new_row.append(myMap[col][len(myMap[0]) - row - 1])
        retval.append(tuple(new_row))  # convert each new row to a tuple
    return tuple(retval)  # convert the entire structure to a tuple of tuples


@cache
def rotate_cw(myMap):
    retval = []
    for col in range(len(myMap[0])):  # iterate over the number of columns in the original map
        new_col = []
        for row in range(len(myMap)):  # iterate over the number of rows in the original map
            new_col.append(myMap[len(myMap) - row - 1][col])  # append elements in a clockwise manner
        retval.append(tuple(new_col))  # convert each new column to a tuple
    return tuple(retval)  # convert the entire structure to a tuple of tuples



@cache
def spin_cycle(myMap):
    #north
    myMap = tilt_north(myMap)
    #west
    myMap = rotate_cw(myMap)
    myMap = tilt_north(myMap)
    #south
    myMap = rotate_cw(myMap)
    myMap = tilt_north(myMap)
    #east
    myMap = rotate_cw(myMap)
    myMap = tilt_north(myMap)
    # reorent to north
    myMap = rotate_cw(myMap)
    return myMap
    
@cache
def score_map(myMap):
    score=0
    for col in range(len(myMap[0])):
        for row in range(len(myMap)):
            if myMap[row][col] == 'O':
                score+=len(myMap)-row
    return score

def part1(parsed_data):
    myMap = deepcopy(parsed_data)
    retval = 0;
    myMap = tilt_north(myMap)
    #print_map(parsed_data,'After')
    retval = score_map(myMap)
    return retval

def part2(parsed_data):
    myMap = deepcopy(parsed_data)
    retval = 0;
    seen = set(myMap)
    maps = [myMap]
    idx=0
    Continue = True
    while True:
        idx+=1
        myMap = spin_cycle(myMap)
        if myMap in seen:
            break
        print(f'Seen: {"".join(["".join(inner_tuple) for inner_tuple in myMap])}')
        seen.add(myMap)
        maps.append(myMap)
        
    print(f'MyMap: {"".join(["".join(inner_tuple) for inner_tuple in myMap])}')
    #First repeated pattern
    first = maps.index(myMap)
    cycle_length = idx-first
    print(f'First: {first}')
    print(f'Last: {idx}')
    print(f'Cycle: {cycle_length}')
    for myIdx in range(len(maps)):
        myMap = maps[myIdx]
        myScore=score_map(myMap)
        print(f'Map: [{myIdx}] [{myScore}] {"".join(["".join(inner_tuple) for inner_tuple in myMap])}')
    targetIdx = (1000000000 - first) % (idx - first) + first
    print(f'Target: {targetIdx}')
    myMap = maps[targetIdx]
    retval = score_map(myMap) 
    return retval

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())
    #print(parsed_data)
    #print_map(parsed_data,'Start')
    #print("Part 1")
    answer1 = part1(parsed_data)
    
    #print("Part 2")
    answer2 = part2(parsed_data)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    