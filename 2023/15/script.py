import sys
import re

def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')
    codes = []
    for line in lines:
        for code in line.split(','):
            codes.append(code)
    
    return tuple(codes)

def myHash(mystring):
    retval = 0
    for char in mystring:
        #Determine the ASCII code for the current character of the string.
        #Increase the current value by the ASCII code you just determined.
        retval+=ord(char)
        #Set the current value to itself multiplied by 17.
        retval*=17
        #Set the current value to the remainder of dividing itself by 256.
        retval = retval % 256
    return retval

def part1(parsed_data):
    retval = 0;
    for code in parsed_data:
        retval+=myHash(code)
    return retval

def part2(parsed_data):
    retval = 0;
    boxes = [[] for _ in range(256)]
    patCode = '([a-z]+)([=-])(\d*)'
    for code in parsed_data:
        matches = re.findall(patCode, code)
        for match in matches:
            label, op, fl = match
            codehash=myHash(label)
            #print(label,codehash)
            box = boxes[codehash]
            if op == '=':
                replaced=False
                newbox = []
                for item in box:
                    if not item[0] == label:
                        newbox.append(item)
                    else:
                        newbox.append([label,int(fl)])
                        replaced = True
                if not replaced:
                    newbox.append([label,int(fl)])
                boxes[codehash] = newbox
            elif op == '-':
                box = [item for item in box if not item[0] == label]
                boxes[codehash] = box

    for idx in range(len(boxes)):
        for idx2 in range(len(boxes[idx])):
            #One plus the box number of the lens in question.
            power = idx+1
            #The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
            power*= idx2+1
            #The focal length of the lens.
            power*= boxes[idx][idx2][1]
            retval += power
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
    