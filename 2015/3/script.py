import sys

def part1(data):
    Lat=0
    Long=0
    houses = {f'{Lat}-{Long}': 1}
    for char in data:
        if char == '>':
            Long+=1
        elif char == '<':
            Long-=1
        elif char == 'v':
            Lat-=1
        elif char == '^':
            Lat+=1
        house_name = f'{Lat}-{Long}'
        if house_name in houses:
            houses[house_name] += 1
        else:
            houses[house_name] = 1
    return len(houses)

def part2(data):
    vehicles = ['Santa','RoboSanta']
    Lat = {'Santa': 0,'RoboSanta': 0} 
    Long = {'Santa': 0,'RoboSanta': 0} 
    houses = {f'{Lat["Santa"]}-{Long["Santa"]}': 2}
    vIdx = -1
    for char in data:
        vIdx+=1
        if vIdx > 1:
            vIdx=0
        vehicle=vehicles[vIdx]
        if char == '>':
            Long[vehicle]+=1
        elif char == '<':
            Long[vehicle]-=1
        elif char == 'v':
            Lat[vehicle]-=1
        elif char == '^':
            Lat[vehicle]+=1
        house_name = f'{Lat[vehicle]}-{Long[vehicle]}'
        if house_name in houses:
            houses[house_name] += 1
        else:
            houses[house_name] = 1
    return len(houses)

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        data = f.read()
    
    answer1 = part1(data)
    
    #print("Part 2")
    answer2 = part2(data)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    