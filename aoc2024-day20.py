"""
    https://adventofcode.com/2024/day/20

    --- Day 20: Race Condition ---
    The Historians are quite pixelated again. This time, a massive, black building looms over you
    - you're right outside the CPU!

    While The Historians get to work, a nearby program sees that you're idle and challenges you to a
    race. Apparently, you've arrived just in time for the frequently-held race condition festival!

    The race takes place on a particularly long and twisting code path; programs compete to see who
    can finish in the fewest picoseconds. The winner even gets their very own mutex!

    They hand you a map of the racetrack (your puzzle input). For example:

    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #######.#.#.###
    #######.#.#...#
    #######.#.###.#
    ###..E#...#...#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############
    The map consists of track (.) - including the start (S) and end (E) positions (both of which
    also count as track) - and walls (#).

    When a program runs through the racetrack, it starts at the start position. Then, it is allowed
    to move up, down, left, or right; each such move takes 1 picosecond. The goal is to reach the
    end position as quickly as possible. In this example racetrack, the fastest time is 84
    picoseconds.

    Because there is only a single path from the start to the end and the programs all go the same
    speed, the races used to be pretty boring. To make things more interesting, they introduced a
    new rule to the races: programs are allowed to cheat.

    The rules for cheating are very strict. Exactly once during a race, a program may disable
    collision for up to 2 picoseconds. This allows the program to pass through walls as if they were
    regular track. At the end of the cheat, the program must be back on normal track again;
    otherwise, it will receive a segmentation fault and get disqualified.

    So, a program could complete the course in 72 picoseconds (saving 12 picoseconds) by cheating
    for the two moves marked 1 and 2:

    ###############
    #...#...12....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #######.#.#.###
    #######.#.#...#
    #######.#.###.#
    ###..E#...#...#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############
    Or, a program could complete the course in 64 picoseconds (saving 20 picoseconds) by cheating
    for the two moves marked 1 and 2:

    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #######.#.#.###
    #######.#.#...#
    #######.#.###.#
    ###..E#...12..#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############
    This cheat saves 38 picoseconds:

    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #######.#.#.###
    #######.#.#...#
    #######.#.###.#
    ###..E#...#...#
    ###.####1##.###
    #...###.2.#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############
    This cheat saves 64 picoseconds and takes the program directly to the end:

    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #######.#.#.###
    #######.#.#...#
    #######.#.###.#
    ###..21...#...#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############
    Each cheat has a distinct start position (the position where the cheat is activated, just before
    the first move that is allowed to go through walls) and end position; cheats are uniquely
    identified by their start position and end position.

    In this example, the total number of cheats (grouped by the amount of time they save) are as
    follows:

    There are 14 cheats that save 2 picoseconds.
    There are 14 cheats that save 4 picoseconds.
    There are 2 cheats that save 6 picoseconds.
    There are 4 cheats that save 8 picoseconds.
    There are 2 cheats that save 10 picoseconds.
    There are 3 cheats that save 12 picoseconds.
    There is one cheat that saves 20 picoseconds.
    There is one cheat that saves 36 picoseconds.
    There is one cheat that saves 38 picoseconds.
    There is one cheat that saves 40 picoseconds.
    There is one cheat that saves 64 picoseconds.
    You aren't sure what the conditions of the racetrack will be like, so to give yourself as many
    options as possible, you'll need a list of the best cheats. How many cheats would save you at
    least 100 picoseconds?

    --- Part Two ---
    The programs seem perplexed by your list of cheats. Apparently, the two-picosecond cheating rule
    was deprecated several milliseconds ago! The latest version of the cheating rule permits a
    single cheat that instead lasts at most 20 picoseconds.

    Now, in addition to all the cheats that were possible in just two picoseconds, many more cheats
    are possible. This six-picosecond cheat saves 76 picoseconds:

    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #1#####.#.#.###
    #2#####.#.#...#
    #3#####.#.###.#
    #456.E#...#...#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############
    Because this cheat has the same start and end positions as the one above, it's the same cheat,
    even though the path taken during the cheat is different:

    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S12..#.#.#...#
    ###3###.#.#.###
    ###4###.#.#...#
    ###5###.#.###.#
    ###6.E#...#...#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############
    Cheats don't need to use all 20 picoseconds; cheats can last any amount of time up to and
    including 20 picoseconds (but can still only end when the program is on normal track). Any cheat
    time not used is lost; it can't be saved for another cheat later.

    You'll still need a list of the best cheats, but now there are even more to choose between. Here
    are the quantities of cheats in this example that save 50 picoseconds or more:

    There are 32 cheats that save 50 picoseconds.
    There are 31 cheats that save 52 picoseconds.
    There are 29 cheats that save 54 picoseconds.
    There are 39 cheats that save 56 picoseconds.
    There are 25 cheats that save 58 picoseconds.
    There are 23 cheats that save 60 picoseconds.
    There are 20 cheats that save 62 picoseconds.
    There are 19 cheats that save 64 picoseconds.
    There are 12 cheats that save 66 picoseconds.
    There are 14 cheats that save 68 picoseconds.
    There are 12 cheats that save 70 picoseconds.
    There are 22 cheats that save 72 picoseconds.
    There are 4 cheats that save 74 picoseconds.
    There are 3 cheats that save 76 picoseconds.
    Find the best cheats using the updated cheating rules. How many cheats would save you at least
    100 picoseconds?
"""
import time
import heapq
from collections import defaultdict
from common import (parse_args, read_aoc_map, string_to_aoc_map, grid_to_string, aoc_map_to_grid)

SYMBOLS = {".", "#", "S", "E", "O", "1", "2"} # Symbols in the maze.
EMPTY, WALL, START, END, PATH, CHEAT1, CHEAT2 = 0, 1, 2, 3, 4, 5, 6 # Numerical values for the symbols.
NUM_TO_SYMBOL = {EMPTY: ".", WALL: "#", START: "S", END: "E", PATH: "O", CHEAT1: "1", CHEAT2: "2"}
SYMBOL_TO_NUM = {v: k for k, v in NUM_TO_SYMBOL.items()}
assert SYMBOLS == set(SYMBOL_TO_NUM)

def start_end_(grid):
    "Return the start and end positions in the grid."
    start = end = None
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == START: start = (y, x)
            elif cell == END: end = (y, x)
    return start, end

def w_h_(grid): return len(grid[0]), len(grid)

def reconstruct_path(to_prev, y, x):
    "Reconstruct the path traversed from the `to_prev` dictionary starting at (y, x)."
    path = [(y, x)]
    while to_prev[(y, x)]:
        y, x = to_prev[(y, x)]
        path.append((y, x))
    path.reverse()
    return path

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)] # (dy, dx) for right, down, left, up

def solve_grid(grid, w, h, start, end):
    """Return the least costly path through `maze` using Uniform Cost search.
        Maze is a 2D array of 0 (empty) and 1 (wall) cells.
        NOTE: We can't re-use the solve_maze() from day 16 because the long paths take too long
        to reconstruct.
    """
    pq = [(0, start)]     # (score, (y, x), last))
    visited = set()             # (y, x) visited
    to_prev = {start: None}     # (y, x) -> (y, x) previous
    best_score, best_path = float("inf"), [] # Best score and path
    heapq.heapify(pq)

    while pq:
        score, (y, x) = heapq.heappop(pq)
        if (y, x) in visited: continue
        visited.add((y, x))

        if (y, x) == end:
            path = reconstruct_path(to_prev, y, x)
            if score < best_score: best_score, best_path = score, path
            continue

        for dy, dx in DIRECTIONS:
            ny, nx = y + dy, x + dx
            if (ny, nx) in visited: continue
            if not (0 <= ny < h and 0 <= nx < w and grid[ny][nx] != WALL): continue
            heapq.heappush(pq, (score + 1, (ny, nx)))
            to_prev[(ny, nx)] = (y, x)

    return best_score, best_path

def improvements1_(grid, w, h, path):
    """Return a dictionary of improvements that can be made to the path.
        An improvement is a cheat that saves at least 1 picosecond.
        The dictionary keys are (y1, x1, y2, x2) where (y1, x1) is the start of the improvement
        and (y2, x2) is the end of the improvement. The value is the number of picoseconds saved.
    """
    coord_score = {(y, x): score for score, (y, x) in enumerate(path)}
    improvements = {}
    for (y, x), score in coord_score.items():
        for dy1, dx1 in DIRECTIONS:
            y1, x1 = y + dy1, x + dx1
            if not (0 <= y1 < h and 0 <= x1 < w): continue
            if grid[y1][x1] != WALL: continue
            for dy2, dx2 in DIRECTIONS:
                y2, x2 = y1 + dy2, x1 + dx2
                score2 = coord_score.get((y2, x2), score)
                improvement = score - score2 - 2
                if improvement > 0: improvements[(y1, x1, y2, x2)] = improvement
    return improvements

def cheat_len_(p1, p2):
    "Return the Manhattan distance between two points."
    y1, x1 = p1
    y2, x2 = p2
    return abs(y1 - y2) + abs(x1 - x2)

def improvements2_(path, max_cheat, min_improvement):
    """Return a dictionary of improvements that can be made to the path.
        An improvement is a cheat that saves at least `min_improvement` picoseconds.
        Cheat sequences must be at most `max_cheats` long and consist of one of lines that can be
        vertical or horizontal.
        The dictionary keys are (y1, x1, y2, x2) where (y1, x1) is the start of the improvement
        and (y2, x2) is the end of the improvement. The value is the number of picoseconds saved.
    """
    coord_score = {(y, x): score for score, (y, x) in enumerate(path)}
    improvements = {}
    for (y1, x1), dist1 in coord_score.items():
        for (y2, x2), dist2 in coord_score.items():
            cheat_len = cheat_len_((y1, x1), (y2, x2))
            improvement = dist2 - dist1
            if cheat_len <= max_cheat and improvement >= min_improvement + cheat_len:
                improvements[(y1, x1, y2, x2)] = improvement
    return improvements

maze_text = """
    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #######.#.#.###
    #######.#.#...#
    #######.#.###.#
    ###..E#...#...#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############
"""
def test_grid_(): return aoc_map_to_grid(string_to_aoc_map(maze_text, SYMBOLS), SYMBOL_TO_NUM)

def test1():
    grid = test_grid_()
    w, h = w_h_(grid)
    start, end = start_end_(grid)
    print(f"start={start} end={end}")
    print(f"w={w} h={h}")
    score, path = solve_grid(grid, w, h, start, end)
    for y, x in path: grid[y][x] = PATH
    print(f"score={score} maze=\n{grid_to_string(grid, NUM_TO_SYMBOL)}")
    assert score == 84, f"score={score}"

def test2():
    grid = test_grid_()
    w, h = w_h_(grid)
    start, end = start_end_(grid)
    score, path = solve_grid(grid, w, h, start, end)
    print(f"w={w} h={h}")
    print(f"start={start} end={end}")
    print(f"initial_score={score}")
    print(f"grid=\n{grid_to_string(grid, NUM_TO_SYMBOL)}")
    improvements = improvements1_(grid, w, h, path)

    count_improvements = {}
    for (y1, x1, y2, x2), improvement in improvements.items():
        count_improvements[improvement] = count_improvements.get(improvement, 0) + 1
    for improvement, count in sorted(count_improvements.items()):
        print(f"There are {count:2} cheats that save {improvement:2} picoseconds.")

def part1(grid):
    "Solution to part 1. (1422)"
    MIN_IMPROVEMENT = 100
    w, h = w_h_(grid)
    start, end = start_end_(grid)
    _, path = solve_grid(grid, w, h, start, end)
    improvements = improvements1_(grid, w, h, path)
    num_improvements = sum(1 for improvement in improvements.values() if improvement >= MIN_IMPROVEMENT)
    print(f"The number of cheats that improve the score sufficiently is: {num_improvements}")

def part2(grid):
    "Solution to part 2. (1009299)"
    MIN_IMPROVEMENT = 100
    MAX_DIST = 20
    w, h = w_h_(grid)
    start, end = start_end_(grid)
    _, path = solve_grid(grid, w, h, start, end)
    improvements = improvements2_(path, MAX_DIST, MIN_IMPROVEMENT)
    num_improvements = sum(1 for improvement in improvements.values() if improvement >= MIN_IMPROVEMENT)
    print(f"The number of cheats that improve the score sufficiently is: {num_improvements}")

args = parse_args("Advent of Code 2024 - Day 20", "problems/aoc2024-day20-input.txt")

if args.testing:
    # test1()
    test2()
    exit()

aoc_map = read_aoc_map(args.input, SYMBOLS)
grid = aoc_map_to_grid(aoc_map, SYMBOL_TO_NUM)

t0 = time.time()
part1(grid)
t1 = time.time() - t0
t0 = time.time()
part2(grid)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
