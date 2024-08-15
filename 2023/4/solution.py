"""
Advent Of Code 2023 day 4

"""
# import system modules
import time
import re

# import my modules
import aoc # pylint: disable=import-error

def parse_cards(lines):
    """
    Function to parse card data
    """
    # init cards
    cards = {}
    # walk lines
    for line in lines:
        # split card and nums
        [card, nums_str] = line.split(':',2)
        # extract card_id from card
        card_id = int(card.replace("Card ",''))
        # init card for card_id
        cards[card_id] = {'matches':0, 'score':0, 'clones': []}
        # seperate wins from card nums
        [str_winning, card_nums_str] = nums_str.split('|')
        # get digits from both
        cards[card_id]['winning_nums'] = re.findall(r'\d+', str_winning)
        cards[card_id]['card_nums'] = re.findall(r'\d+', card_nums_str)
        # walk card nums
        for card_num in cards[card_id]['card_nums']:
            # walk win nums
            for win_num in cards[card_id]['winning_nums']:
                # if card num = win_num
                if card_num == win_num:
                    # increment matches
                    cards[card_id]['matches'] += 1
                    # init score, or multiply
                    if cards[card_id]['score'] == 0:
                        cards[card_id]['score'] = 1
                    else:
                        cards[card_id]['score'] *= 2
        # if matches, generate clone list
        if cards[card_id]['matches'] > 0:
            cards[card_id]['clones'] = list(
                range(card_id + 1, card_id + cards[card_id]['matches'] + 1)
            )
    return cards

def count_cards (cards, idx):
    """
    Recursive function to count cloned cards
    """
    # init count
    count = 1 # count self
    # walk clones
    for clone in cards[idx]['clones']:
        # recurse clone
        count += count_cards(cards, clone)
    return count

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # parse data
    cards = parse_cards(input_value)
    # init result
    result = 0
    #walk cards
    for card_id, card in cards.items():
        if part == 1:
            # get score
            result += card['score']
        if part == 2:
            # get clone count
            result += count_cards(cards, card_id)
    return result

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2023,4)
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
