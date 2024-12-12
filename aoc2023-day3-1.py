"""
    https://adventofcode.com/2023/day/3
"""
import re

VERBOSE = False
TEST = False

if TEST:
    INPUT = "aoc2023-day3-input-test.txt"
else:           
    INPUT = "aoc2023-day3-input.txt"


def matches_(regex, text):
    """
    Find all matches of `regex` in `text`.
    Return a list of tuples (start, end, match) for each match.
    """
    matches = list(regex.finditer(text))
    return [(m.start(), m.end(), m.group(0)) for m in matches]

lines = open(INPUT).read().splitlines()


RE_NUMBER = re.compile(r"(\d+)")
RE_SYMBOL = re.compile(r"[^.\d]")

if VERBOSE:
    for regex in [RE_NUMBER, RE_SYMBOL]:
        print("----------------------")
        print(f"regex: {regex}")
        for i, line in enumerate(lines):
            matches = matches_(regex, line)
            print(f"{i:4}: '{line}' {matches} ")

# Find all symbols in lines
# symbols[i][j] exists if character `j` in line `i` is a symbol.
symbols = {}
for i, line in enumerate(lines):
    matches = matches_(RE_SYMBOL, line)
    if not matches:
        continue
    symbols[i] = set()
    for m in matches:
        start, end, _ = m
        symbols[i] |= set(range(start, end))

if VERBOSE:
    print("----------------------")
    for i in sorted(symbols.keys()):
        print(f"{i:4}: {sorted(symbols[i])}")
   
# Find all numbers in lines
# numbers is a list of tuples (line number, start, end, value)
numbers = []
for i, line in enumerate(lines):
    matches = matches_(RE_NUMBER, line)
    for m in matches:
        start, end, v = m
        numbers.append((i, start, end, int(v)))

# Find all numbers that are adjacent to symbols
# part_numbers is a list of numbers that are are adjacent to symbols in `line`.
part_numbers = []
for i, start, end, v in numbers:
    is_part = False
    j0 = max(0, i-1)
    j1 = min(len(lines), i+2)
    k0 = max(0, start-1)
    k1 = min(len(line), end+1)
    for j in range(j0, j1):
        if j in symbols:
            for k in range(k0, k1):
                if k in symbols[j]:
                    is_part = True
                    break   
            if is_part:
                break
    if is_part:
        part_numbers.append(v)

if VERBOSE:
    print("----------------------")
    for  v in part_numbers:  
        print(f"{v}")
print(f"Sum of part numbers: {sum(part_numbers)}")
