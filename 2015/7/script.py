import sys
import re
"""
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""

def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')
    # define regex patterns, tested against sample data already
    rePatterns = {
        'init' : re.compile(r'^(\d+) -> ([a-z]+)'),
        'not'  : re.compile(r'(NOT) (.+) -> ([a-z]+)'),
        'andor': re.compile(r'(.+) (AND|OR) ([a-z]+) -> ([a-z]+)'),
        'shift': re.compile(r'([a-z]+) (.SHIFT) (\d+) -> ([a-z]+)'),
        'copy' : re.compile(r'^([a-z]+) -> ([a-z]+)'),
    }
    circuit = {}
    # loop through lines
    for line in lines:
        cmdType = None
        groups = []
        cmd = {}
        found = False
        for pattern in rePatterns.keys():
            if 'c' in line:
                print(pattern)
            match = rePatterns[pattern].search(line)
            if match:
                if 'c' in line:
                    print(f'  Matched: {line}')
                    print(match)
                found = True
                cmd['type'] = pattern
                if pattern == 'init':
                    cmd['value'] = int(match.groups(1)[0])
                    cmd['target'] = match.groups(1)[1]
                elif pattern == 'andor':
                    cmd['L'] = match.groups(1)[0]
                    cmd['operator'] = match.groups(1)[1]
                    cmd['R'] = match.groups(1)[2]
                    cmd['target'] = match.groups(1)[3]
                    if 'c' in line:
                        print(cmd)
                    
                elif pattern == 'shift':
                    cmd['L'] = match.groups(1)[0]
                    cmd['operator'] = match.groups(1)[1]
                    cmd['bits'] = int(match.groups(1)[2])
                    cmd['target'] = match.groups(1)[3]
                elif pattern == 'not':
                    cmd['operator'] = match.groups(1)[0]
                    cmd['L'] = match.groups(1)[1]
                    cmd['target'] = match.groups(1)[2]
                elif pattern == 'copy':
                    cmd['source'] = match.groups(1)[0]
                    cmd['target'] = match.groups(1)[1]
        if not found:
            print(f'unmatched line: {line}')
        if 'c' in line:
            print(f'{cmd["target"]} {cmd}')
        if len(cmd) > 0:
            circuit[cmd['target']]=cmd
    return circuit

def print_circuit(circuit):
    for wire in sorted(circuit.keys()):
        print(f'{wire}: {circuit[wire]}')
    print()

def wire_trace(target,wires,circuit):
    print(f'wire_trace({target},{wires},)')
    print(circuit['c'])
    cmd = circuit[target]
    if cmd['type'] == 'init':
        wires[cmd['target']] = cmd['value']
    elif cmd['type'] == 'andor':
        if not (cmd['L'] in wires):
            wire_trace(cmd['L'],wires,circuit)
        if not (cmd['R'] in wires):
            wire_trace(cmd['R'],wires,circuit)
        if cmd['operator'] == 'AND':
            wires[cmd['target']] = wires[cmd['L']] & wires[cmd['R']]
        else:
            wires[cmd['target']] = wires[cmd['L']] | wires[cmd['R']]
    elif cmd['type'] == 'not':
        if not (cmd['L'] in wires):
            wire_trace(cmd['L'],wires,circuit)
        # Bitmask for 8-bit
        bitmask = 0xFFFF
        wires[cmd['target']] = (~wires[cmd['L']] ) & bitmask
    elif cmd['type'] == 'copy':
        if not (cmd['source'] in wires):
            wire_trace(cmd['source'],wires,circuit)
        wires[cmd['target']] = wires[cmd['source']]
    else:
        if not (cmd['L'] in wires):
            wire_trace(cmd['L'],wires,circuit)
        if cmd['operator'] == 'RSHIFT':
            wires[cmd['target']] = wires[cmd['L']] >> cmd['bits']
        elif cmd['operator'] == 'LSHIFT':
            wires[cmd['target']] = wires[cmd['L']] << cmd['bits']
        else:
            print(cmd)
            print("This shouldn't happen")
            exit()
    #print(f'Target {target}')
    #print(cmd)
    #print(wires)
    return wires[target]

def part1(parsed_data):
    wires = {'1': 1} # hard wire this to handle "1 AND" entries
    wire_trace('a',wires,parsed_data)
    print_circuit(wires)
    return wires['a']

def part2(parsed_data):
    wires = {
        '1': 1, # hard wire this to handle "1 AND" entries
        'b': 956 # hard wire b to match part1 a
    }
    wire_trace('a',wires,parsed_data)
    print_circuit(wires)
    return wires['a']

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
    