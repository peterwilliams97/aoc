"""
    https://adventofcode.com/2024/day/5

    47|53
    97|13
    97|61
    97|47
    75|29
    61|13
    75|53
    29|13
    97|29
    53|29
    61|53
    97|53
    61|29
    47|13
    75|47
    97|75
    47|61
    75|61
    47|29
    75|13
    53|13

    75,47,61,53,29
    97,61,53,29,13
    75,29,13
    75,97,47,61,53
    61,13,29
    97,13,75,29,47

    Part 1:
    ------
    The first section specifies the page ordering rules, one per line. The first rule, 47|53, means
    that if an update includes both page number 47 and page number 53, then page number 47 must be
    printed at some point before page number 53. (47 doesn't necessarily need to be immediately
    before 53; other pages are allowed to be between them.)

    The second section specifies the page numbers of each update. Because most safety manuals are
    different, the pages needed in the updates are different too. The first update, 75,47,61,53,29,
    means that the update consists of page numbers 75, 47, 61, 53, and 29.

    For some reason, the Elves also need to know the middle page number of each update being
    printed. Because you are currently only printing the correctly-ordered updates, you will need to
    find the middle page number of each correctly-ordered update. In the above example, the
    correctly-ordered updates are:

    75,47,61,53,29
    97,61,53,29,13
    75,29,13

    Part 2:
    ------
    For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers
    in the right order. For the above example, here are the three incorrectly-ordered updates and
    their correct orderings:

    75,97,47,61,53 becomes 97,75,47,61,53.
    61,13,29 becomes 61,29,13.
    97,13,75,29,47 becomes 97,75,47,29,13.
"""
from collections import defaultdict
from common import parse_args, read_lines

def rule_sets_(rules):
    "Return a dictionary of rules as sets."
    rule_sets = defaultdict(set)
    for pre, post in rules:
        rule_sets[pre].add(post)
    return rule_sets

def parse_input(lines):
    "Parse the input into a list of rules and a list of updates."

    rules = []
    updates = []
    for line in lines:
        if "|" in line:
            parts = line.split("|")
            parts = [int(v) for v in parts]
            rules.append(parts)
        elif "," in line:
            parts = line.split(",")
            parts = [int(v) for v in parts]
            updates.append(parts)

    return rule_sets_(rules), updates

def is_valid_update(rule_sets, update):
    "Return True if the update is valid according to the rules."
    for i, u in enumerate(update):
        if u not in rule_sets:
            continue
        for v in update[:i]:
            s = rule_sets[u]
            if v in s:
                # print(f"  {i}:{u} >= {v} is invalid {s}")
                return False
    # print("  **Valid**")
    return True

def validate_one_update(rule_sets, update):
    for i, u in enumerate(update):
        if u not in rule_sets:
            continue
        for j, v in enumerate(update[:i]):
            s = rule_sets[u]
            if v in s:
                fixed = update
                fixed[i] = v
                fixed[j] = u
                return fixed, True
    return update, False

def validate_update(rule_sets, update):
    "Return a valid update."
    fixed = update
    while True:
        fixed, changed = validate_one_update(rule_sets, fixed)
        if not changed:
            break
    return fixed

def center_value(update):
    "Return the center value of an update."
    assert len(update) % 2 == 1
    return update[len(update) // 2]

def part1(rule_sets, updates):
    "Solution to part 1. 143 for the test input."
    valid = [u for u in updates if is_valid_update(rule_sets, u)]
    centers = [center_value(u) for u in valid]
    # print(f"Valid updates: {valid}")
    # print(f"Center values: {centers}")
    print(f"Part 1: {sum(centers)}")

def part2(rule_sets, updates):
    "Solution to part 2. 123 for the test input."
    updates = [u for u in updates if not is_valid_update(rule_sets, u)]
    fixed_updates = [validate_update(rule_sets, u) for u in updates]
    centers = [center_value(u) for u in fixed_updates]
    print(f"Part 2: {sum(centers)}")

args = parse_args("Advent of Code 2024 - Day 5", "problems/aoc2024-day5-input-test.txt")
lines = read_lines(args.input)
rule_sets, updates = parse_input(lines)
part1(rule_sets, updates)
part2(rule_sets, updates)
