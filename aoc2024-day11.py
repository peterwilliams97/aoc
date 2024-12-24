"""
    https://adventofcode.com/2024/day/11

    As you observe them for a while, you find that the stones have a consistent behavior. Every time
    you blink, the stones each simultaneously change according to the first applicable rule in this
    list:

    - If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    - If the stone is engraved with a number that has an even number of digits, it is replaced by two
      stones. The left half of the digits are engraved on the new left stone, and the right half of
       the digits are engraved on the new right stone. (The new numbers don't keep extra leading
       zeroes: 1000 would become stones 10 and 0.)
    - If none of the other rules apply, the stone is replaced by a new stone; the old stone's number
      multiplied by 2024 is engraved on the new stone.

    Part 1:
    How many stones would you have after blinking a total of 25 times?

    Part 2:
    How many stones would you have after blinking a total of 75 times?
"""
import time
from common import parse_args, read_text, numbers_

def apply_rule(n):
    "Applies the first applicable rule to `n`."
    if n == 0: return [1]
    s = str(n)
    if len(s) % 2 == 0: return [int(s[:len(s) // 2]), int(s[len(s) // 2:])]
    return [n * 2024]

def blink_once(numbers):
    "Returns a new list of numbers after applying the rules to each number in the input list."
    new_numbers = []
    for n in numbers: new_numbers.extend(apply_rule(n))
    return new_numbers

def blink_once_cache(cache, number_counts):
    """
    Returns a new dict of {number: count} after applying the rules to each number in the input dict.
    `cache` is a dictionary of {number: [new_number]} where `number` is a number and `new_number` is
    the result of applying the rules to `number`.
    `number_counts` is a dictionary of {number: count} where `number` is a number and `count` is the
    number of times that number appears in the current state of the stones.
    """
    for n in number_counts.keys():
        if n not in cache: cache[n] = apply_rule(n)

    new_number_counts = {}
    for n, c in number_counts.items():
        for v in cache[n]:
            if v in new_number_counts: new_number_counts[v] += c
            else: new_number_counts[v] = c
    return new_number_counts

def part1(numbers):
    "Solution to part 1. 55312 for the test input. (194482)"
    blinks = 25
    for _ in range(blinks): numbers = blink_once(numbers)
    print(f"Part 1: {len(numbers)}")

def part2(numbers):
    "Solution to part 2. (232454623677743)"
    blinks = 75
    number_counts = {n: 1 for n in numbers}
    numbers_cache = {}
    for _ in range(blinks): number_counts = blink_once_cache(numbers_cache, number_counts)
    print(f"Part 2: {sum(number_counts.values())}")

args = parse_args("Advent of Code 2024 - Day 11", "problems/aoc2024-day11-input-test.txt")
text = read_text(args.input)
numbers = numbers_(text)
t0 = time.time()
part1(numbers)
t1 = time.time() - t0
t0 = time.time()
part2(numbers)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
