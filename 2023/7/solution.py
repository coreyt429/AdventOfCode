"""
Advent Of Code 2023 day 7

"""

# import system modules
import logging
import argparse
from collections import defaultdict

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
VALUES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def count_cards(hand):
    """count cards in hand"""
    counts = defaultdict(int)
    for char in hand:
        counts[char] += 1

    return counts


def replace_jokers(hand, new_value):
    """replace jokers in hand with new value"""

    new_hand = []

    for card in hand:
        if card == "J":
            new_hand.append(new_value)

        else:
            new_hand.append(card)

    return new_hand


def value_jokers(hand):
    """value jokers in hand to maximize hand value"""
    if isinstance(hand, str):
        hand = list(hand)
    final_hand = hand.copy()
    max_score = 0
    for card in CARDS:
        if card == "J":
            continue
        test_hand = replace_jokers(hand, card)
        if get_type(test_hand) > max_score:
            max_score = get_type(test_hand)
            final_hand = test_hand
    return final_hand


def get_type(hand):
    """classify hand without jokers"""
    counts = count_cards(hand)
    biggest = max(counts.values())
    count_len = len(counts)
    # four or five of a kind
    if biggest in (4, 5):
        return biggest + 2
    # full house or 4 of a kind
    if count_len == 2:
        if biggest == 3:
            return 5
    # three of a kind
    if biggest == 3:
        return 4
    # pair or two pairs
    if biggest == 2:
        # one pair
        if count_len == 4:
            return 2
        # two pairs
        return 3
    # High card
    if count_len == 5:
        return 1
    raise ValueError("Invalid hand type")


def parse_input(lines, part=2):
    """
    Docstring for parse_input

    :param data: Description
    """
    # Split the data into lines
    hands = []
    for line in lines:
        hand = line.split()[0]
        bid = line.split()[1]
        hand_type = get_type(hand)
        if part == 2:
            hand_type = get_type(value_jokers(hand))
        hands.append({"hand": hand, "bid": int(bid), "type": hand_type})
    return hands


def sort_hands(hands, part=2):
    """sort hands"""
    values = VALUES.copy()
    if part == 2:
        values["J"] = 1

    def compare_hands(dict_item):
        """Compare two hands"""
        # Complex comparison logic here
        cards = dict_item["hand"]
        # get values of cards
        key_list = [dict_item["type"]]
        for card in cards:
            key_list.append(values[card])
        return tuple(key_list)

    return sorted(hands, key=compare_hands)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    parsed_data = parse_input(input_value, part=part)
    winnings = 0
    hands = sort_hands(parsed_data, part=part)
    # print(hands)
    for i, hand in enumerate(hands):
        winnings += (i + 1) * hand["bid"]
    return winnings


YEAR = 2023
DAY = 7
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
