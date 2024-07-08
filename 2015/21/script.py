import sys
import re

boss = {
    'hp': 100,
    'damage': 8,
    'armor': 2
}

player={
    'hp': 100,
    'damage': 0,
    'armor': 0
}

weapons = [
    {"name": "Dagger", "cost": 8, "damage": 4, "armor": 0},
    {"name": "Shortsword", "cost": 10, "damage": 5, "armor": 0},
    {"name": "Warhammer", "cost": 25, "damage": 6, "armor": 0},
    {"name": "Longsword", "cost": 40, "damage": 7, "armor": 0},
    {"name": "Greataxe", "cost": 74, "damage": 8, "armor": 0}
]

armor = [
    {"name": "Leather", "cost": 13, "damage": 0, "armor": 1},
    {"name": "Chainmail", "cost": 31, "damage": 0, "armor": 2},
    {"name": "Splintmail", "cost": 53, "damage": 0, "armor": 3},
    {"name": "Bandedmail", "cost": 75, "damage": 0, "armor": 4},
    {"name": "Platemail", "cost": 102, "damage": 0, "armor": 5},
    {"name": "None", "cost": 0, "damage": 0, "armor": 0}
]

rings = [
    {"name": "Damage +1", "cost": 25, "damage": 1, "armor": 0},
    {"name": "Damage +2", "cost": 50, "damage": 2, "armor": 0},
    {"name": "Damage +3", "cost": 100, "damage": 3, "armor": 0},
    {"name": "Defense +1", "cost": 20, "damage": 0, "armor": 1},
    {"name": "Defense +2", "cost": 40, "damage": 0, "armor": 2},
    {"name": "Defense +3", "cost": 80, "damage": 0, "armor": 3},
    {"name": "None1", "cost": 0, "damage": 0, "armor": 0},
    {"name": "None2", "cost": 0, "damage": 0, "armor": 0}
]

def deal_damage(p1,p2):
    damage = p1['damage'] - p2['armor']
    if damage <=0:
        damage = 1
    p2['hp'] -= damage
    return damage

def battle(player1,player2):
    p1=player1.copy()
    p2=player2.copy()
    print(p1)
    print(p2)
    
    while p1['hp'] > 0 and p2['hp'] > 0:
        print(f"p1: {p1['hp']}, p2: {p2['hp']}")
        damage=deal_damage(p1,p2)
        print(f'Player deals {damage} damage')
        damage=deal_damage(p2,p1)
        print(f'Boss deals {damage} damage')
    return p1,p2

def simulate_battle(player1,player2):
    boss_hp = player2['hp']
    boss_armor = player2['armor']
    boss_damage = player2['damage']
    boss_power = boss_armor + boss_damage
    
    p_hp = player1['hp']
    p_armor = player1['armor']
    p_damage = player1['damage']
    p_power = p_armor + p_damage
    prediction = False
    if p_power >= boss_power:
        prediction = True
    return prediction
    while True:
        boss_hp -= max(1, p_damage - boss_armor)
        if boss_hp <= 0:
            if not prediction:
                print(f"missed prediction {player1}")
            return True
        p_hp -= max(1, boss_damage - p_armor)
        if p_hp <= 0:
            if prediction:
                print(f"missed prediction {player1}")
            return False

def try_battle(playerO,bossO,weapon,armor={},ring1={},ring2={}):
    player = playerO.copy()
    boss = bossO.copy()
    cost=0
    items= set()
    for item in [weapon,armor,ring1,ring2]:
        if item:
            player['damage']+=item['damage']
            player['armor']+=item['armor']
            cost+=item['cost']
            items.add(item['name'])
    win=simulate_battle(player,boss)
    return win,cost

def part1():
    global player
    global boss
    global weapons
    global armor
    global rings

    retval = None;
    for weapon in weapons:
        for arm in armor:
            for ring1 in rings:
                for ring2 in rings:
                    if not ring1 == ring2:
                        win,cost = try_battle(player,boss,weapon,arm,ring1,ring2)
                        if win: # winner
                            if not retval or cost < retval:
                                retval = cost
    return retval

def part2():
    global player
    global boss
    global weapons
    global armor
    global rings

    retval = None;
    for weapon in weapons:
        for arm in armor:
            for ring1 in rings:
                for ring2 in rings:
                    if not ring1 == ring2:
                        win,cost = try_battle(player,boss,weapon,arm,ring1,ring2)
                        if not win: # winner
                            if not retval or cost > retval:
                                retval = cost                
    return retval

if __name__ == "__main__":
    #print("Part 1")
    answer1 = part1()
    
    #print("Part 2")
    answer2 = part2()

    print(f"Part1: {answer1}")
    print(f"Part2: {answer2}")
    