"""
    https://adventofcode.com/2024/day/1

    The engineers are trying to figure out which reports are safe. The Red-Nosed reactor safety
    systems can only tolerate levels that are either gradually increasing or gradually decreasing.
    So, a report only counts as safe if both of the following are true:

    Part 1:
    ------
    The levels are either all increasing or all decreasing.
    Any two adjacent levels differ by at least one and at most three.
    In the example above, the reports can be found safe or unsafe by checking those rules:

    7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
    1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
    9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
    1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
    8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
    1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.


    Part 2:
    ------
    Now, the same rules apply as before, except if removing a single level from an unsafe report
    would make it safe, the report instead counts as safe.



"""
from common import parse_args, read_lines, numbers_

def diff_(row):
    return [b-a for a,b in zip(row[:-1], row[1:])]

def pos_neg(diffs):
    pos = [v for v in diffs if v >= 0]
    neg = [v for v in diffs if v <= 0]
    return pos, neg

def is_valid_(row):
    diffs = diff_(row)
    pos, neg = pos_neg(diffs)
    if pos and neg: return False
    if neg:
        pos = [-v for v in neg]
    return all(1 <= v <= 3 for v in pos)

# def is_valid_(row):
#     is_valid = _is_valid_(row)
#     print(f"   -  {row}: {is_valid}")
#     return is_valid

def is_valid_tol(row):
    if is_valid_(row): return True
    for i in range(len(row)):
        if is_valid_(row[:i] + row[i+1:]): return True
    return False

# def is_valid_tol(row):
#     is_valid = _is_valid_tol(row)
#     print(f" --  {row}: {is_valid}")
#     return is_valid

def part1(lines):
    "Solution to part 1. 2 for the test input."
    rows = [numbers_(line) for line in lines]
    valids = [is_valid_(row) for row in rows]
    # for i, v in enumerate(rows):
    #     print(f"{i:2}: {v}")
    # for i, v in enumerate(valids):
    #     print(f"{i:2}: {v}")
    print(f"Part 1: {sum(valids)}")

def part2(lines):
    "Solution to part 2. 2 for the test input."
    rows = [numbers_(line) for line in lines]
    # diffs = [diff_(row) for row in rows]
    valids = [is_valid_tol(row) for row in rows]
    # for i, v in enumerate(rows):
    #     print(f"{i:2}: {v}")
    # for i, v in enumerate(valids):
    #     print(f"{i:2}: {v}")
    print(f"Part 2: {sum(valids)}")

args = parse_args("Advent of Code 2024 - Day 2", "aoc2024-day2-input-test.txt")
lines = read_lines(args.input)
part1(lines)
part2(lines)
