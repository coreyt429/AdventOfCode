import sys
import copy

def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')
    char_lists = [list(line) for line in lines]
    return char_lists

def print_map(data,label):
    print(label)
    max_row = max(pair[0] for pair in data)+1
    max_col = max(pair[1] for pair in data)+1
    for row in range(max_row):
        for col in range(max_col):
            found = False
            for galaxy in data:
                if galaxy[0] == row and galaxy[1] == col:
                    found=True
            if found:
                print('#', end = '')
            else:
                print('.', end = '')
        print()

def get_galaxies(map):
    galaxies = []
    # find galaxies
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == '#':
                galaxies.append([row,col])
    return galaxies

def expand_universe(galaxies,factor=2):
    factor-=1
    max_row = max(pair[0] for pair in galaxies)+1
    max_col = max(pair[1] for pair in galaxies)+1
    expand_rows = []
    expand_cols = []
    for row in range(max_row):
        has_galaxy=False
        for galaxy in galaxies:
            if galaxy[0] == row:
                has_galaxy=True
        if not has_galaxy:
            expand_rows.append(row)
    for col in range(max_col):
        has_galaxy=False
        for galaxy in galaxies:
            if galaxy[1] == col:
                has_galaxy=True
        if not has_galaxy:
            expand_cols.append(col)
    expand_rows.sort(reverse=True)
    expand_cols.sort(reverse=True)
    for row in expand_rows:
        for galaxy in galaxies:
            if galaxy[0] > row:
                galaxy[0]+=factor
    for col in expand_cols:
        for galaxy in galaxies:
            if galaxy[1] > col:
                galaxy[1]+=factor
    return galaxies

def distance(map,g1,g2):
    #print(f'Distance from {map[g1]} to {map[g2]}')
    rows = abs(map[g1][0] - map[g2][0])
    #print(f'Rows {rows}')
    cols = abs(map[g1][1] - map[g2][1])
    #print(f'Cols {cols}')
    distance = rows + cols
    #print(f'Distance {distance}')
    return distance


def part1(map):
    retval = 0;
    galaxies = expand_universe(copy.deepcopy(map))
    print_map(galaxies,'Part1:')
    
    
    #print(f'{len(galaxies)} Galaxies')
    for g1 in range(len(galaxies)):
        for g2 in range(g1+1,len(galaxies)):
            #print(f'{g1} - {g2}')
            dist = distance(galaxies,g1,g2)
            retval+=dist
    return retval

def part2(map):
    retval = 0;
    galaxies = expand_universe(copy.deepcopy(map),1000000)
    #print_map(galaxies,'Part2:')
    
    
    #print(f'{len(galaxies)} Galaxies')
    for g1 in range(len(galaxies)):
        for g2 in range(g1+1,len(galaxies)):
            dist = distance(galaxies,g1,g2)
            #print(f'{g1} - {g2} = {dist}')
            retval+=dist
    return retval

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())
    mapStart = get_galaxies(parsed_data)
    print_map(mapStart,'Start:')
    
    #print("Part 1")
    answer1 = part1(mapStart)
    
    #print("Part 2")
    answer2 = part2(mapStart)
    
    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    