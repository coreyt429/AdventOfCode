"""
Advent Of Code 2019 day 14

This one was fairly straight forward.  Part 1 was easy.  Part 2, I had to optimize
a bit to minimize loops.

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


class NanoFactory:
    """
    Class to represent a nano factory
    """

    def __init__(self, rules_text):
        """init"""
        # init inventory
        self.inventory = {}
        # parse data to rules, also sets inventory
        self.rules = self.parse_data(rules_text.splitlines())
        # init ore collected and production
        self.ore_collected = 0
        self.production = {}
        # init production elements based on inventory
        for element in self.inventory:
            self.production[element] = 0

    def parse_data(self, lines):
        """Parse text data"""
        # init rules
        rules = []
        # iterate over lines
        for line in lines:
            # split into input/output sections
            input_str, output = line.split(" => ")
            # split inputs
            inputs = input_str.split(", ")
            # split outputs
            outputs = output.split(", ")
            # init rule
            rule = {"inputs": [], "outputs": []}
            # iterate over inputs
            for input_str in inputs:
                # split quantity and element
                quantity, element = input_str.split(" ")
                # convert to int
                quantity = int(quantity)
                # add input to rule
                rule["inputs"].append({"quantity": quantity, "element": element})
                # init inventory for element
                self.inventory[element] = 0
            # iterate over outputs
            for output in outputs:
                # split quantitiy and element
                quantity, element = output.split(" ")
                # convert to int
                quantity = int(quantity)
                # add output to rule
                rule["outputs"].append({"quantity": quantity, "element": element})
                # init inventory for element
                self.inventory[element] = 0
            # append rule
            rules.append(rule)
        # return rules
        return rules

    def collect_ore(self, quantity=1):
        """collect ore"""
        # increment stats
        self.ore_collected += quantity
        self.inventory["ORE"] += quantity
        self.production["ORE"] += quantity
        return True

    def make(self, quantity, element):
        """Make element"""
        # print(f"Making {quantity} {element}")
        production_quantity = 0
        # return true if we already have enough
        if self.inventory[element] >= quantity:
            return True
        # init wip
        wip = {}
        # if ore, just collect some
        if element == "ORE":
            return self.collect_ore(quantity)
        # get rule
        rule = self.get_rule(element)
        # print(rule)
        # iterate over outputs
        for output in rule["outputs"]:
            # find target output
            if output["element"] == element:
                # init prod_qty
                prod_qty = 1
                # set production_quantity
                production_quantity = output["quantity"]
                # if we don't have enough, with 1 prod_qty, start with close guess
                if output["quantity"] * prod_qty + self.inventory[element] < quantity:
                    prod_qty += (quantity - self.inventory[element]) // output[
                        "quantity"
                    ] - 1
                # loop until production is satisfactory
                while (
                    output["quantity"] * prod_qty + self.inventory[element] < quantity
                ):
                    prod_qty += 1
        # iterate over inputs
        for input_val in rule["inputs"]:
            # if we don't have enough
            if self.inventory[input_val["element"]] < input_val["quantity"] * prod_qty:
                # make it
                if not self.make(
                    input_val["quantity"] * prod_qty, input_val["element"]
                ):
                    return False
            # take from inventory
            self.inventory[input_val["element"]] -= input_val["quantity"] * prod_qty
            # # check for negative values, I think this is fixed, so commenting out
            # if self.inventory[input["element"]] < 0:
            #     # print(f"{input['element']} depleted: {self.inventory[input['element']]}")
            #     raise ValueError
            # add to wip
            wip[input_val["element"]] = wip.get(input_val["element"], 0)
            wip[input_val["element"]] += input_val["quantity"] * prod_qty
        # produce element from wip
        self.inventory[element] += prod_qty * production_quantity
        self.production[element] += prod_qty * production_quantity
        return True

    def get_rule(self, element):
        """get rule"""
        # iterate over rules
        for rule in self.rules:
            # iterate over outputs
            for output in rule["outputs"]:
                # if we find it, return it
                if output["element"] == element:
                    return rule
        return None


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    # init nano_factory
    nano_factory = NanoFactory(input_value)
    # make 1 fuel
    nano_factory.make(1, "FUEL")
    if part == 1:
        return nano_factory.ore_collected
    # init target
    target = 1000000000000
    # start count at low bar of how many we would make
    # if they all needed as much ore as the first
    current_count = target // nano_factory.ore_collected
    # init last_count and last_ore
    last_count = current_count
    last_ore = nano_factory.ore_collected
    # start with big step size
    step_size = 10000000
    # loop while we are under target and not stepping over it by too many
    while last_ore <= target or step_size >= 2:
        # if we went over ore
        if last_ore > target:
            # cut step size in half
            step_size = step_size // 2
            # back off to step size from last_count
            current_count = last_count + step_size
        else:
            # update last_count
            last_count = current_count
            # increment current_count
            current_count += step_size
        # init nano factory
        nano_factory = NanoFactory(input_value)
        # make current_count FUEL
        nano_factory.make(current_count, "FUEL")
        # update last_ore
        last_ore = nano_factory.ore_collected
    # return last_count, it will be the last successful under target count
    return last_count


def parse_input(input_text):
    """
    Return stripped rule lines.
    """
    return input_text.strip()


YEAR = 2019
DAY = 14
input_format = {
    1: parse_input,
    2: parse_input,
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
