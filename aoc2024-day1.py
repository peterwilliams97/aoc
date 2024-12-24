"""
    https://adventofcode.com/2024/day/1

    3   4
    4   3
    2   5
    1   3
    3   9
    3   3

    Part 1:
    ------


    Part 2:
    ------
    Calculate a total similarity score by adding up each number in the left list after multiplying
    it by the number of times that number appears in the right list.
"""
import time
from common import parse_args, read_lines, numbers_

def part1(lines):
    "Solution to part 1. 11 for the test input."
    rows = [numbers_(line) for line in lines]
    columns = [sorted(c) for c in zip(*rows)]
    distances = [abs(a - b) for a, b in zip(*columns)]
    print(f"Part 1: {sum(distances)}")

def part2(lines):
    "Solution to part 2. 31 for the test input."
    rows = [numbers_(line) for line in lines]
    columns = list(zip(*rows))
    right_counts = {}
    for c in columns[1]:
        right_counts[c] = right_counts.get(c, 0) + 1
    similiarities = [v * right_counts.get(v, 0) for v in columns[0]]
    print(f"Part 2: {sum(similiarities)}")

args = parse_args("Advent of Code 2024 - Day 1", "problems/aoc2024-day1-input-test.txt")
lines = read_lines(args.input)
t0 = time.time()
part1(lines)
t1 = time.time() - t0
t0 = time.time()
part2(lines)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
