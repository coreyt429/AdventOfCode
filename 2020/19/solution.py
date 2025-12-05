"""
Advent Of Code 2020 day 19

Part 1 works.  Part 2 still needs some guardrails or a new strategy

20251203 - updated to use CYK parsing algorithm for context-free grammars.

"""

# import system modules
import logging
import argparse
from collections import defaultdict

# import my modules
from aoc import AdventOfCode  # pylint: disable=import-error

TEMPLATE_VERSION = "20251203"

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)


def build_grammar(rules):
    """
    rules: dict[lhs] -> list[tuple[rhs symbols]]
      - lhs, rhs symbols are strings, e.g. "0", "42", "a", "b"
      - For AoC 2020.19, terminals are single lowercase letters ("a", "b")
        and nonterminals are numeric strings ("0", "1", ..., "42", etc.)
    """

    terminals = defaultdict(set)  # ch -> set(lhs)
    binaries = defaultdict(set)  # (B, C) -> set(lhs)
    unit_productions = defaultdict(set)  # child_nonterminal -> set(parent_nonterminal)

    def add_binary_chain(lhs, symbols):
        """
        Convert A -> X1 X2 ... Xn (n >= 2, all nonterminals)
        into binary rules using fresh helper nonterminals.

        Example: A -> X1 X2 X3
          A        -> X1 A_bin_0
          A_bin_0  -> X2 X3
        """
        assert len(symbols) >= 2
        prev_lhs = lhs
        for i in range(len(symbols) - 2):
            b = symbols[i]
            new_nt = f"{lhs}_bin_{i}"  # synthetic nonterminal
            binaries[(b, new_nt)].add(prev_lhs)
            prev_lhs = new_nt

        # last two symbols
        b = symbols[-2]
        c = symbols[-1]
        binaries[(b, c)].add(prev_lhs)

    for lhs, rhs_list in rules.items():
        for rhs in rhs_list:
            # Single symbol on RHS
            if len(rhs) == 1:
                sym = rhs[0]

                if sym.islower():
                    # terminal: lhs -> 'a' or 'b'
                    terminals[sym].add(lhs)
                else:
                    # unit production: lhs -> sym (both nonterminals)
                    unit_productions[sym].add(lhs)

            # Two symbols on RHS: binary rule A -> B C
            elif len(rhs) == 2:
                b, c = rhs
                binaries[(b, c)].add(lhs)

            # Longer RHS: A -> X1 X2 X3 ... Xn (n >= 3)
            else:
                # For AoC 2020.19, these should all be nonterminals (digits),
                # not mixed terminals; if they are, that's a parsing bug.
                add_binary_chain(lhs, rhs)

    return terminals, binaries, unit_productions


def close_under_unit_productions(cell, unit_productions):
    """
    Given a set of nonterminals in `cell`, add all A such that there's a chain
    A -> ... -> B where B is in `cell`, following only unit productions.
    """
    stack = list(cell)
    while stack:
        b = stack.pop()
        for a in unit_productions.get(b, ()):
            if a not in cell:
                cell.add(a)
                stack.append(a)


def _populate_cyk_cell(table, i, length, binaries, unit_productions):
    """Populate CYK table cell for a given start index and substring length."""
    cell = table[i][length]
    for split in range(1, length):
        left = table[i][split]
        right = table[i + split][length - split]
        if not left or not right:
            continue
        for b in left:
            for c in right:
                parents = binaries.get((b, c))
                if parents:
                    cell |= parents

    if cell:
        close_under_unit_productions(cell, unit_productions)


def cyk_accepts(message, start_symbol, terminals, binaries, unit_productions):
    """CYK algorithm to determine if message is in the language of the grammar."""
    n = len(message)
    if n == 0:
        return False

    # T[i][length] -> set of nonterminals that derive message[i : i+length]
    table = [[set() for _ in range(n + 1)] for _ in range(n)]

    # ----- length 1 substrings -----
    for i, ch in enumerate(message):
        cell = table[i][1]
        cell |= terminals.get(ch, set())
        close_under_unit_productions(cell, unit_productions)

    # ----- length >= 2 -----
    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            _populate_cyk_cell(table, i, length, binaries, unit_productions)

    return start_symbol in table[0][n]


def parse_rule(rule_text):
    """Parse a rule string into a tuple of options."""
    result = []
    options = rule_text.split(" | ")
    for option in options:
        values = [int(num) for num in option.split(" ")]
        result.append(tuple(values))
    return tuple(result)


def parse_grammar(rule_text):
    """Parse a rule string into a tuple of options."""
    result = []
    options = rule_text.split(" | ")
    for option in options:
        values = list(num for num in option.split(" "))
        result.append(tuple(values))
    return tuple(result)


def parse_input(text):
    """Parse input text into rules and messages."""
    rules_text, messages_text = text.split("\n\n")
    messages = messages_text.splitlines()
    grammar_dict = {}
    for line in rules_text.splitlines():
        rule_id, rule_text = line.split(": ")
        rule_id = int(rule_id)
        if '"' in rule_text:
            grammar_dict[str(rule_id)] = rule_text.replace('"', "")
        else:
            grammar_dict[str(rule_id)] = parse_grammar(rule_text)
    return messages, grammar_dict


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    messages, grammar_dict = parse_input(input_value)
    # longest_message = len(max(messages, key=len))
    if part == 2:
        # Modify rules for part 2
        # 8: 42 | 42 8
        grammar_dict["8"] = (("42",), ("42", "8"))
        # 11: 42 31 | 42 11 31
        grammar_dict["11"] = (("42", "31"), ("42", "11", "31"))

    terminals, binaries, unit_productions = build_grammar(grammar_dict)

    count = sum(
        1
        for msg in messages
        if cyk_accepts(
            msg,
            start_symbol="0",
            terminals=terminals,
            binaries=binaries,
            unit_productions=unit_productions,
        )
    )
    logger.debug("Part %s: Accepted messages count: %s", part, count)
    return count


YEAR = 2020
DAY = 19
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
