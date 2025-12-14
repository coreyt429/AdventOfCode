"""
Advent Of Code 2022 day 19

"""

# import system modules
import logging
import re
import argparse
from heapq import heappop, heappush


# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


elements = ["ore", "clay", "obsidian", "geode"]
ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3


def tadd_old(a, b):
    """
    Add two tuples element-wise.
    Takes two tuples of equal length and returns a new tuple where each element
    is the sum of the corresponding elements from the input tuples.
    :param a: First tuple of numeric values
    :param b: Second tuple of numeric values (must be same length as a)
    :return: A new tuple containing element-wise sums
    :raises: ValueError if tuples have different lengths (from zip)
    Example:
        >>> tadd((1, 2, 3), (4, 5, 6))
        (5, 7, 9)
    """
    return tuple(x + y for x, y in zip(a, b))


def tadd(a, b):
    """simpe function to add two 4-tuples"""
    return (
        a[0] + b[0],
        a[1] + b[1],
        a[2] + b[2],
        a[3] + b[3],
    )


def estimate_geodes(geodes, geode_robots, minutes):
    """
    Heuristic function for A* search
    Estimate the maximum number of geodes that can be produced
    Assuming a new geode robot is built every minute
    """
    return geodes + geode_robots * minutes + minutes * (minutes - 1) // 2
    # potential_geodes = geodes
    # for _ in range(minutes):
    #     potential_geodes += geode_robots
    #     geode_robots += 1
    # return potential_geodes


class RobotFactory:
    """
    Class to represent a robot factory
    """

    def __init__(self, blueprint):
        # logger.debug("Initialized RobotFactory with blueprint: %s", blueprint)
        values = re.findall(r"(\d+)", blueprint)
        self._id = int(values[0])
        self.robots = {
            "ore": (-1 * int(values[1]), 0, 0, 0),
            "clay": (-1 * int(values[2]), 0, 0, 0),
            "obsidian": (-1 * int(values[3]), -1 * int(values[4]), 0, 0),
            "geode": (-1 * int(values[5]), 0, -1 * int(values[6]), 0),
        }
        self.max_geodes = 0
        self.target_time = 24
        # max resources you could ever need in a *single minute*
        self.max_cost = [
            0,
            0,
            0,
            0,
        ]  # ORE, CLAY, OBSIDIAN, GEODE (GEODE usually irrelevant here)

        for cost in self.robots.values():
            for i in range(3):  # only care about ORE, CLAY, OBSIDIAN
                # costs are stored as negative
                self.max_cost[i] = max(self.max_cost[i], -cost[i])

    @property
    def quality_level(self):
        """
        Function to get the quality level
        """
        return self._id * self.max_geodes

    def get_robot_cost(self, robot_type):
        """
        Function to get the cost of a robot
        """
        return self.robots[robot_type]

    def can_build_robot(self, robot_type, inventory):
        """
        Function to check if a robot can be built
        """
        cost = self.get_robot_cost(robot_type)
        # logger.debug(
        #     "Checking if can build robot: %s with inventory: %s and cost: %s",
        #     robot_type,
        #     inventory,
        #     cost,
        # )
        return all(inventory[i] + cost[i] >= 0 for i in range(4))

    def calc_limits(self, minutes, inventory, robots):
        """
        Function to calculate limits for pruning
        """
        time_left = self.target_time - minutes
        max_ore_spend = time_left * self.max_cost[ORE]
        max_clay_spend = time_left * self.max_cost[CLAY]
        max_obs_spend = time_left * self.max_cost[OBSIDIAN]

        inventory = (
            min(inventory[ORE], max_ore_spend),
            min(inventory[CLAY], max_clay_spend),
            min(inventory[OBSIDIAN], max_obs_spend),
            inventory[GEODE],  # geodes are the goal, don't cap
        )
        robots = (
            min(robots[ORE], self.max_cost[ORE]),
            min(robots[CLAY], self.max_cost[CLAY]),
            min(robots[OBSIDIAN], self.max_cost[OBSIDIAN]),
            robots[GEODE],  # no cap; more geode robots always good
        )
        return time_left, inventory, robots

    def simulate(self):
        """
        Function to simulate the robot factory
        """
        # logger.debug("Simulating RobotFactory ID: %s", self._id)
        # Simulation logic goes here
        heap = []
        inventory = (0, 0, 0, 0)
        robots = (1, 0, 0, 0)
        heappush(heap, (0, 0, inventory, robots))
        visited = set()
        while heap:
            neg_potential, minutes, inventory, robots = heappop(heap)
            potential = -1 * neg_potential
            # logger.debug("Minute: %s, Inventory: %s, Robots: %s, Potential: %s, Max Geodes: %s",
            #             minutes, inventory, robots, potential, self.max_geodes)
            time_left, inventory, robots = self.calc_limits(minutes, inventory, robots)
            # logger.debug("After calc_limits - Time left: %s, Inventory: %s, Robots: %s",
            #              time_left, inventory, robots)
            if time_left < 0:
                continue

            # upper bound from this state
            upper_bound = estimate_geodes(
                inventory[GEODE],
                robots[GEODE],
                time_left,
            )
            # logger.debug("Upper bound estimate: %s", upper_bound)
            if upper_bound <= self.max_geodes:
                continue

            if (inventory, robots) in visited:
                continue
            visited.add((inventory, robots))

            if 0 < potential <= self.max_geodes:
                continue
            if minutes == self.target_time:
                continue
            new_inventory = tadd(inventory, robots)
            self.max_geodes = max(self.max_geodes, new_inventory[GEODE])
            potential = estimate_geodes(
                new_inventory[GEODE], robots[GEODE], self.target_time - (minutes + 1)
            )
            # if we can build a geode robot, always do it
            if self.can_build_robot("geode", inventory) and time_left > 1:
                # logger.debug("Building geode robot")
                # update by new_inventory
                updated_inventory = tadd(new_inventory, self.get_robot_cost("geode"))
                updated_robots = list(robots)
                updated_robots[elements.index("geode")] += 1
                potential = estimate_geodes(
                    updated_inventory[GEODE],
                    updated_robots[GEODE],
                    self.target_time - (minutes + 1),
                )
                heappush(
                    heap,
                    (
                        -1 * potential,
                        minutes + 1,
                        updated_inventory,
                        tuple(updated_robots),
                    ),
                )
                continue  # always build geode if we can
            # only then explore the wait branch
            heappush(heap, (-potential, minutes + 1, new_inventory, robots))
            # build conditions, work with start inventory,
            if time_left < 1:
                continue
            # not new_inventory for deciding if we can build
            for element_idx, element in enumerate(elements[:-1]):
                # logger.debug("Considering building robot: %s, inventory: %s", element, inventory)
                if (
                    robots[element_idx] >= self.max_cost[element_idx]
                    and element != "geode"
                ):
                    # logger.debug("Skipping building %s robot as we have enough", element)
                    continue
                # check by inventory
                if self.can_build_robot(element, inventory):
                    # logger.debug("Building robot: %s", element)
                    # update by new_inventory
                    updated_inventory = tadd(
                        new_inventory, self.get_robot_cost(element)
                    )
                    updated_robots = list(robots)
                    updated_robots[elements.index(element)] += 1
                    potential = estimate_geodes(
                        updated_inventory[GEODE],
                        updated_robots[GEODE],
                        self.target_time - (minutes + 1),
                    )
                    heappush(
                        heap,
                        (
                            -1 * potential,
                            minutes + 1,
                            updated_inventory,
                            tuple(updated_robots),
                        ),
                    )

    def __str__(self):
        """string representation"""
        return f"RobotFactory ID: {self._id}, Robots: {self.robots}, Max Geodes: {self.max_geodes}"


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    if part == 2:
        max_geodes_product = 1
        for line in input_value[:3]:
            factory = RobotFactory(line)
            factory.target_time = 32
            # logger.debug("Starting simulation for Factory %s", factory)
            factory.simulate()
            max_geodes_product *= factory.max_geodes
            # logger.debug("Factory ID %s produced max geodes: %s", factory._id, factory.max_geodes)
        return max_geodes_product

    quality_level = 0
    for line in input_value:
        factory = RobotFactory(line)
        # logger.debug("Starting simulation for Factory %s", factory)
        factory.simulate()
        quality_level += factory.quality_level
        # logger.debug("Factory ID %s produced max geodes: %s", factory._id, factory.max_geodes)
    return quality_level


YEAR = 2022
DAY = 19
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
