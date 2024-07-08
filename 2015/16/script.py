import sys
import re

#Sue 1: goldfish: 9, cars: 0, samoyeds: 9
def parse_input(data):
    retval = {}
    lines = data.strip().split('\n')

    for line in lines:
        key, properties_str = line.split(': ', 1)
        properties = {}
        for prop in properties_str.split(', '):
            prop_name, prop_value = prop.split(': ')
            properties[prop_name] = int(prop_value)  
        retval[key]=properties
    return retval

#children: 3
def parse_input2(data):
    retval = {}
    # Split the data into lines
    lines = data.strip().split('\n')
    for line in lines:
        key, val = line.split(': ')
        retval[key]=int(val)
    return retval

def part1(parsed_data,ticker_tape):
    retval = 0;
    matches={}
    for sue in parsed_data:
        for key in ticker_tape:
            if key in parsed_data[sue].keys():
                #print(parsed_data[sue][key],ticker_tape[key])
                if parsed_data[sue][key] == ticker_tape[key]:
                    if sue not in matches:
                        matches[sue]=1
                    else:
                        matches[sue]+=1
    # Find the key with the largest value
    key_with_largest_value = max(matches, key=matches.get)
    # The largest value can be accessed using the key
    largest_value = matches[key_with_largest_value]
    #print(f"The largest value is {largest_value} and its key is '{key_with_largest_value}'.")
    return key_with_largest_value

def part2(parsed_data,ticker_tape):
    retval = 0;
    matches={}
    for sue in parsed_data:
        for key in ticker_tape:
            if key in parsed_data[sue].keys():
                #print(parsed_data[sue][key],ticker_tape[key])
                if key in ['cats','trees']:
                    if parsed_data[sue][key] > ticker_tape[key]:
                        if sue not in matches:
                            matches[sue]=1
                        else:
                            matches[sue]+=1
                elif key in ['pomeranians','goldfish']:
                    if parsed_data[sue][key] < ticker_tape[key]:
                        if sue not in matches:
                            matches[sue]=1
                        else:
                            matches[sue]+=1
                elif parsed_data[sue][key] == ticker_tape[key]:
                    if sue not in matches:
                        matches[sue]=1
                    else:
                        matches[sue]+=1
    # Find the key with the largest value
    key_with_largest_value = max(matches, key=matches.get)
    # The largest value can be accessed using the key
    largest_value = matches[key_with_largest_value]
    #print(f"The largest value is {largest_value} and its key is '{key_with_largest_value}'.")
    return key_with_largest_value

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())
    #print(parsed_data)
    with open(sys.argv[2] , "r") as f:
        ticker_tape = parse_input2(f.read())
    #print(ticker_tape)
    #print("Part 1")
    answer1 = part1(parsed_data,ticker_tape)
    
    #print("Part 2")
    answer2 = part2(parsed_data,ticker_tape)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    