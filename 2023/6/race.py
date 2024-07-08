import sys

def parse_input2(data):
    # Split the data into lines
    lines = data.strip().replace(' ','').split('\n')

    # Split each line by whitespace and remove the first element (the label)
    time_values = [int(value) for value in lines[0].split(':')[1:]]
    distance_values = [int(value) for value in lines[1].split(':')[1:]]

    # Combine the time and distance values into a list of tuples
    time_distance_pairs = list(zip(time_values, distance_values))
    return time_distance_pairs

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
    retval = 1;
    # foreach pair
    for time, distance in parsed_data:
        wins=0
        for ms in range(1,time):
            if ms*(time-ms) > distance:
                wins+=1
        retval*=wins
    return retval

def part2(parsed_data):
    retval = 1;
    # foreach pair
    for time, distance in parsed_data:
        wins=0
        for ms in range(1,time):
            if ms*(time-ms) > distance:
                wins+=1
        retval*=wins
    return retval

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data1 = parse_input(f.read())
    print(parsed_data1)

    with open(sys.argv[1] , "r") as f:
        parsed_data2 = parse_input2(f.read())
    print(parsed_data2)

    print("--- PART 1 ---")
    answer1 = part1(parsed_data1)
    
    print("\n--- PART 2 ---")
    answer2 = part2(parsed_data2)

    print("\n--- ANSWERS ---")
    print(f"PART1 -  {answer1}")
    print(f"PART2 -  {answer2}")
    