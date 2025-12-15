"""
Advent Of Code 2023 day 4

"""

# import system modules
import logging
import argparse
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_cards(lines):
    """
    Function to parse card data
    """
    cards = {}
    for line in lines:
        card, nums_str = line.split(":", 2)
        card_id = int(card.replace("Card ", ""))
        cards[card_id] = {"matches": 0, "score": 0, "clones": []}
        str_winning, card_nums_str = nums_str.split("|")
        cards[card_id]["winning_nums"] = re.findall(r"\d+", str_winning)
        cards[card_id]["card_nums"] = re.findall(r"\d+", card_nums_str)
        for card_num in cards[card_id]["card_nums"]:
            for win_num in cards[card_id]["winning_nums"]:
                if card_num == win_num:
                    cards[card_id]["matches"] += 1
                    if cards[card_id]["score"] == 0:
                        cards[card_id]["score"] = 1
                    else:
                        cards[card_id]["score"] *= 2
        if cards[card_id]["matches"] > 0:
            cards[card_id]["clones"] = list(
                range(card_id + 1, card_id + cards[card_id]["matches"] + 1)
            )
    return cards


def count_cards(cards, idx):
    """
    Recursive function to count cloned cards
    """
    count = 1  # count self
    for clone in cards[idx]["clones"]:
        count += count_cards(cards, clone)
    return count


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    cards = parse_cards(input_value)
    result = 0
    for card_id, card in cards.items():
        if part == 1:
            result += card["score"]
        else:
            result += count_cards(cards, card_id)
    return result


YEAR = 2023
DAY = 4
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
