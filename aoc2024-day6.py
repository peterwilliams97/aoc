"""
    https://adventofcode.com/2024/day/4

    Part 1:
    ------
    You start by making a map (your puzzle input) of the situation. For example:

    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #.........
    ......#...

    The map shows the current position of the guard with ^ (to indicate the guard is currently
    facing up from the perspective of the map). Any obstructions - crates, desks, alchemical
    reactors, etc. - are shown as #.

    Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following t
    hese steps:

    If there is something directly in front of you, turn right 90 degrees.
    Otherwise, take a step forward.

    Part 2:
    ------

"""
import time
from common import parse_args, read_rows, char_positions

# Directions: (dy,dx) up, right, down, left
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def search(w, h, B, y0, x0, direction):
    "Return True if the guard can escape the map of blockers `B`, False otherwise."
    visited = {(y, x): set() for y in range(h) for x in range(w)}
    y, x = y0, x0
    dy, dx = DIRECTIONS[direction]
    visited[(y, x)].add(direction)
    n = 0
    while True:
        if (y+dy, x+dx) in B:
            direction = (direction + 1) % 4
            dy, dx = DIRECTIONS[direction]
        else:
            y, x = y+dy, x+dx
            if not (0 <= x < w and 0 <= y < h):
                return True
            if direction in visited[(y, x)]:
                return False
            visited[(y, x)].add(direction)
        n += 1
        assert n < w * h * 1000, "Infinite loop"

def part1(rows):
    "Solution to part 1. 41 for the test input."
    w, h = len(rows[0]), len(rows)
    B, P = [char_positions(rows, c) for c in "#^"]
    print(f"Map: {w}x{h}")
    # print(f"B={sorted(B)}")
    # print(f"P={sorted(P)}")
    assert len(P) == 1, f"Expected 1 guard, got {len(P)}"
    direction = 0
    y, x = list(P)[0]
    dy, dx = DIRECTIONS[direction]
    visited = {(y, x)}
    while True:
        if (y+dy, x+dx) in B:
            direction = (direction + 1) % 4
            dy, dx = DIRECTIONS[direction]
        else:
            ny, nx = y+dy, x+dx
            # duplicate = (ny, nx) in visited
            # print(f"{len(visited):2}: [{y:2}, {x:2}] {[dy,dx]} {'D' if duplicate else ''}")
            y, x = ny, nx
            if not (0 <= x < w and 0 <= y < h):
                break
            visited.add((y, x))
    print(f"Part 1: {len(visited)}")

def part2(rows):
    "Solution to part 2. 6 for the test input."
    w, h = len(rows[0]), len(rows)
    B0, P = [char_positions(rows, c) for c in "#^"]
    A = B0 | P
    y0, x0 = list(P)[0]

    obstructions = set()
    for y in range(h):
        for x in range(w):
            o = (y, x)
            if o in A:
                continue
            B = B0 | {o}
            escaped = search(w, h, B, y0, x0, 0)
            if not escaped:
                # print(f"Obstruction: {o} blocks escape")
                obstructions.add(o)
    print(f"Part 2: {len(obstructions)}")

args = parse_args("Advent of Code 2024 - Day 6", "problems/aoc2024-day6-input-test.txt")
rows = read_rows(args.input)
t0 = time.time()
part1(rows)
t1 = time.time() - t0
t0 = time.time()
part2(rows)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
