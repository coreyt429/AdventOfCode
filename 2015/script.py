import sys
import re

def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')
    # define regex patterns, tested against sample data already
    rePatterns = {
        'init' : re.compile(r'^(\d+) -> (.+)'),
        'not'  : re.compile(r'(NOT) (.+) -> (.+)'),
        'andor': re.compile(r'(.+) (AND|OR) (.+) -> (.+)'),
        'shift': re.compile(r'(.+) (.SHIFT) (\d+) -> (.+)'),
    }
    circuit = []
    # loop through lines
    for line in lines:
    return circuit

def part1(parsed_data):
    retval = 0;
    return retval

def part2(parsed_data):
    retval = 0;
    return retval

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())
    print(parsed_data)

    #print("Part 1")
    answer1 = part1(parsed_data)
    
    #print("Part 2")
    answer2 = part2(parsed_data)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    