import sys
import re

def parse_input(data):
    # Split the data into lines
    retval = []
    lines = data.strip().split('\n')
    # loop through lines
    for line in lines:
        intDataList = []
        for strData in line.split():
            intDataList.append(int(strData))
        retval.append(intDataList)
    return retval

def prev_value(Datalist):
    #print(f'nextVal({Datalist})')
    myData = Datalist.copy()
    newData = []
    for i in range(0,len(myData)-1):
        newData.append(myData[i+1]-myData[i])
    allzeros = True
    for i in newData:
        if i != 0:
            allzeros = False
    if not allzeros:
        newData.insert(0,prev_value(newData))
    return myData[0] - newData[0]

def next_value(Datalist):
    #print(f'nextVal({Datalist})')
    myData = Datalist.copy()
    newData = []
    for i in range(0,len(myData)-1):
        newData.append(myData[i+1]-myData[i])
    allzeros = True
    for i in newData:
        if i != 0:
            allzeros = False
    if not allzeros:
        newData.append(next_value(newData))
    return myData[-1] + newData[-1]


def part1(parsed_data):
    retval = 0;
    for intDataList in parsed_data:
        #print(intDataList)
        nextVal = next_value(intDataList)
        retval+=nextVal
        #print(nextVal)
        #break # just process the first one until we are ready
    return retval

def part2(parsed_data):
    retval = 0;
    for intDataList in parsed_data:
        nextVal = prev_value(intDataList)
        retval+=nextVal
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
    