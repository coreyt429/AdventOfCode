import re

# Using readlines()
file1 = open('input.txt', 'r')
Lines = file1.readlines()

"""
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
numbers = []
for idx,line in enumerate(Lines):
    for match in re.finditer(r'\d+', line):
        numbers.append({'line': idx,'number':int(match.group()),'start': match.start(), 'end': match.end() })

symbols = []
for idx,line in enumerate(Lines):
    for match in re.finditer(r'[^\d\.]', line.strip()):
        symbols.append({'line': idx,'symbol': match.group(), 'start': match.start(), 'end': match.end() })
answer=0

for sym in symbols:
    isgear=0 
    count=0
    gearratio=1 # sum of gear part numbers
    if sym['symbol'] == '*':
        print(sym)
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
            print(count,gearratio)
            isgear=1
            answer+=gearratio

print(answer)
