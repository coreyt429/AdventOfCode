import re

# Using readlines()
file1 = open('input.txt', 'r')
Lines = file1.readlines()

"""
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
cards = {}
for line in Lines:
    [card,strNums] = line.split(':',2)
    cardId=int(card.replace("Card ",''))
    cards[cardId] = {'matches':0, 'score':0}
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


print(cards);
answer=0
for cardId in cards:
    print(cardId,cards[cardId]['score'])
    answer+=cards[cardId]['score']
print(answer)

