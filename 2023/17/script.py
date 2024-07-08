import sys
from copy import deepcopy
from functools import cache
import heapq


# FAIL.  I've got to study this solution more.

def dijkstra(grid, start, end):
    print(f'dijkstra(grid, {start}, {end})')
    rows, cols = len(grid), len(grid[0])
    distances = [[float('inf')] * cols for _ in range(rows)]
    distances[start[0]][start[1]] = grid[start[0]][start[1]]

    # Priority queue: (cost, (x, y), [last three directions])
    queue = [(grid[start[0]][start[1]], start, [])]

    # Directions: up, down, left, right
    directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

    while queue:
        current_distance, current_position, direction_history = heapq.heappop(queue)
        x, y = current_position

        if current_position == end:
            break

        # Explore neighbors with direction constraint
        for dir, (dx, dy) in directions.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                # Check if the same direction is repeated more than 3 times
                #print(direction_history,dir,direction_history[-3:].count(dir))
                if direction_history[-3:].count(dir) < 3:
                    distance = current_distance + grid[nx][ny]
                    if distance < distances[nx][ny]:
                        distances[nx][ny] = distance
                        new_direction_history = direction_history[-2:] + [dir]  # Keep only last 3 directions
                        heapq.heappush(queue, (distance, (nx, ny), new_direction_history))
    print_map(distances,'dijkstra')
    return distances[end[0]][end[1]]


def parse_input(data):
    rows = []
    # Split the data into lines
    lines = data.strip().split('\n')
    for line in lines:
        rows.append(tuple(map(int, line)))
    return tuple(rows)

@cache
def get_neighbors(myMap,currPos): 
    neighbors = {}
    #print(currPos)
    if currPos[0] > 0: # Not at top
        neighbors['n'] = tuple([currPos[0]-1,currPos[1]])
    if currPos[0] < len(myMap)-1: # not at bottom
        neighbors['s'] = tuple([currPos[0]+1,currPos[1]])
    if currPos[1] < len(myMap[0])-1: # not at right
        neighbors['e'] = tuple([currPos[0],currPos[1]+1])
    if currPos[1] > 0: # not at left
        neighbors['w'] = tuple([currPos[0],currPos[1]-1])
    return neighbors

@cache
def get_cost(myMap,myPath):
    cost = 0
    for node in myPath:
        row, col = node
        cost += myMap[row][col]
    return cost

def detect_loop(sequence):
    seen = set()
    for idx in range(len(sequence) - 1):
        pair = (sequence[idx], sequence[idx + 1])
        if pair in seen:
            return True  # Loop detected
        seen.add(pair)
    return False  # No loop found

# FIXME:  too much recurstion, convert to iterative, queuing state objects
# FIXME: iterative is too much to process as well, we may have to learn dijkstra
def least_cost_path(myMap,currPos,destination):
    lowest_cost = None
    lowest_cost_path = tuple()
    cost=None
    myPath = []
    myPath.append(currPos)
    # (position,path,Qdirection)
    stack = []
    neighbors = get_neighbors(myMap,currPos)
    for direction in neighbors:
        newPath = deepcopy(myPath)
        newPath.append(neighbors[direction])
        Qdirection=tuple(['x','y',direction])
        stack.append(tuple(tuple([neighbors[direction],tuple(newPath),Qdirection])))

    while stack:
        currPos,myPath,Qdirection =stack.pop()
        #print(f'Queued: {len(stack)}, CurPos: {currPos},Path:{myPath},Direction:{Qdirection}')
        #if len(stack) > 100:
        #    exit()
        if currPos == destination:
            cost = get_cost(myMap,myPath)
            print(f'Reached destination: Cost: {cost}, Least: {lowest_cost}, Path:{myPath}')
            if lowest_cost is None or cost < lowest_cost:
                lowest_cost = get_cost(myMap,myPath)
                lowest_cost_path =myPath
        else:
            #print(f'Current Position: {currPos}')
            neighbors = get_neighbors(myMap,currPos)
            #print(f'Neighbors: {neighbors}')
            for direction in neighbors:
                #print(direction,neighbors[direction])
                if all(x == direction for x in Qdirection):
                    #print(f'The last three moves were {direction}, so we can not go that way')
                    continue
                if neighbors[direction] == myPath[-2]:
                    #print(f'We can\'t backtrack to  {neighbors[direction]}')
                    continue
                if detect_loop(myPath):
                    #print('Loop detected')
                    continue

                # fix mypath and qdirection
                newPath=list(myPath)
                newPath.append(neighbors[direction])
                newQdirection = list(Qdirection)
                newQdirection.pop(0)
                newQdirection.append(direction)
                if lowest_cost is not None:
                    cost = get_cost(myMap,tuple(newPath))
                    if cost > lowest_cost: # we don't care about the rest of this path:
                        #print(f'Abandoning expensive path: {newPath}')
                        continue
                stack.append(tuple([tuple(neighbors[direction]),tuple(newPath),tuple(newQdirection)]))
    return lowest_cost, lowest_cost_path

def print_map(myMap,label):
    print(f'{label}:')
    for line in myMap:
        print(' '.join(str(number) for number in line))
    print()

@cache
def init_myPath(myMap):
    global myPath
    myPath = []
    for row in range(len(myMap)):
        myPath.append([])
        for col in  range(len(myMap[row])):
            myPath[row].append(myMap[row][col])

myPath = []

def part1(parsed_data):
    global myPath
    myMap = deepcopy(parsed_data)
    #cost,path = least_cost_path(myMap,tuple([0,0]),tuple([len(myMap)-1,len(myMap[0])-1]))
    # Start and end positions
    start = (0, 0)
    end = (len(myMap)-1, len(myMap[0])-1)

    # Calculate the shortest path
    shortest_path_cost = dijkstra(myMap, start, end)
    print(shortest_path_cost)
    retval = 0;
    return retval

def part2(parsed_data):
    retval = 0;
    return retval

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())
    #print(parsed_data)

    #print("Part 1")
    answer1 = part1(parsed_data)
    
    #print("Part 2")
    answer2 = part2(parsed_data)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    