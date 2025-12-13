"""
Advent Of Code 2015 day 21

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

# globals for boss and player.  boss data will be populated by input
boss = {"hp": 0, "damage": 0, "armor": 0}

player = {"hp": 100, "damage": 0, "armor": 0}

# globals for weapons, armor, and rings
weapons = [
    {"name": "Dagger", "cost": 8, "damage": 4, "armor": 0},
    {"name": "Shortsword", "cost": 10, "damage": 5, "armor": 0},
    {"name": "Warhammer", "cost": 25, "damage": 6, "armor": 0},
    {"name": "Longsword", "cost": 40, "damage": 7, "armor": 0},
    {"name": "Greataxe", "cost": 74, "damage": 8, "armor": 0},
]

armor = [
    {"name": "Leather", "cost": 13, "damage": 0, "armor": 1},
    {"name": "Chainmail", "cost": 31, "damage": 0, "armor": 2},
    {"name": "Splintmail", "cost": 53, "damage": 0, "armor": 3},
    {"name": "Bandedmail", "cost": 75, "damage": 0, "armor": 4},
    {"name": "Platemail", "cost": 102, "damage": 0, "armor": 5},
    {"name": "None", "cost": 0, "damage": 0, "armor": 0},
]

rings = [
    {"name": "Damage +1", "cost": 25, "damage": 1, "armor": 0},
    {"name": "Damage +2", "cost": 50, "damage": 2, "armor": 0},
    {"name": "Damage +3", "cost": 100, "damage": 3, "armor": 0},
    {"name": "Defense +1", "cost": 20, "damage": 0, "armor": 1},
    {"name": "Defense +2", "cost": 40, "damage": 0, "armor": 2},
    {"name": "Defense +3", "cost": 80, "damage": 0, "armor": 3},
    {"name": "None1", "cost": 0, "damage": 0, "armor": 0},
    {"name": "None2", "cost": 0, "damage": 0, "armor": 0},
]


def simulate_battle(player1, player2):
    """
    Function to simulate a battle
    """
    # boss_hp = player2['hp']
    boss_armor = player2["armor"]
    boss_damage = player2["damage"]
    boss_power = boss_armor + boss_damage

    # p_hp = player1['hp']
    p_armor = player1["armor"]
    p_damage = player1["damage"]
    p_power = p_armor + p_damage
    prediction = False
    if p_power >= boss_power:
        prediction = True
    return prediction


def try_battle(player_0, boss_0, **kwargs):
    """
    Function to try a battle
    """
    p_weapon = kwargs.get("weapon", {})
    p_armor = kwargs.get("armor", {})
    p_ring1 = kwargs.get("ring1", {})
    p_ring2 = kwargs.get("ring2", {})
    player_1 = player_0.copy()
    boss_1 = boss_0.copy()
    cost = 0
    items = set()
    for item in [p_weapon, p_armor, p_ring1, p_ring2]:
        if item:
            player_1["damage"] += item["damage"]
            player_1["armor"] += item["armor"]
            cost += item["cost"]
            items.add(item["name"])
    win = simulate_battle(player_1, boss_1)
    return win, cost


def part1():
    """
    Function to solve part 1
    """
    retval = None
    for weapon in weapons:
        for arm in armor:
            for ring1 in rings:
                for ring2 in rings:
                    if ring1 == ring2:
                        continue
                    win, cost = try_battle(
                        player, boss, weapon=weapon, armor=arm, ring1=ring1, ring2=ring2
                    )
                    if win and (not retval or cost < retval):
                        retval = cost
    return retval


def part2():
    """
    Function to solve part 2
    """
    retval = None
    for weapon in weapons:
        for arm in armor:
            for ring1 in rings:
                for ring2 in rings:
                    if ring1 == ring2:
                        continue
                    win, cost = try_battle(
                        player, boss, weapon=weapon, armor=arm, ring1=ring1, ring2=ring2
                    )
                    if not win and (not retval or cost > retval):
                        retval = cost
    return retval


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # ['Hit Points: 100', 'Damage: 8', 'Armor: 2']
    boss["hp"] = int(input_value[0].split(" ")[-1])
    boss["damage"] = int(input_value[1].split(" ")[-1])
    boss["armor"] = int(input_value[2].split(" ")[-1])
    if part == 1:
        return part1()
    return part2()


YEAR = 2015
DAY = 21
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
