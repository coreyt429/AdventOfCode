import sys
import re

def look_and_say(strNum):
    retval = '';
    last=''
    count=0
    for char in strNum:
        if last == '':
            last=char
            count=1
        elif last != char:
            retval+=str(count)+last
            last = char
            count=1
        else:
            count+=1
    retval+=str(count)+last
    return retval


def part1():
    retval = '1113222113';
    for idx in range(40):
        retval = look_and_say(retval)
    return len(retval)

def part2():
    retval = '1113222113';
    for idx in range(50):
        retval = look_and_say(retval)
    return len(retval)

if __name__ == "__main__":
    #with open(sys.argv[1] , "r") as f:
    #    parsed_data = parse_input(f.read())
    #print(parsed_data)

    #print("Part 1")
    answer1 = part1()
    
    #print("Part 2")
    answer2 = part2()

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    