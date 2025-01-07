"""
    https://adventofcode.com/2024/day/16

    --- Day 16: Reindeer Maze ---
    It's time again for the Reindeer Olympics! This year, the big event is the Reindeer Maze, where
    the Reindeer compete for the lowest score.

    You and The Historians arrive to search for the Chief right as the event is about to start. It
    wouldn't hurt to watch a little, right?

    The Reindeer start on the Start Tile (marked S) facing East and need to reach the End Tile
    (marked E). They can move forward one tile at a time (increasing their score by 1 point), but
    never into a wall (#). They can also rotate clockwise or counterclockwise 90 degrees at a time
    (increasing their score by 1000 points).

    To figure out the best place to sit, you start by grabbing a map (your puzzle input) from a
    nearby kiosk. For example:

    ###############
    #.......#....E#
    #.#.###.#.###.#
    #.....#.#...#.#
    #.###.#####.#.#
    #.#.#.......#.#
    #.#.#####.###.#
    #...........#.#
    ###.#.#####.#.#
    #...#.....#.#.#
    #.#.#.###.#.#.#
    #.....#...#.#.#
    #.###.#.#.#.#.#
    #S..#.....#...#
    ###############
    There are many paths through this maze, but taking any of the best paths would incur a score of
    only 7036. This can be achieved by taking a total of 36 steps forward and turning 90 degrees a
    total of 7 times:


    ###############
    #.......#....E#
    #.#.###.#.###^#
    #.....#.#...#^#
    #.###.#####.#^#
    #.#.#.......#^#
    #.#.#####.###^#
    #..>>>>>>>>v#^#
    ###^#.#####v#^#
    #>>^#.....#v#^#
    #^#.#.###.#v#^#
    #^....#...#v#^#
    #^###.#.#.#v#^#
    #S..#.....#>>^#
    ###############
    Here's a second example:

    #################
    #...#...#...#..E#
    #.#.#.#.#.#.#.#.#
    #.#.#.#...#...#.#
    #.#.#.#.###.#.#.#
    #...#.#.#.....#.#
    #.#.#.#.#.#####.#
    #.#...#.#.#.....#
    #.#.#####.#.###.#
    #.#.#.......#...#
    #.#.###.#####.###
    #.#.#...#.....#.#
    #.#.#.#####.###.#
    #.#.#.........#.#
    #.#.#.#########.#
    #S#.............#
    #################
    In this maze, the best paths cost 11048 points; following one such path would look like this:

    #################
    #...#...#...#..E#
    #.#.#.#.#.#.#.#^#
    #.#.#.#...#...#^#
    #.#.#.#.###.#.#^#
    #>>v#.#.#.....#^#
    #^#v#.#.#.#####^#
    #^#v..#.#.#>>>>^#
    #^#v#####.#^###.#
    #^#v#..>>>>^#...#
    #^#v###^#####.###
    #^#v#>>^#.....#.#
    #^#v#^#####.###.#
    #^#v#^........#.#
    #^#v#^#########.#
    #S#>>^..........#
    #################
    Note that the path shown above includes one 90 degree turn as the very first move, rotating the
    Reindeer from facing East to facing North.

    Analyze your map carefully. What is the lowest score a Reindeer could possibly get?

    --- Part Two ---
    Now that you know what the best paths look like, you can figure out the best spot to sit.

    Every non-wall tile (S, ., or E) is equipped with places to sit along the edges of the tile.
    While determining which of these tiles would be the best spot to sit depends on a whole bunch of
    factors (how comfortable the seats are, how far away the bathrooms are, whether there's a pillar
    blocking your view, etc.), the most important factor is whether the tile is on one of the best
    paths through the maze. If you sit somewhere else, you'd miss all the action!

    So, you'll need to determine which tiles are part of any best path through the maze, including
    the S and E tiles.

    In the first example, there are 45 tiles (marked O) that are part of at least one of the various
    best paths through the maze:

    ###############
    #.......#....O#
    #.#.###.#.###O#
    #.....#.#...#O#
    #.###.#####.#O#
    #.#.#.......#O#
    #.#.#####.###O#
    #..OOOOOOOOO#O#
    ###O#O#####O#O#
    #OOO#O....#O#O#
    #O#O#O###.#O#O#
    #OOOOO#...#O#O#
    #O###.#.#.#O#O#
    #O..#.....#OOO#
    ###############
    In the second example, there are 64 tiles that are part of at least one of the best paths:

    #################
    #...#...#...#..O#
    #.#.#.#.#.#.#.#O#
    #.#.#.#...#...#O#
    #.#.#.#.###.#.#O#
    #OOO#.#.#.....#O#
    #O#O#.#.#.#####O#
    #O#O..#.#.#OOOOO#
    #O#O#####.#O###O#
    #O#O#..OOOOO#OOO#
    #O#O###O#####O###
    #O#O#OOO#..OOO#.#
    #O#O#O#####O###.#
    #O#O#OOOOOOO..#.#
    #O#O#O#########.#
    #O#OOO..........#
    #################
    Analyze your map further. How many tiles are part of at least one of the best paths through the
    maze?
"""
import time
import heapq
from common import parse_args, read_aoc_map, string_to_aoc_map, concat, mark_aoc_map, clean_map_text

SYMBOLS = {'#', '.', 'S', 'E', 'O'} # Symbols in the maze

def find_start_end(maze):
    "Find the start and end positions in the maze."
    start = end = None
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == 'S': start = (y, x)
            elif char == 'E': end = (y, x)
    return start, end

DIRECTIONS = [(0, 1, 'E'), (1, 0, 'S'), (0, -1, 'W'), (-1, 0, 'N')] # (dy, dx, direction)
DIRECTION_MAP = {'E': 0, 'S': 1, 'W': 2, 'N': 3} # {d: i for i, (_, _, d) in enumerate(DIRECTIONS)}

PENALTY_MOVE = 1 # Penalty for moving forward
PENALTY_TURN = 1000 # Penalty for turning

def reconstruct_paths(predecessors, end):
    "Reconstruct the paths traversed from the `predecessors` dictionary starting at `end`."
    stack = [[end]]
    paths = []
    while stack:
        path = stack.pop()
        current = path[-1]
        if current not in predecessors: paths.append(path)
        else: stack.extend(path + [pred] for pred in predecessors[current])
    return [[(y, x) for (y, x, _, _) in path] for path in paths]

def reconstruct_points(predecessors, end):
    "Return the unique points in the paths traversed `predecessors` starting at `end`"
    stack = [end]
    points = set()
    while stack:
        current = stack.pop()
        points.add(tuple(current[:2]))
        if current in predecessors: stack.extend(predecessors[current])
    return points

def solve_maze_paths(maze):
    """Return all the least costly paths through `maze` using Uniform Cost search.
        The maze is a list of strings where each string is a row of the maze.
        The maze is a rectangular grid of tiles. The tiles are: '#', '.', 'S', 'E'.
        The start tile is 'S' and the end tile is 'E'.
    """
    w, h = len(maze[0]), len(maze)
    start, end = find_start_end(maze)
    y, x = start

    start_state = ("E", (y, x, 0, 0)) # (direction, (y, x, dy, dx))
    pq = [(0, start_state)]           # (score, state)
    visited = set()                   # (y, x) visited
    predecessors = {}                 # {point on path: [predecessors]}
    best_score, best_paths = float('inf'), [] # Best score and paths

    heapq.heapify(pq)

    while pq:
        score, (direction, (y, x, dy, dx)) = heapq.heappop(pq)
        if (y, x, dy, dx) in visited: continue
        visited.add((y, x, dy, dx))

        if (y, x) == end:
            paths = reconstruct_paths(predecessors, (y, x, dy, dx))
            if score < best_score: best_score, best_paths = score, paths
            elif score == best_score: best_paths.extend(paths)
            continue

        for ndy, ndx, new_direction in DIRECTIONS:
            ny, nx = y + ndy, x + ndx
            if (ny, nx, ndy, ndx) in visited: continue
            if not (0 <= ny < h and 0 <= nx < w and maze[ny][nx] != '#'): continue
            new_state = (new_direction, (ny, nx, ndy, ndx))
            new_score = score + PENALTY_MOVE + PENALTY_TURN * int(direction != new_direction)
            heapq.heappush(pq, (new_score, new_state))
            if (ny, nx, ndy, ndx) not in predecessors: predecessors[(ny, nx, ndy, ndx)] = []
            predecessors[(ny, nx, ndy, ndx)].append((y, x, dy, dx))

    return best_score, best_paths

def solve_maze_points(maze):
    """Return all points in all the least costly paths through `maze` using Uniform Cost search.
        The maze is a list of strings where each string is a row of the maze.
        The maze is a rectangular grid of tiles. The tiles are: '#', '.', 'S', 'E'.
        The start tile is 'S' and the end tile is 'E'.
        This uses less memory than solve_maze_points() as it doesn't store every best path.
    """
    w, h = len(maze[0]), len(maze)
    start, end = find_start_end(maze)
    y, x = start

    start_state = ("E", (y, x, 0, 0)) # (direction, (y, x, dy, dx))
    pq = [(0, start_state)]           # (score, state)
    visited = set()                   # (y, x) visited
    predecessors = {}                 # {point on path: [predecessors]}
    best_score, best_points = float('inf'), set() # Best score and point.

    heapq.heapify(pq)

    while pq:
        score, (direction, (y, x, dy, dx)) = heapq.heappop(pq)
        if (y, x, dy, dx) in visited: continue
        visited.add((y, x, dy, dx))

        if (y, x) == end:
            points = reconstruct_points(predecessors, (y, x, dy, dx))
            if score < best_score: best_score, best_points = score, points
            elif score == best_score: best_points.union(points)
            continue

        for ndy, ndx, new_direction in DIRECTIONS:
            ny, nx = y + ndy, x + ndx
            if (ny, nx, ndy, ndx) in visited: continue
            if not (0 <= ny < h and 0 <= nx < w and maze[ny][nx] != '#'): continue
            new_state = (new_direction, (ny, nx, ndy, ndx))
            new_score = score + PENALTY_MOVE + PENALTY_TURN * int(direction != new_direction)
            heapq.heappush(pq, (new_score, new_state))
            if (ny, nx, ndy, ndx) not in predecessors: predecessors[(ny, nx, ndy, ndx)] = []
            predecessors[(ny, nx, ndy, ndx)].append((y, x, dy, dx))

    return best_score, best_points

def part1(maze):
    "Solution to part 1. 7036 for the test input. (127520)"
    score, _  = solve_maze_points(maze)
    print(f"The minimum score to solve the Reindeer Maze is: {score}")

def part2(maze, optimise):
    "Solution to part 2. 45 for the test input. (565)"
    if optimise:
        tiles = solve_maze_points(maze)
    else:
        _, paths = solve_maze_paths(maze)
        tiles = {(y, x) for p in paths for y, x in p}
    print(f"There are {len(tiles)} tiles in the best path through the maze.")

args = parse_args("Advent of Code 2024 - Day 16", "problems/aoc2024-day16-input-test.1.txt")
maze = read_aoc_map(args.input, SYMBOLS)

t0 = time.time()
part1(maze)
t1 = time.time() - t0
t0 = time.time()
part2(maze, args.optimise)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
