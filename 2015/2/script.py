import sys

def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')

    # Split each line by whitespace and remove the first element (the label)
    presents = []
    for line in lines:
        presents.append(line.split('x'))
    for present in presents:
        for i in range(0,len(present)):
            present[i] = int(present[i])
    return presents

def area_plus_side(p):
    p.sort()
    sides = []
    sides.append(2*p[0]*p[1]) # l*w*2
    sides.append(2*p[1]*p[2]) # w*h*2
    sides.append(2*p[0]*p[2]) # l*h*2
    sides.append(p[0]*p[1]) # area of smallest side
    return sum(sides)

def ribbon(p):
    p.sort()
    #print(f'ribbon = 2*{p[0]}+2*{p[1]}+{p[0]}*{p[1]}*{p[2]}')
    ribbon = 2*p[0]+2*p[1]+p[0]*p[1]*p[2]
    return ribbon


def part1(parsed_data):
    retval = 0
    for present in parsed_data:
        retval+=area_plus_side(present);
    return retval

"""
A present with dimensions 2x3x4 requires 2+2+3+3 = 10 feet of ribbon to wrap the present 
plus 2*3*4 = 24 feet of ribbon for the bow, 
for a total of 34 feet.
"""
def part2(parsed_data):
    retval = 0;
    for present in parsed_data:
        retval+=ribbon(present);
    return retval

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())
    #print(parsed_data1)
    #print(parsed_data)
    #print("Part 1")
    answer1 = part1(parsed_data)
    
    #print("Part 2")
    answer2 = part2(parsed_data)

    print(f"Part1: {int(answer1)}")
    print(f"Part2: {answer2}")
    