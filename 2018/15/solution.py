"""
Advent Of Code 2018 day 15

This one has been fun and frustrating.

I realized quickly that the flexibility of my grid code was a liability (slow).
So I've spent most of my time ripping out the complex() and list(list()) code
from it to focus on dict(tuple(x/y)) grids instead.  So far they have seemed
faster and more flexible (especially for infinite cartesian grid problems)

I then had this working for 4/6 test cases for part 1, and just couldn't get
the last two. I ran the solution below from u/Moriarty82 and compared the output.
I was mostly right, but some of my movements were off in later rounds.

https://github.com/tms7331/adventofcode2018/blob/master/15.ipynb

Reinspecting the rules, I realized I was supposed to sort the players by reading
order at the beginning of each round.  Now I pass 6/6 test cases, and still get
the wrong answer.  Next step compare the output for part 1 to see what I'm doing
wrong.

Okay, comparing the input data runs, I found a bug in the calculation of paths to the
second step.  We were skipping this step if there were less than two shortest paths,
not less than two steps in the shortest path.  if condition fixed, now I match for
turn 1.  back to debugging for turn 2.

The turn 2 issue was with my first step selection.  I was choosing the second step
as the path to determine if there were multiple first steps.  The current solution
is to walk all the steps backwards to find the first step options, but that is slower
I think, maybe, just scan up to the first one that is not on the same line. Well, that
saved 5 seconds, and broke the pervious behavior. backing out.

In turn 24, this guy  (10, 15) is going right instead of left:
#...........#########.##.#....##
#.........G.#########.......#### 200
#...........#########.##......##

Okay, the turn 24 issue, was in my shortest_path function in Grid().  I had left off
the continue for the current_node.position == goal check. So the goal was added to the
closed set, and multiple paths were not possible.  Crossing fingers and hoping
this is the last bug for this one.

Yes, part 1 finished after 3 days. At least I have more faith in Grid() now!

Still a bit slow on part 1 (36 seconds), maybe revisit the first step selection.
Instead of starting at the penultimate step, let's try starting with the second step,
and move out until we have multiple first steps or we reach the penultimate step.

Part 2, solution works for test case 1.

Solution for input data gets:
Elf Power: 34, score: 41552, winner: E, elf_losses: 0

Which AoC said was too low.  Try other test cases to see if something is off there.
All of the test cases run perectly.
the input data ends in the right number of turns, and the remaining hit_points are off
by 15.  The difference appears to be in elves 8 and 19.  Try printing that round to compare.

9/9/2023 update.

I revisited this for a bit after updating the Grid().shortest_paths() function. I thought the
modifications would have eliminated the need to walk the path back to find the possible first
steps, and it seems to not work without that step.  This solution is still super slow, but letting
it run to see if the part 2 answer is right after those changes.  Yeah, answers are off, will need
to debug this one again.

Updated to use networkx.DiGraph() with directional weights to try to force the "reading order" rules
Something is still off, but at least it is fasster.

After deep testing, I found and fixed a type (wrong variable in comparison).  So part1 is getting
the right answer now.

Debugging hasn't turned up anything else, and I'm not sure I'm following my original logic.
My recommendation next time is to rebuild attempt_move from the ground up with careful attention
to the rules.  We must be doing something wrong here.

"""

# import system modules
import time
import networkx

# import my modules
import aoc  # pylint: disable=import-error
from grid import Grid, manhattan_distance  # pylint: disable=import-error

test_games = [
    """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######""",
    """#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######""",
    """#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######""",
    """#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######""",
    """#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######""",
    """#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########""",
]


class PlayerIterator:
    """Iterator for players that skips dead players"""

    def __init__(self, players):
        self.players = players
        self.iter_index = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.iter_index += 1
        if self.iter_index > len(self.players) - 1:
            raise StopIteration
        while not self.players[self.iter_index].alive:
            self.iter_index += 1
            if self.iter_index > len(self.players) - 1:
                raise StopIteration
        return self.players[self.iter_index]


class Players:
    """Container for players"""

    def __init__(self):
        self.players = []

    def append(self, player):
        """Add a player to the container"""
        self.players.append(player)

    def sort(self):
        """Sort players by reading order"""
        self.players.sort()

    def __len__(self):
        return len(self.players)

    def __iter__(self):
        return PlayerIterator(self.players)

    def __str__(self):
        return "Players:\n" + "\n".join(f"  {player}" for player in self) + "\n"


class Player:
    """Class to represent a player"""

    directions = ["n", "w", "e", "s"]

    def __init__(self, container, grid, team, pos, attack=3, hit_points=200):
        self.player_id = len(container)
        self.grid = grid
        self.team = team
        self.pos = pos
        self.stats = {
            "attack": attack,
            "hit_points": hit_points,
            "alive": True,
        }
        self.grid.map[pos] = "."
        self.grid.overrides[pos] = self.team
        self.graph = None
        self.container = container

    @property
    def alive(self):
        """Get alive status"""
        return self.stats["alive"]

    @property
    def opponent(self):
        """Get opponent team"""
        return "E" if self.team == "G" else "G"

    def can_attack(self):
        """Determine if we can attack from current position"""
        return self.square_can_attack(self.pos)

    def opponent_by_position(self, pos):
        """Get opponent by position"""
        for opponent in self.container:
            if opponent.pos == pos:
                return opponent
        return None

    def square_can_attack(self, pos=None):
        """Determine if we can attack from specified position"""
        can_attack = False
        targets = set()
        if not pos:
            pos = self.pos
        neighbors = self.grid.get_neighbors(
            point=pos, directions=self.directions, invalid=["#"]
        )
        # walk neighbors
        for neighbor in neighbors.values():
            # is neighbor opponent
            if self.grid.get_point(neighbor) == self.opponent:
                # we can attack!
                can_attack = True
                targets.add(self.opponent_by_position(neighbor))
        return can_attack, targets

    def find_opponents(self):
        """Find all opponents"""
        opponents = []
        for other in self.container:
            if other.team == self.opponent:
                opponents.append(other)
        opponents.sort(key=lambda opponent: manhattan_distance(self.pos, opponent.pos))
        return opponents

    def open_squares(self):
        """Find all open squares"""
        empty = set()
        for point in self.grid:
            if self.grid.get_point(point=point) == ".":
                empty.add(point)
        return empty

    def build_graph(self):
        """Build movement graph"""
        weights = {"n": 0.01, "w": 0.02, "e": 0.03, "s": 0.04}
        self.graph = networkx.DiGraph()
        empty = self.open_squares()
        for point in empty.union(set([self.pos])):
            self.graph.add_node(point)
        for point in empty.union(set([self.pos])):
            for direction, neighbor in self.grid.get_neighbors(
                point=point, directions=self.directions, invalid=["#", "G", "E"]
            ).items():
                if self.graph.has_node(neighbor):
                    if point == self.pos:
                        self.graph.add_edge(
                            point, neighbor, weight=1 + weights[direction] + 0.5
                        )
                    else:
                        # self.graph.add_edge(point, neighbor, weight=1+weights[direction])
                        self.graph.add_edge(point, neighbor, weight=1)

    def find_open_squares(self, opponents):
        """Find all open squares adjacent to opponents"""
        open_squares = []
        for other in opponents:
            # that are in range of each target; these are the squares which are adjacent
            # (immediately up, down, left, or right) to any target
            neighbors = self.grid.get_neighbors(
                point=other.pos, directions=self.directions, invalid=["#", "G", "E"]
            )
            for neighbor in neighbors.values():
                #  and which aren't already occupied by a wall or another unit.
                if self.graph.has_node(neighbor):
                    open_squares.append(neighbor)
        return open_squares

    def move(self, pos):
        """Move to specified position"""
        self.grid.overrides.pop(self.pos, None)
        self.pos = pos
        self.grid.overrides[self.pos] = self.team

    def eval_points(self, points):
        """Evaluate points to find the one that comes first in reading order"""
        if isinstance(points, set):
            points = list(points)
        if not points:
            return None
        choice = points[0]
        for point in points:
            if point[1] < choice[1]:
                choice = point
            elif point[1] == choice[1] and point[0] < choice[0]:
                choice = point
        return choice

    def attempt_move(self, opponents):
        """Attempt to move towards closest opponent"""
        # Then, the unit identifies all of the open squares (.)
        # If the unit is not already in range of a target,
        # and there are no open squares which are in range of a target, the unit ends its turn.
        self.build_graph()
        closest_distance = float("infinity")
        # find the path to the closest square
        # find shortests paths to any open_squares
        shortest_paths = []
        for open_square in self.find_open_squares(opponents):
            try:
                path = networkx.shortest_path(
                    self.graph, source=self.pos, target=open_square, weight="weight"
                )
            except networkx.exception.NetworkXNoPath:
                continue
            if len(path) < closest_distance:
                closest_distance = len(path)
                shortest_paths = [path]
            elif len(path) == closest_distance:
                shortest_paths.append(path)
        # not any, then we can't move, no problem, end turn
        if not shortest_paths:
            return True

        # identify nearest targets from shortest paths
        nearest_targets = [path[-1] for path in shortest_paths]
        # choose the target that comes first in the original order
        opponent_set = set()
        opponent_dict = {}
        for target in nearest_targets:
            # get the opponent(s) square can attack
            _, opponents = self.square_can_attack(target)
            opponent_dict[target] = opponents
            opponent_set.update([opponent.pos for opponent in opponents])
        # get the closest opponent
        nearest_opponent = self.eval_points(opponent_set)
        # find targets that can attack nearest opponent
        possible_targets = set()
        for target in nearest_targets:
            for opponent in opponent_dict[target]:
                if opponent.pos == nearest_opponent:
                    possible_targets.add(target)
        # which target matches our selection rule
        target = self.eval_points(possible_targets)
        self.graph.add_node(target)
        neighbors = self.grid.get_neighbors(
            point=target, directions=self.directions, invalid=["#", "G", "E"]
        )
        # invert weights, since direction is releative to target
        for neighbor in neighbors.values():
            self.graph.add_edge(neighbor, target, weight=1)
        try:
            path = networkx.shortest_path(
                self.graph, source=self.pos, target=target, weight="weight"
            )
        except networkx.exception.NetworkXNoPath:
            print(f"No path from {self.pos} to {target}")
            self.graph.remove_node(target)
            return False
        self.graph.remove_node(target)
        self.move(path[1])
        return True

    def do_attack(self, targets):
        """Perform attack on target"""
        if isinstance(targets, set):
            targets = list(targets)
        # To attack, the unit first determines all of the targets that are in range
        # print(f"attack({targets})")
        # of it by being immediately adjacent to it.
        # If there are no such targets, the unit ends its turn.
        if not targets:
            return False
        if len(targets) == 1:
            target = targets[0]
        # Otherwise, the adjacent target with the fewest hit points is selected;
        hit_points = [target.stats["hit_points"] for target in targets]
        min_hit_points = min(hit_points)
        min_targets = [
            target for target in targets if target.stats["hit_points"] == min_hit_points
        ]
        # in a tie, the adjacent target with the fewest hit points which is first in
        # reading order is selected.
        for target in self.container:
            if target in min_targets:
                break
        # The unit deals damage equal to its attack power to the selected target, reducing
        # its hit points by that amount.
        # print(f"{self} attacks {target}")
        target.stats["hit_points"] -= self.stats["attack"]
        if target.stats["hit_points"] <= 0:
            target.death()
        return True

    def death(self):
        """Handle death of player"""
        self.stats["alive"] = False
        self.grid.overrides.pop(self.pos, None)
        # self.container.pop(self.container.index(self))

    def play_turn(self):
        """Play a turn for this player"""
        # Each unit begins its turn by identifying all possible targets (enemy units).
        # print(f"{self}: find_opponents")
        opponents = self.find_opponents()
        # If no targets remain, combat ends.
        if not opponents:
            # print(f"{self} did not find an opponent")
            return False

        # print(f"{self}: can attack?")
        can_attack, targets = self.can_attack()
        # Alternatively, the unit might already be in range of a target.
        if not can_attack:
            # print(f"{self}: Can't attack, so moving")
            self.attempt_move(opponents)

        can_attack, targets = self.can_attack()
        # Can we attack now?
        if can_attack:
            # let's do it
            # print(f"{self}: attack")
            self.do_attack(targets)

        return True

    def __lt__(self, other):
        if self.pos[1] < other.pos[1]:
            return True
        if self.pos[1] == other.pos[1] and self.pos[0] < other.pos[0]:
            return True
        return False

    def __str__(self):
        return (
            f"{self.player_id}: {self.team} @ {self.pos} [{self.stats['hit_points']}]"
        )


def play_game(game, elf_attack=3):
    """Function to play the game"""
    players = Players()
    my_map = Grid(game)
    for point in my_map:
        team = my_map.get_point(point)
        if team in ["G", "E"]:
            new_player = Player(players, my_map, team, point)
            if new_player.team == "E":
                new_player.stats["attack"] = elf_attack
            players.append(new_player)
    completed_turns = 0
    game_over = False
    while not game_over:
        # For instance, the order in which units take their turns within a round is
        # the reading order of their starting positions
        # in that round,  <-- rather important I missed this intially
        # regardless of the type of unit or whether other units have moved
        # after the round started
        players.sort()  # sort by reading order
        for player in players:
            if not player.play_turn():
                game_over = True
                break
        if game_over:
            break
        completed_turns += 1
        players.sort()
        map_list = str(my_map).splitlines()
        for line in map_list:
            line += "    "
        for player in players:
            map_list[player.pos[1]] += f" {player.stats['hit_points']}"
        for line in map_list:
            line = line.replace("     ", "    ")
        # print('\n'.join(map_list))
        # part 2 short circuit on first elf death
        for player in players.players:
            if (
                player.team == "E"
                and player.stats["attack"] > 3
                and not player.stats["alive"]
            ):
                game_over = True

    winner = next(iter(players)).team
    remaining_hit_points = [player.stats["hit_points"] for player in players]
    # print(f"Team {winner} wins!")
    # print(f"Outcome: {completed_turns} * {sum(remaining_hit_points)} = {result}")
    # for player in players.players:
    #     print(f"player: {player}, alive: {player.alive}")
    elf_losses = len(
        [
            player
            for player in players.players
            if player.team == "E" and not player.alive
        ]
    )
    return completed_turns * sum(remaining_hit_points), winner, elf_losses


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        # return None
        score, _, elf_losses = play_game(input_value)
        return score

    if part == 2:
        elf_power = 34
        elf_losses = -1
        while elf_losses != 0:
            elf_power += 1
            score, _, elf_losses = play_game(input_value, elf_power)
        return score
    raise ValueError(f"Invalid part specified: {part}")


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018, 15)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    correct = {1: 221754, 2: 41972}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_lines, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if answer[my_part] != correct[my_part]:
            print(f"Incorrect answer {answer[my_part]} != {correct[my_part]}")
