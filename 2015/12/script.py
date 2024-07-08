import sys
import re
from json import loads

def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')
    return lines

def part1(parsed_data):
    retval = 0;
    pattern = r'-*\d+'
    for line in parsed_data:
        for num in re.findall(pattern,line):
            retval+=int(num)
    return retval

# I stole this, but it makes sense.  
# My first thought was to use json.loads, 
# but then I assumed the data file would make this take too long
def n(j):
    if type(j) == int:
        return j
    if type(j) == list:
        return sum([n(j) for j in j])
    if type(j) != dict:
        return 0
    if 'red' in j.values():
        return 0
    return n(list(j.values()))

def part2(parsed_data):
    retval = n(loads(open(sys.argv[1], 'r').read()));
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
    