"""
AdventOfCode 2016 day 10

Again this one felt very familiar, I'm starting to think 2016 might be the year I tried
this and gave up.

Okay, as usual, I missed something in the instructions.
I need to load all the instructions as potential actions for the bots.
Then modify the give function to be recursive.

Okay I went another direction, and made it object oriented.

update: minor changes to main and solve() to update format. cleanup for pylint

"""

# import system modules
import logging
import argparse
import re

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

# global state
state = {"bot": {}, "output": {}}


def reset_state():
    """
    Reset global state between runs.
    """
    state["bot"] = {}
    state["output"] = {}


class Bin:
    """
    Simple class for output bins
    """

    def __init__(self, idx):
        """
        init Bin object
        """
        self.idx = idx
        self.type = "output"
        # start empty
        self.chips = []

    def __str__(self):
        """
        String representation of bin
        """
        return f"output bin {self.idx} contains {self.chips}"

    def receive(self, chip):
        """
        Receive a chip from a bot
        """
        # add chip to chips, no other actions for output bins
        self.chips.append(chip)


class Bot:
    """
    class for bots
    """

    def __init__(self, idx):
        self.idx = idx
        self.type = "bot"
        # chips empty
        self.chips = []
        self.comparisons = set()
        # placeholders for high and low targets
        self.targets = {"high": None, "low": None}

    def __str__(self):
        """
        String representation of bot
        """
        targets = {"high": None, "low": None}
        for high_low in ["high", "low"]:
            if not self.targets[high_low] is None:
                targets[high_low] = (
                    f"{self.targets[high_low].type} {self.targets[high_low].idx}"
                )
        retval = f"""
        bot {self.idx} has chips {self.chips}
          sends high to {targets["high"]}
          sends low to {targets["low"]}
        """
        retval = (
            f"bot {self.idx} {self.chips} comparisons: {self.comparisons}, "
            f"high to {targets['high']}, low to {targets['low']}"
        )

        return retval

    def receive(self, chip):
        """
        Receive a chip from a bot or input bin
        """
        # add chip to chips
        self.chips.append(chip)
        # need a trigger here for too many chips
        if len(self.chips) >= 2:
            self.comparisons.add(tuple(sorted(self.chips)))
            # distribute chips
            for high_low in ["high", "low"]:
                if not self.targets[high_low] is None:
                    self.give(self.targets[high_low], high_low)

    def give(self, target, highlow):
        """
        Function to give chip to another bot or bin
        """
        # give away a chip
        if highlow == "high":
            # high, set chip to maximum value in bot, and remove that chip from bot
            chip = self.chips.pop(self.chips.index(max(self.chips)))
        else:
            # high, set chip to minumum value in bot, and remove that chip from bot
            chip = self.chips.pop(self.chips.index(min(self.chips)))
        target.receive(chip)


# regular expressions to match instructions
value_pattern = re.compile(r"value (\d+) goes to bot (\d+)")
gives_pattern = re.compile(
    r"bot (\d+) gives (\w+) to (\w+) (\d+)( and (\w+) to (\w+) (\d+))?"
)


def parse_instruction(instruction):
    """
    Function to parse instruction string, and update bots and bins

    parameters:
      - instruction: string

    returns:
      - None

    This function does not return a value, it updates the global state data structure
    """
    # is it a value instruction?
    match = value_pattern.match(instruction)
    if match:
        # initialize bot if it doesn't exist yet
        chip, idx = match.groups()
        if not idx in state["bot"]:
            state["bot"][idx] = Bot(idx)
        # give bot the new chip
        state["bot"][idx].receive(int(chip))
    else:
        # is it a give instruction
        match = gives_pattern.match(instruction)
        if match:
            groups = match.groups()
            # first chip rule
            idx = groups[0]

            # initialize bot if it doesn't exist
            if not idx in state["bot"]:
                state["bot"][idx] = Bot(idx)
            bot = state["bot"][idx]
            for high_low, target_type, target_idx in (groups[1:4], groups[5:]):
                if high_low is None:
                    continue
                # initialize target if it doesn't exist
                if not target_idx in state[target_type]:
                    if target_type == "bot":
                        state[target_type][target_idx] = Bot(target_idx)
                    else:
                        state[target_type][target_idx] = Bin(target_idx)
                # set target
                bot.targets[high_low] = state[target_type][target_idx]
        else:
            # we shouldn't get here, but who knows what is in the input
            print(f"Unhandled instruction: {instruction}")


def solve(lines, part):
    """
    Function to solve puzzle
    """
    logger.debug("lines: %s", lines)
    reset_state()
    for line in sorted(lines):
        parse_instruction(line)
    if part == 1:
        target = (17, 61)
        for idx, bot in state["bot"].items():
            if target in bot.comparisons:
                logger.debug(
                    "bot %s(%s) is responsible for comparing %s",
                    type(bot.idx),
                    bot.idx,
                    target,
                )
                return int(bot.idx)
    # part 2
    product = 1
    for idx in range(3):
        product *= int(state["output"][str(idx)].chips[0])
    logger.debug("outputs: %s", state["output"])
    logger.debug("product: %s(%d)", type(product), product)
    return product


YEAR = 2016
DAY = 10
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
