"""
Advent Of Code 2018 day 24

Part 1 went pretty smoothly, but ran a bit slow. 

I tripped up on the stalemates in part 2, and overlooked it for a while.

If I started at the right boost I got the correct answer, but had issues detcting
the right boost.

minimized sorts to speed things up, and it runs pretty well now.
"""
# import system modules
import time
import re
# import my modules
import aoc # pylint: disable=import-error

class Combatants():
    """
    Player container class, but they aren't really playing
    """
    def __init__(self):
        """Init combatants"""
        # init empty set
        self.armies = set()
        # init phase
        self.phase = 'idle'
        self.groups = {}

    def add_army(self, army):
        """add and army"""
        # add army
        self.armies.add(army)
        # connect army back to Combants
        army.parent = self

    def update(self):
        """
        Update group list caches
        """
        for key in ['all', 'alive', 'selection', 'attack', 'idle']:
            self.groups[key] = []
        for army in self.armies:
            # walk groups
            for group in army.groups:
                # add group
                self.groups['all'].append(group)
                if any((unit.alive for unit in group.units)):
                    self.groups['alive'].append(group)
                    self.groups['selection'].append(group)
                    self.groups['attack'].append(group)
        self.groups['selection'].sort(
            key=lambda g: (g.stats['effective_power'], g.stats['initiative']),
            reverse=True
        )
        self.groups['attack'].sort(key=lambda g: (g.stats['initiative']), reverse=True)

    def selection_phase(self):
        """run selection phase"""
        # set phase to selection
        self.phase = 'selection'
        # walk groups, not selection phase sorting occurs in __iter__
        for group in self:
            # select target
            group.select_target()
        # return phase to idle
        self.phase = 'idle'

    def attack_phase(self):
        """run attack phase"""
        # set phase to attack
        self.phase = 'attack'
        # walk groups
        for group in self:
            # attack
            group.attack()
        # return phase to idle
        self.phase = 'idle'

    def battle(self):
        """fight a battle"""
        self.update()
        # run selections
        self.selection_phase()
        # print()
        # run attacks
        self.attack_phase()
        # print()
        # walk armies
        for army in self:
            # check for loser
            if army.groups_remaining() < 1:
                # don't continue
                return False
        # continue
        return True

    def stalemate(self):
        """
        method to detect stalemates
        """
        # enumerate teams
        teams = set()
        for army in self.armies:
            teams.add(army.team)
        # init dicts
        attacks = {}
        immunities = {}
        can_win = {}
        # walk teams
        for team in teams:
            # init sets
            attacks[team] = set()
            immunities[team] = set()
            can_win[team] = False
        # walk groups
        for group in self.groups['alive']:
            # populate attacks and immunities
            attacks[group.army.team].add(group.stats['attack_type'])
            immunities[group.army.team].update(group.mods['immunities'])
        # walk groups
        for group in self.groups['alive']:
            # get opposing team
            opponent = [team for team in teams if team != group.army.team][0]
            # walk attacks
            for attack in attacks[group.army.team]:
                # if attack is not blocked by an immunity
                if attack not in immunities[opponent]:
                    # group can win
                    can_win[group.army.team] = True
        return not any(can_win.values())

    def war(self):
        """fight a war"""
        counter = 0
        # print()
        # print('='*50)
        # print(f"Begin:\n{self}")
        # init previous_scores
        previous_scores = [army.units_remaining() for army in self]
        # do battle until there is a winner
        idle_counter = 0
        while self.battle():
            counter += 1
            # print(f"{'-'*50}\nAfter battle {counter}:\n{self}")
            # if counter > 3500:
                # print("Counter break")
                # break
            # get scores after battle
            scores = [army.units_remaining() for army in self]
            # if there are only 3 scores between previous_scores and scores
            # then one team is no longer able to do damage and will lose
            if len(set(previous_scores + scores)) == 3:
                idle_counter += 1
                if idle_counter > 1:
                    if self.stalemate():
                        return Army(team='stalemate')
                    # print("Only one team losing units")
                    for army in self:
                        # print(f"{army.team}: {army.units_remaining()} in {previous_scores}")
                        if army.units_remaining() in set(previous_scores) & set(scores):
                            # return winner
                            return army
            # update previous_scores
            previous_scores = scores
        # print(f"{'-'*50}\nEnd:\n{self}\n")
        # walk armies to find winner
        for army in self:
            # if army has units left they one
            if army.units_remaining() > 0:
                # return winner
                return army
        # we shouldn't get here, but lets return something to make pylint happy
        return False

    def __iter__(self):
        """
        Iterate Combatants
        
        this is the magic to getting the order right

        We adjust the sorting rules based on phase.
        """
        if self.phase == 'idle':
            return iter(self.armies)
        return iter(self.groups[self.phase])

    def __str__(self):
        """String"""
        # save phase, in case the caller needs it back
        phase = self.phase
        # set to idle so we get armies when we iterate instead of groups
        self.phase = 'idle'
        # init my_string
        my_string = ''
        # walk armies
        for army in self:
            # add army to string
            my_string += str(army)
        # restore phase
        self.phase = phase
        # return result
        return my_string

class Army():
    """
    Container class for groups
    """
    def __init__(self, team=None):
        """Init Function"""
        self.team = team
        self.groups = []
        self.parent = None

    def add_group(self, group):
        """
        add a group
        """
        # connect group to army
        group.army = self
        # add group
        self.groups.append(group)
        # set groups id for printing
        group.g_id = self.groups.index(group) + 1

    def groups_remaining(self):
        """
        return groups with live units
        """
        # init remainig
        remaining = 0
        # walk groups
        for group in self.groups:
            # if group has live units
            if group.stats['unit_count'] > 0:
                # increment
                remaining += 1
        # return
        return remaining

    def units_remaining(self):
        """
        calculate remaining live units
        """
        # init remaining
        remaining = 0
        # walk groups
        for group in self.groups:
            # increment
            remaining += group.stats['unit_count']
        return remaining

    def __str__(self):
        """String"""
        # init my_string
        my_string = f"{self.team}:\n"
        # walk groups
        for group in self.groups:
            # add group data
            my_string += f"{group}: {group.stats['unit_count']} units each with "
            my_string += f"{group.stats['hit_points']} hit_points ("
            if group.mods['immunities']:
                my_string += f"immune to {', '.join(group.mods['immunities'])}; "
            if group.mods['weaknesses']:
                my_string += f"weak to {', '.join(group.mods['weaknesses'])}"
            my_string += f")  with an attack that does {group.stats['attack_damage']} "
            my_string += f"{group.stats['attack_type']} "
            my_string += f"damage at initiative {group.stats['initiative']}, "
            my_string += f"effective_power: {group.stats['effective_power']}\n"
        # return
        return my_string

class Group():
    """
    Container class for Units
    """
    def __init__(self, **kwargs):
        """Init Function"""
        self.g_id = None
        self.units = []
        self.army = None
        self.stats = {}
        self.stats['hit_points'] = kwargs.get('hit_points')
        self.stats['attack_damage'] = kwargs.get('attack_damage')
        self.stats['attack_type'] = kwargs.get('attack_type')
        self.stats['initiative'] = kwargs.get('initiative')
        self.stats['unit_count'] = 0
        self.mods = {
            "weaknesses": [],
            "immunities": []
        }
        self.attacking = None
        self.defending = None
        mods = kwargs.get('mods').split('; ')
        # walk mods
        for mod in mods:
            if mod.startswith('weak'):
                self.mods['weaknesses'] = mod.split(' to ')[1].split(', ')
            if mod.startswith('immune'):
                self.mods['immunities'] = mod.split(' to ')[1].split(', ')
        for _ in range(kwargs.get('units')):
            self.add_unit(Unit())

    def add_unit(self, unit):
        """add a unit"""
        # attach to group
        unit.group = self
        # add unit
        self.units.append(unit)
        # increment unit count
        self.stats['unit_count'] += 1
        # recalc effective_power
        self.update_effective_power()

    # def unit_count(self):
    #     """gets count of live units"""
    #     return self.stats['unit_count']
    #     # return len([unit for unit in self.units if unit.alive])

    def update_effective_power(self):
        """calculate effective_power"""
        self.stats['effective_power'] = self.stats['unit_count'] * self.stats['attack_damage']

    def get_enemies(self):
        """find enemies"""
        # Filter out same team groups using filter
        enemy_groups = list(
            filter(
                lambda group: group.army.team != self.army.team, self.army.parent.groups['alive']
            )
        )
        return enemy_groups

    def calc_attack(self, enemy):
        """calculate attack"""
        if self.stats['attack_type'] in enemy.mods['immunities']:
            return 0
        # init effective_damage
        effective_damage = self.stats['effective_power']
        # However, if the defending group is immune to the attacking group's attack type,
        # the defending group instead takes no damage;

        # if the defending group is weak to the attacking group's attack type, the defending
        # group instead takes double damage.
        if self.stats['attack_type'] in enemy.mods['weaknesses']:
            effective_damage *= 2
        # return
        return effective_damage

    def select_target(self):
        """
        3) The attacking group chooses to target the group in the enemy army to which it would
            deal the most damage (after accounting for weaknesses and immunities,
            but not accounting for whether the defending group has enough units to actually
            receive all of that damage).

        4) If an attacking group is considering two defending groups to which it would deal
        equal damage, it chooses to target the defending group with the largest effective power;
        5) if there is still a tie, it chooses the defending group with the highest initiative.
        If it cannot deal any defending groups damage, it does not choose a target.
        """
        # 6) Defending groups can only be chosen as a target by one attacking group.
        # get target groups
        target_groups = list(filter(lambda group: not group.defending, self.get_enemies()))

        # init max values
        max_attack = 0
        max_targets = []
        # walk targets
        for group in target_groups:
            # get effective_attack
            effective_attack = self.calc_attack(group)
            # we can't attack if we will not do damage
            if effective_attack < 1:
                continue
            # print(f"{self} would deal defending group {group.g_id} {effective_attack} damage")
            # if new max, replace
            if effective_attack > max_attack:
                max_attack = effective_attack
                max_targets = [group]
            # if tied max update
            if effective_attack == max_attack:
                max_targets.append(group)
        # if max_attack > 0 and there are targets
        if  max_attack and max_targets:
            # sort targets by effective_power and initiative
            max_targets.sort(
                key=lambda g: (g.stats['effective_power'], g.stats['initiative']),
                reverse=True
            )
            # grab the first target
            target = max_targets[0]
            # set attacking
            self.attacking = target
            # set defending
            target.defending = self

    def attack(self):
        """attack"""
        # nothing to do?
        if not self.attacking:
            return
        target = self.attacking
        if self.stats['unit_count'] == 0:
            self.attacking = None
            target.defending = None
            return
        # Infection group 2 attacks defending group 2, killing 84 units
        effective_attack = self.calc_attack(target)
        # two versions of this, if you uncomment the print lines, swap to teh second version
        target.defend(effective_attack)
        # units_killed = target.defend(effective_attack)
        # print(f"{self} attacks defending group {target.g_id}, killing {units_killed} units")
        # reset attacking and defending
        self.attacking = None
        target.defending = None

    def defend(self, damage):
        """defend"""
        # init killed
        killed = 0
        # loop until damage will no longer kill
        while damage > self.stats['hit_points']:
            # walk units
            for unit in self.units:
                if unit.alive:
                    # kill unit
                    killed += 1
                    unit.alive = False
                    self.stats['unit_count'] -= 1
                    # recalc effective_power
                    self.update_effective_power()
                    # decrement damage
                    damage -= self.stats['hit_points']
                    break # only kill one per pass, so we recheck damage
            # if all units are dead, break the loop
            if not any((unit.alive for unit in self.units)):
                break
        # return kill count
        return killed

    def __str__(self):
        """String"""
        my_string = f"{self.army.team} group {self.g_id}"
        return my_string

class Unit():
    """
    Class for fighting units
    Units within a group all have the same hit points (amount of damage a unit can take
    before it is destroyed), attack damage (the amount of damage each unit deals), an attack
    type, an initiative (higher initiative units attack first and win ties), and sometimes
    weaknesses or immunities. Here is an example group:

    Note, I should probably do away with this class, and use a dict for Unit, but it works
    so here it is.
    """
    def __init__(self):
        """Init"""
        self.alive = True
        self.group = None

    def is_alive(self):
        """useless method 1 to make pylint happy"""
        return self.alive

    def get_group(self):
        """useless method 2 to make pylint happy"""
        return self.group

def parse_data(lines):
    """Parse input data"""
    # init combatants
    combatants = Combatants()
    # init regexes
    pattern_army = re.compile(r'(.*):')
    pg_str = r'(\d+) uni.*th (\d+) h.*ts\s*\(?([^)]*?)\)?\s*wi.*es (\d+) (\w+) da.*ve (\d+)'
    pattern_group = re.compile(pg_str)
    # walk lines
    for line in lines:
        # match army pattern
        match = pattern_army.match(line)
        if match:
            # create new army
            current_army = Army(team=match.group(1))
            # add to compatants
            combatants.add_army(current_army)
        # match group pattern
        match = pattern_group.match(line)
        if match:
            # add new group
            current_army.add_group(
                Group(
                    units = int(match.group(1)),
                    hit_points = int(match.group(2)),
                    mods = match.group(3),
                    attack_damage = int(match.group(4)),
                    attack_type = match.group(5),
                    initiative = int(match.group(6))
                )
            )
    # return
    return combatants

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # Part 1
    if part == 1:
        # parse data, and build armies
        armies = parse_data(input_value)
        armies.update()
        # get winner
        winner = armies.war()
        # print(winner)
        # return units remaining
    # Part 2
    if part == 2:
        # manual testing shows a range of 12 (Infection won) and 25 (Immune won)
        # incremental testing indicated 16 is the appropriate boost
        # narrowing range to minimize test time
        # 3302 too low
        # 36856 not the right answer
        # okay, so 16 actually stated a series of stalemates that needed to be detected
        # 35 is the answer
        for boost in range(35, 36):
            # parse data, and build armies
            armies = parse_data(input_value)
            armies.update()
            for army in armies:
                if army.team == 'Immune System':
                    # print(f"Boosting {army.team} by {boost} with {army.units_remaining()} units")
                    for group in army.groups:
                        group.stats['attack_damage'] += boost
                        group.update_effective_power()
                        # print(f"{group}: {group.stats['attack_damage']}")
                    # print()
            # get winner
            winner = armies.war()
            # print(f"{winner.team} Wins")
            if winner.team == "Immune System":
                break
    # print(armies)
    return winner.units_remaining()


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018,24)
    #input_text = my_aoc.load_text()
    #print(input_text)
    input_lines = my_aoc.load_lines()
    # print(input_lines)
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
