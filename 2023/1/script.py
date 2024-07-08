import re
import sys

def calibrate(Lines):
    total = 0
    for line in Lines:
        digits = re.findall(r'\d', line)
        if len(digits) > 0:
            # If not empty, proceed with your operation
            digit = digits[0] + digits[-1]
        else:
            # Handle the case where the list is empty
            digit = 0
        total+=int(digit)
    return total

def part1(Lines):
    return calibrate(Lines)

def part2(Lines):
    strNums = ["zero","one","two","three","four","five", "six", "seven","eight","nine"]
    myLines = [];
    for line in Lines:
        for idx, numStr in enumerate(strNums):
            line = line.replace(numStr,numStr[0]+str(idx)+numStr[-1])
        myLines.append(line)
    return calibrate(myLines)


if __name__ == "__main__":
    # Using readlines()
    file1 = open(sys.argv[1], 'r')
    Lines = file1.readlines()
    answer1 = part1(Lines)
    answer2 = part2(Lines)
    print(f'Part 1: {answer1}')
    print(f'Part 2: {answer2}')
    
    exit();
    