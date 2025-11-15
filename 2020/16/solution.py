"""
Advent Of Code 2020 day 16
For once, my initial work wasn't wasted and completely rewritten
to support part 2 :)

set() and enumerate() ruled the day here.

"""

# import system modules
import time

# import my modules
import aoc  # pylint: disable=import-error


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


if __name__ == "__main__":
    my_aoc = aoc.AdventOfCode(2020, 16)
    input_text = my_aoc.load_text()
    # parts dict to loop
    parts = {1: 1, 2: 2}
    # dict to store answers
    answer = {1: None, 2: None}
    # correct answers once solved, to validate changes
    correct = {1: 23954, 2: 453459307723}
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
