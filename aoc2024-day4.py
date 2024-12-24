"""
    https://adventofcode.com/2024/day/4

    Part 1:
    ------
    In this word search, XMAS occurs a total of 18 times; here's the same word search again, but
    where letters not involved in any XMAS have been replaced with .:

    ....XXMAS.
    .SAMXMS...
    ...S..A...
    ..A.A.MS.X
    XMASAMX.MM
    X.....XA.A
    S.S.S.S.SS
    .A.A.A.A.A
    ..M.M.M.MM
    .X.X.XMASX

    Part 2:
    ------
    Looking for the instructions, you flip over the word search to find that this isn't actually an
    XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an
    X. One way to achieve that is like this:

    M.S
    .A.
    M.S
    Irrelevant characters have again been replaced with . in the above diagram. Within the X, each
    MAS can be written forwards or backwards.
"""
from common import parse_args, read_rows, char_positions


def part1(rows):
    "Solution to part 1. 18 for the test input."
    X, M, A, S = [char_positions(rows, c) for c in "XMAS"]

    base_spans = [(0, 1), (1, 0), (1, 1), (1, -1)]
    spans = base_spans
    spans += [(-dx, -dy) for dx, dy in base_spans]
    spans += [(dx, -dy) for dx, dy in base_spans]
    spans += [(-dx, dy) for dx, dy in base_spans]
    spans = sorted(set(spans))

    matches = []
    for y, x in X:
        for dx, dy in spans:
            if (y+dx, x+dy) in M and (y+2*dx, x+2*dy) in A and (y+3*dx, x+3*dy) in S:
                matches.append((y,x))
    print(f"Part 1: {len(matches)}")

def part2(rows):
    "Solution to part 2. 1 for aoc2024-day3-input-test2.txt."
    M, A, S = [char_positions(rows, c) for c in "MAS"]
    matches = []
    for y, x in A:
        n = 0
        for dy, dx in [(-1, -1), (-1, 1)]:
            is_match = False
            for (a,b) in [(M,S), (S,M)]:
                if (y+dy, x+dx) in a and (y-dy, x-dx) in b:
                    is_match = True
                    break
            if is_match:
                n += 1
        if n == 2:
            matches.append((y,x))
    print(f"Part 2: {len(matches)}")

args = parse_args("Advent of Code 2024 - Day 4", "problems/aoc2024-day4-input-test.txt")
rows = read_rows(args.input)
part1(rows)
part2(rows)
