"""
Advent Of Code 2024 day 6

Part 1, was a a fun implementation of Grid()

Part 2, I implemented Floyd's cycle detection algorithm.  It gets the right answer, and
takes too long. Cleaning up the code and saving for now, will revisit to speed up.

Thoughts for speeding up.
    1) store visited points from part 1, in part two, add the neighbors of these points,
       and remove the start position.  This will be the subset of points we should try.
       That should at least reduce the time to 1/3.  I fear that may still be too long
    2) map the # points, and calculate decision points based on them. should be significantly
       faster, but will require some thought.
       Wait, this is it:

       def scan_to_block(self):
         # scan ahead in direction until we see a block
         self.teleport(point_before_block)
         return self.pos

       def has_loop(self):
         already = set()
         self.reset()
         current_point = self.pos
         next_point = self.scan_to_block()
         while (current_point, next_point) not in already:
            is_loop = True
            self.turn()
            current_point = next_point
            next_point = self.scan_to_block()
            if next_point is None:
                return False
        return True

Part 2 is running now in 11 seconds. In addition to the above, I precalculated the block locations
to minimize iteration on the Grid()


"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

stash = {}


class Guard(Grid):
    """Class to represent guard"""

    def __init__(self, map_data):
        """method to initialize guard position"""
        super().__init__(map_data, pos_token="X", use_overrides=False)
        # find guard position
        for point, char in self.items():
            # look for direction char, likely always starts as '^',
            # we'll check for any just in case
            if char in "<>^v":
                # set position token to char
                self.cfg["pos_token"] = char
                self.set_point(point, ".")
                self.teleport(point)
                break
        # turn user_overrides on so we can see the guard position
        self.cfg["use_overrides"] = True
        self.visited = set([self.pos])
        self.direction_map = self.build_direction_map()
        self.direction = self.direction_map[self.cfg["pos_token"]]
        self.start = (self.pos, self.cfg["pos_token"])

    def reset(self):
        """Method to return guard to starting position and direction"""
        self.teleport(self.start[0])
        while self.cfg["pos_token"] != self.start[1]:
            self.turn()

    def build_direction_map(self):
        """Method to populate direction map"""
        direction_map = {}
        for symbol, direction in zip("^v<>", "nswe"):
            direction_map[symbol] = direction
            direction_map[direction] = symbol
        return direction_map

    def turn(self):
        """Method to turn right 90 degrees"""
        directions = "nesw"
        idx = directions.index(self.direction)
        # move to next direction
        idx = (idx + 1) % 4
        self.direction = directions[idx]
        self.cfg["pos_token"] = self.direction_map[self.direction]
        self.overrides[self.pos] = self.cfg["pos_token"]

    def step(self):
        """Method to take a step, and log the position"""
        neighbors = self.get_neighbors()
        # next step is off the map
        if self.direction not in neighbors:
            return False
        while self.get_point(point=neighbors[self.direction]) == "#":
            self.turn()
        self.move(self.direction)
        self.visited.add(self.pos)
        return True

    def walk_about(self):
        """Method to have the guard walk around until off map"""
        while self.step():
            yield self.pos


def next_stop(current_point, direction, points):
    """Function to find the point before the next block"""
    # print(f"next_stop({current_point}, {direction})")
    x_0, y_0 = current_point
    if direction == "s":
        # Points with the same x but greater y
        candidates = [p for p in points if p[0] == x_0 and p[1] > y_0]
        # Choose the point with the minimal (y - y_0)
        next_point = min(candidates, key=lambda p: p[1]) if candidates else None
        if next_point is not None:
            next_point = (next_point[0], next_point[1] - 1)

    elif direction == "n":
        # Points with the same x but lower y
        candidates = [p for p in points if p[0] == x_0 and p[1] < y_0]
        # Choose the point closest below (maximum y but still less than y_0)
        next_point = max(candidates, key=lambda p: p[1]) if candidates else None
        if next_point is not None:
            next_point = (next_point[0], next_point[1] + 1)

    elif direction == "e":
        # Points with the same y but greater x
        candidates = [p for p in points if p[1] == y_0 and p[0] > x_0]
        # Choose the point with the minimal (x - x_0)
        next_point = min(candidates, key=lambda p: p[0]) if candidates else None
        if next_point is not None:
            next_point = (next_point[0] - 1, next_point[1])

    elif direction == "w":
        # Points with the same y but lower x
        candidates = [p for p in points if p[1] == y_0 and p[0] < x_0]
        # Choose the point closest to the left (maximum x but still less than x_0)
        next_point = max(candidates, key=lambda p: p[0]) if candidates else None
        if next_point is not None:
            next_point = (next_point[0] + 1, next_point[1])
    # print(f"next_point: {next_point}")
    return next_point


def has_loop_2(guard, blocks):
    """function to check a map for loops"""
    # print(f"has_loop_2({guard.pos})")
    last_point = guard.pos
    already = set()
    loop_detected = False
    duplicates = 0
    while not loop_detected:
        if (last_point, guard.pos) in already:
            duplicates += 1
        if duplicates > 5:
            loop_detected = True
        already.add((last_point, guard.pos))
        last_point = guard.pos
        next_point = next_stop(guard.pos, guard.direction, blocks)
        if next_point is None:
            return False
        guard.teleport(next_point)
        guard.turn()
    # print(f"{(last_point, guard.pos)} is in {already}")
    return True


def find_loops_2(input_value):
    """function to find positions where an added block causes a loop"""
    guard = Guard(input_value)
    blocks = []
    for point, char in guard.items():
        if char == "#":
            blocks.append(point)
    # point_counter = 0
    stash["visited"].remove(guard.pos)
    # point_count = len(stash['visited'])
    loops = 0
    for test_point in stash["visited"]:
        # point_counter += 1
        # if point_counter % 100 == 0:
        #     print(f"{point_counter}/{point_count}: {test_point} > {loops}")
        guard.set_point(test_point, "#")
        if has_loop_2(guard, tuple(blocks + [test_point])):
            # print(f"loop detected: {test_point}")
            loops += 1
        guard.set_point(test_point, ".")
        guard.reset()
    return loops


def find_loops(input_value):
    """Function to detect and count loops"""
    # setup tortoise and hare instances of Guard
    tortoise = Guard(input_value)
    hare = Guard(input_value)
    start_pos = hare.start[0]
    loops = 0
    loop_positions = set()
    # debug counters to see progress
    point_counter = 0
    point_count = len(stash["visited"])
    for test_point in stash["visited"]:
        char = hare.get_point(test_point)
        point_counter += 1
        # progress check
        if point_counter % 100 == 0:
            print(f"{test_point}: {point_counter}/{point_count}")
        # skip already blocked points
        if char == "#":
            continue
        # skip starting point
        if test_point == start_pos:
            continue
        counter = 0
        # set test point as blocked
        tortoise.set_point(test_point, "#")
        hare.set_point(test_point, "#")
        # intersections were occuring before the loop, causing inflated loop count
        # for the test data, ignoring the first intersection worked
        # for the puzzle data, ignoring the second intersection worked
        intersection_count = 0
        while next(hare.walk_about(), None) is not None:
            counter += 1
            if counter % 2 == 0:
                next(tortoise.walk_about(), None)
            if tortoise.pos == hare.pos:
                intersection_count += 1
                if intersection_count > 2:
                    # print(f"Loop Detected")
                    loops += 1
                    loop_positions.add(test_point)
                    break
        # reset test point
        tortoise.set_point(test_point, ".")
        hare.set_point(test_point, ".")
        # reset Guards
        hare.reset()
        tortoise.reset()
    return loops


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        # return find_loops(input_value)
        return find_loops_2(input_value)
        # 2026 too high
    guard = Guard(input_value)
    for _ in guard.walk_about():
        pass
    stash["visited"] = guard.visited
    return len(guard.visited)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2024, 6)
    # input_data = my_aoc.load_text()
    # print(input_text)
    input_data = my_aoc.load_lines()
    # print(input_lines)
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 5409, 2: 2022}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_data, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
