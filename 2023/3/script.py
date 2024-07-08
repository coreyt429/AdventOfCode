import re
import sys

def parse_parts(Lines):
    numbers = []
    for idx,line in enumerate(Lines):
        #print(idx,line)
        for match in re.finditer(r'\d+', line):
            #print(match)
            numbers.append({'line': idx,'number':int(match.group()),'start': match.start(), 'end': match.end() })

    symbols = []
    for idx,line in enumerate(Lines):
        #print(idx,line)
        for match in re.finditer(r'[^\d\.]', line.strip()):
            #print(match)
            symbols.append({'line': idx,'symbol': match.group(), 'start': match.start(), 'end': match.end() })
    #print(symbols)
    return [numbers,symbols]

def part1(numbers,symbols):
    answer=0
    for num in numbers:
        partnum=0;
        for sym in symbols:
            #if(sym['line'] == 138):
                #print(sym)
            if sym['line'] == num['line']-1 or sym['line'] == num['line']+1: # line before
                # look for sym start/end to be num start/end+/-1
                if num['start']-1 <= sym['start'] and num['end']+1 >= sym['end']:
                    partnum=1
            elif sym['line'] == num['line']:
                # look for sym start/end to be num start-1 or num end +1
                if num['start']-1 == sym['start'] or num['end']+1 == sym['end']:
                    partnum=1
        if partnum:
            answer+=num['number']
    return answer

def part2(numbers,symbols):
    answer=0
    for sym in symbols:
        isgear=0 
        count=0
        gearratio=1 # sum of gear part numbers
        if sym['symbol'] == '*':
            for num in numbers:
                if sym['line'] == num['line']-1 or sym['line'] == num['line']+1: # line before
                    # look for sym start/end to be num start/end+/-1
                    if num['start']-1 <= sym['start'] and num['end']+1 >= sym['end']:
                        count+=1
                        gearratio*=num['number']
                elif sym['line'] == num['line']:
                    # look for sym start/end to be num start-1 or num end +1
                    if num['start']-1 == sym['start'] or num['end']+1 == sym['end']:
                        count+=1
                        gearratio*=num['number']
            if count == 2:
                isgear=1
                answer+=gearratio
    return answer

if __name__ == "__main__":
    # Using readlines()
    file1 = open(sys.argv[1], 'r')
    Lines = file1.readlines()
    [numbers,symbols] = parse_parts(Lines)
    answer1 = part1(numbers,symbols)
    answer2 = part2(numbers,symbols)
    print(f'Part 1: {answer1}')
    print(f'Part 2: {answer2}')
    
    exit();
    