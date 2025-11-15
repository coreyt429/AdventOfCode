"""
Advent Of Code 2017 day 20

"""

# import system modules
import time
import re
from heapq import heappop, heappush

# import my modules
import aoc  # pylint: disable=import-error
from grid import manhattan_distance  # pylint: disable=import-error

# regex to find numbers
pattern_nums = re.compile(r"(\-*\d+)")


class Particle:
    """
    Class to represent particle
    """

    # x, y, z constants
    X = 0
    Y = 1
    Z = 2

    def __init__(self, p_id, position, velocity, acceleration):
        """
        init particle
        """
        # id
        self.p_id = p_id
        # position
        self.position = list(position)
        # velocity
        self.velocity = list(velocity)
        # acceleration
        self.acceleration = acceleration
        # current tick
        self.tick = 0
        # current distance from (0, 0)
        self.distance = self.get_distance()

    def move(self):
        """
        Function to move particle
        #Increase the X velocity by the X acceleration.
        #Increase the Y velocity by the Y acceleration.
        #Increase the Z velocity by the Z acceleration.
        #Increase the X position by the X velocity.
        #Increase the Y position by the Y velocity.
        #Increase the Z position by the Z velocity.
        """
        # for x, y, and z
        for dimension in [self.X, self.Y, self.Z]:
            # update velocity based on acceleration
            self.velocity[dimension] += self.acceleration[dimension]
            # update position based on velocity
            self.position[dimension] += self.velocity[dimension]
        self.get_distance()

    def get_distance(self):
        """
        function to set self.distance
        """
        # get manhattan_distance using grid.manhattan_distance
        self.distance = manhattan_distance((0, 0, 0), self.position)
        # return self.distance
        return self.distance

    def __str__(self):
        """
        string representation for debugging
        """
        s_p = self.position
        s_v = self.velocity
        s_a = self.acceleration
        my_string = f"p=<{s_p[self.X]},{s_p[self.Y]},{s_p[self.Z]}>, "
        my_string += f"v=<{s_v[self.X]},{s_v[self.Y]},{s_v[self.Z]}>, "
        my_string += f"a=<{s_a[self.X]},{s_a[self.Y]},{s_a[self.Z]}> "
        my_string += f"{self.distance}"
        return my_string

    def __lt__(self, other):
        """
        less than for heap sorting
        """
        return self.distance < other.distance


def parse_input(lines):
    """
    Function to parse input
    """
    # init collection
    collection = []
    # enumerate lines
    for idx, line in enumerate(lines):
        # find all numbers and store as ints
        nums = [int(string) for string in pattern_nums.findall(line)]
        # add particle to collection
        collection.append(
            Particle(idx, tuple(nums[:3]), tuple(nums[3:6]), tuple(nums[6:9]))
        )
    return collection


def run_simulation(particles):
    """
    Function to simulate particle movement
    """
    # init variables
    ticks_since_change = 0
    limit = 275000
    ticks = -1
    closest_p = None
    # init heap, using heapq to sort by current tick, then distance,
    # then ticks since this particle was closes, then last time it was closest,
    # lastly by particle.distance
    heap = []
    # load particles into heap
    for particle in particles:
        heappush(heap, (0, particle.distance, 0, 0, particle))
    closest = {}
    # process heap
    while heap:
        # get next from heap
        ticks, _, _, last_closest, particle = heappop(heap)
        # if there isn't a closest for this tick, then it is you!
        if ticks not in closest:
            closest[ticks] = float("infinity")
        # if not 0, move it
        if ticks > 0:
            particle.move()
            ticks_since_change += 1
        # if this particle is closest so far
        if particle.distance < closest[ticks]:
            # if no closest, then it is you
            if not closest_p:
                closest_p = particle
            # if your still the closest, I don't want to change
            if closest_p and particle.p_id != closest_p.p_id:
                ticks_since_change = 0
                closest_p = particle
            # update distance
            closest[ticks] = particle.distance
            # set last_closest
            last_closest = ticks
            # print(f"{ticks}: Particle {closest_p.p_id} is closest at {closest_p.distance}")
        # if closest hasn't changed since limit, we may have our answer,
        # if not, we need to increase limit
        if ticks_since_change > limit:
            # return closest_packet
            return closest_p
        # push packet back on heap, incrementing ticks
        heappush(
            heap,
            (
                ticks + 1,
                ticks - last_closest,
                particle.distance,
                last_closest,
                particle,
            ),
        )


def find_collisions(particles):
    """
    Function to find collisions
    """
    # last collision was 0 ticks ago
    last_collision = 0
    # how many ticks should we go without a collision to delcare them collision free?
    # lucky guess here, 10 was the magic number for the gap between
    # collisions, and it was my first guess :)
    limit = 10
    # loop
    while True:
        # increment last_collision
        last_collision += 1
        # init collisions
        collisions = set()
        # move all particles 1 tick
        for particle in particles:
            particle.move()
        # walk particles
        for p_1 in particles:
            # walk particles
            for p_2 in particles:
                # don't compare yourself
                if p_2.p_id == p_1.p_id:
                    continue
                # if you are in the same position, add both to collisions
                # this will result in multiple adds for each, but the
                # set will take care of that for us
                if p_2.position == p_1.position:
                    collisions.add(p_1)
                    collisions.add(p_2)
        # if we had collisions
        if collisions:
            # walk collision particles
            for particle in collisions:
                # remove them from particles
                particles.pop(particles.index(particle))
            # reset last_collisiont
            last_collision = 0
        # if we haven't seen a collision in limit ticks
        if last_collision == limit:
            # return length of particles
            return len(particles)


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # parse data
    my_particles = parse_input(input_value)
    # part 1, find closest particle in the long run
    if part == 1:
        closest_particle = run_simulation(my_particles)
        return closest_particle.p_id
    # part 2, find count of particles after collisions
    return find_collisions(my_particles)


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2017, 20)
    # grab input
    input_lines = my_aoc.load_lines()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
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
