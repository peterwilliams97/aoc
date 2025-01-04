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
import heapq

def parse_maze(maze):
    start, end = None, None
    grid = []

    for r, line in enumerate(maze):
        grid.append(list(line))
        for c, char in enumerate(line):
            if char == 'S':
                start = (r, c)
            elif char == 'E':
                end = (r, c)

    return grid, start, end

# Directions (NORTH, EAST, SOUTH, WEST) in (dy, dx) form
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def dijkstra_min_score(maze):
    grid, start, end = parse_maze(maze)

    # Priority queue: (score, row, col, direction)
    pq = [(0, start[0], start[1], 1)]  # Start facing EAST
    visited = set()

    while pq:
        score, r, c, dir_idx = heapq.heappop(pq)

        if (r, c, dir_idx) in visited:
            continue
        visited.add((r, c, dir_idx))

        # Check if we reached the end
        if (r, c) == end:
            return score

        # 1. Move forward
        dr, dc = directions[dir_idx]
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
            heapq.heappush(pq, (score + 1, nr, nc, dir_idx))

        # 2. Turn left (counterclockwise)
        new_dir_left = (dir_idx - 1) % 4
        heapq.heappush(pq, (score + 1000, r, c, new_dir_left))

        # 3. Turn right (clockwise)
        new_dir_right = (dir_idx + 1) % 4
        heapq.heappush(pq, (score + 1000, r, c, new_dir_right))

def dijkstra_all_best_paths(maze):
    grid, start, end = parse_maze(maze)

    # Priority queue: (score, row, col, direction, path)
    pq = [(0, start[0], start[1], 1, [])]  # Start facing EAST
    visited, best_score, all_best_paths  = set(), float('inf'), []

    while pq:
        score, r, c, dir_idx, path = heapq.heappop(pq)

        if (r, c, dir_idx) in visited and score >= best_score: continue
        visited.add((r, c, dir_idx))

        # Check if we reached the end
        if (r, c) == end:
            if score < best_score:
                best_score = score
                all_best_paths = [path + [(r, c)]]
            elif score == best_score: all_best_paths.append(path + [(r, c)])
            continue

        # 1. Move forward
        dr, dc = directions[dir_idx]
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
            heapq.heappush(pq, (score + 1, nr, nc, dir_idx, path + [(r, c)]))

        # 2. Turn left (counterclockwise)
        new_dir_left = (dir_idx - 1) % 4
        heapq.heappush(pq, (score + 1000, r, c, new_dir_left, path))

        # 3. Turn right (clockwise)
        new_dir_right = (dir_idx + 1) % 4
        heapq.heappush(pq, (score + 1000, r, c, new_dir_right, path))

    return all_best_paths

def find_best_path_tiles(maze):
    all_best_paths = dijkstra_all_best_paths(maze)
    tiles_on_best_paths = set()

    for path in all_best_paths:
        for r, c in path:
            tiles_on_best_paths.add((r, c))

    return tiles_on_best_paths


# Sample input
maze_input = [
    "###############",
    "#.......#....E#",
    "#.#.###.#.###.#",
    "#.....#.#...#.#",
    "#.###.#####.#.#",
    "#.#.#.......#.#",
    "#.#.#####.###.#",
    "#...........#.#",
    "###.#.#####.#.#",
    "#...#.....#.#.#",
    "#.#.#.###.#.#.#",
    "#.....#...#.#.#",
    "#.###.#.#.#.#.#",
    "#S..#.....#...#",
    "###############",
]

# Part 1
real_maze_input = open("problems/aoc2024-day16-input.txt").read().strip().split("\n")
print("Minimum score:", dijkstra_min_score(maze_input))
print("Real minimum score:", dijkstra_min_score(real_maze_input))

# Part 2
tiles_on_best_paths = find_best_path_tiles(maze_input)
real_tiles_on_best_paths = find_best_path_tiles(real_maze_input)
num_best_path_tiles = len(tiles_on_best_paths)

# Visualize the maze with best path tiles marked as 'O'
def visualize_maze_with_best_paths(maze, best_path_tiles):
    grid = [list(line) for line in maze]
    for r, c in best_path_tiles:
        if grid[r][c] not in ['S', 'E']:
            grid[r][c] = 'O'

    for row in grid:
        print(''.join(row))

print(f"Number of tiles on best paths: {len(real_tiles_on_best_paths)}")
visualize_maze_with_best_paths(maze_input, tiles_on_best_paths)
