"""
    https://adventofcode.com/2023/day/3
"""
import re

VERBOSE = False
TEST = False
PART_1 = False

if TEST:
    INPUT = "aoc2023-day3-input-test.txt"
else:           
    INPUT = "aoc2023-day3-input.txt"

def matches_(regex, text):
    """
    Return a list of tuples (start, end, match) for each match of `regex` in `text`.
    """
    matches = regex.finditer(text)
    return [(m.start(), m.end(), m.group(0)) for m in matches]

lines = open(INPUT).read().splitlines()

# Regular expressions to find number
RE_NUMBER = re.compile(r"(\d+)")
# Regular expressions to find all symbols
RE_SYMBOL = re.compile(r"[^.\d]")
RE_STAR = re.compile(r"\*")

if VERBOSE:
    for regex in [RE_NUMBER, RE_SYMBOL]:
        print("----------------------")
        print(f"regex: {regex}")
        for i, line in enumerate(lines):
            matches = matches_(regex, line)
            print(f"{i:4}: '{line}' {matches} ")

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


   
# Find all numbers in lines
# `numbers` is a list of tuples (line number, start, end, value) for each number in `lines`.
numbers = []
for i, line in enumerate(lines):
    matches = matches_(RE_NUMBER, line)
    for m in matches:
        start, end, v = m
        numbers.append((i, start, end, int(v)))

def is_adjacent_(symbols, i, start, end):
    """
    Return True if number at line `i`, `start` <= x < `end` is adjacent to a `symbols` element
    """
    y0 = max(0, i-1)
    y1 = min(len(lines), i+2)
    x0 = max(0, start-1)
    x1 = min(len(line), end+1)
    for y in range(y0, y1):
        if y in symbols:
            for x in range(x0, x1):
                if x in symbols[y]:
                    return True
    return False

def adjacent_symbols_(symbols, i, start, end):
    """
    Return True if number at line `i`, `start` <= x < `end` is adjacent to a `symbols` element
    """
    adjacent = []
    y0 = max(0, i-1)
    y1 = min(len(lines), i+2)
    x0 = max(0, start-1)
    x1 = min(len(line), end+1)
    for y in range(y0, y1):
        if y in symbols:
            for x in range(x0, x1):
                if x in symbols[y]:
                    adjacent.append((y, x))
    return adjacent

if PART_1:
    symbols = symbols_(RE_SYMBOL, lines)
    if VERBOSE:
        print("----------------------")
        for i in sorted(symbols.keys()):
            print(f"{i:4}: {sorted(symbols[i])}")

    # Find all numbers that are adjacent to symbols
    # `part_numbers` is a list of numbers that are are adjacent to symbols in `line`.
    part_numbers = [v for i, start, end, v in numbers if is_adjacent_(symbols, i, start, end)]

    if VERBOSE:
        print("----------------------")
        for  v in part_numbers:  
            print(f"{v}")
    print(f"Sum of part numbers: {sum(part_numbers)}")

else:
    symbols = symbols_(RE_STAR, lines)
    symbols_neighbours = {}
    for i, start, end, v in numbers:
        adjacent_symbols = adjacent_symbols_(symbols, i, start, end) 
        if not adjacent_symbols:
            continue
        # print(f"{v}: {adjacent_symbols}")
        for neighbour in adjacent_symbols:
            if neighbour not in symbols_neighbours:
                symbols_neighbours[neighbour] = set()
            symbols_neighbours[neighbour].add(v)
    symbols_neighbours = {k: sorted(v) for k, v in symbols_neighbours.items() if len(v) > 1}    
    if VERBOSE:
        print("----------------------")
        for k, v in symbols_neighbours.items():
            print(f"{k}: {v}")

    gear_ratios = [v[0] * v[1] for v in symbols_neighbours.values()]
    print(f"Gear ratio: {sum(gear_ratios)}")

