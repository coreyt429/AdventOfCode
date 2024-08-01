"""
Advent Of Code 2015 day 22

"""
# import system modules
import time
from heapq import heappop, heappush

# import my modules
import aoc # pylint: disable=import-error

# hp,attack populate from input
boss = {
    'hp': 0,
    'attack': 0
}

# hp,mana
player={
    'hp': 50,
    'mana': 500
}

spells = {}
# Magic Missile costs 53 mana. It instantly does 4 damage.
spells['Magic Missile'] = {
    'cost': 53,
    'damage': 4,
    'heal': 0,
    'armor': 0,
    'mana': 0,
    'duration': 0
}

# Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
spells['Drain'] = {
    'cost': 73,
    'damage': 2,
    'heal': 2,
    'armor': 0,
    'mana': 0,
    'duration': 0
}

# Shield costs 113 mana. It starts an effect that lasts for 6 turns.
# While it is active, your armor is increased by 7.
spells['Shield'] = {
    'cost': 113,
    'damage': 0,
    'heal': 0,
    'armor': 7,
    'mana': 0,
    'duration': 6
}

# Poison costs 173 mana. It starts an effect that lasts for 6 turns.
# At the start of each turn while it is active, it deals the boss 3 damage.
spells['Poison'] = {
    'cost': 173,
    'damage': 3,
    'heal': 0,
    'armor': 0,
    'mana': 0,
    'duration': 6
}

# Recharge costs 229 mana. It starts an effect that lasts for 5 turns.
# At the start of each turn while it is active, it gives you 101 new mana.
spells['Recharge'] = {
    'cost': 229,
    'damage': 0,
    'heal': 0,
    'armor': 0,
    'mana': 101,
    'duration': 5
}

def find_spells_for_target(target):
    """
    Function to find spells that add up to target mana
    """
    heap = []
    heappush(heap, (0, []))

    while heap:
        mana, spell_list = heappop(heap)
        if mana > target:
            continue
        if mana == target:
            print(mana, spell_list)
        else:
            for spell, props in spells.items():
                heappush(heap, (mana + props['cost'], spell_list + [spell]))

def simulate_game(part_two=False):
    """
    Function to simulate game
    """
    lowest_win_cost=10**9
    heap = []
    #turn_num, mana_spent, boss_hp, player_hp, player_turn, spell_history, active_spells
    heappush(heap,tuple([0,0,boss['hp'],boss['attack'],player['hp'],player['mana'],True,[],[]]))
    while heap:
        won = False
        lost = False
        # reset player armor at the beginning of each turn
        player_armor = 0
        (
            turn_num,
            mana_spent,
            boss_hp,
            boss_attack,
            player_hp,
            player_mana,
            player_turn,
            spell_history,
            active_spells
        ) = heappop(heap)
        if player_turn and part_two:
            player_hp -= 1
            if player_hp <=0:
                lost = True
                continue # lose

        turn_num+=1
        # short circuit
        if mana_spent > lowest_win_cost:
            continue
        new_active_spells = []
        # process active spells at the beginning of each turn
        while active_spells:
            spellname, turns = active_spells.pop()
            player_armor += spells[spellname]['armor']
            player_hp += spells[spellname]['heal']
            player_mana += spells[spellname]['mana']
            boss_hp -= spells[spellname]['damage']
            if boss_hp <= 0:
                if mana_spent < lowest_win_cost:
                    won = True
                    lowest_win_cost = mana_spent
            turns -= 1
            if turns > 0:
                new_active_spells.append((spellname,turns))
        active_spells = new_active_spells
        if won or lost:
            continue
        if player_turn:
            active_spell_names = {spell[0] for spell in active_spells}
            for spell, props in spells.items():
                spells_cast = 0
                if not spell in active_spell_names:
                    if player_mana >= props['cost']:
                        spells_cast += 1
                        if props['duration'] == 0: # instant spells
                            if boss_hp - props['damage'] < 1:
                                if mana_spent + props['cost'] < lowest_win_cost:
                                    won = True
                                    lowest_win_cost = mana_spent + props['cost']
                            heappush(
                                heap,
                                tuple(
                                    [
                                        turn_num,
                                        mana_spent + props['cost'],
                                        boss_hp - props['damage'],
                                        boss_attack,
                                        player_hp + props['heal'],
                                        player_mana - props['cost'],
                                        not player_turn, spell_history + [spell],
                                        active_spells
                                    ]
                                )
                            )
                        else:
                            heappush(
                                heap,
                                tuple(
                                    [
                                        turn_num,
                                        mana_spent + props['cost'],
                                        boss_hp,
                                        boss_attack,
                                        player_hp,
                                        player_mana - props['cost'],
                                        not player_turn,
                                        spell_history + [spell],
                                        active_spells + [(spell,props['duration'])]
                                    ]
                                )
                            )
                if not spells_cast:
                    lost = True
                    #print(lowest_win_cost)
        else: # boss turn
            player_damage = boss_attack - player_armor
            player_damage = max(player_damage, 1)
            if player_hp > player_damage:
                heappush(
                    heap,
                    tuple(
                            [
                                turn_num,
                                mana_spent,
                                boss_hp,
                                boss_attack,
                                player_hp - player_damage,
                                player_mana,
                                not player_turn,
                                spell_history,
                                active_spells
                            ]
                        )
                )
            else:
                lost = True
    return lowest_win_cost

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # ['Hit Points: 55', 'Damage: 8']
    boss['hp'] = int(input_value[0].split(' ')[-1])
    boss['attack'] = int(input_value[1].split(' ')[-1])
    if part == 1:
        return simulate_game()
    return simulate_game(True)

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2015, 22)
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

    find_spells_for_target(953)
    find_spells_for_target(1289)