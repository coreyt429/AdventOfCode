import sys
from copy import deepcopy


sys.setrecursionlimit(2200)


"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')
    myMap = []
    for line in lines:
        myMap.append(list(line))
    return myMap

def print_map(myMap,label):
    print(f'{label}:')
    for line in myMap:
        print(''.join(line))
    print()

def next_location(target,direction):
    r=target[0]
    c=target[1]
    if direction == '>':
        c+=1
    elif direction == '<':
        c-=1
    elif direction == '^':
        r-=1
    elif direction == 'v':
        r+=1
    else:
        print(f'next_location Unkown direction: {direction}')
        exit()

    return tuple([r,c])

splitters = set()

def move_beam_iterative(myMap, start_direction, start_target):
    #print(f'move_beam_iterative({start_direction},{start_target})')
    stack = [(start_direction, start_target)]
    splitters = set()  # Assuming splitters is a set to track visited splitters

    turnmap = {
        '/': {'>': '^', '<': 'v', '^': '>', 'v': '<'},
        '\\': {'>': 'v', '<': '^', '^': '<', 'v': '>'}
    }

    while stack:
        direction, target = stack.pop()
        if not (0 <= target[0] < len(myMap)) or not (0 <= target[1] < len(myMap[target[0]])):
            continue  # Skip invalid targets

        currPos = myMap[target[0]][target[1]]
        eMap[target[0]][target[1]] = '#'
        # Process the current position as in your original function
        # Similar logic to your recursive function, adapted for iteration
        if currPos == '.':
            myMap[target[0]][target[1]] = direction
        elif (currPos == '|' and direction in ['^', 'v']):
            pass  # Continue in the same direction
        elif currPos in ['<', '>', '^', 'v']:
            myMap[target[0]][target[1]] = '2'
        elif (currPos == '|' and target not in splitters): 
            splitters.add(target)
            stack.append(('^', next_location(target, '^')))
            stack.append(('v', next_location(target, 'v')))
            continue
        elif (currPos == '-' and target not in splitters):
            splitters.add(target)
            stack.append(('<', next_location(target, '<')))
            stack.append(('>', next_location(target, '>')))
            continue
        elif currPos in ['/','\\']:
            direction = turnmap[currPos][direction]
        elif currPos.isdigit():
            myval = min(int(currPos) + 1, 9)
            myMap[target[0]][target[1]] = str(myval)
        elif currPos in ['-','|']:
            #print(f'Reused splitter {currPos}, cowardly refusing to loop')
            #print(splitters)
            continue

        # Add the next position to the stack
        next_dir, next_target = direction, next_location(target, direction)
        stack.append((next_dir, next_target))

    # Function does not return anything; it modifies myMap in place


def move_beam(myMap,direction,target):  # recursive failed on the part2 data set due to too deep recursion
    #print(f'move_beam(myMap,{direction},{target})')
    # myMap map opbject
    # direction >,<,^,v
    # target tuple next coordinates (0,0)
    global splitters
    global eMap

    turnmap = {}
    turnmap['/'] = { '>': '^', '<': 'v','^': '>','v': '<'}
    turnmap['\\'] = { '>': 'v', '<': '^','^': '<','v': '>'}
    if target[0] == 27:
        if target[1] == 3:
            print(f'move_beam(myMap,{direction},{target})')
            print(f'Current: {myMap[target[0]][target[1]]}')
    if target[0] >= 0 and target[0] < len(myMap): # valid row
        if target[1] >= 0 and target[1] < len(myMap[target[0]]): # valid column 
            currPos = myMap[target[0]][target[1]]
            eMap[target[0]][target[1]] = '#'
            if currPos == '.':
                myMap[target[0]][target[1]] = direction
                move_beam(myMap,direction,next_location(target,direction))
            if (currPos == '|' and direction in ['^','v']) or (currPos == '-' and direction in ['<','>']):
                move_beam(myMap,direction,next_location(target,direction))
            elif currPos in ['<','>','^','v']:
                myMap[target[0]][target[1]] = '2'
                move_beam(myMap,direction,next_location(target,direction))
            elif currPos == '|' and not target in splitters:
                splitters.add(target)
                move_beam(myMap,'^',next_location(target,'^'))
                move_beam(myMap,'v',next_location(target,'v'))
            elif currPos == '-' and not target in splitters:
                splitters.add(target)
                move_beam(myMap,'<',next_location(target,'<'))
                move_beam(myMap,'>',next_location(target,'>'))
            elif currPos in  ['/','\\']:
                next_dir = turnmap[currPos][direction]
                move_beam(myMap,next_dir,next_location(target,next_dir))
            elif currPos.isdigit():
                myval = int(currPos)+1
                if myval > 9:
                    myval = 9
                myMap[target[0]][target[1]] = str(myval)
                move_beam(myMap,direction,next_location(target,direction))
            elif currPos in ['-','|']:
                print(f'Reused splitter {currPos}, cowardly refusing to loop')
                print(splitters)
            
                
def get_neighbors(myMap,currPos): # not used because mark_energized was scrapped
    neighbors = {}
    print(currPos)
    if currPos[0] > 0: # Not at top
        neighbors['n'] = myMap[currPos[0]-1][currPos[1]]
    if currPos[0] < len(myMap)-1: # not at bottom
        neighbors['s'] = myMap[currPos[0]+1][currPos[1]]
    if currPos[1] < len(myMap[0])-1: # not at right
        neighbors['e'] = myMap[currPos[0]][currPos[1]+1]
    if currPos[1] > 0: # not at left
        neighbors['w'] = myMap[currPos[0]][currPos[1]-1]
    return neighbors


def mark_energized(myMap): # scrapped because it made more sense to mark this Map as we traversed the main map
    eMap=deepcopy(myMap)
    for row in range(len(myMap)):
        for col in range(len(myMap[row])):
            neighbors = get_neighbors(eMap,[row,col])
            if eMap[row][col] in ['<','>','^','v','2','3','4','5','6','7','8','9','#']:
                eMap[row][col] = '#'
            elif eMap[row][col] == '-':
                if 'n' in neighbors:
                    if neighbors['n'] in ['v','#','2','3','4','5','6','7','8','9']:
                        eMap[row][col] = '#'
                if 's' in neighbors:
                    if neighbors['s'] in ['^','#','2','3','4','5','6','7','8','9']:
                        eMap[row][col] = '#'
                if 'e' in neighbors:
                    if neighbors['e'] in ['<','#','2','3','4','5','6','7','8','9']:
                        eMap[row][col] = '#'
                if 'w' in neighbors:
                    if neighbors['w'] in ['>','#','2','3','4','5','6','7','8','9']:
                        eMap[row][col] = '#'
            elif eMap[row][col] == '|':
                if 'n' in neighbors:
                    if neighbors['n'] in ['^','#','2','3','4','5','6','7','8','9']:
                        eMap[row][col] = '#'
                if 's' in neighbors:
                    if neighbors['s'] in ['v','#','2','3','4','5','6','7','8','9']:
                        eMap[row][col] = '#'
                if 'e' in neighbors:
                    if neighbors['e'] in ['<','#','2','3','4','5','6','7','8','9']:
                        eMap[row][col] = '#'
                if 'w' in neighbors:
                    if neighbors['w'] in ['>','#','2','3','4','5','6','7','8','9']:
                        eMap[row][col] = '#'
            elif eMap[row][col] in ['/','\\']:
                if 'n' in neighbors:
                    if neighbors['n'] in ['^','v','#','2','3','4','5','6','7','8','9']:
                        eMap[row][col] = '#'
                if 's' in neighbors:
                    if neighbors['s'] in ['^','v','#','2','3','4','5','6','7','8','9']:
                        eMap[row][col] = '#'
                if 'e' in neighbors:
                    if neighbors['e'] in ['<','>','#','2','3','4','5','6','7','8','9']:
                        eMap[row][col] = '#'
                if 'w' in neighbors:
                    if neighbors['w'] in ['<','>','#','2','3','4','5','6','7','8','9']:
                        eMap[row][col] = '#'

    return eMap

eMap = []

def init_eMap(myMap):
    global eMap
    eMap = []
    for row in range(len(myMap)):
        eMap.append([])
        for col in  range(len(myMap[row])):
            eMap[row].append('.')

def part1(parsed_data):
    myMap = deepcopy(parsed_data)
    global eMap
    init_eMap(myMap)
    retval = 0;
    move_beam_iterative(myMap,'>',tuple([0,0]))
#    print_map(myMap,'Final')
#    print_map(eMap,'Energized')
    for row in range(len(eMap)):
        for col in  range(len(eMap[row])):
            if eMap[row][col] == '#':
                retval+=1
    return retval

def count_energized(eMap):
    energized = 0
    for row in range(len(eMap)):
        for col in  range(len(eMap[row])):
            if eMap[row][col] == '#':
                energized+=1
    return energized

def part2(parsed_data):
    retval= 0
    global eMap

    for direction in ['>','<','v','^']:
        listCol = {}
        listRow = {}
        if direction in ['>','<']:
            listCol['>'] = 0
            listCol['<'] = len(parsed_data[0])-1
            for row in range(len(parsed_data)):
                myMap = deepcopy(parsed_data)
                init_eMap(myMap)
                move_beam_iterative(myMap,direction,tuple([row,listCol[direction]]))
                energized = count_energized(eMap)
                if energized > retval:
                    retval = energized
                    #print_map(myMap,f'{direction},{row},{listCol[direction]},{energized}')
                    #print_map(eMap,'energized')
        if direction in ['v','^']:
            listRow['v'] = 0
            listRow['^'] = len(parsed_data)-1
            for col in range(len(parsed_data)):
                myMap = deepcopy(parsed_data)
                init_eMap(myMap)
                move_beam_iterative(myMap,direction,tuple([listRow[direction],col]))
                energized = count_energized(eMap)
                if energized > retval:
                    retval = energized
                #print_map(myMap,f'{direction},{listRow[direction]},{col},{energized}')
                #print_map(eMap,'energized')

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
    