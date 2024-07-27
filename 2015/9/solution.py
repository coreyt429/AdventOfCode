"""
Advent Of Code 2015 day 9

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def parse_input(lines):
    """
    Function to parse line data
    """
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

def goto(parsed_data,routes,locations,current_loc,already):
    """
    Recursive function to map route
    """
    #print(f'map,locations,{current_loc},{already}')
    visited = already + (current_loc,)
    for next_loc in locations:
        if next_loc not in visited:
            goto(parsed_data,routes,locations,next_loc,visited)
    all_visited = True
    for location in locations:
        if location not in visited:
            all_visited = False
    if all_visited:
        routes.append(list(visited))

def get_distance(mapdata,start,end):
    """
    Function to get calcultate distance
    """
    retval = -1
    for entry in mapdata:
        if entry['start'] == start and entry['end'] == end:
            retval = entry['distance']
        elif entry['start'] == end and entry['end'] == start:
            retval = entry['distance']
    return retval

def part1(parsed_data):
    """
    Function to solve part 1
    """
    retval = -1

    locations = set()
    routes = []
    for route in parsed_data:
        locations.add(route['start'])
        locations.add(route['end'])
    #print(locations)
    for start in locations:
        goto(parsed_data,routes,locations,start,())
    for route in routes:
        distance=0
        for idx in range(len(route)-1):
            distance+=get_distance(parsed_data,route[idx],route[idx+1])
        if retval < 0 < distance:
            retval = distance
        elif distance < retval:
            retval = distance
        #print(route,distance)
    return retval

def part2(parsed_data):
    """
    Function to solve part 2
    """
    retval = -1

    locations = set()
    routes = []
    for route in parsed_data:
        locations.add(route['start'])
        locations.add(route['end'])
    #print(locations)
    for start in locations:
        goto(parsed_data,routes,locations,start,())
    for route in routes:
        distance=0
        for idx in range(len(route)-1):
            distance+=get_distance(parsed_data,route[idx],route[idx+1])
        if distance > retval:
            retval = distance
        #print(route,distance)
    return retval

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015,9)
    #input_text = my_aoc.load_text()
    #print(input_text)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {
        1: 1,
        2: 2
    }
    # dict to store answers
    answer = {
        1: None,
        2: None
    }
    # dict to map functions
    funcs = {
        1: part1,
        2: part2
    }
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](parse_input(input_lines))
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
