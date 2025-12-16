"""
Advent Of Code 2023 day 10

"""

# import system modules
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)



def find_start(rows):
    col = -1
    for row in range(len(rows)):
        col = rows[row].find('S')
        if col != -1:
            break
    return [row,col]

def get_dots(grid):
    dots = []
    for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == '.':
                    dots.append([row,col])
    return dots

def fix_start(grid):
    global DEBUG
    DEBUG = False
    pipes = {
        '|': ['N','S'],
        '-': ['E','W'],
        'L': ['N','E'],
        'J': ['N','W'],
        '7': ['W','S'],
        'F': ['E','S']
    }
    start=find_start(grid)
    logger.debug('Start: %s', start)
    row=start[0]
    col=start[1]
    neighbors=get_neighbor_coordinates(grid,start[0],start[1])
    """
    0 1 2
    3   4
    5 6 7
    ('.', '.', 'F')
    ('.', 'S', 'J')
    ('.', '|', 'F')
    """
    potential = {
        'N': grid[neighbors[1][0]][neighbors[1][1]],
        'S': grid[neighbors[6][0]][neighbors[6][1]],
        'E': grid[neighbors[4][0]][neighbors[4][1]],
        'W': grid[neighbors[5][0]][neighbors[5][1]]
    }
    logger.debug('%s', neighbors)
    logger.debug(
        '%s',
        (
            grid[neighbors[0][0]][neighbors[0][1]],
            grid[neighbors[1][0]][neighbors[1][1]],
            grid[neighbors[2][0]][neighbors[2][1]],
        ),
    )
    logger.debug(
        '%s',
        (
            grid[neighbors[3][0]][neighbors[3][1]],
            grid[row][col],
            grid[neighbors[4][0]][neighbors[4][1]],
        ),
    )
    logger.debug(
        '%s',
        (
            grid[neighbors[5][0]][neighbors[5][1]],
            grid[neighbors[6][0]][neighbors[6][1]],
            grid[neighbors[7][0]][neighbors[7][1]],
        ),
    )
    connections = {}
    for direction in potential.keys():
        opposite=reverse_direction(direction)
        if potential[direction] in pipes.keys():
            if opposite in pipes[potential[direction]]:
                connections[direction] = potential[direction]
    if len(connections) == 2: # there are only two possibilities, so just find what matches them
        mates = sorted(connections.keys())
        for pipe in pipes:
                check=sorted(pipes[pipe])
                if check == mates:
                        set_point(grid,row,col,pipe)
    else: # there are more than two, filter out the ones that aren't in loop
        print('write this when we need it')

def find_neighbors(currPos,rows):
    retval = {'N': None, 'S': None, 'E': None, 'W': None}
    if currPos[0] != 0:
        retval['N'] = rows[currPos[0]-1][currPos[1]]
    if currPos[1] != 0:
        retval['W'] = rows[currPos[0]][currPos[1]-1]
    if currPos[0] != len(rows[currPos[0]]):
        retval['E'] = rows[currPos[0]][currPos[1]+1]
    if currPos[0] != len(rows):
        retval['S'] = rows[currPos[0]+1][currPos[1]]
    # ignore ground
    for neighbor in retval:
        if retval[neighbor] == '.':
            retval[neighbor] = None
    if retval['N'] not in ['|','7','F']:
        retval['N'] = None
    if retval['S'] not in ['|','L','J']:
        retval['S'] = None
    if retval['W'] not in ['-','L','F']:
         retval['S'] = None
    if retval['E'] not in ['-','J','7']:
         retval['S'] = None
    return retval

def move(currPos,direction):
    if direction == 'N':
        currPos[0]-=1
    elif direction == 'S':
        currPos[0]+=1
    elif direction == 'E':
        currPos[1]+=1
    elif direction == 'W':
        currPos[1]-=1
    return currPos
        
"""
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
"""

def reverse_direction(direction):
    retval = None
    if direction == 'N':
        retval = 'S'
    elif direction == 'S':
        retval = 'N'
    elif direction == 'E':
        retval = 'W'
    elif direction == 'W':
        retval = 'E'
    
    return retval

def next_direction(pipe,direction):
    pipes = {
        '|': ['N','S'],
        '-': ['E','W'],
        'L': ['N','E'],
        'J': ['N','W'],
        '7': ['W','S'],
        'F': ['E','S']
    }
    opposite = reverse_direction(direction)
    if opposite in pipes[pipe]:
        retval = pipes[pipe][0]
        if retval == opposite:
            retval = pipes[pipe][1]
    else:
        print("Error in next_direction, last pipe doesn't connect to this pipe")
        exit();
    return retval

def part1(parsed_data):
    retval = 0;
    start=find_start(parsed_data)
    currPos = start
    neighbors = find_neighbors(currPos,parsed_data)
    for direction in neighbors:
        if neighbors[direction] is not None:
            break
    currPos = move(currPos,direction)
    steps = 1;
    while parsed_data[currPos[0]][currPos[1]] != 'S':
        direction = next_direction(parsed_data[currPos[0]][currPos[1]],direction)
        currPos = move(currPos,direction)
        steps+=1
    return int(steps/2)

def set_point(grid,row,col,value):
    # Convert the specific string to a list of characters
    row_list = list(grid[row])
    # Modify the desired character
    row_list[col] = value
    # Reconstruct the string and put it back in the grid
    grid[row] = ''.join(row_list)

def get_neighbor_coordinates(grid,row,col):
    retval = []
    neighbors = [
        [row-1,col-1], [row-1,col], [row-1,col+1],
        [row,col-1], [row,col+1],
        [row+1,col-1], [row+1,col], [row+1,col+1],
    ]
    for neighbor in neighbors:
        valid = True
        if neighbor[0] < 0 or neighbor[1] < 0:
            valid = False
        elif neighbor[0] >= len(grid):
            valid = False
        elif neighbor[1] >= len(grid[neighbor[0]]):
            valid = False
        if valid:
            retval.append(neighbor)
        else:
            retval.append([None,None])
    return retval

def can_connect(pipe1,pipe2,direction):
    #print(f'can_connect({pipe1},{pipe2},{direction})')
    retval = False
    pipes = {
        '|': ['N','S'],
        '-': ['E','W'],
        'L': ['N','E'],
        'J': ['N','W'],
        '7': ['W','S'],
        'F': ['E','S']
    }
    if pipe1 in pipes:
        if direction in pipes[pipe1]: # can we even go out of pipe one the way we need to?
            if pipe2 in pipes:
                opposite = reverse_direction(direction)
                if opposite in pipes[pipe2]: # can we go the opposite direction from pipe2?
                    retval = True
    #print(retval)
    return retval

def follow_squeeze(grid,posA,posB,direction):
    retval = None
    pos1 = posA.copy();
    pos2 = posB.copy();
    
    logger.debug('follow_squeeze(grid,%s,%s,%s):', pos1, pos2, direction)
    opposite = reverse_direction(direction)
    # logger.debug('lets not go %s, we are already traveling %s', opposite, direction)
    pos3 = pos1.copy()
    pos4 = pos2.copy()
    targets = []
    if direction == 'E':
        """
        13
        24
        """
        pos3[1]+=1
        pos4[1]+=1
        logger.debug(
            '\n%s%s\n%s%s',
            grid[pos1[0]][pos1[1]],
            grid[pos3[0]][pos3[1]],
            grid[pos2[0]][pos2[1]],
            grid[pos4[0]][pos4[1]],
        )
        if grid[pos3[0]][pos3[1]] == 'O' or grid[pos4[0]][pos4[1]] == 'O':
            retval =  'O' # found a path to outside, so lets roll with it
        elif grid[pos3[0]][pos3[1]] == '.' or grid[pos4[0]][pos4[1]] == '.':
            retval = '.' # found a path to another unkown or inside
        elif grid[pos3[0]][pos3[1]] == 'S' or grid[pos4[0]][pos4[1]] == 'S':
            retval = '.' # found a path to start
        elif pos3[1] >= len(grid[pos3[0]]):
            logger.debug('We have reached the right edge')
            retval = 'O'
        else: # check remaining directions
            if(not can_connect(grid[pos3[0]][pos3[1]],grid[pos4[0]][pos4[1]],'S')):
                logger.debug('We can proceed east')
                targets.append([pos3,pos4,'E'])
            if(not can_connect(grid[pos1[0]][pos1[1]],grid[pos3[0]][pos3[1]],'E')):
                logger.debug('We can proceed North')
                targets.append([pos1,pos3,'N'])
            if(not can_connect(grid[pos2[0]][pos2[1]],grid[pos4[0]][pos4[1]],'E')):
                logger.debug('We can proceed South')
                targets.append([pos2,pos4,'S'])
    elif direction == 'W':
        """
        31
        42
        """
        pos3[1]-=1
        pos4[1]-=1
        logger.debug(
            '\n%s%s\n%s%s',
            grid[pos3[0]][pos3[1]],
            grid[pos1[0]][pos1[1]],
            grid[pos4[0]][pos4[1]],
            grid[pos2[0]][pos2[1]],
        )
        if grid[pos3[0]][pos3[1]] == 'O' or grid[pos4[0]][pos4[1]] == 'O':
            retval = 'O' # found a path to outside, so lets roll with it
        elif grid[pos3[0]][pos3[1]] == '.' or grid[pos4[0]][pos4[1]] == '.':
            retval = '.' # found a path to another unkown or inside
        elif grid[pos3[0]][pos3[1]] == 'S' or grid[pos4[0]][pos4[1]] == 'S':
            retval = '.' # found a path to start
        elif pos3[1] < 0:
            logger.debug('We have reached the left edge')
            retval = 'O'
        else:
            if(not can_connect(grid[pos3[0]][pos3[1]],grid[pos4[0]][pos4[1]],'S')):
                logger.debug('We can proceed west')
                targets.append([pos3,pos4,'W'])
            if(not can_connect(grid[pos1[0]][pos1[1]],grid[pos3[0]][pos3[1]],'W')):
                logger.debug('We can proceed North')
                targets.append([pos3,pos1,'N'])
            if(not can_connect(grid[pos2[0]][pos2[1]],grid[pos4[0]][pos4[1]],'W')):
                logger.debug('We can proceed South')
                targets.append([pos4,pos2,'S'])
    elif direction == 'N':
        """
        34
        12
        """
        pos3[0]-=1
        pos4[0]-=1
        logger.debug('%s', (pos1, pos2, pos3, pos4))
        logger.debug(
            '\n%s%s\n%s%s',
            grid[pos3[0]][pos3[1]],
            grid[pos4[0]][pos4[1]],
            grid[pos1[0]][pos1[1]],
            grid[pos2[0]][pos2[1]],
        )
        if grid[pos3[0]][pos3[1]] == 'O' or grid[pos4[0]][pos4[1]] == 'O':
            retval = 'O' # found a path to outside, so lets roll with it
        elif grid[pos3[0]][pos3[1]] == '.' or grid[pos4[0]][pos4[1]] == '.':
            retval = '.' # found a path to another unkown or inside
        elif grid[pos3[0]][pos3[1]] == 'S' or grid[pos4[0]][pos4[1]] == 'S':
            retval = '.' # found a path to start
        elif pos3[0] < 0:
            logger.debug('We have reached the top edge')
            retval = 'O'
        else: # check remaining directions
            if(not can_connect(grid[pos3[0]][pos3[1]],grid[pos4[0]][pos4[1]],'E')):
                logger.debug('We can proceed North')
                targets.append([pos3,pos4,'N'])
            if(not can_connect(grid[pos2[0]][pos2[1]],grid[pos4[0]][pos4[1]],'N')):
                logger.debug('We can proceed East')
                targets.append([pos4,pos2,'E'])
            if(not can_connect(grid[pos1[0]][pos1[1]],grid[pos3[0]][pos3[1]],'N')):
                logger.debug('%s,%s', grid[pos3[0]][pos3[1]], grid[pos1[0]][pos1[1]])
                logger.debug('We can proceed West')
                targets.append([pos3,pos1,'W'])
    elif direction == 'S':
        """
        12
        34
        """
        pos3[0]+=1
        pos4[0]+=1
        logger.debug('%s', (pos1, pos2, pos3, pos4))
        logger.debug(
            '\n%s%s\n%s%s',
            grid[pos1[0]][pos1[1]],
            grid[pos2[0]][pos2[1]],
            grid[pos3[0]][pos3[1]],
            grid[pos4[0]][pos4[1]],
        )
        if grid[pos3[0]][pos3[1]] == 'O' or grid[pos4[0]][pos4[1]] == 'O':
            logger.debug('Found O South')
            retval =  'O' # found a path to outside, so lets roll with it
        elif grid[pos3[0]][pos3[1]] == '.' or grid[pos4[0]][pos4[1]] == '.':
            retval = '.' # found a path to another unkown or inside
        elif grid[pos3[0]][pos3[1]] == 'S' or grid[pos4[0]][pos4[1]] == 'S':
            retval = '.' # found a path to start
        elif pos3[0] >= len(grid):
            logger.debug('We have reached the bottom edge')
            retval = 'O'
        else: # check remaining directions
            if(not can_connect(grid[pos3[0]][pos3[1]],grid[pos4[0]][pos4[1]],'E')):
                logger.debug('We can proceed South')
                targets.append([pos3,pos4,'S'])
            if(not can_connect(grid[pos1[0]][pos1[1]],grid[pos3[0]][pos3[1]],'S')):
                logger.debug('We can proceed West')
                targets.append([pos1,pos3,'W'])
            if(not can_connect(grid[pos2[0]][pos2[1]],grid[pos4[0]][pos4[1]],'S')):
                logger.debug('We can proceed East')
                targets.append([pos2,pos4,'E'])
    logger.debug('Targets: %s', targets)
    logger.debug('Retval: %s', retval)
    if retval is None:
        if len(targets) < 1: # we hit a dead end
            retval = '.'
        else:
            for target in targets:
                logger.debug('Target:%s', target)
                retval = follow_squeeze(grid,target[0],target[1],target[2])
                logger.debug('returned %s', retval)
                if retval == 'O':
                    break
    elif retval == 'O':
        logger.debug('Found 0, returning it')
    elif len(targets) < 1: # we hit a dead end
        retval = '.'
    
    return retval
    



def can_squeezeold(grid,row,col):
    logger.debug('can_squeeze(grid,%s,%s)', row, col)
    retval = []
    pipes = {
        '|': ['N','S'],
        '-': ['E','W'],
        'L': ['N','E'],
        'J': ['N','W'],
        '7': ['W','S'],
        'F': ['E','S']
    }
    neighbors = get_neighbor_coordinates(grid,row,col)
    """
    0 1 2
    3   4
    5 6 7
    """
    logger.debug('%s', neighbors)
    logger.debug('%s', grid[4][13])
    logger.debug(
        '%s',
        (
            grid[neighbors[0][0]][neighbors[0][1]],
            grid[neighbors[1][0]][neighbors[1][1]],
            grid[neighbors[2][0]][neighbors[2][1]],
        ),
    )
    logger.debug(
        '%s',
        (
            grid[neighbors[3][0]][neighbors[3][1]],
            grid[row][col],
            grid[neighbors[4][0]][neighbors[4][1]],
        ),
    )
    logger.debug(
        '%s',
        (
            grid[neighbors[5][0]][neighbors[5][1]],
            grid[neighbors[6][0]][neighbors[6][1]],
            grid[neighbors[7][0]][neighbors[7][1]],
        ),
    )
    
    pairs = [
        {'pos': [0,1], 'direction': 'E', 'egress': 'N'},
        {'pos': [1,2], 'direction': 'E', 'egress': 'N'},
        {'pos': [0,3], 'direction': 'S', 'egress': 'W'},
        {'pos': [2,4], 'direction': 'S', 'egress': 'E'},
        {'pos': [3,5], 'direction': 'S', 'egress': 'W'},
        {'pos': [4,7], 'direction': 'S', 'egress': 'E'},
        {'pos': [5,6], 'direction': 'E', 'egress': 'S'},
        {'pos': [6,7], 'direction': 'E', 'egress': 'S'},
    ]
    for idx2 in range(len(pairs)):
        for pair in pairs:
            pos = pair['pos']
            direction = pair['direction']
            neighbor1 = neighbors[pos[0]]
            neighbor2 = neighbors[pos[1]]
            logger.debug(
                'can_squeeze: %s,%s',
                pair,
                ([grid[neighbor1[0]][neighbor1[1]]], grid[neighbor2[0]][neighbor2[1]]),
            )

            if grid[neighbor1[0]][neighbor1[1]] in pipes:
                if grid[neighbor2[0]][neighbor2[1]] in pipes:
                    if not can_connect(grid[neighbor1[0]][neighbor1[1]],grid[neighbor2[0]][neighbor2[1]],direction):
                        logger.debug(
                            '(can_squeeze%s,%s) squeeze through %s[%s]/%s[%s]',
                            row,
                            col,
                            pos[0],
                            grid[neighbor1[0]][neighbor1[1]],
                            pos[1],
                            grid[neighbor2[0]][neighbor2[1]],
                        )
                        result = follow_squeeze(grid,[neighbor1[0],neighbor1[1]],[neighbor2[0],neighbor2[1]],pair['egress'])
                        set_point(grid,row,col,result)
                        logger.debug('follow_squeeze: %s', result)
                        if result == 'O': # break if we find success, so we don't overwrite it
                            break
                elif grid[neighbor1[0]][neighbor1[1]] == 'O' or grid[neighbor2[0]][neighbor2[1]] == 'O':
                    set_point(grid,row,col,'O')
            elif grid[neighbor1[0]][neighbor1[1]] == 'O' or grid[neighbor2[0]][neighbor2[1]] == 'O':
                set_point(grid,row,col,'O')
                break
    return retval


def set_outside(grid,row,col):
    set_point(grid,row,col,'O')
    

def mark_outside(grid):
    for i in range(len(grid)):
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == '.':
                    for neighbor in get_neighbor_coordinates(grid,row,col):
                        if neighbor[0] is None:
                            set_point(grid,row,col,'O')
                        elif grid[neighbor[0]][neighbor[1]] == 'O':
                            set_point(grid,row,col,'O')

def O_next_door(grid,dot):
    row = dot[0]
    col = dot[1]
    logger.debug('can_squeeze(grid,%s,%s)', row, col)
    retval = False
    neighbors = get_neighbor_coordinates(grid,row,col)
    for neighbor in neighbors:
        if grid[neighbor[0]][neighbor[1]] == 'O':
            retval = True
    return retval

def can_squeeze(grid,dot):
    row = dot[0]
    col = dot[1]
    logger.debug('can_squeeze(grid,%s,%s)', row, col)
    retval = []
    pipes = {
        '|': ['N','S'],
        '-': ['E','W'],
        'L': ['N','E'],
        'J': ['N','W'],
        '7': ['W','S'],
        'F': ['E','S']
    }
    neighbors = get_neighbor_coordinates(grid,row,col)
    """
    0 1 2
    3   4
    5 6 7
    """
    logger.debug('%s', neighbors)
    logger.debug('%s', grid[4][13])
    logger.debug(
        '%s',
        (
            grid[neighbors[0][0]][neighbors[0][1]],
            grid[neighbors[1][0]][neighbors[1][1]],
            grid[neighbors[2][0]][neighbors[2][1]],
        ),
    )
    logger.debug(
        '%s',
        (
            grid[neighbors[3][0]][neighbors[3][1]],
            grid[row][col],
            grid[neighbors[4][0]][neighbors[4][1]],
        ),
    )
    logger.debug(
        '%s',
        (
            grid[neighbors[5][0]][neighbors[5][1]],
            grid[neighbors[6][0]][neighbors[6][1]],
            grid[neighbors[7][0]][neighbors[7][1]],
        ),
    )
    
    pairs = [
        {'pos': [0,1], 'direction': 'E', 'egress': 'N'},
        {'pos': [1,2], 'direction': 'E', 'egress': 'N'},
        {'pos': [0,3], 'direction': 'S', 'egress': 'W'},
        {'pos': [2,4], 'direction': 'S', 'egress': 'E'},
        {'pos': [3,5], 'direction': 'S', 'egress': 'W'},
        {'pos': [4,7], 'direction': 'S', 'egress': 'E'},
        {'pos': [5,6], 'direction': 'E', 'egress': 'S'},
        {'pos': [6,7], 'direction': 'E', 'egress': 'S'},
    ]
    squeezes = []
    for pair in pairs:
        pos = pair['pos']
        direction = pair['direction']
        neighbor1 = neighbors[pos[0]]
        neighbor2 = neighbors[pos[1]]
        logger.debug(
            'can_squeeze: %s,%s',
            pair,
            ([grid[neighbor1[0]][neighbor1[1]]], grid[neighbor2[0]][neighbor2[1]]),
        )

        if grid[neighbor1[0]][neighbor1[1]] in pipes:
            if grid[neighbor2[0]][neighbor2[1]] in pipes:
                if not can_connect(grid[neighbor1[0]][neighbor1[1]],grid[neighbor2[0]][neighbor2[1]],direction):
                    logger.debug(
                        '(can_squeeze%s,%s) squeeze through %s[%s]/%s[%s]',
                        row,
                        col,
                        pos[0],
                        grid[neighbor1[0]][neighbor1[1]],
                        pos[1],
                        grid[neighbor2[0]][neighbor2[1]],
                    )
                    squeezes.append([[neighbor1[0],neighbor1[1]],[neighbor2[0],neighbor2[1]],pair['egress']])
    return squeezes

def get_loop(grid):
    loop = []
    start=find_start(grid)
    currPos = start
    neighbors = find_neighbors(currPos,grid)
    for direction in neighbors:
        if neighbors[direction] is not None:
            break
    loop.append(currPos.copy())
    currPos = move(currPos,direction)
    loop.append(currPos.copy())
    steps = 1;
    while parsed_data[currPos[0]][currPos[1]] != 'S':
        direction = next_direction(parsed_data[currPos[0]][currPos[1]],direction)
        currPos = move(currPos,direction)
        loop.append(currPos.copy())
        steps+=1
    return loop

def print_map(grid,label):
    pretty = {
        'S': 'S',
        '|': '|',
        '-': '-',
        'L': '└',
        'J': '┘',
        '7': '┐',
        'F': '┌'
    } 
    print(f'{label}:')
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] in pretty:
                print(pretty[grid[row][col]],end='')
            else:
                print(grid[row][col],end='')
        print()
    print()

def part2(parsed_data):
    global DEBUG
    DEBUG=False
    loop = get_loop(parsed_data)
    print_map(parsed_data,'Full Map')
    grid = parsed_data.copy()
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            set_point(grid,row,col,'.')
    for pos in loop:
        set_point(grid,pos[0],pos[1],parsed_data[pos[0]][pos[1]])
    print_map(grid,'Loop:')
    mark_outside(grid)
    print_map(grid,'Marked:') # 737
    dots = get_dots(grid)
    squeeze_dots = []
    for i in range(6):
        for dot in dots:
            if O_next_door(grid,dot):
                set_point(grid,dot[0],dot[1],'O')
            else:
                squeeze_dots = can_squeeze(grid,dot)
                logger.debug('Squeeze Dots: %s', squeeze_dots)
                for squeeze_dot in squeeze_dots:
                    logger.debug('Squeeze Dot: %s', squeeze_dot)
                    result = follow_squeeze(grid,squeeze_dot[0],squeeze_dot[1],squeeze_dot[2])
                    if result == 'O':
                        set_point(grid,dot[0],dot[1],'O')
                    logger.debug('squeeze2: %s, %s', squeeze_dot, result)
        dots = get_dots(grid)
    print_map(grid,'Squeezed:') # 473            
    fix_start(grid)
    #oddballs = [[31,72],[34,74]] 
    #print(oddballs)
    dots = get_dots(grid)
    squeeze_dots = []
    #for i in range(2):
    for dot in dots:
        if O_next_door(grid,dot):
                set_point(grid,dot[0],dot[1],'O')
        else:
            squeeze_dots = can_squeeze(grid,dot)
            logger.debug('Squeeze Dots: %s', squeeze_dots)
            for squeeze_dot in squeeze_dots:
                logger.debug('Squeeze Dot: %s', squeeze_dot)
                result = follow_squeeze(grid,squeeze_dot[0],squeeze_dot[1],squeeze_dot[2])
                if result == 'O':
                    set_point(grid,dot[0],dot[1],'O')
                logger.debug('squeeze2: %s, %s', squeeze_dot, result)
    print_map(grid,'Oddballs:') # 593            
    dots = get_dots(grid)
    return len(dots)

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        return part1(input_value)
    return part2(input_value)

YEAR = 2023
DAY = 10
input_format = {
    1: "lines",
    2: "lines",
}

funcs = {
    1: solve,
    2: solve,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    aoc = AdventOfCode(
        year=YEAR,
        day=DAY,
        input_formats=input_format,
        funcs=funcs,
        test_mode=args.test,
    )
    aoc.run(submit=args.submit)
