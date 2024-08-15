"""
Advent Of Code 2023 day 2

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error

def parse_games(lines):
    """
    Function to parse input
    """
    games = {}
    for line in lines:
        [game, str_rolls] = line.split(':',2)
        game_id = int(game.replace("Game ", ''))
        games[game_id] = {}
        games[game_id]['turns'] = {}
        turn = 0
        for roll in str_rolls.split(';'):
            turn += 1
            games[game_id]['turns'][turn] = {}
            for cube in roll.split(','):
                cube = cube.strip()
                [qty, color] = cube.split(' ')
                games[game_id]['turns'][turn][color]= int(qty)
    return games

def part1(games):
    """
    Function to solve part 1
    """
    cubes = {'red' : 12, 'green': 13, 'blue': 14}
    result = 0
    for game_id in games:
        valid = 1
        for turn in games[game_id]['turns']:
            for color in games[game_id]['turns'][turn]:
                if games[game_id]['turns'][turn][color] > cubes[color]:
                    valid=0
        #print(valid)
        if valid:
            result += game_id
    return result

def part2(games):
    """
    function to solve part 2
    """
    result = 0
    # find minimum number of cubes of each color for each game
    # calculate power of cube set for game red * green * blue
    # sum up power as answer
    for game_id in games:
        min_set = {'red': 0, 'green':0, 'blue':0}
        for turn in games[game_id]['turns']:
            for color in games[game_id]['turns'][turn]:
                if games[game_id]['turns'][turn][color] > min_set[color]:
                    min_set[color] = games[game_id]['turns'][turn][color]
        power = min_set['red'] * min_set['blue'] * min_set['green']
        result += power
    return result

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    games = parse_games(input_value)
    if part == 1:
        return part1(games)
    return part2(games)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2023,2)
    #input_text = my_aoc.load_text()
    #print(input_text)
    input_lines = my_aoc.load_lines()
    #print(input_lines)
    # parts dict to loop
    parts = {
        1: 1,
        2: 2
    }
    # dict to store answers
    answer = {
        1: None,
        2: None
    }
    # dict to map functions
    funcs = {
        1: solve,
        2: solve
    }
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(f"Part {my_part}: {answer[my_part]}, took {end_time-start_time} seconds")
