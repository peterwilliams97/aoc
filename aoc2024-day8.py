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

"""
import time
import numpy as np
from scipy import ndimage
from common import parse_args, read_rows, char_positions

# Directions: (dy,dx) up, right, down, left
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def is_edge(w, h, img, y, x):
    "Return True if (y, x) is on the edge of the map."
    if img[y, x] == 0:
        return False
    if y == 0 or y == h-1 or x == 0 or x == w-1:
        return True
    for dy, dx in DIRECTIONS:
        ny, nx = y+dy, x+dx
        if img[ny, nx] == 0:
            return True
    return False

def edge_(img):
    "Return the number of connected components that are on the edge of the map."
    h,w = img.shape
    edge = np.zeros((h, w), dtype=int)
    for y in range(h):
        for x in range(w):
            if is_edge(w, h, img, y, x):
                edge[y, x] = 1
    edge += img
    return edge

def connected_components(rows):
    w, h = len(rows[0]), len(rows)
    img = np.zeros((h, w), dtype=int)
    for y in range(h):
        for x in range(w):
            img[y, x] = 1 if rows[y][x] == "#" else 0

    labeled, n = ndimage.label(img)
    print(f"img={h}x{w}\n{img}")
    print(f"labeled={labeled.shape}\n{labeled}")
    print(f"n={n}")
    for i in range(1, n+1):
        print(f"Component {i}: {np.sum(labeled == i)}")
        cpt = np.zeros((h, w), dtype=int)
        cpt[labeled == i] = 1
        print(f"{cpt}")
        edge = edge_(cpt)
        print(f"{edge}")

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

def antinodes_(img):
    "Return pairs coordinates of antinodes."
    w, h = img.shape
    yx = {}
    xy = {}
    for y in range(h):
        for x in range(w):
            if img[y, x] != 0:
                if y not in yx: yx[y] = set()
                if x not in xy: xy[x] = set()
                yx[y].add(x)
                xy[x].add(y)
    antinodes = set()
    def add_antinode(y, x):
        fit = 0 <= y < h and 0 <= x < w
        if fit:
            antinodes.add((y, x))
        return fit

    y_keys = sorted(yx)
    x_keys = sorted(xy)
    for i, y in enumerate(y_keys):
        for y1 in y_keys[i+1:]:
            dy = y1 - y
            for j, x in enumerate(x_keys):
                for x1 in x_keys[j+1:]:
                    dx = x1 - x
                    if dx == 2 * dy or dy == 2 * dx:
                        xlo = x - dx
                        xhi = x1 + dx
                        ylo = y - dy
                        yhi = y1 + dy
                        if add_antinode(ylo, xlo):
                            print(f"    {[y,x]}, {[y1,x1]} -> {ylo, xlo}")
                        if add_antinode(yhi, xhi):
                            print(f"    {[y,x]}, {[y1,x1]} -> {yhi, xhi}")
    return antinodes

MARK = 9

def part1(rows):
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
        antinodes = antinodes_(img_k)
        valids = antinodes - exclusions[k]
        print(f"Antinodes {k}: {len(antinodes)}->{len(valids)} {antinodes} -> {valids}")
        antinodes = valids
        all_antinodes.update(antinodes)
        for y, x in antinodes:
            img_k[y,x] = MARK
        print(f"img_{k}=\n{img_k}")
    for y, x in all_antinodes:
        img[y, x] = MARK
    print(f"img=\n{img}")
    print(f"Part 1: {len(all_antinodes)}")

def part2(rows):
    "Solution to part 2. 6 for the test input."

    print(f"Part 2: {len(obstructions)}")

args = parse_args("Advent of Code 2024 - Day 8", "aoc2024-day8-input-test.txt")
rows = read_rows(args.input)
# connected_components(rows)
# exit(0)
t0 = time.time()
part1(rows)
t1 = time.time() - t0
t0 = time.time()
# part2(rows)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
