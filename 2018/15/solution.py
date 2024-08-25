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

Still a bit slow on part 1 (36 seconds), maybe revisit the first step selection.  Instead of starting
at the penultimate step, let's try starting with the second step, and move out until we
we have multiple first steps or we reach the penultimate step.

"""
# import system modules
import time

# import my modules
import aoc # pylint: disable=import-error
from grid import Grid, manhattan_distance # pylint: disable=import-error
debug = False
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
#########"""
]


class PlayerIterator:
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
    def __init__(self):
        self.players = []
    
    def append(self, player):
        self.players.append(player)
    
    def sort(self):
        self.players.sort()
    
    def __len__(self):
        return len(self.players)
    
    def __iter__(self):
        return PlayerIterator(self.players)
    
    def __str__(self):
        my_string = "Players:\n"
        for player in self:
            print(f"  {player}")
        return my_string
    

class Player:
    directions = ['n','w','e','s']
    def __init__(self, container, grid, team, pos, attack=3, hit_points=200):
        self.player_id = len(container)
        self.grid = grid
        self.team = team
        self.opponent = "E" if team == "G" else "G"
        self.pos = pos
        self.attack = attack
        self.hit_points = hit_points
        self.grid.map[pos] = '.'
        self.grid.overrides[pos] = self.team
        self.container = container
        self.alive = True
    
    def can_attack(self):
        return self.square_can_attack(self.pos)

    def opponent_by_position(self, pos):
        for opponent in self.container:
            if opponent.pos == pos:
                return opponent
        return None

    def square_can_attack(self, pos=None):
        can_attack = False
        targets = set()
        if not pos:
            pos = self.pos
        #if debug: print(f"square_can_attack({pos})")
        neighbors = self.grid.get_neighbors(point=pos, directions=self.directions, invalid=['#'])
        #if debug: print(f"neighbors({neighbors})")
        # walk neighbors
        for neighbor in neighbors.values():
            #if debug: print(f"neighbor({neighbor})")
            # is neighbor opponent
            #if debug: print(f"self.grid.get_point(neighbor)({self.grid.get_point(neighbor)})")
            if self.grid.get_point(neighbor) == self.opponent:
                #if debug: print(f"{pos} can attack {neighbor}")
                # we can attack!
                can_attack = True
                targets.add(self.opponent_by_position(neighbor))
        #if debug: print(f"returning {can_attack}, {[target for target in targets]}")
        return can_attack, targets

    def find_opponents(self):
        opponents = []
        for other in self.container:
            if other.team == self.opponent:
                opponents.append(other)
        opponents.sort(key=lambda opponent: manhattan_distance(self.pos, opponent.pos))
        return opponents

    def find_open_squares(self, opponents):
        open_squares = []
        for other in opponents:
                #if debug: print(f"checking opponent {other}")
                # that are in range of each target; these are the squares which are adjacent
                # (immediately up, down, left, or right) to any target
                neighbors = self.grid.get_neighbors(point=other.pos, directions=self.directions, invalid=['#', 'G', 'E'])
                #if debug: print(f"neighbors: {neighbors}")
                for neighbor in neighbors.values():
                    #if debug: print(f"{neighbor} not in {self.grid.overrides}: {neighbor not in self.grid.overrides}")
                    #  and which aren't already occupied by a wall or another unit.
                    if neighbor not in self.grid.overrides:
                        #if debug: print(f"add open_square: {neighbor}")
                        open_squares.append(neighbor)
        return open_squares

    def find_shortest_paths(self, open_squares, limit=None, **kwargs):
        debug = kwargs.get('debug', False)
        #if debug: print(f"find_shortest_paths({open_squares})")
        if not open_squares:
            return []
        if isinstance(open_squares, set):
            open_squares = list(open_squares)
        if isinstance(open_squares[0], int):
            open_squares = [open_squares]
        #if debug: print(f"open_squares: {open_squares}")
        shortest_paths = []
        shortest_path_length = float('infinity')
        open_squares.sort(key=lambda open_square: manhattan_distance(self.pos, open_square))
        for open_square in open_squares:
            #if debug: print(f"{self}:  trying open_square: {open_square}")
            # I have a feeling that we are also going to need to pass self.grid.overrides.keys() to prevent
            # moving through another player, but we'll see.  the shortest_path function will have to be updated to handle that.
            # this may be resolved with modifications to get_neighbors
            paths = self.grid.shortest_paths(self.pos, open_square, directions=self.directions, invalid=['#','G','E'], max_paths=10, limit=shortest_path_length, debug=debug)
            #if debug: print(f"paths: {paths}")
            # no path?
            if not paths:
                continue
            for path in paths:
                # first or tie?
                if not shortest_paths or len(path) == shortest_path_length:
                    shortest_paths.append(path)
                    shortest_path_length = len(path)
                # new shortest
                if len(path) < shortest_path_length:
                    shortest_paths = [path]
                    shortest_path_length = len(path)
        return shortest_paths
    
    def move(self, pos):
        self.grid.overrides.pop(self.pos, None)
        self.pos = pos
        self.grid.overrides[self.pos] = self.team

    def eval_points(self, points):
       ##if debug: print(f"eval_points({points})")
        if isinstance(points,set):
            points = list(points)
       ##if debug: print(f"eval_points({points})")
        if not points:
            return None
        choice = points[0]
        for point in points:
               ##if debug: print(f"before point:{point}, choice: {choice}")
                if point[1] < choice[1]:
                   ##if debug: print("Y is smaller")
                    choice = point
                elif point[1] == choice[1] and point[0] < choice[0]:
                   ##if debug: print("X is smaller")
                    choice = point
               ##if debug: print(f"after point:{point}, choice: {choice}")
       ##if debug: print(f"return: {choice}")
        return choice
    
    def attempt_move(self, opponents, debug=False):
        #if debug: print(self.grid)
        #if debug: print(f"attempt_move({self}{[opponent.pos for opponent in opponents]})")
        # Then, the unit identifies all of the open squares (.)   If the unit is not already in range of a target,
        # and there are no open squares which are in range of a target, the unit ends its turn.
        open_squares = self.find_open_squares(opponents)
        #if debug: print(f"open_squares: {open_squares}")
        # find the path to the closest square
        # find shortests paths to any open_squares
        shortest_paths = self.find_shortest_paths(open_squares)
        #if debug: print(f"shortest_paths: {shortest_paths}")
        # not any, then we can't move, no problem, end turn
        if not shortest_paths:
            #if debug: print(f"{self}:\n    Can't move")
            return True
        # identify nearest targets from shortest paths
        nearest_targets = [path[-1] for path in shortest_paths]
        #if debug: print(f"nearest_targets: {nearest_targets}")
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
        #if debug: print(f"nearest_opponent: {nearest_opponent}")
        # find targets that can attack nearest opponent
        possible_targets = set()
        for target in nearest_targets:
            for opponent in opponent_dict[target]:
                if opponent.pos == nearest_opponent:
                    possible_targets.add(target)
        # which target matches our selection rule
        #if debug: print(f"possible_targets: {possible_targets}")
        target = self.eval_points(possible_targets)
        #if debug: print(f"target: {target}")
        shortest_paths = self.find_shortest_paths(target)
        #if debug: print(f"I see {len(shortest_paths)} paths to {target}")
        while shortest_paths and len(shortest_paths[0]) > 2:
            last_steps = set([path[-2] for path in shortest_paths])
            #if debug: print(f"last_steps: {last_steps}")
            shortest_paths = self.find_shortest_paths(last_steps)
            #if debug: print(f"shortest_paths: {shortest_paths}")

        first_steps = set([path[1] for path in shortest_paths])
        #if debug: print(f"first_steps: {first_steps}")
        next_step = self.eval_points(first_steps)
        #if debug: print(f"next_step: {next_step}")
        self.move(next_step)

    def do_attack(self, targets):
        if isinstance(targets, set):
            targets = list(targets)
        # To attack, the unit first determines all of the targets that are in range
        #print(f"attack({targets})")
        # of it by being immediately adjacent to it.
        # If there are no such targets, the unit ends its turn.
        if not targets:
            return False
        if len(targets) == 1:
            target = targets[0]
        # Otherwise, the adjacent target with the fewest hit points is selected;
        hit_points = [target.hit_points for target in targets]
        min_hit_points = min(hit_points)
        min_targets = [target for target in targets if target.hit_points == min_hit_points]
        # in a tie, the adjacent target with the fewest hit points which is first in
        # reading order is selected.
        for target in self.container:
            if target in min_targets:
                break
        # The unit deals damage equal to its attack power to the selected target, reducing
        # its hit points by that amount.
        #print(f"{self} attacks {target}")
        target.hit_points -= self.attack
        if target.hit_points <= 0:
            target.death()
        return True
    
    def death(self):
        self.alive = False
        self.grid.overrides.pop(self.pos, None)
        #self.container.pop(self.container.index(self))

    def play_turn(self):
        # Each unit begins its turn by identifying all possible targets (enemy units).
        #print(f"{self}: find_opponents")
        opponents = self.find_opponents()
        # If no targets remain, combat ends.
        if not opponents:
            #print(f"{self} did not find an opponent")
            return False
        
        #print(f"{self}: can attack?")
        can_attack, targets = self.can_attack()
        # Alternatively, the unit might already be in range of a target.
        if not can_attack:
            #print(f"{self}: Can't attack, so moving")
            self.attempt_move(opponents)
        
        can_attack, targets = self.can_attack()
        # Can we attack now?
        if can_attack:
            # let's do it
            #print(f"{self}: attack")
            self.do_attack(targets)

        return True
    
    def __lt__(self, other):
        if self.pos[1] < other.pos[1]:
            return True
        if self.pos[1] == other.pos[1] and self.pos[0] < other.pos[0]:
            return True
        return False

    def __str__(self):
        return f"{self.player_id}: {self.team} @ {self.pos} [{self.hit_points}]"

def play_game(game):
    players = Players()
    my_map = Grid(game)
    for point in my_map:
        team = my_map.get_point(point)
        if team in ['G','E']:
            players.append(Player(players, my_map, team, point))
    #print(my_map)
    #print(f"Initial: {[player.hit_points for player in players]}")
    completed_turns = 0
    game_over = False
    while not game_over:
        # For instance, the order in which units take their turns within a round is
        # the reading order of their starting positions
        # in that round,  <-- rather important I missed this intially
        # regardless of the type of unit or whether other units have moved
        # after the round started
        players.sort() # sort by reading order
        for player in players:
            if not player.play_turn():
                game_over = True
                break
        if game_over:
                break
        completed_turns += 1
        #print(f"Turn {completed_turns}: {[player.hit_points for player in players]}")
        players.sort()
        #print(completed_turns)
        map_list = str(my_map).splitlines()
        for line in map_list:
            line += '    '
        #print(my_map)
        for player in players:
            map_list[player.pos[1]] += f' {player.hit_points}'
        for line in map_list:
            line = line.replace('     ','    ')
        #print('\n'.join(map_list))
          
            
    
    remaining_hit_points = [player.hit_points for player in players]
    result = completed_turns * sum(remaining_hit_points)
    #print(f"Outcome: {completed_turns} * {sum(remaining_hit_points)} = {result}")
    return result

def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 1:
        #return None
        return play_game(input_value)

    if part == 2:
        #for game in test_games:
        #    play_game(game)
        return None
    
    if part == 3:
        return None
    

if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2018,15)
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {
        1: 1,
        2: 2,
        3: 3
    }
    # dict to store answers
    answer = {
        1: None,
        2: None,
        3: None
    }
    # dict to map functions
    funcs = {
        1: solve,
        2: solve,
        3: solve
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
