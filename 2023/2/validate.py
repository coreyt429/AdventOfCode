import re

# Using readlines()
file1 = open('input.txt', 'r')
Lines = file1.readlines()

cubes = {'red' : 12, 'green': 13, 'blue': 14}

count = 0
games = {};
for line in Lines:
    count+=1
    print("Line{}: {}".format(count, line.strip()))
    [game,strRolls] = line.split(':',2)
    gameId=int(game.replace("Game ",''))
    games[gameId] = {}
    games[gameId]['turns'] = {}
    print(gameId,strRolls)
    turn = 0;
    for roll in strRolls.split(';'):
        print(roll)
        turn+=1;
        games[gameId]['turns'][turn] = {}
        for cube in roll.split(','):
            cube = cube.strip();
            print(cube)
            [qty,color] = cube.split(' ')
            print(color,qty)
            games[gameId]['turns'][turn][color]= int(qty)

answer=0
for gameId in games:
    #print(gameId)
    valid=1
    for turn in games[gameId]['turns']:
        for color in games[gameId]['turns'][turn]:
            if games[gameId]['turns'][turn][color] > cubes[color]:
                valid=0
    #print(valid)
    if valid:
        answer+=gameId

print(answer)

#print(games)
#print(cubes)
#print(cubes['red'])