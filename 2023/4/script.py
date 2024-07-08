import re
import sys

def parse_cards(Lines):
    cards = {}
    for line in Lines:
        [card,strNums] = line.split(':',2)
        cardId=int(card.replace("Card ",''))
        cards[cardId] = {'matches':0, 'score':0, 'clones': []}
        [strWinning,strCardNums] = strNums.split('|')
        cards[cardId]['winningNums'] = re.findall(r'\d+',strWinning)
        cards[cardId]['cardNums'] = re.findall(r'\d+',strCardNums)
        for testNum in cards[cardId]['cardNums']:
            for winNum in cards[cardId]['winningNums']:
                if testNum == winNum:
                    cards[cardId]['matches']+=1
                    if cards[cardId]['score'] == 0:
                        cards[cardId]['score']=1
                    else:
                        cards[cardId]['score']*=2
        if cards[cardId]['matches'] > 0:
            cards[cardId]['clones']= list(range(cardId+1,cardId+cards[cardId]['matches']+1))
    return cards

def part1(cards):
    answer=0
    for cardId in cards:
        answer+=cards[cardId]['score']
    return answer

def count_cards (idx):
    count=1 # count self
    for clone in cards[idx]['clones']:
        count+=count_cards(clone)
    return count;

def part2(cards):
    answer=0
    for card in cards:
        answer+=count_cards(card);
    return answer

if __name__ == "__main__":
    # Using readlines()
    file1 = open(sys.argv[1], 'r')
    Lines = file1.readlines()
    cards = parse_cards(Lines)
    answer1 = part1(cards)
    answer2 = part2(cards)
    print(f'Part 1: {answer1}')
    print(f'Part 2: {answer2}')
    
    exit();
    