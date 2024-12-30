"""
    https://adventofcode.com/2024/day/14

    -- Day 14: Restroom Redoubt ---

    You make a list (your puzzle input) of all of the robots' current positions (p) and velocities
    (v), one robot per line. For example:

    p=0,4 v=3,-3
    p=6,3 v=-1,-3
    p=10,3 v=-1,2
    p=2,0 v=2,-1
    p=0,0 v=1,3
    p=3,0 v=-2,-2
    p=7,6 v=-1,-3
    p=3,0 v=-1,-2
    p=9,3 v=2,3
    p=7,3 v=-1,2
    p=2,4 v=2,-3
    p=9,5 v=-3,-3
    Each robot's position is given as p=x,y where x represents the number of tiles the robot is from
    the left wall and y represents the number of tiles from the top wall (when viewed from above).
    So, a position of p=0,0 means the robot is all the way in the top-left corner.

    Each robot's velocity is given as v=x,y where x and y are given in tiles per second. Positive x
    means the robot is moving to the right, and positive y means the robot is moving down. So, a
    velocity of v=1,-2 means that each second, the robot moves 1 tile to the right and 2 tiles up.

    The robots outside the actual bathroom are in a space which is 101 tiles wide and 103 tiles tall
    (when viewed from above). However, in this example, the robots are in a space which is only 11
    tiles wide and 7 tiles tall.

    The robots are good at navigating over/under each other (due to a combination of springs,
    extendable legs, and quadcopters), so they can share the same tile and don't interact with each
    other. Visually, the number of robots on each tile in this example looks like this:

    1.12.......
    ...........
    ...........
    ......11.11
    1.1........
    .........1.
    .......1...
    These robots have a unique feature for maximum bathroom security: they can teleport. When a
    robot would run into an edge of the space they're in, they instead teleport to the other side,
    effectively wrapping around the edges. Here is what robot p=2,4 v=2,-3 does for the first few
    seconds:

    Initial state:
    ...........
    ...........
    ...........
    ...........
    ..1........
    ...........
    ...........

    After 1 second:
    ...........
    ....1......
    ...........
    ...........
    ...........
    ...........
    ...........

    After 2 seconds:
    ...........
    ...........
    ...........
    ...........
    ...........
    ......1....
    ...........

    After 3 seconds:
    ...........
    ...........
    ........1..
    ...........
    ...........
    ...........
    ...........

    After 4 seconds:
    ...........
    ...........
    ...........
    ...........
    ...........
    ...........
    ..........1

    After 5 seconds:
    ...........
    ...........
    ...........
    .1.........
    ...........
    ...........
    ...........
    The Historian can't wait much longer, so you don't have to simulate the robots for very long.
    Where will the robots be after 100 seconds?

    In the above example, the number of robots on each tile after 100 seconds has elapsed looks like
    this:

    ......2..1.
    ...........
    1..........
    .11........
    .....1.....
    ...12......
    .1....1....
    To determine the safest area, count the number of robots in each quadrant after 100 seconds.
    Robots that are exactly in the middle (horizontally or vertically) don't count as being in any
    quadrant, so the only relevant robots are:

    ..... 2..1.
    ..... .....
    1.... .....

    ..... .....
    ...12 .....
    .1... 1....
    In this example, the quadrants contain 1, 3, 4, and 1 robot. Multiplying these together gives a
    total safety factor of 12.

    Predict the motion of the robots in your list within a space which is 101 tiles wide and 103
    tiles tall. What will the safety factor be after exactly 100 seconds have elapsed?

    --- Part Two ---
    During the bathroom break, someone notices that these robots seem awfully similar to ones built
    and used at the North Pole. If they're the same type of robots, they should have a hard-coded
    Easter egg: very rarely, most of the robots should arrange themselves into a picture of a
    Christmas tree.

    What is the fewest number of seconds that must elapse for the robots to display the Easter egg?
"""
import time
import re, os, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from common import parse_args, read_lines, MyNamespace as ns

# p=0,4 v=3,-3
RE_POS_VEL = re.compile(r"p=(-?\d+),(-?\d+)\s*v=(-?\d+),(-?\d+)")

def robots_(line):
    "Return a tuple of 4 integers from a line."
    m = RE_POS_VEL.search(line)
    assert m, f"Bad line: {line}"
    pv = tuple(map(int, m.groups()))
    return ns(pos=ns(x=pv[0], y=pv[1]), vel=ns(x=pv[2], y=pv[3]))

def test_robots_():
    text = """
    p=0,4 v=3,-3
    p=6,3 v=-1,-3
    p=10,3 v=-1,2
    p=2,0 v=2,-1
    p=0,0 v=1,3
    p=3,0 v=-2,-2
    p=7,6 v=-1,-3
    p=3,0 v=-1,-2
    p=9,3 v=2,3
    p=7,3 v=-1,2
    p=2,4 v=2,-3
    p=9,5 v=-3,-3
    """
    lines = text.splitlines()
    lines = [line for line in lines if line.strip()]
    for line in lines:
        print(robots_(line))

def s(pv): return f"({pv.pos.x},{pv.pos.y})"
def show(q): print(f"{len(q):4}: {' '.join(s(pv) for pv in q)}")

IMAGE_DIR = "images-day14.8"
os.makedirs(IMAGE_DIR, exist_ok=True)

def csv_name_(counter, base): return os.path.join(IMAGE_DIR, f"{base}{counter:03d}.csv")
def img_name_(counter, base): return os.path.join(IMAGE_DIR, f"{base}{counter:03d}.png")

def expand_img(img, min_size):
    "Expand `img` to `min_size` x `min_size` ."
    h, w = img.shape
    if h >= min_size and w >= min_size:
        return img
    n = max(min_size // h, min_size // w)
    expanded = np.repeat(img, n, axis=0)
    expanded = np.repeat(expanded, n, axis=1)
    return expanded

def draw_img(counter, w, h, posvels):
    "Draw the robots on a grid."
    img = np.ones((h, w), dtype=np.uint8) * 255
    for pv in posvels:
        img[pv.pos.y, pv.pos.x] = 0
    img_name = img_name_(counter, "posvels")

    expanded = expand_img(img, 600)
    try:
        plt.imsave(img_name, expanded, cmap='gray', format='png')
    except Exception as e:
        print(f"Error saving {img_name}: expanded={expanded.shape}", file=sys.stderr)
        raise
    return img_name

def move(posvels, w, h):
    "Move the robots one time."
    for pv in posvels:
        pv.pos.x = (pv.pos.x + pv.vel.x + w) % w
        pv.pos.y = (pv.pos.y + pv.vel.y + h) % h

def pv_hash(posvels): return tuple((pv.pos.x, pv.pos.y) for pv in posvels)

CORNER_SIZE = 1.0 / 6.0     # The fraction of the width or height that is a corner.
MAX_IN_CORNERS = 1.0 / 400   # The maximum fraction of points in the corners.

def is_tree(w, h, posvels):
    """Return True if the robots could form a tree. Few points in the corners and a 3x3 contiguous
        block of robots.
    """
    # Check if there are too many points in the corners first because it's faster.
    tx, ty = w * CORNER_SIZE, h * CORNER_SIZE
    w2, h2 = w // 2, h // 2
    max_bad = max(1, MAX_IN_CORNERS * (w * h))
    n_bad = 0
    for pv in posvels:
        x, y = pv.pos.x, pv.pos.y
        dy = y if y < h2 else h - y
        dx = x if x < w2 else w - x
        if dx * ty + dy * tx < tx * ty:
            n_bad += 1
            if n_bad > max_bad: return False
    # Check for a 3x3 block of robots.
    img = np.zeros((h, w), dtype=np.uint8)
    for pv in posvels:  img[pv.pos.y, pv.pos.x] = 1
    for y in range(h - 2):
        for x in range(w - 2):
            if np.all(img[y:y+3, x:x+3]): return True
    return False

def part1(w, h, lines, VERBOSE):
    "Solution to part 1. 12 for the test input. (230900224)"
    NUM_SECS = 100
    robots = [robots_(line) for line in lines]
    print(f"{len(robots)} robots {w}x{h} moving for {NUM_SECS} seconds")
    print(f"{0:4}: {robots[0]}")

    pos = [pv.pos for pv in robots]
    pos.sort(key=lambda p: (p.y, p.x))

    w2, h2 = w // 2, h // 2
    print(f"w2={w2} h2={h2}")
    if VERBOSE:
        for p in pos:
            v, h = " ", " "
            if p.x < w2: h = "-"
            elif p.x > w2: h = "+"
            if p.y < h2: v = "-"
            elif p.y > h2: v = "+"
            print(p, h, v)

    q1, q2, q3, q4 = [], [], [], []
    for pv in robots:
        x, y = pv.pos.x, pv.pos.y
        if   x < w2 and y < h2: q1.append(pv)
        elif x > w2 and y < h2: q2.append(pv)
        elif x < w2 and y > h2: q3.append(pv)
        elif x > w2 and y > h2: q4.append(pv)

    print(len(q1), len(q2), len(q3), len(q4))
    if VERBOSE:
        for q in [q1, q2, q3, q4]: show(q)

    print(f"{len(q1) + len(q2)+ len(q3) + len(q4)} safe robots")
    print(f"Part 1: {len(q1) * len(q2) * len(q3) * len(q4)}")

def part2(w, h, lines, VERBOSE):
    "Solution to part 2.  (6532)"
    robots = [robots_(line) for line in lines]
    print(f"{len(robots)} robots {w}x{h}")
    print(f"{0:4}: {robots[0]}")

    seen = set()
    good = 0
    last = 0
    tree_i = -1
    draw_img(0, w, h, robots)
    for i in range(10_000_000):
        hs = pv_hash(robots)
        if hs in seen:
            print(f"Repeat at {i}")
            break
        seen.add(hs)
        move(robots, w, h)
        if not is_tree(w, h, robots): continue
        good += 1
        print(f"{i+1:4}: {good:4} ({(i+1)//good}) {i - last}")
        last = i
        draw_img(i+1, w, h, robots)
        if tree_i < 0: tree_i = i
    print(f"Part 2: {tree_i}")

args = parse_args("Advent of Code 2024 - Day 13", "problems/aoc2024-day14-input-test.txt")
if args.testing:
    test_robots_()
    exit(0)

lines = read_lines(args.input)
if args.input == "problems/aoc2024-day14-input-test.txt":
    w, h = 11, 7
else:
    w, h = 101, 103
t0 = time.time()
part1(w, h, lines, args.verbose)
t1 = time.time() - t0
t0 = time.time()
part2(w, h, lines, args.verbose)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
