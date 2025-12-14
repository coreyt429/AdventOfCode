"""
Advent Of Code 2019 day 22

I need to revisit this one and wrap my head around the math.

I understand it on some level, but not enough to see the solution.

"""

# import system modules
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


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


YEAR = 2019
DAY = 22
input_format = {
    1: "lines",
    2: "lines",
}

funcs = {
    1: solve,
    2: solve,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    aoc = AdventOfCode(
        year=YEAR,
        day=DAY,
        input_formats=input_format,
        funcs=funcs,
        test_mode=args.test,
    )
    aoc.run(submit=args.submit)
