"""
Advent Of Code 2020 day 19

Part 1 works.  Part 2 still needs some guardrails or a new strategy


"""

# import system modules
import time
from functools import lru_cache
# from heapq import heappop, heappush
# import sys
# sys.setrecursionlimit(20000)

# import my modules
import aoc  # pylint: disable=import-error


def parse_rule(rule_text):
    """Parse a rule string into a tuple of options."""
    result = []
    options = rule_text.split(" | ")
    for option in options:
        values = [int(num) for num in option.split(" ")]
        result.append(tuple(values))
    return tuple(result)


def parse_input(text):
    """Parse input text into rules and messages."""
    rules_text, messages_text = text.split("\n\n")
    messages = messages_text.splitlines()
    rules_dict = {}
    for line in rules_text.splitlines():
        rule_id, rule_text = line.split(": ")
        rule_id = int(rule_id)
        if '"' in rule_text:
            rules_dict[rule_id] = rule_text.replace('"', "")
        else:
            rules_dict[rule_id] = parse_rule(rule_text)
    rules = []
    for key in sorted(list(rules_dict.keys())):
        rules.append(rules_dict[key])
    return tuple(rules), messages


@lru_cache(maxsize=None)
def strings_for_rule(rule, rules, part, recursion_depth=0):
    """Generate all possible strings for a given rule."""
    # print(f"strings_for_rule({rule}, rules, {recursion_depth})")
    if recursion_depth > 20:
        return [""]
    if isinstance(rule, str):
        return [rule]
    if isinstance(rule, int):
        return strings_for_rule(rules[rule], rules, part, recursion_depth + 1)
    results = []
    # if len(rule) > 1:
    for option in rule:
        # print(f"option: {option}")
        partial_results = [""]
        for sub_rule in option:
            # print(f"sub_rule: {sub_rule}")
            sub_strings = strings_for_rule(sub_rule, rules, part, recursion_depth + 1)
            # print(f"after sub_strings {len(sub_strings)}")
            # Generate all combinations of `partial_results` and `sub_strings`.
            # if partial_results and sub_strings:
            #     print(len(partial_results[0]), len(sub_strings[0]))
            partial_results = [
                p_r + s_s for p_r in partial_results for s_s in sub_strings
            ]
            # print(f"after partial_results {len(partial_results)}")
        if partial_results != [""]:
            results.extend(partial_results)
    # rule_cache[rule] = results
    # 265 too high
    return results


@lru_cache(maxsize=None)
def match_rule_orig(message, rule_id, rules, part):
    """Original matching function using precomputed strings."""
    if message in strings_for_rule(rules[rule_id], rules, part):
        return True
    return False


@lru_cache(maxsize=None)
def match_rule(message, rule_id, rules, part, recursion_depth=0):
    """Recursive matching function."""
    if recursion_depth > 20:  # Limit recursion depth to avoid infinite loops
        return False

    rule = rules[rule_id]
    if isinstance(rule, str):  # Base case for character match
        return message == rule

    # For recursive cases in Part 2
    if part == 2:
        if rule_id == 8:  # Rule 8: match one or more of Rule 42
            return any(
                match_sequence(message, [42] * i, rules, part, recursion_depth + 1)
                for i in range(1, len(message) // 2 + 1)
            )

        if rule_id == 11:  # Rule 11: match equal numbers of Rule 42 and Rule 31
            for i in range(1, len(message) // 2 + 1):
                if match_sequence(
                    message, [42] * i + [31] * i, rules, part, recursion_depth + 1
                ):
                    return True
            return False

    # Standard recursive match for other rules
    return any(
        match_sequence(message, tuple(option), rules, part, recursion_depth + 1)
        for option in rule
    )


@lru_cache(maxsize=None)
def match_sequence(message, rule_ids, rules, part, recursion_depth=0):
    """Match a sequence of rules against the message."""
    if not rule_ids:
        return message == ""

    first_rule = rule_ids[0]
    for i in range(1, len(message) + 1):
        prefix = message[:i]
        if match_rule(prefix, first_rule, rules, part, recursion_depth):
            if match_sequence(
                message[i:], tuple(rule_ids[1:]), rules, part, recursion_depth + 1
            ):
                return True
    return False


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    rules, messages = parse_input(input_value)
    # longest_message = len(max(messages, key=len))
    if part == 2:
        # print(rules[8])
        # print(rules[11])
        # ((42,),)
        # ((42, 31),)
        rules = list(rules)
        rules[8] = ((42,), (42, 8))
        # 11: 42 31 | 42 11 31
        rules[11] = ((42, 31), (42, 11, 31))
        rules = tuple(rules)
        # return part
    counter = 0
    for message in messages:
        matches = match_rule(message, 0, rules, part)
        if matches:
            counter += 1
        # print(f"message[{idx}]: {message}, matches: {matches}")

    return counter


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020, 19)
    input_text = my_aoc.load_text()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 132, 2: 306}
    # dict to map functions
    funcs = {1: solve, 2: solve}
    # loop parts
    for my_part in parts:
        # log start time
        start_time = time.time()
        # get answer
        answer[my_part] = funcs[my_part](input_text, my_part)
        # log end time
        end_time = time.time()
        # print results
        print(
            f"Part {my_part}: {answer[my_part]}, took {end_time - start_time} seconds"
        )
        if correct[my_part]:
            assert correct[my_part] == answer[my_part]
