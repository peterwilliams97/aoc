"""
    https://adventofcode.com/2024/day/18

    --- Day 18: RAM Run ---
    You and The Historians look a lot more pixelated than you remember. You're inside a computer at
    the North Pole!

    Just as you're about to check out your surroundings, a program runs up to you. "This region of
    memory isn't safe! The User misunderstood what a pushdown automaton is and their algorithm is
    pushing whole bytes down on top of us! Run!"

    The algorithm is fast - it's going to cause a byte to fall into your memory space once every
    nanosecond! Fortunately, you're faster, and by quickly scanning the algorithm, you create a list
    of which bytes will fall (your puzzle input) in the order they'll land in your memory space.

    Your memory space is a two-dimensional grid with coordinates that range from 0 to 70 both
    horizontally and vertically. However, for the sake of example, suppose you're on a smaller grid
    with coordinates that range from 0 to 6 and the following list of incoming byte positions:

    5,4
    4,2
    4,5
    3,0
    2,1
    6,3
    2,4
    1,5
    0,6
    3,3
    2,6
    5,1
    1,2
    5,5
    2,5
    6,5
    1,4
    0,4
    6,4
    1,1
    6,1
    1,0
    0,5
    1,6
    2,0
    Each byte position is given as an X,Y coordinate, where X is the distance from the left edge of
    your memory space and Y is the distance from the top edge of your memory space.

    You and The Historians are currently in the top left corner of the memory space (at 0,0) and
    need to reach the exit in the bottom right corner (at 70,70 in your memory space, but at 6,6 in
    this example). You'll need to simulate the falling bytes to plan out where it will be safe to
    run; for now, simulate just the first few bytes falling into your memory space.

    As bytes fall into your memory space, they make that coordinate corrupted. Corrupted memory
    coordinates cannot be entered by you or The Historians, so you'll need to plan your route
    carefully. You also cannot leave the boundaries of the memory space; your only hope is to reach
    the exit.

    In the above example, if you were to draw the memory space after the first 12 bytes have fallen
    (using . for safe and # for corrupted), it would look like this:

    ...#...
    ..#..#.
    ....#..
    ...#..#
    ..#..#.
    .#..#..
    #.#....
    You can take steps up, down, left, or right. After just 12 bytes have corrupted locations in
    your memory space, the shortest path from the top left corner to the exit would take 22 steps.
    Here (marked with O) is one such path:

    OO.#OOO
    .O#OO#O
    .OOO#OO
    ...#OO#
    ..#OO#.
    .#.O#..
    #.#OOOO
    Simulate the first kilobyte (1024 bytes) falling onto your memory space. Afterward, what is the
    minimum number of steps needed to reach the exit?

    --- Part Two ---
    The Historians aren't as used to moving around in this pixelated universe as you are. You're
    afraid they're not going to be fast enough to make it to the exit before the path is completely
    blocked.

    To determine how fast everyone needs to go, you need to determine the first byte that will cut
    off the path to the exit.

    In the above example, after the byte at 1,1 falls, there is still a path to the exit:

    O..#OOO
    O##OO#O
    O#OO#OO
    OOO#OO#
    ###OO##
    .##O###
    #.#OOOO
    However, after adding the very next byte (at 6,1), there is no longer a path to the exit:

    ...#...
    .##..##
    .#..#..
    ...#..#
    ###..##
    .##.###
    #.#....
    So, in this example, the coordinates of the first byte that prevents the exit from being
    reachable are 6,1.

    Simulate more of the bytes that are about to corrupt your memory space. What are the coordinates
    of the first byte that will prevent the exit from being reachable from your starting position?
    (Provide the answer as two integers separated by a comma with no other characters.)
"""
import time
import heapq
from common import read_lines, parse_args, grid_to_string

def reconstruct_path(to_prev, y, x):
    """Reconstruct the path traversed from the `to_prev` dictionary starting at (y, x).
       (y, x) is the last position.
    """
    path = [(y, x)]
    while to_prev[(y, x)]:
        y, x = to_prev[(y, x)]
        path.append((y, x))
    path.reverse()
    return path

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
EMPTY, WALL, PATH = 0, 1, 2
NUM_TO_SYMBOL = {EMPTY: ".", WALL: "#", PATH: "O"}
INFINITY = float('inf')

def solve_grid(w, h, maze, verbose=False):
    """Return the least costly path through `maze` using Uniform Cost search.
        Maze is a 2D array of 0 (empty) and 1 (wall) cells.
        It is `w` cells wide and `h` cells high.
        The starting pint is (0,0) and the ending point is (h-1, w-1).
        NOTE: We can't re-use the solve_grid() from da 16 because the long paths take too long
        to reconstruct.
    """
    start, end = (0, 0), (h-1, w-1)

    pq = [(0, start)]           # (score, state)
    visited = set()             # (y, x) visited
    to_prev = {start: None}     # (y, x) -> (y, x) previous
    best_score, best_path = INFINITY, [] # Best score and path
    heapq.heapify(pq)
    num_steps = 0

    while pq:
        score, (y, x) = heapq.heappop(pq)
        if (y, x) in visited: continue
        visited.add((y, x))
        num_steps += 1

        if verbose:
            if num_steps % 1_000 == 100:
                print(f"    Step {num_steps} ({y},{x}) score={score} pq={len(pq)}")

        if (y, x) == end:
            if verbose: print(f"    Found end: {score}")
            path = reconstruct_path(to_prev, y, x)
            if verbose:
                for i, path in enumerate(path):
                    print(f"    Path[{i+1}] {len(path)} {[f'{y}-{x}' for (y,x) in path]}")
            if score < best_score: best_score, best_path = score, path
            continue

        for ndy, ndx in DIRECTIONS:
            ny, nx = y + ndy, x + ndx
            if (ny, nx) in visited: continue
            if not (0 <= ny < h and 0 <= nx < w and maze[ny][nx] == EMPTY): continue
            heapq.heappush(pq, (score + 1, (ny, nx)))
            to_prev[(ny, nx)] = (y, x)

    return best_score, best_path, num_steps

def test_grid():
    """Return a test grid."""
    w, h = 7, 7
    walls = [(5, 4), (4, 2), (4, 5), (3, 0), (2, 1), (6, 3), (2, 4), (1, 5), (0, 6), (3, 3),
              (2, 6), (5, 1), (1, 2), (5, 5), (2, 5), (6, 5), (1, 4), (0, 4), (6, 4), (1, 1),
              (6, 1), (1, 0), (0, 5), (1, 6), (2, 0)]
    walls = walls[:12]

    maze = [[EMPTY for _ in range(w)] for _ in range(h)]
    for x,y in walls: maze[y][x] = WALL
    return maze, w, h, walls

def test1():
    """Test part 1."""
    grid, w, h, walls = test_grid()

    maze_text = grid_to_string(grid, NUM_TO_SYMBOL)
    print(f"Points: {len(walls)} {walls}")
    print(f"Maze:\n{maze_text}")

    score, path, num_steps = solve_grid(w, h, grid)
    print(f"  Best score {score} in {num_steps} steps")
    for y, x in path: grid[y][x] = PATH
    maze_text = grid_to_string(grid, NUM_TO_SYMBOL)
    print(f"  Best score {score} in {num_steps} steps")
    print(f"Path: {len(path)} {path}")
    print(f"Maze:\n{maze_text}")

def test2():
    """Test part 2."""
    maze0, w, h, walls = test_grid()

    maze_text = grid_to_string(maze0, NUM_TO_SYMBOL)

    score, path, num_steps = solve_grid(w, h, maze0)
    print(f"  Best score {score} in {num_steps} steps")
    maze_text = grid_to_string(maze0, NUM_TO_SYMBOL)

    print(f"Path: {len(path)} {path}")
    print(f"Maze0:\n{maze_text}")
    maze1 = [row.copy() for row in maze0]
    for y, x in path: maze1[y][x] = PATH
    maze_text = grid_to_string(maze1, NUM_TO_SYMBOL)
    print(f"Maze1:\n{maze_text}")

    for y, x in path[1:-1]:
        maze = [row.copy() for row in maze0]
        if maze[y][x] == WALL: continue
        maze[y][x] = WALL
        score, path, _ = solve_grid(w, h, maze)
        print(f"Blocking {x} {y}  Best score {score} in {num_steps} steps")
        if score == INFINITY: break

    maze_text = grid_to_string(maze, NUM_TO_SYMBOL)
    print(f"Path: {len(path)} {path}")
    print(f"Maze:\n{maze_text}")

def part1(w,h, max_points, points, verbose):
    """Solution to part 1. (344)"""
    maze = [[EMPTY for _ in range(w)] for _ in range(h)]
    assert len(points) > max_points, f"Too many points {len(points)} < {max_points}"
    for x,y in points[:max_points]: maze[y][x] = WALL
    score, _, _ = solve_grid(w, h, maze, verbose)
    print(f"Part 1: The shortest path is: {score}")

def part2(w,h, max_points, points, verbose):
    "Solution to part 2. (46,18)"
    maze0 = [[EMPTY for _ in range(w)] for _ in range(h)]
    assert len(points) > max_points, f"Too many points {len(points)} < {max_points}"
    print(f"Points: {len(points)} max={max_points} diff={len(points) - max_points}")

    for x,y in points[:max_points]: maze0[y][x] = WALL

    score0, path0, _ = solve_grid(w, h, maze0, verbose)
    print(f"path0: {len(path0)}")
    print(f"score0: {score0}")

    # TODO: Check points argainst most recent path.
    existing_path = {(y, x) for (y, x) in path0 if not ((x == 0 and y == 0) or (x == w-1 and y == h-1))}
    assert len(existing_path) == len(path0) - 2, f"Invalid existing_path {len(existing_path)} != {len(path0)}"

    print(f"Points: {len(points)} {len(points[max_points:])} ============================")
    maze = [row[:] for row in maze0]

    for (x, y) in points:
        maze[y][x] = WALL
        _, path, _ = solve_grid(w, h, maze)
        if not path:
            blocker = (x, y)
            break

    print(f"Part 2: First blocker {blocker}")

args = parse_args("Advent of Code 2024 - Day 18", "problems/aoc2024-day18-input-test.txt")

if args.testing:
    test1()
    test2()
    exit()

lines = read_lines(args.input)
points = [tuple(map(int, line.split(","))) for line in lines]

if args.input == "problems/aoc2024-day18-input-test.txt":
    W, H = 7, 7
    MAX_POINTS = 12
else:
    W, H = 71, 71
    MAX_POINTS = 1024

t0 = time.time()
part1(W, H, MAX_POINTS, points, args.verbose)
t1 = time.time() - t0
t0 = time.time()
part2(W, H, MAX_POINTS, points, args.verbose)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
