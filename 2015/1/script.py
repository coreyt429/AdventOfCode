import sys

def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')

    # Split each line by whitespace and remove the first element (the label)
    time_values = [int(value) for value in lines[0].split()[1:]]
    distance_values = [int(value) for value in lines[1].split()[1:]]

    # Combine the time and distance values into a list of tuples
    time_distance_pairs = list(zip(time_values, distance_values))
    return time_distance_pairs
#0 0 3 3 3 -1 -1 -3
def part1(data):
    retval = 0
    for char in data:
        if char == '(':
            retval+=1
        elif char == ')':
            retval-=1
    return retval

def part2(data):
    retval=0
    floor=0
    for i in range(0,len(data)):
        char=data[i]
        if char == '(':
            floor+=1
        elif char == ')':
            floor-=1
        if floor == -1:
            retval=i+1
            break
    return retval

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        data = f.read()
    
    answer1 = part1(data)
    
    #print("Part 2")
    answer2 = part2(data)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    