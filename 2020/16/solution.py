"""
Advent Of Code 2020 day 16
For once, my initial work wasn't wasted and completely rewritten
to support part 2 :)

set() and enumerate() ruled the day here.

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


def rule_match(number, rules):
    """
    Function to find the rules that match a number
    """
    matches = []
    for rule_name, rule in rules.items():
        if number in rule:
            matches.append(rule_name)
    return matches


def reduce_fields(fields):
    """
    Function to eliminate identified field names from the possibilites
    for other indices.

    for example if field[0] = {'class', 'seat'} and field[1] = {'seat'}, then
    field[0] can't be 'seat', so we remove it
    """
    changed = True
    while changed:
        changed = False
        for idx, values in enumerate(fields):
            if len(values) == 1:
                number = list(values)[0]
                for idx_2, values_2 in enumerate(fields):
                    if idx == idx_2:
                        continue
                    if number in values_2:
                        changed = True
                        values_2.difference_update(values)
    # This function updates fields in place, returning anyway
    # to make a more logical return statement in other functions
    return fields


def identify_fields(tickets, rules):
    """
    Function to scan ticket data to identify which fields are
    in each index position
    """
    fields = []
    # init sets with first ticket values
    for num in tickets[0]:
        fields.append(set(rule_match(num, rules)))
    # iterate over all tickets
    for ticket in tickets[1:]:
        for idx, num in enumerate(ticket):
            new_fields = set(rule_match(num, rules))
            # reduce posibilities for this position to the intesection of new fields
            fields[idx].intersection_update(new_fields)
    return reduce_fields(fields)


def parse_rules(rules_string):
    """Function to parse rule strings"""
    rules = {}
    for rule_string in rules_string.splitlines():
        rule_name, rule = rule_string.split(": ")
        ranges = rule.split(" or ")
        rules[rule_name] = set()
        for num_range in ranges:
            start, end = [int(num) for num in num_range.split("-")]
            for num in range(start, end + 1):
                rules[rule_name].add(num)
    return rules


def parse_input(input_string):
    """Function to parse input file"""
    rules_str, my_ticket_str, nearby_tickets_str = input_string.split("\n\n")
    rules = parse_rules(rules_str)
    my_ticket = [int(num) for num in my_ticket_str.splitlines()[1].split(",")]
    nearby_tickets = []
    for ticket in nearby_tickets_str.splitlines()[1:]:
        nearby_tickets.append([int(num) for num in ticket.split(",")])
    return rules, my_ticket, nearby_tickets


def get_valid_tickets(my_ticket, tickets, rules):
    """
    Function to filter out invalid tickets
    """
    invalid_nums = []
    valid_tickets = [my_ticket]
    valid_nums = set()
    for num_set in rules.values():
        valid_nums = valid_nums.union(num_set)
    for ticket in tickets:
        valid = True
        for num in ticket:
            if num not in valid_nums:
                valid = False
                invalid_nums.append(num)
        if valid:
            valid_tickets.append(ticket)
    return valid_tickets, invalid_nums


def solve(input_value, part):
    """
    Function to solve puzzle
    """
    rules, my_ticket, nearby_tickets = parse_input(input_value)
    valid_tickets, invalid_nums = get_valid_tickets(my_ticket, nearby_tickets, rules)
    if part == 1:
        return sum(invalid_nums)
    # part 2:
    fields = identify_fields(valid_tickets, rules)
    product = 1
    for idx, field_set in enumerate(fields):
        field_name = list(field_set)[0]
        if "departure" in field_name:
            # print(idx, field_name, my_ticket[idx])
            product *= my_ticket[idx]
    return product


YEAR = 2020
DAY = 16
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
