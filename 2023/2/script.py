import re
import sys

def parse_games(Lines):
    games = {}
    for line in Lines:
        [game,strRolls] = line.split(':',2)
        gameId=int(game.replace("Game ",''))
        games[gameId] = {}
        games[gameId]['turns'] = {}
        turn = 0;
        for roll in strRolls.split(';'):
            turn+=1;
            games[gameId]['turns'][turn] = {}
            for cube in roll.split(','):
                cube = cube.strip();
                [qty,color] = cube.split(' ')
                games[gameId]['turns'][turn][color]= int(qty)
    return games

def part1(games):
    cubes = {'red' : 12, 'green': 13, 'blue': 14}
    answer=0
    for gameId in games:
        valid=1
        for turn in games[gameId]['turns']:
            for color in games[gameId]['turns'][turn]:
                if games[gameId]['turns'][turn][color] > cubes[color]:
                    valid=0
        #print(valid)
        if valid:
            answer+=gameId
    return answer

def part2(Lines):
    answer=0
    # find minimum number of cubes of each color for each game
    # calculate power of cube set for game red * green * blue
    # sum up power as answer
    for gameId in games:
        minSet = {'red': 0, 'green':0, 'blue':0}
        for turn in games[gameId]['turns']:
            for color in games[gameId]['turns'][turn]:
                if games[gameId]['turns'][turn][color] > minSet[color]:
                    minSet[color] = games[gameId]['turns'][turn][color]
        power = minSet['red']*minSet['blue']*minSet['green']
        answer+=power
    return answer

if __name__ == "__main__":
    # Using readlines()
    file1 = open(sys.argv[1], 'r')
    Lines = file1.readlines()
    games = parse_games(Lines)
    answer1 = part1(games)
    answer2 = part2(Lines)
    print(f'Part 1: {answer1}')
    print(f'Part 2: {answer2}')
    
    exit();
    