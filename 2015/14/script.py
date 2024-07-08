import sys
import re

#Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
def parse_input(data):
    reindeer = {}
    # Split the data into lines
    lines = data.strip().split('\n')
    # loop through lines
    for line in lines:
        tmp = line.split(' ')
        reindeer[tmp[0]]={
            'speed': int(tmp[3]),
            'duration': int(tmp[6]),
            'rest': int(tmp[13])
        }
    return reindeer

def distance_traveled(reindeer,seconds):
    distance_per_interval = reindeer['speed']*reindeer['duration']
    cycle = reindeer['rest']+reindeer['duration']
    intervals = int(seconds/cycle)
    remainder  = seconds % cycle
    distance = 0
    if remainder >= reindeer['duration']:
        intervals+=1
    else:
        distance = remainder*reindeer['speed']
    distance += intervals*distance_per_interval
    return distance

def part1(parsed_data):
    retval = 0
    seconds = 2503
    for reindeer in parsed_data:
        distance = distance_traveled(parsed_data[reindeer],seconds)
        #print(reindeer,distance)
        if distance > retval:
            retval = distance
    return retval

def part2(parsed_data):# 1564 too high
    retval = 0
    seconds = 2503
    scores = {}
    for reindeer in parsed_data:
        scores[reindeer]=0
    for sec in range(seconds):
        leaders = []
        high=0
        for reindeer in parsed_data:
            distance = distance_traveled(parsed_data[reindeer],sec+1)
            if distance > high:
                high = distance
                leaders = [reindeer]
            elif distance == high:
                leaders.append(reindeer)
        for leader in leaders:
            scores[leader]+=1
    print(scores)
    return max(scores.values())

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
    