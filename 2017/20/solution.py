"""
Advent Of Code 2017 day 20

"""

# import system modules
from __future__ import annotations
import logging
import argparse
import re
from heapq import heappop, heappush

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import manhattan_distance  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s",
)
logger = logging.getLogger(__name__)

pattern_nums = re.compile(r"(-*\d+)")


class Particle:
    """
    Class to represent particle
    """

    X = 0
    Y = 1
    Z = 2

    def __init__(self, p_id, position, velocity, acceleration):
        """
        Initialize a particle with kinematic parameters.

        Args:
            p_id (int): Identifier for reporting.
            position (tuple[int, int, int]): Initial coordinates.
            velocity (tuple[int, int, int]): Initial velocity vector.
            acceleration (tuple[int, int, int]): Constant acceleration vector.
        """
        self.p_id = p_id
        self.position = list(position)
        self.velocity = list(velocity)
        self.acceleration = acceleration
        self.tick = 0
        self.distance = self.get_distance()

    def move(self):
        """Advance one tick by applying acceleration and velocity."""
        for dimension in [self.X, self.Y, self.Z]:
            self.velocity[dimension] += self.acceleration[dimension]
            self.position[dimension] += self.velocity[dimension]
        self.get_distance()

    def get_distance(self):
        """
        Update and return the particle's Manhattan distance to the origin.
        """
        self.distance = manhattan_distance((0, 0, 0), tuple(self.position))
        return self.distance

    def __str__(self):
        s_p = self.position
        s_v = self.velocity
        s_a = self.acceleration
        my_string = f"p=<{s_p[self.X]},{s_p[self.Y]},{s_p[self.Z]}>, "
        my_string += f"v=<{s_v[self.X]},{s_v[self.Y]},{s_v[self.Z]}>, "
        my_string += f"a=<{s_a[self.X]},{s_a[self.Y]},{s_a[self.Z]}> "
        my_string += f"{self.distance}"
        return my_string

    def __lt__(self, other):
        return self.distance < other.distance


def parse_input(lines):
    """
    Parse puzzle input into Particle objects.
    """
    collection = []
    for idx, line in enumerate(lines):
        nums = [int(string) for string in pattern_nums.findall(line)]
        collection.append(
            Particle(idx, tuple(nums[:3]), tuple(nums[3:6]), tuple(nums[6:9]))
        )
    return collection


def run_simulation(particles):
    """
    Simulate particles to determine which stays closest long term.
    """
    ticks_since_change = 0
    limit = 275000
    closest_p = None
    heap = []
    for particle in particles:
        heappush(heap, (0, particle.distance, 0, 0, particle))
    closest = {}
    while heap:
        ticks, _, _, last_closest, particle = heappop(heap)
        if ticks not in closest:
            closest[ticks] = float("infinity")
        if ticks > 0:
            particle.move()
            ticks_since_change += 1
        if particle.distance < closest[ticks]:
            if not closest_p:
                closest_p = particle
            if closest_p and particle.p_id != closest_p.p_id:
                ticks_since_change = 0
                closest_p = particle
            closest[ticks] = particle.distance
            last_closest = ticks
        if ticks_since_change > limit:
            return closest_p
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
    raise RuntimeError("Shouldn't get here")


def find_collisions(particles):
    """
    Simulate particle removal by collisions.
    """
    last_collision = 0
    limit = 10
    while True:
        last_collision += 1
        collisions = set()
        for particle in particles:
            particle.move()
        for p_1 in particles:
            for p_2 in particles:
                if p_2.p_id == p_1.p_id:
                    continue
                if p_2.position == p_1.position:
                    collisions.add(p_1)
                    collisions.add(p_2)
        if collisions:
            for particle in collisions:
                particles.pop(particles.index(particle))
            last_collision = 0
        if last_collision == limit:
            return len(particles)


def solve(input_value, part):
    """
    Solve both parts of the particle tracking puzzle.
    """
    my_particles = parse_input(input_value)
    if part == 1:
        closest_particle = run_simulation(my_particles)
        return closest_particle.p_id
    return find_collisions(my_particles)


YEAR = 2017
DAY = 20
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
