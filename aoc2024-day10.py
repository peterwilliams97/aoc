"""
    https://adventofcode.com/2024/day/10

    The topographic map indicates the height at each position using a scale from 0 (lowest) to 9
    (highest). For example:

    0123
    1234
    8765
    9876

    A trailhead is any position that starts one or more hiking trails - here, these positions will
    always have height 0. Assembling more fragments of pages, you establish that a trailhead's score
    is the number of 9-height positions reachable from that trailhead via a hiking trail. In the
    above example, the single trailhead in the top left corner has a score of 1 because it can reach
    a single 9 (the one in the bottom left).

    Part 1:
    ------

    Here's a larger example:

    89010123
    78121874
    87430965
    96549874
    45678903
    32019012
    01329801
    10456732
    This larger example has 9 trailheads. Considering the trailheads in reading order, they have
    scores of 5, 6, 5, 3, 1, 3, 5, 3, and 5. Adding these scores together, the sum of the scores of
    all trailheads is 36.

    Part 2:
    ------
    The paper describes a second way to measure a trailhead called its rating. A trailhead's rating
    is the number of distinct hiking trails which begin at that trailhead. For example:

    .....0.
    ..4321.
    ..5..2.
    ..6543.
    ..7..4.
    ..8765.
    ..9....

    The above map has a single trailhead; its rating is 3 because there are exactly three distinct
    hiking trails which begin at that position:

"""
import time
import numpy as np
from common import parse_args, read_rows

# Directions: (dy,dx) up, right, down, left
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def trailhead_destinations(chart, y0, x0):
    """
    Calculate the destinations (locations with value 9) that can be reached from a starting point
    'y0, x0' on `chart`.
    """
    h,w = chart.shape
    v = chart[y0, x0]
    if v == 9:
        return {(y0, x0)}
    destinations = set()
    for dy, dx in DIRECTIONS:
        y, x = y0 + dy, x0 + dx
        if 0 <= y < h and 0 <= x < w and chart[y, x] == v + 1:
            s = trailhead_destinations(chart, y, x)
            destinations.update(s)
    return destinations

def complete_trails(chart, y0, x0):
    """
    Returns all complete trails that can be reached from a starting point
    'y0, x0' on `chart`.
    A complete trail is a sequence of points that has a length of 18 (9*2) and chart[y,x] == i
    for i in 0..9.
    i.e. trail = [(y0, x0), (y1, x1), ... (y9, x9)] where chart[y0, x0] == 0 and chart[y9, x9] == 9.
    """
    h,w = chart.shape
    v = chart[y0, x0]
    step = (y0, x0)
    if v == 9:
        return {(step)}
    trails = set()
    for dy, dx in DIRECTIONS:
        y, x = y0 + dy, x0 + dx
        if 0 <= y < h and 0 <= x < w and chart[y, x] == v + 1:
            plist = complete_trails(chart, y, x)
            # print(f"  num_paths[{v}]({y0},{x0}) -> ({y},{x}) -> {plist}")
            for p in plist:
                # print(f"    {p} {len(p)} {9-v}")
                if len(p) == 2*(9-v):
                    q = list(reversed(p))
                    q.extend(list(reversed(step)))
                    q.reverse()
                    trails.add(tuple(q))
    return trails

def part1(chart):
    "Solution to part 1. 36 for the test input. (557)"
    w, h = len(chart[0]), len(chart)
    total = 0
    for y in range(h):
        for x in range(w):
            if chart[y][x] == 0:
                score = trailhead_destinations(chart, y, x)
                total += len(score)
                # print(f"Trailhead at ({y},{x}) has score {score}={len(score)} (total {total})")

    print(f"Part 1: {total}")

def part2(chart):
    "Solution to part 2. 81 for the test input. (1062)"
    w, h = len(chart[0]), len(chart)
    total = 0
    for y in range(h):
        for x in range(w):
            if chart[y][x] == 0:
                trails = complete_trails(chart, y, x)
                total += len(trails)
                # print(f"Trailhead at ({y},{x}) has score {score}={len(score)} (total {total})")

    print(f"Part 2: {total}")

args = parse_args("Advent of Code 2024 - Day 10", "aoc2024-day10-input-test.txt")
rows = read_rows(args.input)
chart = np.array([[int(c) for c in row] for row in rows])
t0 = time.time()
part1(chart)
t1 = time.time() - t0
t0 = time.time()
part2(chart)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
