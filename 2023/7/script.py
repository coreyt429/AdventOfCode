import sys

def get_type(hand):
    counts = {}
    for char in hand:
        if char in counts.keys():
            counts[char]+=1
        else:
            counts[char]=1
    retval = 0
    biggest=max(counts.values())
    # five of a kind
    if biggest == 5:
        retval = 7
    # four of a kind
    elif biggest == 4:
        retval = 6

    # full house or 4 of a kind
    elif len(counts.keys()) == 2:
        if biggest == 3:
            retval = 5
    # three of a kind
    elif biggest == 3:
        retval = 4
    # pair or two pairs
    elif biggest == 2:
        # one pair
        if len(counts.keys()) == 4:
            retval = 2
        # two pairs
        else:
            retval = 3
    # High card
    elif len(counts.keys()) == 5:
        retval = 1
    else:
        print("We shouldn't get here, bailing")
        exit()
    return retval

def get_type2(hand):
    counts = {}
    for char in hand:
        if char in counts.keys():
            counts[char]+=1
        else:
            counts[char]=1
    retval = 0
    biggest=max(counts.values())
    # no jokers, type normal:
    #print(hand)
    if not 'J' in hand:
        #print('normal typing')
        retval = get_type(hand)
    elif counts['J'] >= 4: # five jokers or 4 jokers and any
        #print('4+ jokers')
        retval = 7
    elif counts['J'] == 3: # 3 jokers
        #print('3 jokers')
        if len(counts.keys()) == 2: # 3 j + 2 any 
            retval = 7
        else: # 4 of a kind
            retval = 6
    elif counts['J'] == 2: # two jokers
        #print('2 jokers')
        if len(counts.keys()) == 2: # 2j + 3 any 
            retval = 7
        elif len(counts.keys()) == 3: # 2j + 2 any + 1 odd 
            retval = 6
        elif len(counts.keys()) == 4: # 2j + 1 any + 2 odd 
            retval = 4
    elif counts['J'] == 1: # one jokers
        #print('1 jokers')
        if len(counts.keys()) == 2: # 1j + 4 any
            retval = 7
        elif len(counts.keys()) == 3: # 4 of a kind or full house 
            smallest = 5
            for rank in counts.keys():
                if rank != 'J':
                    if counts[rank] < smallest:
                        smallest = counts[rank]
            if smallest == 1: # 4 of a kind 
                retval = 6
            else: # full house
                retval = 5
        elif len(counts.keys()) == 4: # 3 of a kind 
            retval = 4
        elif len(counts.keys()) == 5: # j + any = pair 
            retval = 2
    #print(retval)
    return retval



def parse_input(data):
    # Split the data into lines
    lines = data.strip().split('\n')
    hands = []
    for line in lines:
        hand=line.split()[0]
        bid=line.split()[1]
        Type=get_type(hand)
        Type2=get_type2(hand)
        hands.append({'hand': hand, 'bid': int(bid), 'type': Type,'type2': Type2})
    return hands

"""
-Five of a kind, where all five cards have the same label: AAAAA rank 7
-Four of a kind, where four cards have the same label and one card has a different label: AA8AA rank 6
-Full house, where three cards have the same label, and the remaining two cards share a different label: 23332 rank 5
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98 rank 4
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: rank 3 
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: rank 2 
-High card, where all cards' labels are distinct: rank 1
"""
def compare_hands(dict_item):
    # Complex comparison logic here
    cards = dict_item['hand']
    # get rank
    values = {'2': 2,'3': 3,'4': 4,'5': 5,'6': 6,'7': 7,'8': 8,'9': 9,'T':10,'J':11,'Q':12,'K':13,'A':14}
    # get values of cards
    #print(dict_item['type'], values[cards[0]], values[cards[1]], values[cards[2]], values[cards[3]], values[cards[4]])
    return dict_item['type'], values[cards[0]], values[cards[1]], values[cards[2]], values[cards[3]], values[cards[4]]

def compare_hands2(dict_item):
    # Complex comparison logic here
    cards = dict_item['hand']
    # get rank
    values = {'2': 2,'3': 3,'4': 4,'5': 5,'6': 6,'7': 7,'8': 8,'9': 9,'T':10,'J':1,'Q':12,'K':13,'A':14}
    # get values of cards
    #print(dict_item['type2'], values[cards[0]], values[cards[1]], values[cards[2]], values[cards[3]], values[cards[4]])
    return dict_item['type2'], values[cards[0]], values[cards[1]], values[cards[2]], values[cards[3]], values[cards[4]]

def part1(parsed_data):
    retval = 0;
    hands=sorted(parsed_data, key=compare_hands)
    #print(hands)
    for i in range(len(hands)):
        retval+=(i+1)*hands[i]["bid"]
    return retval

def part2(parsed_data):
    retval = 0;
    hands=sorted(parsed_data, key=compare_hands2)
    #print(hands)
    for i in range(len(hands)):
        retval+=(i+1)*hands[i]["bid"]
    return retval

if __name__ == "__main__":
    with open(sys.argv[1] , "r") as f:
        parsed_data = parse_input(f.read())
    #print(parsed_data)

    #print("Part 1")
    answer1 = part1(parsed_data)
    
    #print("Part 2")
    answer2 = part2(parsed_data)

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    