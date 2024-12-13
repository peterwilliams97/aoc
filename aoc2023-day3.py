"""
    https://adventofcode.com/2023/day/3
"""
import re

def ruler(): print("============================")

def matches_(regex, text):
    """
    Return a list of tuples (start, end, match) for each match of `regex` in `text`.
    """
    matches = regex.finditer(text)
    return [(m.start(), m.end(), m.group(0)) for m in matches]

# Regular expressions to find number.
RE_NUMBER = re.compile(r"(\d+)")
# Regular expressions to find all symbols.
RE_SYMBOL = re.compile(r"[^.\d]")
# Regular expressions to find all "*".
RE_STAR = re.compile(r"\*")

def symbols_(regex, lines):
    """
    Return a dictionary of symbols in `lines` where the key is the line number and the value is a set
    of column numbers.
    `symbols`[i][j] exists if character `j` in line `i` is a symbol.
    """
    symbols = {}
    for i, line in enumerate(lines):
        matches = matches_(regex, line)
        if not matches:
            continue
        symbols[i] = set()
        for m in matches:
            start, end, _ = m
            symbols[i] |= set(range(start, end))
    return symbols

def numbers_(lines):
    """Return a list of tuples (line number, start, end, value) for each number in `lines`.
    """
    numbers = []
    for i, line in enumerate(lines):
        matches = matches_(RE_NUMBER, line)
        for m in matches:
            start, end, v = m
            numbers.append((i, start, end, int(v)))
    return numbers

def is_adjacent_(symbols, i, start, end):
    """
    Return True if the number at line `i`, `start` <= x < `end` is adjacent to a `symbols` element.
    """
    y0, y1 = i-1, i+2
    x0, x1 = start-1, end+1
    for y in range(y0, y1):
        if y in symbols:
            for x in range(x0, x1):
                if x in symbols[y]:
                    return True
    return False

def adjacent_symbols_(symbols, i, start, end):
    """
    Returns (y, x) for all symbols[y][x] that are adjacent to the number at
    line `i`, `start` <= x < `end`.
    """
    y0, y1 = i-1, i+2
    x0, x1 = start-1, end+1
    adjacent = []
    for y in range(y0, y1):
        if y in symbols:
            for x in range(x0, x1):
                if x in symbols[y]:
                    adjacent.append((y, x))
    return adjacent

def part1(lines, verbose=False):
    """
    Find all numbers that are adjacent to symbols and print their sum.
    """
    numbers = numbers_(lines)
    symbols = symbols_(RE_SYMBOL, lines)
    if verbose:
        ruler
        for i in sorted(symbols.keys()):
            print(f"{i:4}: {sorted(symbols[i])}")

    # Find all numbers that are adjacent to symbols
    # `part_numbers` is a list of numbers that are are adjacent to symbols in `line`.
    part_numbers = [v for i, start, end, v in numbers if is_adjacent_(symbols, i, start, end)]

    if verbose:
        ruler()
        for  v in part_numbers:
            print(f"{v}")
    print(f"Part 1: Sum of part numbers: {sum(part_numbers)}")

def part2(lines, verbose=False):
    """
    Find pairs of numbers that are adjacent to a "*" and print the sum of their products which is
    called the "gear ratio" in the problem description.
    """
    numbers = numbers_(lines)
    symbols = symbols_(RE_STAR, lines)
    symbols_neighbours = {}
    for i, start, end, v in numbers:
        adjacent_symbols = adjacent_symbols_(symbols, i, start, end)
        if not adjacent_symbols:
            continue
        for neighbour in adjacent_symbols:
            if neighbour not in symbols_neighbours:
                symbols_neighbours[neighbour] = set()
            symbols_neighbours[neighbour].add(v)
    symbols_neighbours = {k: sorted(v) for k, v in symbols_neighbours.items() if len(v) > 1}
    if verbose:
        ruler
        for k, v in symbols_neighbours.items():
            print(f"{k}: {v}")

    gear_ratios = [v[0] * v[1] for v in symbols_neighbours.values()]
    print(f"Part 2: Gear ratio: {sum(gear_ratios)}")

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Advent of Code 2023 Day 3 solution")
    parser.add_argument('-i', '--input', default="aoc2023-day3-input-test.txt", help="Input file path")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output")
    return parser.parse_args()

args = parse_args()
lines = open(args.input).read().splitlines()
if args.verbose:
    print(f"Processing file: {args.input}")
    for regex in [RE_NUMBER, RE_SYMBOL]:
        ruler()
        print(f"regex: {regex}")
        for i, line in enumerate(lines):
            matches = matches_(regex, line)
            print(f"{i:4}: '{line}' {matches} ")
part1(lines, args.verbose)
part2(lines, args.verbose)
