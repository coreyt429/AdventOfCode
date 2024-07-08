import sys
import re

def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')
    return lines

def part1(parsed_data):
    reHex=r'(\\x[0-9a-f]{2})'
    retval = 0;
    sum1 = 0
    sum2 = 0
    for line in parsed_data:
        size1 = len(line)
        line2 = line.replace('\\\\', '#')
        line2 = line2.replace(r'\"', '#')
        line2 = line2.replace('"','')
        sum1+=size1
        line2 = re.sub(reHex,'#',line2)
        whitespace_chars = " \t\n\r"  # Space, tab, newline, carriage return
        for char in whitespace_chars:
            line2 = line2.replace(char, "")
        size2 = len(line2)
        sum2 += size2
    retval = sum1 - sum2
    return retval

def part2(parsed_data):
    reHex=r'(\\x[0-9a-f]{2})'
    retval = 0;
    sum1 = 0
    sum2 = 0
    for line in parsed_data:
        size1 = len(line)
        line2 = line.replace('\\\\', '#')
        line2 = line2.replace('\"', '%')
        line2 = line2.replace('"','\\"')
        line2 = line2.replace('#','\\\\\\\\')
        line2 = line2.replace('%','"\\"')
        sum1+=size1
        line2 = re.sub(reHex,"\\\\\\\\xNN",line2)
        whitespace_chars = " \t\n\r"  # Space, tab, newline, carriage return
        for char in whitespace_chars:
            line2 = line2.replace(char, "")
        size2 = len(line2)
        sum2 += size2
    retval = sum2 - sum1
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
    