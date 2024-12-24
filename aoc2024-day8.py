"""
    https://adventofcode.com/2024/day/8

    ............
    ........0...
    .....0......
    .......0....
    ....0.......
    ......A.....
    ............
    ............
    ........A...
    .........A..
    ............
    ............

    Part 1:
    ------
    The signal only applies its nefarious effect at specific antinodes based on the resonant
    frequencies of the antennas. In particular, an antinode occurs at any point that is perfectly in
    line with two antennas of the same frequency - but only when one of the antennas is twice as far
    away as the other. This means that for any pair of antennas with the same frequency, there are
    two antinodes, one on either side of them.

    Part 2:
    ------
    After updating your model, it turns out that an antinode occurs at any grid position exactly in
    line with at least two antennas of the same frequency, regardless of distance. This means that
    some of the new antinodes will occur at the position of each antenna (unless that antenna is
    the only one of its frequency).

    So, these three T-frequency antennas now create many antinodes:

    T....#....
    ...T......
    .T....#...
    .........#
    ..#.......
    ..........
    ...#......
    ..........
    ....#.....
    ..........

"""
import time
import numpy as np
from common import parse_args, read_rows

VERBOSE = False

def antinodes_(img, extend):
    "Return pairs coordinates of antinodes."
    w, h = img.shape
    points = set()
    for y0 in range(h):
        for x0 in range(w):
            if img[y0, x0] != 0:
                points.add((y0, x0))

    antinodes = set()
    def add_antinode(y, x):
        fit = 0 <= y < h and 0 <= x < w
        if fit:
            antinodes.add((y, x))
        return fit

    sorted_points = sorted(points)
    if VERBOSE:
        print(f"sorted_points={len(sorted_points)}")
        for i, p in enumerate(sorted_points):
            print(f"{i:4}: {p}")
    pairs = set()
    for i, p0 in enumerate(sorted_points):
        for p1 in sorted_points[i+1:]:
            y0, x0 = p0
            y1, x1 = p1
            if y1 < y0:
                p0, p1 = p1, p0
            pairs.add((p0, p1))

    sorted_pairs = sorted(pairs)
    if VERBOSE:
        print(f"sorted_pairs={len(sorted_pairs)}")
        for i, p in enumerate(sorted_pairs):
            print(f"{i:4}: {p}")
    for (y0, x0), (y1, x1) in sorted(pairs):
        dy = y1 - y0
        dx = x1 - x0
        if dx == 0 or dy == 0:
            continue
        elements = []
        ylo, xlo = y0, x0
        while True:
            xlo -= dx
            ylo -= dy
            if add_antinode(ylo, xlo):
                elements.append((ylo, xlo))
            else:
                break
            if not extend:
                break
        yhi, xhi = y1, x1
        while True:
            xhi += dx
            yhi += dy
            if add_antinode(yhi, xhi):
                elements.append((yhi, xhi))
            else:
                break
            if not extend:
                break
        if VERBOSE: print(f"    {[y0,x0]}, {[y1,x1]} -> {elements}")
    return antinodes

MARK = 9

ANSWER = """
##....#....#
.#.#....0...
..#.#0....#.
..##...0....
....0....#..
.#...#A....#
...#..#.....
#....#.#....
..#.....A...
....#....A..
.#........#.
...#......##
"""
ANSWER = ANSWER.strip().splitlines()

def solve(rows, extend):
    "Solution to part 1. 14 for the test input."
    w, h = len(rows[0]), len(rows)
    img = np.zeros((h, w), dtype=int)
    sym_num = {}
    current = 0
    for y in range(h):
        for x in range(w):
            sym = rows[y][x]
            if sym.isalpha() or sym.isdigit():
                if sym not in sym_num:
                    current += 1
                    sym_num[sym] = current
                num = sym_num[sym]
                img[y, x] = num
    if VERBOSE:
        print(f"img={img.shape}\n{img}")
        print(f"sym_num={sym_num}")
    vals = sorted(sym_num.values())
    originals = {}
    for k in vals:
        originals[k] = {(y, x) for y in range(h) for x in range(w) if img[y, x] == k}
    exclusions = {}
    for k in vals:
        exclusions[k] = {x for l, v in originals.items() if l != k for x in v}
    all_antinodes = set()
    for k in vals:
        img_k = (img == k).astype(int)
        antinodes = antinodes_(img_k, extend)
        valids = antinodes - exclusions[k]
        if VERBOSE: print(f"Antinodes {k}: {len(antinodes)}->{len(valids)} {antinodes} -> {valids}")
        all_antinodes.update(antinodes)
        for y, x in antinodes:
            img_k[y,x] = MARK
        if VERBOSE: print(f"img_{k}=\n{img_k}")
    for y, x in all_antinodes:
        img[y, x] = MARK
    if VERBOSE: print(f"img=\n{img}")

    for i, row in enumerate(img):
        n = sum(row!=0)
        if VERBOSE:  print(f"{i:2}: {n} {row}")
    if extend:
        return sum([sum(row!=0) for row in img])
    return len(all_antinodes)

def part1(rows):
    "Solution to part 1. 14 for the test input."
    n = solve(rows, False)
    print(f"Part 1: {n}")

def part2(rows):
    "Solution to part 2. 34 for the test input."
    n = solve(rows, True)
    print(f"Part 2: {n}")

args = parse_args("Advent of Code 2024 - Day 8", "problems/aoc2024-day8-input-test.txt")
rows = read_rows(args.input)
t0 = time.time()
part1(rows)
t1 = time.time() - t0
t0 = time.time()
part2(rows)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
