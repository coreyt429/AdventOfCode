import sys
import re
from copy import deepcopy

# hp,attack
boss = tuple([55,8])
# hp,mana
player=tuple([50,500])
lowest_win_cost=10**9

"""
Magic Missile costs 53 mana. It instantly does 4 damage.
Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.
"""
spells = tuple(["Magic Missile","Drain","Shield","Poison","Recharge"])
#spells = tuple(["Magic Missile"])
# cost, damage, heal, armor, mana, duration, index
spell_props = tuple([
    tuple([53 , 4, 0, 0, 0,   0, 0]),
    tuple([73 , 2, 2, 0, 0,   0, 1]),
    tuple([113, 0, 0, 7, 0,   6, 2]),
    tuple([173, 0, 3, 0, 0,   6, 3]),
    tuple([229, 0, 0, 0, 101, 5, 4])
])

# cost, damage, heal, armor, mana, duration, index
def play_turn(bossHP, bossDmg, myHP, myMana, activespells, playerTurn, manaUsed, inPart2):    
    #print(f'Play Turn: {bossHP}, {myHP}, {myMana}, {activespells}, {playerTurn}, {manaUsed}')
    global spells
    global spell_props
    global lowest_win_cost
    myArmour = 0
    # part 2 rule change
    if playerTurn and inPart2:
        myHP -= 1
        if myHP <= 0:
            return False
    # process active spells first, regardless of turn
    newActiveSpells = []
    for activespell in activespells:
        if activespell[5] >= 0: # spell effect applies now
            bossHP -= activespell[1]
            myHP += activespell[2]
            myArmour += activespell[3]
            myMana += activespell[4]

        newActiveSpell = (activespell[0], activespell[1], activespell[2], activespell[3], activespell[4], activespell[5]-1, activespell[6])
        if newActiveSpell[5] > 0: # spell carries over
            newActiveSpells.append(newActiveSpell)
    
    # did activespells win
    if bossHP <= 0:
        global lowest_win_cost
        if manaUsed < lowest_win_cost:
            lowest_win_cost = manaUsed
        return True
    # are we out of mana?
    if manaUsed >= lowest_win_cost:
        return False

    if playerTurn: # execute as player
        for idx in range(len(spell_props)):
            spell = spell_props[idx]
            #print(f'Spell: {spell}')
            isActive = False
            for idx2 in range(len(newActiveSpells)):
                if newActiveSpells[idx2][6] == spell[6]:
                    #print(f'skipping active spell')
                    isActive = True
                    break # skip active spells, we can't have two of the same spell active
            spellManaCost = spell[0]
            if spellManaCost <= myMana and not isActive:
                a = deepcopy(newActiveSpells)
                a.append(spell)
                play_turn(bossHP, bossDmg, myHP, myMana - spellManaCost, a, False, manaUsed+spellManaCost, inPart2)
    else: # execute as boss
        #print(f'Boss: {bossHP}, {myHP}, {myMana}, {activespells}, {playerTurn}, {manaUsed}')
        myHP += myArmour-bossDmg if myArmour-bossDmg < 0 else -1
        if myHP > 0:
            play_turn(bossHP, bossDmg, myHP, myMana,newActiveSpells, True,manaUsed,inPart2)
    return False


def part1():
    global player
    global boss
    global spells
    global lowest_win_cost
    lowest_win_cost = 10**9
    p=player
    b=boss
    play_turn(b[0],b[1],p[0],p[1],[],True,0,False)
    return lowest_win_cost

def part2():
    global player
    global boss
    global spells
    global lowest_win_cost
    lowest_win_cost = 10**9
    p=player
    b=boss
    play_turn(b[0],b[1],p[0],p[1],[],True,0,True)
    return lowest_win_cost

if __name__ == "__main__":
    #print("Part 1")
    answer1 = part1()
    
    #print("Part 2")
    answer2 = part2()

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    