"""
Advent Of Code 2020 day 22

I had this one except for one little line I missed in the instructions:
(the quantity of cards copied is equal to the number on the card they drew to trigger the sub-game)

Without this, the test data worked, and the puzzle data looped forever.

Add this in, and the puzzle data finishes in about 3 seconds.

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


def parse_data(text):
    """function to parse input data"""
    text_hands = text.split("\n\n")
    hands = {}
    for text_hand in text_hands:
        name, *cards = text_hand.splitlines()
        name = name.replace(":", "")
        cards = [int(card) for card in cards]
        hands[name] = cards
    return hands


def play_cards(hands):
    """function to get next card from each player"""
    table = {}
    # both players draw their top card
    for player in hands.keys():
        table[player] = hands[player].pop(0)
    return table


def check_winner(table):
    """function to identify the hand winner"""
    # the player with the higher-valued card wins the round.
    high_card = 0
    low_card = float("infinity")
    winner = None
    for player, card in table.items():
        high_card = max(high_card, card)
        low_card = min(low_card, card)
        if card == high_card:
            winner = player
    return winner, high_card, low_card


def is_winner(hands):
    """Function to check for end of game"""
    for cards in hands.values():
        if len(cards) == 0:
            return False
    return True


def score_hand(hand):
    """Funciton to score a hand"""
    # Once the game ends, you can calculate the winning player's score.
    # The bottom card in their deck is worth the value of the card multiplied by 1,
    # the second-from-the-bottom card is worth the value of the card multiplied by 2,
    # and so on. With 10 cards, the top card is worth the value on the card multiplied by 10.
    # In this example, the winning player's score is:
    multiplier = 1
    score = 0
    for card in hand[::-1]:
        score += card * multiplier
        multiplier += 1
    return score


def play_combat(hands):
    """function to play a game of combat"""
    # Then, the game consists of a series of rounds:
    game_on = True
    table = {}
    while game_on:
        table = play_cards(hands)
        winner, high_card, low_card = check_winner(table)
        # The winner keeps both cards
        # placing them on the bottom of their own deck so that the
        # winner's card is above the other card.
        hands[winner].append(high_card)
        hands[winner].append(low_card)
        # If this causes a player to have all of the cards, they win, and the game ends.
        game_on = is_winner(hands)
    return winner, hands[winner]


def play_recursive_combat(hands):
    # print(f"play_recursive_combat({start_hands}, {game_id})")
    """Function to play recursive combat"""
    # hands = {}
    # for hand in start_hands:
    #     hands[hand[0]] = list(hand[1])
    seen = set()
    game_on = True
    table = {}
    while game_on:
        # Before either player deals a card, if there was a previous round in this game
        # that had exactly the same cards in the same order in the same players' decks,
        # the game instantly ends in a win for player 1. Previous rounds from other games
        # are not considered. (This prevents infinite games of Recursive Combat, which
        # everyone agrees is a bad idea.)
        hands_tuple = tuple((tuple(cards) for cards in hands.values()))
        if hands_tuple in seen:
            return "Player 1", hands["Player 1"]
        seen.add(hands_tuple)
        # Otherwise, this round's cards must be in a new configuration; the players begin
        # the round by each drawing the top card of their deck as normal.
        table = play_cards(hands)
        # If both players have at least as many cards remaining in their deck as the value
        # of the card they just drew, the winner of the round is determined by playing a
        # new game of Recursive Combat (see below).
        recurse = True
        for player, hand in hands.items():
            if len(hand) < table[player]:
                recurse = False

        if recurse:
            # winner, hand = play_recursive_combat(
            #     tuple(
            #         (tuple([key, tuple(value[:table[key]])]
            #         ) for key, value in hands.items()))
            # )
            winner, hand = play_recursive_combat(
                {key: value[: table[key]] for key, value in hands.items()}
            )
            hands[winner].append(table[winner])
            for player, card in table.items():
                if player != winner:
                    hands[winner].append(card)
        else:
            # Otherwise, at least one player must not have enough cards left
            # in their deck to recurse;
            # the winner of the round is the player with the higher-value card.
            winner, high_card, low_card = check_winner(table)
            hands[winner].append(high_card)
            hands[winner].append(low_card)

        # If this causes a player to have all of the cards, they win, and the game ends.
        game_on = is_winner(hands)
    return winner, hands[winner]


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # Before the game starts, split the cards so each player has their own deck (your puzzle input).
    hands = parse_data(input_value)
    # Then, the game consists of a series of rounds:
    if part == 1:
        _, winning_hand = play_combat(hands)
        return score_hand(winning_hand)
    _, winning_hand = play_recursive_combat(hands)
    return score_hand(winning_hand)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020, 22)
    input_text = my_aoc.load_text()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 32366, 2: 30891}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
