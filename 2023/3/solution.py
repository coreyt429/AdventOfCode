"""
Advent Of Code 2023 day 3

"""
# import system modules
import time
import re

# import my modules
import aoc # pylint: disable=import-error

def parse_parts(lines):
    """
    Parse input
    """
    numbers = []
    for idx,line in enumerate(lines):
        #print(idx,line)
        for match in re.finditer(r'\d+', line):
            #print(match)
            numbers.append({
                'line': idx, 'number':int(match.group()), 'start': match.start(), 'end': match.end()
            })

    symbols = []
    for idx,line in enumerate(lines):
        #print(idx,line)
        for match in re.finditer(r'[^\d\.]', line.strip()):
            #print(match)
            symbols.append({
                'line': idx, 'symbol': match.group(), 'start': match.start(), 'end': match.end()
                })
    #print(symbols)
    return [numbers,symbols]

def part1(numbers,symbols):
    """
    solve part 1
    """
    result = 0
    for num in numbers:
        partnum = 0
        for sym in symbols:
            #if(sym['line'] == 138):
                #print(sym)
            if sym['line'] == num['line'] - 1 or sym['line'] == num['line'] + 1: # line before
                # look for sym start/end to be num start/end+/-1
                if num['start'] - 1 <= sym['start'] and num['end'] + 1 >= sym['end']:
                    partnum=1
            elif sym['line'] == num['line']:
                # look for sym start/end to be num start-1 or num end +1
                if num['start'] -1  == sym['start'] or num['end'] + 1 == sym['end']:
                    partnum = 1
        if partnum:
            result += num['number']
    return result

def part2(numbers, symbols):
    """
    solve part 2
    """
    result = 0
    for sym in symbols:
        count = 0
        gearratio = 1 # sum of gear part numbers
        if sym['symbol'] == '*':
            for num in numbers:
                if sym['line'] == num['line'] - 1 or sym['line'] == num['line'] + 1: # line before
                    # look for sym start/end to be num start/end+/-1
                    if num['start'] - 1 <= sym['start'] and num['end'] + 1 >= sym['end']:
                        count += 1
                        gearratio *= num['number']
                elif sym['line'] == num['line']:
                    # look for sym start/end to be num start-1 or num end +1
                    if num['start'] - 1 == sym['start'] or num['end'] + 1 == sym['end']:
                        count += 1
                        gearratio *= num['number']
            if count == 2:
                result += gearratio
    return result

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    [numbers, symbols] = parse_parts(input_value)
    if part == 2:
        return part2(numbers, symbols)
    return part1(numbers, symbols)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2023,3)
    #input_text = my_aoc.load_text()
    #print(input_text)
    input_lines = my_aoc.load_lines()
    #print(input_lines)
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
        1: solve,
        2: solve
    }
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
