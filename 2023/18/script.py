import sys
import re
import math


def parse_input(data):
    retval = []
    # Split the data into lines
    lines = data.strip().split('\n')
    #R 6 (#70c710)
    pattern='([RDUL]) (\d+) \((#[a-f0-9]*)\)'
    for line in lines:
        matches=re.match(pattern,line)
        #print(f'{matches.group(1)} {matches.group(2)} {matches.group(3)}')
        retval.append({ 'direction': matches.group(1), 'meters': int(matches.group(2)), 'color': matches.group(3)})
    return retval

def print_map(myMap,label):
    print(f'{label}:')
    for line in myMap:
        print(''.join(line))
    print()

def dig_right(myMap,currPos,instruction):
    newcol=currPos[1]+instruction['meters']
    for col in range(currPos[1]+1,newcol+1):
        if col >= len(myMap[currPos[0]]): # expand rows
            for row in range(len(myMap)):
                if row == currPos[0]:
                    myMap[row].append('#')
                else:
                    myMap[row].append('.')
        else:
            #print(f'{col} <> {len(myMap[currPos[0]])}')
            myMap[currPos[0]][col] ='#'
    currPos[1] = newcol


def dig_down(myMap,currPos,instruction):
    newrow = currPos[0]+instruction['meters']
    for row in range(currPos[0]+1,newrow+1):
        if row >= len(myMap): # new row
            myMap.append(['.' for x in range(len(myMap[0]))])
        myMap[row][currPos[1]] = '#'
    currPos[0] = newrow

def dig_left(myMap,currPos,instruction):
    newcol = currPos[1]-instruction['meters']
    for col in range(currPos[1]-1,newcol-1,-1):
        if col < 0:
            for row in range(len(myMap)):
                if row == currPos[0]:
                    myMap[row].insert(0,'#')
                else:
                    myMap[row].insert(0,'.')
        else:
            myMap[currPos[0]][col] ='#'
    if newcol < 0:
        newcol=0
    currPos[1] = newcol

def dig_up(myMap,currPos,instruction):
    newrow = currPos[0]-instruction['meters']
    for row in range(currPos[0]-1,newrow-1,-1):
        if row <0: # insert a row if we dig too far up
            myMap.insert(0,['.' for x in range(len(myMap[0]))])
            myMap[0][currPos[1]] ='#'
        else:
            myMap[row][currPos[1]] ='#'
    if newrow < 0:
        newrow=0
    currPos[0] = newrow

def dig_outline(instructions):
    currPos=[0,0]
    myMap = [['#']]
    #{'direction': 'R', 'meters': 6, 'color': '#70c710'}
    for instruction  in instructions:
        if instruction['direction'] == 'R':
            dig_right(myMap,currPos,instruction)
        elif instruction['direction'] == 'D':
            dig_down(myMap,currPos,instruction)
        elif instruction['direction'] == 'L':
            dig_left(myMap,currPos,instruction)
        elif instruction['direction'] == 'U':
            dig_up(myMap,currPos,instruction)
    return myMap

def get_neighbor_coordinates(grid, row, col):
    neighbors = [
        (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
        (row, col - 1), (row, col + 1),
        (row + 1, col - 1), (row + 1, col), (row + 1, col + 1),
    ]
    valid_neighbors = []
    for r, c in neighbors:
        if 0 <= r < len(grid) and 0 <= c < len(grid[r]):
            valid_neighbors.append((r, c))
    return valid_neighbors

def mark_outside(grid):
    for i in range(len(grid)):
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == '.':
                    #print(f'Dot: {row},{col}')
                    if row == 0 or col == 0 or row == len(grid)-1 or col == len(grid[row])-1:
                        grid[row][col]='O'
                    else:
                        for neighbor in get_neighbor_coordinates(grid,row,col):
                            #print(f'Neighbor: {neighbor} = {grid[neighbor[0]][neighbor[1]]}')
                            if neighbor[0] is None or grid[neighbor[0]][neighbor[1]] == 'O':
                                grid[row][col]='O'

def fill_inside(grid):
    for i in range(len(grid)):
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == '.':
                    grid[row][col]='I'


def get_edge_points(instructions):
    currX=0
    currY=0
    points = [[currX,currY]]
    #{'direction': 'R', 'meters': 6, 'color': '#70c710'}
    
    for instruction  in instructions:
        if instruction['direction'] == 'R':
            currX+=instruction['meters']
        elif instruction['direction'] == 'D':
            currY-=instruction['meters']
        elif instruction['direction'] == 'L':
            currX-=instruction['meters']
        elif instruction['direction'] == 'U':
            currY+=instruction['meters']
        points.append([currX,currY])

    min_x = min([x for x, y in points])
    min_y = min(y for x, y in points)
    for point in points:
        point[0]+=abs(min_x)
        point[1]+=abs(min_y)
    return points

def calculate_perimeter(points):
    perimeter = 0
    n = len(points)
    for i in range(n):
        # Get the current point and the next point (with wrap-around)
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        # Calculate the distance between the points
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        # Add to the total perimeter
        perimeter += distance
    return perimeter

def polygon_area(points): # chatGPT
    n = len(points)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    area = abs(area) / 2.0
    return area

def picks(points):
    #a+1-b/2 = i
    a=polygon_area(points)
    b=calculate_perimeter(points)
    assert(b % 2 == 0)
    i=a+1-(b//2)
    return int(i+b)

def shoelace(points): # mine.  mine worked, but I forgot the abs().  chatGPT's was a bit cleaner
    retval=0
    x=0
    y=1
    for idx in range(len(points)):
        p1=points[idx]
        if idx < len(points)-1:
            p2=points[idx+1]
        else:
            p2=points[0]
        retval+=(p1[x]*p2[y])-(p1[y]*p2[x])
    retval = abs(retval)/2
    return retval


def part1(parsed_data):
    myMap = dig_outline(parsed_data)
    print_map(myMap,'Outline')
    mark_outside(myMap)
    print_map(myMap,'Outside')
    fill_inside(myMap)
    print_map(myMap,'Inside')
    retval = 0;
    for row in myMap:
        for col in row:
            if col in ['#','I']:
                retval+=1
    return retval

def part1b(parsed_data):
    retval = 0;
    edge_points = get_edge_points(parsed_data)
    area = shoelace(edge_points)
    retval = picks(edge_points)
    return retval

def part2(parsed_data):
    retval = 0;
    newinstructions = [];
    pattern = '#([a-f0-9]{5})([0-3])'
    directions = ['R','D','L','U']
    for instruction in parsed_data:
        matches = re.match(pattern,instruction['color'])
        newinstructions.append({ 'direction': directions[int(matches.group(2))], 'meters': int(matches.group(1),16)})
    edge_points = get_edge_points(newinstructions)
    #edge_points = get_edge_points(parsed_data)
    area = shoelace(edge_points)
    retval = picks(edge_points)
    return retval

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())
    #print(parsed_data)

    #print("Part 1")
    #answer1 = part1(parsed_data)
    answer1 = part1b(parsed_data)
    #print("Part 2")
    answer2 = part2(parsed_data)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    