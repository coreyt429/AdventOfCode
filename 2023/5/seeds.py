import re
import sys

# Using readlines()
file1 = open(sys.argv[1], 'r')
Lines = file1.readlines()

"""
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
seeds = []
maps = []
mapCurrent = {}
for line in Lines:
    #print(line)
    if re.match("seeds:",line):
        [label,strSeeds] = line.strip().split(": ")
        #print(strSeeds)
        seeds = strSeeds.split(" ")
        print(seeds)
    elif re.match(".*map:",line):
        [label,strTmp] = line.strip().split(" ")
        [strFrom,strTmp,strTo] = label.split('-')
        mapCurrent = {'from': strFrom, 'to': strTo, 'mappings': []}
        maps.append(mapCurrent)
        #print(mapCurrent)
    elif re.match(r'^\d',line):
        [strTo,strFrom,strQty] = line.strip().split(" ")
        mapCurrent['mappings'].append({'orig': int(strFrom), 'dest': int(strTo), 'qty': int(strQty)})

def walk_map(typeId,idx):
    retType = ''
    retIdx = idx
    #print(typeId,idx)
    for mapCurrent in maps:
        if mapCurrent['from'] == typeId:
            #print(mapCurrent)
            retType = mapCurrent['to']
            for mapping in mapCurrent['mappings']:
                if mapping['orig'] <= idx and mapping['orig']+mapping['qty']-1 >= idx:
                    retIdx = mapping['dest']+idx-mapping['orig']
    #print("returning",retType,retIdx)
    return [retType,retIdx] 


def location_of_seed(seed):
    [Type,Idx] = walk_map('seed',seed)
    while Type != 'location':
        [Type,Idx] = walk_map(Type,Idx)
    return Idx

minLocation=-1
locations = []
#location_of_seed(14)
#exit()
for myseed in seeds:
    mylocation = location_of_seed(int(myseed))
    locations.append(mylocation)
    if minLocation == -1 or minLocation > mylocation:
        minLocation = mylocation
    print(f'seed {myseed} in location {mylocation}')
locations.sort()
print(minLocation)

