import sys
import re

def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')
    routes = []
    for line in lines:
        tmp = line.split(' ')
        route = {
            'start': tmp[0],
            'end': tmp[2],
            'distance': int(tmp[4]),
        } 
        routes.append(route)
    return routes

def goto(map,routes,locations,currentLoc,already):
    #print(f'map,locations,{currentLoc},{already}')
    visited = already + (currentLoc,)
    for nextLoc in locations:
        if nextLoc not in visited:
            goto(parsed_data,routes,locations,nextLoc,visited)
    all_visited = True
    for currentLoc in locations:
        if currentLoc not in visited:
            all_visited = False
    if all_visited:
        distance = 0
        routes.append(list(visited))

def get_distance(mapdata,start,end):
    retval = -1;
    for entry in mapdata:
        if entry['start'] == start and entry['end'] == end:
            retval = entry['distance']
        elif entry['start'] == end and entry['end'] == start:
            retval = entry['distance']
    return retval

def part1(parsed_data):
    retval = -1;

    locations = set();
    routes = []
    for route in parsed_data:
        locations.add(route['start'])
        locations.add(route['end'])
    #print(locations)
    routes
    for start in locations:
        goto(parsed_data,routes,locations,start,())
    for route in routes:
        distance=0
        for idx in range(len(route)-1):
            distance+=get_distance(parsed_data,route[idx],route[idx+1])
        if retval < 0 and distance > 0:
            retval = distance
        elif distance < retval:
            retval = distance
        print(route,distance)
    return retval

def part2(parsed_data):
    retval = -1;

    locations = set();
    routes = []
    for route in parsed_data:
        locations.add(route['start'])
        locations.add(route['end'])
    #print(locations)
    routes
    for start in locations:
        goto(parsed_data,routes,locations,start,())
    for route in routes:
        distance=0
        for idx in range(len(route)-1):
            distance+=get_distance(parsed_data,route[idx],route[idx+1])
        if distance > retval:
            retval = distance
        print(route,distance)
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
    