"""
Advent Of Code 2018 day 9

deque makes this one pretty easy,  I really like it for circle problems.
It is really easy to rotate the circle clockwise or counter clockwise.

I also used deque for the players to rotate through the players.  A 
current player pointer to a list position might have been more efficient,
but part 2 runs in 1.3 seconds, so not optimizing further.

I used deque for the marbles for the efficient popleft. This could
also have been done br replacing "while marbles" with "for current_marble in
in range(marble_value + 1)", which also might have been more efficient.

I was just having fun with deque today though :)
"""
# import system modules
import time
import re
from collections import deque

# import my modules
import aoc # pylint: disable=import-error

def parse_input(lines):
    """
    Function to parse input
    Args:
        lines: list() of str(), input lines

    Returns:
        games: list() of tuple(player_count, marble_value)
    """
    # init games
    games = []
    # regex to match input nums
    pattern_input = re.compile(r'(\d+)')
    # walk lines
    for line in lines:
        # extract values
        player_count, marble_value = pattern_input.findall(line)
        # append tuple() of ints()
        games.append((int(player_count), int(marble_value)))
    # return
    return games

def play_game(game):
    """
    Function to simulate marble game

    Args:
        game: tuple(int(player_count), int(marble_value))

    Returns: 
        scores: dict() keys=int(player), values=int(score)
    """
    # init scores
    scores = {}
    # unpack player count and high marble value
    player_count, marble_value = game
    # init players
    players = deque(list(player for player in range(player_count)))
    # init marbles
    marbles = deque(list(marble for marble in range(marble_value + 1)))
    # First, the marble numbered 0 is placed in the circle.
    circle = deque([marbles.popleft()])
    # loop until all marbles are played
    while marbles:
        # Then, each Elf takes a turn placing the lowest-numbered remaining marble
        current_player = players[0]
        # advance players for next pass
        players.rotate(-1)
        current_marble = marbles.popleft()
        # However, if the marble that is about to be placed has a number which is a multiple of 23
        if current_marble > 0 and current_marble % 23 == 0:
            # something entirely different happens.
            # First, the current player keeps the marble they would have placed, adding it to
            # their score.
            # init score for current_player if needed
            if current_player not in scores:
                scores[current_player] = 0
            scores[current_player] += current_marble
            # In addition, the marble 7 marbles counter-clockwise from the current marble is
            # removed from the circle
            circle.rotate(7)
            current_marble = circle.popleft()
            # and also added to the current player's score. The marble located immediately clockwise
            # of the marble that was removed becomes the new current marble.
            scores[current_player] += current_marble
            continue
        # into the circle between the marbles that are 1 and 2 marbles clockwise of the current
        # marble. (When the circle is large enough, this means that there is one marble between
        # the marble that was just placed and the current marble.) The marble that was just placed
        # then becomes the current marble.
        circle.rotate(-2)
        circle.appendleft(current_marble)
    return scores

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # there is only one game in the input
    game = parse_input(input_value)[0]
    if part == 2:
        # unpack values
        player_count, marble_value = game
        # What would the new winning Elf's score be if the number of the last marble were 100 times
        # larger?
        marble_value *= 100
        # repack game
        game = (player_count, marble_value)
    # get scores
    scores = play_game(game)
    # return high score
    return max(scores.values())

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018,9)
    input_lines = my_aoc.load_lines()
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
