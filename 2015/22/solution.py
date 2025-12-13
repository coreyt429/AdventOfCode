"""

Advent Of Code 2015 day 22

I struggled with this one the first time through.  I thought I had it, and was just cleaning up code
this time.  Wrong!.  my previous solution (script.py if you dig back into the git repo) runs really
fast, and gets the wrong answer.  So I wrote this more elegant OO monstrocity to solve the problem.
So now I get the right answer, just slowly:
(base) PS AdventOfCode> run
Part 1: 953, took 7.938987493515015 seconds
Part 2: 1289, took 44.9357545375824 seconds

I may revisit my old solution and compare, it must just be missing some condition, but with this
solution, I was able to add tracing to the GameState class (sorry, removed it to speed up once
working) to identify logic issues.  In case this helps in future reviews, the last bug fixed,
was not handling loss in the hard mode hp-1 stage.

"""

# import system modules
import logging
import argparse
from heapq import heappop, heappush

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


class GameState:
    """
    class for game state
    """

    def __init__(self, **kwargs):
        self.turn = kwargs["turn"]
        self.mana_spent = kwargs["mana_spent"]
        self.boss = kwargs["boss"]
        self.player = kwargs["player"]
        self.win = kwargs.get("win", False)
        self.lose = kwargs.get("lose", False)
        self.hard_mode = kwargs.get("hard_mode", False)

    def __lt__(self, other):
        """
        Less than
        """
        return self.mana_spent < other.mana_spent

    def __str__(self):
        """
        String
        """
        my_string = f"turn: {self.turn}, "
        my_string += f"mana: {self.mana_spent}, "
        my_string += f"{self.boss}, "
        my_string += f"{self.player} "
        my_string += f"player_turn: {self.is_player_turn()}"
        return my_string

    def is_player_turn(self):
        """
        Function to determine it it is a player turn
        # even turns are player turns starting at 0
        """
        return self.turn % 2 == 0

    def clone(self):
        """
        Clone GameState
        """
        child = GameState(
            turn=int(self.turn),
            mana_spent=int(self.mana_spent),
            boss=self.boss.clone(),
            player=self.player.clone(),
            win=bool(self.win),
            lose=bool(self.lose),
            hard_mode=bool(self.hard_mode),
        )
        return child


class Player:
    """
    Class for player
    """

    def __init__(self, hit_points, mana, spell_history, active_spells):
        """
        Init function
        """
        self.hit_points = hit_points
        self.mana = mana
        self.spell_history = tuple(spell_history)
        self.active_spells = tuple(active_spells)
        self.armor = 0
        self.damage = 0

    def init_damage(self):
        """
        Function to deal init damage of 1 to player at the beginning
        of a turn in part 2
        """
        self.hit_points -= 1

    def cast_spell(self, game_state, spell):
        """
        Cast a spell
        """
        # subtract mana
        self.mana -= spell.cost
        # add spell to spell history
        self.spell_history = tuple(list(self.spell_history) + [spell])
        game_state.mana_spent += spell.cost
        boss = game_state.boss
        if spell.duration == 0:
            # add healing
            self.hit_points += spell.heal
            # damage boss
            boss.hit_points -= spell.damage
            # did we beat the boss?
            if boss.hit_points < 1:
                game_state.win = True
        else:
            self.active_spells = tuple(list(self.active_spells) + [spell.clone()])

    def __lt__(self, other):
        """
        Less than
        """
        return self.hit_points < other.hit_points

    def __str__(self):
        """
        String
        """
        my_string = f"Player: [hp {self.hit_points}, "
        my_string += f"mana: {self.mana}, "
        my_string += f"active_spells:{[str(spell) for spell in self.active_spells]}, "
        my_string += f"spell_history:{[str(spell) for spell in self.spell_history]}]"
        return my_string

    def clone(self):
        """
        Function to clone a spell
        """
        return Player(
            int(self.hit_points),
            int(self.mana),
            (spell.clone() for spell in self.spell_history),
            (spell.clone() for spell in self.active_spells),
        )


class Boss:
    """
    Class for Boss
    """

    def __init__(self, hit_points, attack):
        """
        Init
        """
        self.hit_points = hit_points
        self.attack = attack
        self.damage = 0

    def __str__(self):
        """
        String
        """
        return f"Boss: [hp {self.hit_points}, attack: {self.attack}]"

    def __lt__(self, other):
        """
        Less than
        """
        return self.hit_points < other.hit_points

    def clone(self):
        """
        Function to clone a spell
        """
        return Boss(int(self.hit_points), int(self.attack))


class Spell:
    """
    Spell class
    """

    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.cost = kwargs["cost"]
        self.damage = kwargs["damage"]
        self.heal = kwargs["heal"]
        self.armor = kwargs["armor"]
        self.mana = kwargs["mana"]
        self.duration = kwargs["duration"]

    def clone(self):
        """
        Function to clone a spell
        """
        return Spell(
            name=self.name,
            cost=self.cost,
            damage=self.damage,
            heal=self.heal,
            armor=self.armor,
            mana=self.mana,
            duration=self.duration,
        )

    def __str__(self):
        """
        String
        """
        return f"{self.name}: {self.duration}"


# hit_points,attack populate from input
boss_start = {"hit_points": 0, "attack": 0}

# hit_points,mana
player_start = {"hit_points": 50, "mana": 500}

spells = [
    # Magic Missile costs 53 mana. It instantly does 4 damage.
    Spell(name="Magic Missile", cost=53, damage=4, heal=0, armor=0, mana=0, duration=0),
    # Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
    Spell(name="Drain", cost=73, damage=2, heal=2, armor=0, mana=0, duration=0),
    # Shield costs 113 mana. It starts an effect that lasts for 6 turns.
    # While it is active, your armor is increased by 7.
    Spell(name="Shield", cost=113, damage=0, heal=0, armor=7, mana=0, duration=6),
    # Poison costs 173 mana. It starts an effect that lasts for 6 turns.
    # At the start of each turn while it is active, it deals the boss 3 damage.
    Spell(name="Poison", cost=173, damage=3, heal=0, armor=0, mana=0, duration=6),
    # Recharge costs 229 mana. It starts an effect that lasts for 5 turns.
    # At the start of each turn while it is active, it gives you 101 new mana.
    Spell(name="Recharge", cost=229, damage=0, heal=0, armor=0, mana=101, duration=5),
]


def process_active_spells(game_state):
    """
    Function to process active spells
    """
    # Effects apply at the start of both the player's turns and the boss' turns.
    # Effects are created with a timer (the number of turns they last); at the
    # start of each turn, after they apply any effect they have, their timer is
    # decreased by one. If this decreases the timer to zero, the effect ends.
    # get player and boss
    player = game_state.player
    boss = game_state.boss
    # init new_active_spells
    new_active_spells = []
    # clone active_spells
    active_spells = [spell.clone() for spell in player.active_spells]
    # process active_spells
    while active_spells:
        # get next spell
        spell = active_spells.pop()
        # increase player stats
        # Shield  While it is active, your armor is increased by 7.
        player.armor += spell.armor
        # nothing should do this, is this a problem?
        player.hit_points += spell.heal
        # Recharge  it gives you 101 new mana.
        player.mana += spell.mana
        # damage boss
        # Poison  it deals the boss 3 damage.
        boss.hit_points -= spell.damage
        # decrement duration
        spell.duration -= 1
        # print(f"Active Spell: {spell.name} boss: {boss.hit_points} duration: {spell.duration}")
        # is boss defeated
        if boss.hit_points <= 0:
            game_state.win = True
        # is spell depleted?
        if spell.duration > 0:
            # no, add to new_active_spells
            new_active_spells.append(spell)
    # replace active spells with new_active_spells
    player.active_spells = tuple(new_active_spells)


def do_player_turn(heap, game_state):
    """
    Function to process player turn
    Parameters:
        heap: heapq
        game_state: GameState()

    Returns:
        new_game_state: GameState
    """
    # get active spell names
    active_spell_names = {spell.name for spell in game_state.player.active_spells}
    # init spells_cast
    spells_cast = False
    # Part 2: At the start of each player turn (before any other effects apply),
    # you lose 1 hit point. If this brings you to or below 0 hit points, you lose.
    if game_state.hard_mode:
        game_state.player.init_damage()
        if game_state.player.hit_points <= 0:
            game_state.lose = True
            return game_state
    for spell in spells:
        if not spell.name in active_spell_names:
            # can player afford the spell
            if game_state.player.mana >= spell.cost:
                spells_cast = True
                # clone game state
                new_game_state = game_state.clone()
                # get player and boss
                player = new_game_state.player
                boss = new_game_state.boss
                # increment turns
                new_game_state.turn += 1
                # cast spell:
                player.cast_spell(new_game_state, spell.clone())
                # did we beat the boss?
                if boss.hit_points < 1:
                    new_game_state.win = True
                # print(f"Post spell case: {new_game_state.player}")
                heappush(heap, new_game_state)
    if not spells_cast:
        game_state.lose = 1
    return game_state


def simulate_game(part):
    """
    Function to simulate game
    """
    # init lowest_win_cost and heap
    lowest_win_cost = float("infinity")
    heap = []
    # turn_num, mana_spent, boss, player, player_turn
    # push start state onto heap
    heappush(
        heap,
        GameState(
            turn=0,
            mana_spent=0,
            boss=Boss(boss_start["hit_points"], boss_start["attack"]),
            player=Player(
                player_start["hit_points"], player_start["mana"], tuple(), tuple()
            ),
            hard_mode=bool(part == 2),
        ),
    )
    # process heap
    while heap:
        # pop from heap
        game_state = heappop(heap)
        # have we already won and lowest?
        if game_state.win and game_state.mana_spent < lowest_win_cost:
            # print(game_state)
            lowest_win_cost = game_state.mana_spent
            continue
        # get player and boss
        player = game_state.player
        boss = game_state.boss
        # reset player armor at the beginning of each turn
        player.armor = 0

        # identify skip conditions
        skip_conditions = [
            player.hit_points <= 0,
            game_state.mana_spent > lowest_win_cost,
            game_state.lose,
            game_state.win,
        ]
        if any(skip_conditions):
            continue

        # BEGIN TURN
        # process active spells, and handle win condition
        process_active_spells(game_state)
        if game_state.win:
            lowest_win_cost = min(lowest_win_cost, game_state.mana_spent)
            continue
        # Player turn?
        if game_state.is_player_turn():
            game_state = do_player_turn(heap, game_state)
            if game_state.win:
                lowest_win_cost = game_state.mana_spent
        else:  # boss turn
            player.damage = max(boss.attack - player.armor, 1)
            if player.hit_points > player.damage:
                new_game_state = game_state.clone()
                new_game_state.turn += 1
                new_game_state.player.hit_points -= player.damage
                heappush(heap, new_game_state)
            else:
                game_state.lose = True
    return lowest_win_cost


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # ['Hit Points: 55', 'Damage: 8']
    boss_start["hit_points"] = int(input_value[0].split(" ")[-1])
    boss_start["attack"] = int(input_value[1].split(" ")[-1])
    return simulate_game(part)


YEAR = 2015
DAY = 22
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
