import sys
import re
import itertools

# Alice would gain 2 happiness units by sitting next to Bob.
def parse_input(data):
    scores = {}
    # Split the data into lines
    lines = data.strip().split('\n')
    # loop through lines
    for line in lines:
        tmp = line.split(' ')
        if not tmp[0] in scores.keys():
            scores[tmp[0]] = {}
        score = int(tmp[3])
        if tmp[2] == 'lose':
            score*=-1
        scores[tmp[0]][tmp[10][:-1]] = score
    return scores

def score(myMap,myPeeps):
    scores = {}
    #print(myMap)
    for idx in range(len(myPeeps)):
        #print(idx,myPeeps[idx])
        #print(myMap[myPeeps[idx]])
        #print(myPeeps[idx],myPeeps[-1])
        if not myPeeps[idx] in scores:
            #print(f'Init score for {myPeeps[idx]}')
            scores[myPeeps[idx]]=0
        if idx == 0:
            #print(myPeeps[idx])
            #print(f'Map: {myMap[myPeeps[idx]]}')
            scores[myPeeps[idx]]+=myMap[myPeeps[idx]][myPeeps[-1]]
            scores[myPeeps[idx]]+=myMap[myPeeps[idx]][myPeeps[idx+1]]
        elif idx == len(myPeeps)-1:
            scores[myPeeps[idx]]+=myMap[myPeeps[idx]][myPeeps[idx-1]]
            scores[myPeeps[idx]]+=myMap[myPeeps[idx]][myPeeps[0]]
        else:
            #print(idx)
            scores[myPeeps[idx]]+=myMap[myPeeps[idx]][myPeeps[idx-1]]
            scores[myPeeps[idx]]+=myMap[myPeeps[idx]][myPeeps[idx+1]]
    return sum(scores.values())


def part1(parsed_data):
    retval = 0
    peeps = set(parsed_data.keys())
    options = list(itertools.permutations(peeps))
    for option in options:
        myscore = score(parsed_data,option)
        #print(option,myscore)
        if myscore > retval:
            retval = myscore
    return retval

def part2(parsed_data):
    parsed_data['Me'] = {}
    for peep in parsed_data.keys():
        if not peep == 'Me':
            parsed_data['Me'][peep] = 0
            parsed_data[peep]['Me'] = 0
    retval = 0
    peeps = set(parsed_data.keys())
    options = list(itertools.permutations(peeps))
    for option in options:
        myscore = score(parsed_data,option)
        #print(option,myscore)
        if myscore > retval:
            retval = myscore
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
    