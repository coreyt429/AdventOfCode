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
    print(idx,line)
    for match in re.finditer(r'\d+', line):
        print(match)
        numbers.append({'line': idx,'number':int(match.group()),'start': match.start(), 'end': match.end() })

symbols = []
for idx,line in enumerate(Lines):
    print(idx,line)
    for match in re.finditer(r'[^\d\.]', line.strip()):
        print(match)
        symbols.append({'line': idx,'symbol': match.group(), 'start': match.start(), 'end': match.end() })
print(symbols)
answer=0
for num in numbers:
    partnum=0;
    print(num);
    for sym in symbols:
        if(sym['line'] == 138):
            print(sym)
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
    print(num['number'],partnum)
print(answer)
