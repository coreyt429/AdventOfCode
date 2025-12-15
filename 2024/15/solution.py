"""
Advent Of Code 2024 day 15

This was a fun extension of Grid().

Part 1, was fairly simple.

Part 2, I had to modify item to take into account the length of symbol
  - added self.positions to hold all postions
  - left self.position to mark the left most position
  - updated WareHouse().get_item to use positions instead of position
  - updated Item().move to add a test run to avoid moving the first
    of a block pair, then getting blocked by the second
  - updates Item().move to handle items of arbitrary width
  - self.position is functionally identical to part 1, so no change to
    total calculations

Only had to fix one bug in part 2.  Initially I used a list for others,
which was causing a scenario where some boxes got moved twice.  Updated
to use a set instead, so they would only be considered once.

"""

# import system modules
import logging
import argparse

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error
from grid import Grid  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_input(text):
    """Function to parse input data"""
    map_text, directions_text = text.split("\n\n")
    directions_text = directions_text.replace("\n", "")
    return map_text, directions_text


class WareHouse(Grid):
    """Class to represent a warehouse"""

    def __init__(self, map_text):
        super().__init__(map_text, use_overrides=False)
        self.boxes = []
        self.robot = None
        self.load_items()

    def load_items(self):
        """Method to load robot and box items"""
        for point, symbol in self.items():
            if symbol == "@":
                self.robot = Item(symbol, point, self)
            elif symbol == "O":
                self.add_item(symbol, point)
            elif symbol == "[":
                self.add_item("[]", point)

    def get_item(self, position):
        """method to get item at position"""
        for item in self.boxes:
            if position in item.positions:
                return item
        return None

    def add_item(self, symbol, position):
        """method to add item to collection"""
        item = Item(symbol, position, self)
        self.boxes.append(item)
        return item


class Item:
    """Class to represent wharehouse items"""

    direction_map = {"^": "n", ">": "e", "v": "s", "<": "w"}

    def __init__(self, symbol, position, parent):
        self.parent = parent
        self.symbol = symbol
        self.position = position
        self.positions = [position]
        last_pos = position
        for _ in range(len(symbol[1:])):
            neighbors = self.parent.get_neighbors(point=last_pos, directions=["e"])
            if "e" in neighbors:
                self.positions.append(neighbors["e"])
                last_pos = neighbors["e"]

    def move(self, instruction, test=False):
        """Method to move an item"""
        direction = self.direction_map[instruction]
        targets = []
        states = []
        for position in self.positions:
            neighbors = self.parent.get_neighbors(
                point=position, directions=[direction]
            )
            targets.append(neighbors[direction])
            states.append(self.parent.get_point(point=neighbors[direction]))

        if "#" in states:
            return False
        others = set()
        for idx, target in enumerate(targets):
            if target in self.positions:
                continue
            if states[idx] == ".":
                continue
            other = self.parent.get_item(position=target)
            if not other.move(instruction, test=True):
                return False
            others.add(other)
        if test:
            return True

        self.position = targets[0]
        for position in self.positions:
            self.parent.set_point(position, ".")
        for other in others:
            other.move(instruction)
        for idx, target in enumerate(targets):
            self.positions[idx] = targets[idx]
            self.parent.set_point(self.positions[idx], self.symbol[idx])
        return True

    def __str__(self):
        """String method"""
        return f"{self.symbol}: {self.position}"


def expand_map(map_text):
    """Function to expand map (part 2)"""
    new_map_text = ""
    for char in map_text:
        if char in "#.":
            new_map_text += char
            new_map_text += char
            continue
        if char == "O":
            new_map_text += "[]"
            continue
        if char == "@":
            new_map_text += "@."
            continue
        new_map_text += char
    return new_map_text


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    map_text, directions_text = parse_input(input_value)
    if part == 2:
        map_text = expand_map(map_text)
    warehouse = WareHouse(map_text)
    for instruction in directions_text:
        warehouse.robot.move(instruction)
    total = 0
    for box in warehouse.boxes:
        total += (100 * box.position[1]) + box.position[0]

    return total


YEAR = 2024
DAY = 15
input_format = {
    1: "text",
    2: "text",
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
