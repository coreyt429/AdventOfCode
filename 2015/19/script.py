import sys
import re

def parse_input(data):
    # Split the data into lines
    replacements = {}
    chart,start = data.strip().split('\n\n')
    for line in chart.split('\n'):
        src,dst = line.split(' => ')
        if not src in replacements:
            replacements[src] = []
        replacements[src].append(dst)
    return start,replacements

compounds = set()

def calibrate(strCurrent,replacements,depth):
    global compounds
    depth-=1
    for idx in range(len(strCurrent)):
        if strCurrent[idx] in replacements:
            for mod in replacements[strCurrent[idx]]:
                strNew = strCurrent[:idx]+mod+strCurrent[idx+1:]
                #print(strNew)
                compounds.add(strNew)
                if(depth > 0):
                    calibrate(strNew,replacements,depth)
        elif strCurrent[idx:idx+2] in replacements:
            for mod in replacements[strCurrent[idx:idx+2]]:
                strNew = strCurrent[:idx]+mod+strCurrent[idx+2:]
                #print(strNew)
                compounds.add(strNew)
                if(depth > 0):
                    calibrate(strNew,replacements,depth)

step_counts=set()
# this brute force method would take forever, 
def build_molecule(strCurrent,replacements,step,target):
    print(f'build_molecule({strCurrent},replacements,{step},{target})')
    global step_counts
    step+=1
    if strCurrent == target:
        print(f'Found one at {step}')
        step_counts.add(step)
    if len(strCurrent) >= len(target): # we missed the mark
        return None
    for idx in range(len(strCurrent)):
        if strCurrent[idx] in replacements:
            for mod in replacements[strCurrent[idx]]:
                strNew = strCurrent[:idx]+mod+strCurrent[idx+1:]
                build_molecule(strNew,replacements,step,target)
        elif strCurrent[idx:idx+2] in replacements:
            for mod in replacements[strCurrent[idx:idx+2]]:
                strNew = strCurrent[:idx]+mod+strCurrent[idx+2:]
                build_molecule(strNew,replacements,step,target)

def reverse_rules(replacements):
    rules = {}
    for key in replacements:
        for value in replacements[key]:
            rules.setdefault(value, []).append(key)
    return rules

from collections import deque

def bfs(start, end, rules):
    #print(f'bfs({start}, {end}, rules)')
    queue = deque([(start, 0)])  # Start with the initial string and step count 0
    visited = set()  # To keep track of visited strings

    while queue:
        current, steps = queue.popleft()
        if current == end:
            return steps

        for key, values in rules.items():
            idx = current.find(key)
            while idx != -1:
                for value in values:
                    next_str = current[:idx] + value + current[idx + len(key):]
                    if next_str not in visited:
                        visited.add(next_str)
                        queue.append((next_str, steps + 1))
                idx = current.find(key, idx + 1)

    return None  # No transformation found

def part1(start,replacements,target):
    retval = 0;
    global compounds
    calibrate(start,replacements,target)
    #print(compounds)
    return len(compounds)

def part2(start,replacements,target):
    retval = 0;
    #build_molecule('e',replacements,0,start)
    rules = reverse_rules(replacements)
    result = bfs(start, 'e', rules)
    print(f"Minimum number of steps: {result}")
    print(rules)
    return retval

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        start,replacements = parse_input(f.read())
    #print(start,replacements)
    target=int(sys.argv[2])
    #print("Part 1")
    answer1 = part1(start,replacements,target)
    
    #print("Part 2")
    answer2 = part2(start,replacements,target)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    