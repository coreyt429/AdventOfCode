"""
Advent Of Code 2019 day 22

I need to revisit this one and wrap my head around the math.

I understand it on some level, but not enough to see the solution.

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


def deal_stack(cards):
    """
    To deal into new stack, create a new stack of cards by dealing the top card of
    the deck onto the top of the new stack repeatedly until you run out of cards
    """
    return cards[::-1]


def cut_deck(deck, count):
    """
    To cut N cards, take the top N cards off the top of the deck and move them as a
    single unit to the bottom of the deck, retaining their order.
    """
    return deck[count:] + deck[:count]


def deal_deck(deck, increment):
    """
    To deal with increment N, start by clearing enough space on your table to lay out
    all of the cards individually in a long line. Deal the top card into the leftmost
    position. Then, move N positions to the right and deal the next card there. If you
    would move into a position past the end of the space on your table, wrap around and
    keep counting from the leftmost card again. Continue this process until you run out
    of cards
    """
    deck_length = len(deck)
    new_deck = list(range(deck_length))
    for idx, card in enumerate(deck):
        new_idx = (idx * increment) % deck_length
        new_deck[new_idx] = card
    return new_deck


def modinv(a, m):
    """Modular inverse using the Extended Euclidean Algorithm."""
    return pow(a, -1, m)


def parse_instructions(instructions, m):
    """Parse the shuffle instructions and return a, b coefficients."""
    a, b = 1, 0  # Start with the identity transformation: f(x) = x
    for instruction in instructions:
        if instruction.startswith("deal into new stack"):
            a, b = -a % m, (-b - 1) % m
        elif instruction.startswith("cut"):
            n = int(instruction.split()[-1])
            b = (b - n) % m
        elif instruction.startswith("deal with increment"):
            n = int(instruction.split()[-1])
            a = (a * n) % m
            b = (b * n) % m
    return a, b


def repeated_shuffle(a, b, n, m):
    """Compute the coefficients of the transformation after n repetitions."""
    an = pow(a, n, m)
    bn = (b * (an - 1) * modinv(a - 1, m)) % m
    return an, bn


def find_card_at_position_2020(instructions, m, n):
    """
    Function to find target card location
    """
    a, b = parse_instructions(instructions, m)
    an, bn = repeated_shuffle(a, b, n, m)
    # Find the card that ends up at position 2020
    pos = 2020
    card = (pos - bn) * modinv(an, m) % m
    return card


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    deck = list(range(10007))
    if part == 2:
        # Parameters for the problem
        m = 119315717514047  # Size of the deck
        n = 101741582076661  # Number of shuffles
        # Find the card at position 2020 after all shuffles
        return find_card_at_position_2020(input_value, m, n)
    for instruction in input_value:
        if "cut" in instruction:
            count = int(instruction.split(" ")[-1])
            deck = cut_deck(deck, count)
        elif "deal into new stack" in instruction:
            deck = deal_stack(deck)
        else:
            count = int(instruction.split(" ")[-1])
            deck = deal_deck(deck, count)
    # deck_string = ' '.join([str(card) for card in deck])
    return deck.index(2019)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2019, 22)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 6850, 2: 13224103523662}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
