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

def part1(parsed_data):
    retval = 0;
    return retval

def part2(parsed_data):
    retval = 0;
    return retval

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())
    #print(parsed_data1)

    #print("Part 1")
    answer1 = part1(parsed_data)
    
    #print("Part 2")
    answer2 = part2(parsed_data)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    