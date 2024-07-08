import sys
import re

def init_light_grid(l=1000, w=1000):
    lights = []
    for i in range(l):
        row = []
        for j in range(w):
            row.append(0)  # Assuming you want to initialize each light to 0
        lights.append(row)
    return lights

def parse_input(data):
    commands = [];
    # Split the data into lines
    lines = data.strip().split('\n')
    parseRegex = r'(.*) (\d+),(\d+) through (\d+),(\d+)'
    for line in lines:
        result = re.findall(parseRegex,line)
        row=result[0]
        commands.append({'command': row[0],'x_start':int(row[1]),'y_start':int(row[2]),'x_end':int(row[3]),'y_end':int(row[4])})
    return commands

def print_lights(lights):
    for x in range(len(lights)):
        row=lights[x]
        for y in range(len(row)):
            print(lights[x][y],end='')
        print()

def count_lights(lights):
    retval=0;
    for x in range(len(lights)):
        row=lights[x]
        for y in range(len(row)):
            if lights[x][y] == 1:
                retval+=1
    return retval

def count_brightness(lights):
    retval=0;
    for x in range(len(lights)):
        row=lights[x]
        for y in range(len(row)):
            retval += lights[x][y]
    return retval

def toggle_lights(lights,x_start,y_start,x_end,y_end):
    for x in range(x_start,x_end+1):
        for y in range(y_start,y_end+1):
            if lights[x][y] == 1:
                lights[x][y]=0
            else:
                lights[x][y]=1

def set_lights(lights,status,x_start,y_start,x_end,y_end):
    for x in range(x_start,x_end+1):
        for y in range(y_start,y_end+1):
            lights[x][y]=status

def adjust_lights(lights,status,x_start,y_start,x_end,y_end):
    for x in range(x_start,x_end+1):
        for y in range(y_start,y_end+1):
            lights[x][y]+=status
            if lights[x][y] < 0:
                lights[x][y] = 0

def part1(parsed_data):
    lights = init_light_grid()
    for command in parsed_data:
        if command['command'] == "turn on":
            set_lights(lights,1,command['x_start'],command['y_start'],command['x_end'],command['y_end'])
        elif command['command'] == "turn off":
            set_lights(lights,0,command['x_start'],command['y_start'],command['x_end'],command['y_end'])
        elif command['command'] == "toggle":
            toggle_lights(lights,command['x_start'],command['y_start'],command['x_end'],command['y_end'])
    retval = count_lights(lights)
    return retval

def part2(parsed_data):
    lights = init_light_grid()
    #print('Before:')
    #print_lights(lights)
    for command in parsed_data:
        if command['command'] == "turn on":
            adjust_lights(lights,1,command['x_start'],command['y_start'],command['x_end'],command['y_end'])
        elif command['command'] == "turn off":
            adjust_lights(lights,-1,command['x_start'],command['y_start'],command['x_end'],command['y_end'])
        elif command['command'] == "toggle":
            adjust_lights(lights,2,command['x_start'],command['y_start'],command['x_end'],command['y_end'])
    #print('after:')
    #print_lights(lights)
    retval = count_brightness(lights)
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
    