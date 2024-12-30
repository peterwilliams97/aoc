"""
    https://adventofcode.com/2024/day/15

    --- Day 15: Warehouse Woes ---
    You appear back inside your own mini submarine! Each Historian drives their mini submarine in a
    different direction; maybe the Chief has his own submarine down here somewhere as well?

    You look up to see a vast school of lanternfish swimming past you. On closer inspection, they
    seem quite anxious, so you drive your mini submarine over to see if you can help.

    Because lanternfish populations grow rapidly, they need a lot of food, and that food needs to be
    stored somewhere. That's why these lanternfish have built elaborate warehouse complexes operated
    by robots!

    These lanternfish seem so anxious because they have lost control of the robot that operates one
    of their most important warehouses! It is currently running amok, pushing around boxes in the
    warehouse with no regard for lanternfish logistics or lanternfish inventory management
    strategies.

    Right now, none of the lanternfish are brave enough to swim up to an unpredictable robot so they
    could shut it off. However, if you could anticipate the robot's movements, maybe they could find
    a safe option.

    The lanternfish already have a map of the warehouse and a list of movements the robot will
    attempt to make (your puzzle input). The problem is that the movements will sometimes fail as
    boxes are shifted around, making the actual movements of the robot difficult to predict.

    For example:

    ##########
    #..O..O.O#
    #......O.#
    #.OO..O.O#
    #..O@..O.#
    #O#..O...#
    #O..O..O.#
    #.OO.O.OO#
    #....O...#
    ##########

    <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
    vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
    ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
    <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
    ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
    ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
    >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
    <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
    ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
    v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
    As the robot (@) attempts to move, if there are any boxes (O) in the way, the robot will also
    attempt to push those boxes. However, if this action would cause the robot or a box to move into
    a wall (#), nothing moves instead, including the robot. The initial positions of these are shown
    on the map at the top of the document the lanternfish gave you.

    The rest of the document describes the moves (^ for up, v for down, < for left, > for right)
    that the robot will attempt to make, in order. (The moves form a single giant sequence; they are
    broken into multiple lines just to make copy-pasting easier. Newlines within the move sequence
    should be ignored.)

    Here is a smaller example to get started:

    ########
    #..O.O.#
    ##@.O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    <^^>>>vv<v>>v<<
    Were the robot to attempt the given sequence of moves, it would push around the boxes as follows:

    Initial state:
    ########
    #..O.O.#
    ##@.O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    Move <:
    ########
    #..O.O.#
    ##@.O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    Move ^:
    ########
    #.@O.O.#
    ##..O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    Move ^:
    ########
    #.@O.O.#
    ##..O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    Move >:
    ########
    #..@OO.#
    ##..O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    Move >:
    ########
    #...@OO#
    ##..O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    Move >:
    ########
    #...@OO#
    ##..O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    Move v:
    ########
    #....OO#
    ##..@..#
    #...O..#
    #.#.O..#
    #...O..#
    #...O..#
    ########

    Move v:
    ########
    #....OO#
    ##..@..#
    #...O..#
    #.#.O..#
    #...O..#
    #...O..#
    ########

    Move <:
    ########
    #....OO#
    ##.@...#
    #...O..#
    #.#.O..#
    #...O..#
    #...O..#
    ########

    Move v:
    ########
    #....OO#
    ##.....#
    #..@O..#
    #.#.O..#
    #...O..#
    #...O..#
    ########

    Move >:
    ########
    #....OO#
    ##.....#
    #...@O.#
    #.#.O..#
    #...O..#
    #...O..#
    ########

    Move >:
    ########
    #....OO#
    ##.....#
    #....@O#
    #.#.O..#
    #...O..#
    #...O..#
    ########

    Move v:
    ########
    #....OO#
    ##.....#
    #.....O#
    #.#.O@.#
    #...O..#
    #...O..#
    ########

    Move <:
    ########
    #....OO#
    ##.....#
    #.....O#
    #.#O@..#
    #...O..#
    #...O..#
    ########

    Move <:
    ########
    #....OO#
    ##.....#
    #.....O#
    #.#O@..#
    #...O..#
    #...O..#
    ########
    The larger example has many more moves; after the robot has finished those moves, the warehouse
    would look like this:

    ##########
    #.O.O.OOO#
    #........#
    #OO......#
    #OO@.....#
    #O#.....O#
    #O.....OO#
    #O.....OO#
    #OO....OO#
    ##########
    The lanternfish use their own custom Goods Positioning System (GPS for short) to track the
    locations of the boxes. The GPS coordinate of a box is equal to 100 times its distance from the
    top edge of the map plus its distance from the left edge of the map. (This process does not stop
    at wall tiles; measure all the way to the edges of the map.)

    So, the box shown below has a distance of 1 from the top edge of the map and 4 from the left
    edge of the map, resulting in a GPS coordinate of 100 * 1 + 4 = 104.

    #######
    #...O..
    #......
    The lanternfish would like to know the sum of all boxes' GPS coordinates after the robot finishes
    moving. In the larger example, the sum of all boxes' GPS coordinates is 10092. In the smaller
    example, the sum is 2028.

    Predict the motion of the robot and boxes in the warehouse. After the robot is finished moving,
    what is the sum of all boxes' GPS coordinates?

    --- Part Two ---
    The lanternfish use your information to find a safe moment to swim in and turn off the
    malfunctioning robot! Just as they start preparing a festival in your honor, reports start
    coming in that a second warehouse's robot is also malfunctioning.

    This warehouse's layout is surprisingly similar to the one you just helped. There is one key
    difference: everything except the robot is twice as wide! The robot's list of movements doesn't
    change.

    To get the wider warehouse's map, start with your original map and, for each tile, make the
    following changes:

    If the tile is #, the new map contains ## instead.
    If the tile is O, the new map contains [] instead.
    If the tile is ., the new map contains .. instead.
    If the tile is @, the new map contains @. instead.
    This will produce a new warehouse map which is twice as wide and with wide boxes that are
    represented by []. (The robot does not change size.)

    The larger example from before would now look like this:

    ####################
    ##....[]....[]..[]##
    ##............[]..##
    ##..[][]....[]..[]##
    ##....[]@.....[]..##
    ##[]##....[]......##
    ##[]....[]....[]..##
    ##..[][]..[]..[][]##
    ##........[]......##
    ####################
    Because boxes are now twice as wide but the robot is still the same size and speed, boxes can be
    aligned such that they directly push two other boxes at once. For example, consider this situation:

    #######
    #...#.#
    #.....#
    #..OO@#
    #..O..#
    #.....#
    #######

    <vv<<^^<<^^
    After appropriately resizing this map, the robot would push around these boxes as follows:

    Initial state:
    ##############
    ##......##..##
    ##..........##
    ##....[][]@.##
    ##....[]....##
    ##..........##
    ##############

    Move <:
    ##############
    ##......##..##
    ##..........##
    ##...[][]@..##
    ##....[]....##
    ##..........##
    ##############

    Move v:
    ##############
    ##......##..##
    ##..........##
    ##...[][]...##
    ##....[].@..##
    ##..........##
    ##############

    Move v:
    ##############
    ##......##..##
    ##..........##
    ##...[][]...##
    ##....[]....##
    ##.......@..##
    ##############

    Move <:
    ##############
    ##......##..##
    ##..........##
    ##...[][]...##
    ##....[]....##
    ##......@...##
    ##############

    Move <:
    ##############
    ##......##..##
    ##..........##
    ##...[][]...##
    ##....[]....##
    ##.....@....##
    ##############

    Move ^:
    ##############
    ##......##..##
    ##...[][]...##
    ##....[]....##
    ##.....@....##
    ##..........##
    ##############

    Move ^:
    ##############
    ##......##..##
    ##...[][]...##
    ##....[]....##
    ##.....@....##
    ##..........##
    ##############

    Move <:
    ##############
    ##......##..##
    ##...[][]...##
    ##....[]....##
    ##....@.....##
    ##..........##
    ##############

    Move <:
    ##############
    ##......##..##
    ##...[][]...##
    ##....[]....##
    ##...@......##
    ##..........##
    ##############

    Move ^:
    ##############
    ##......##..##
    ##...[][]...##
    ##...@[]....##
    ##..........##
    ##..........##
    ##############

    Move ^:
    ##############
    ##...[].##..##
    ##...@.[]...##
    ##....[]....##
    ##..........##
    ##..........##
    ##############
    This warehouse also uses GPS to locate the boxes. For these larger boxes, distances are measured
    from the edge of the map to the closest edge of the box in question. So, the box shown below has
    a distance of 1 from the top edge of the map and 5 from the left edge of the map, resulting in a
    GPS coordinate of 100 * 1 + 5 = 105.

    ##########
    ##...[]...
    ##........
    In the scaled-up version of the larger example from above, after the robot has finished all of
    its moves, the warehouse would look like this:

    ####################
    ##[].......[].[][]##
    ##[]...........[].##
    ##[]........[][][]##
    ##[]......[]....[]##
    ##..##......[]....##
    ##..[]............##
    ##..@......[].[][]##
    ##......[][]..[]..##
    ####################
    The sum of these boxes' GPS coordinates is 9021.

    Predict the motion of the robot and boxes in this new, scaled-up warehouse. What is the sum of
    all boxes' final GPS coordinates?
"""
import time
import numpy as np
from common import read_lines, parse_args

SPACE = 0
WALL = 1
BOX_BASE = 32
BOXsingle, BOXleft, BOXright = BOX_BASE + 0, BOX_BASE + 1, BOX_BASE + 2
ROBOT = 3

SPACE_SYMBOL = "."
WALL_SYMBOL = "#"
BOX_SYMBOLsingle, BOX_SYMBOLleft, BOX_SYMBOLright, = "O", "[", "]"
ROBOT_SYMBOL = "@"

SYMBOL_TO_NUMBER_1 = { # !@#$ Remove
    SPACE_SYMBOL: SPACE,
    WALL_SYMBOL: WALL,
    BOX_SYMBOLsingle: BOXsingle,
    BOX_SYMBOLleft: BOXleft,
    BOX_SYMBOLright: BOXright,
    ROBOT_SYMBOL: ROBOT}
NUMBER_TO_SYMBOL = {v: k for k, v in SYMBOL_TO_NUMBER_1.items()}

SYMBOL_TO_NUMBER = {
    SPACE_SYMBOL: SPACE,
    WALL_SYMBOL: WALL,
    BOX_SYMBOLsingle: BOXsingle,
    BOX_SYMBOLleft: BOXleft,
    BOX_SYMBOLright: BOXright,
    ROBOT_SYMBOL: ROBOT}

SYMBOL_1TO2 = {
    SPACE_SYMBOL: "..",
    WALL_SYMBOL: "##",
    BOX_SYMBOLsingle: "[]",
    ROBOT_SYMBOL: "@."}

concat = "".join

def part1_to_2(lines):
    """Convert the warehouse from part 1 to part 2."""
    return [concat([SYMBOL_1TO2[c] for c in line]) for line in lines]

def is_box(v): return v & BOX_BASE
def is_score_box(v): return v == BOXsingle or v == BOXleft

def valid_part2_grid(grid):
    h, w = grid.shape
    if w % 2 != 0: return f"Expected even width, found {w}", False
    for y in range(h):
        for x in range(w):
            if is_box(grid[y, x]):
                x1, x2 = x - 1, x + 1
                if not (is_box(grid[y, x1]) or is_box(grid[y, x2])):
                    return f"Box not wide enough: {(x1,y)}={grid[y,x1]} {(x2,y)}={grid[y,x2]}", False
    return "", True

def lines_to_grid(lines, is_part2=False):
    """Convert `lines`, a list of strings, to a 2D numpy array.
        The input lines are the string representation of the warehouse in part 1.
        The output is a 2D numpy array that we use to represent a warehouse in our code.
    """
    h, w = len(lines), len(lines[0])
    grid = np.zeros((h, w), dtype=int)
    for y in range(h):
        for x in range(w):
            symbol = lines[y][x]
            grid[y, x] = SYMBOL_TO_NUMBER[symbol]

    if is_part2:
        msg, ok = valid_part2_grid(grid)
        if not ok:
            print(msg)
            print(f"lines=\n{'\n'.join(lines)}")
            print(f"grid=\n{grid_to_text2(grid)}")
            print(grid)
            raise ValueError("Invalid grid")
    return grid

def grid_to_lines1(grid):
    """Convert a 2D numpy array to a list of strings.
        The input is a 2D numpy array that we use to represent a warehouse in our code.
        The output lines are the string representation of the warehouse in part 1.
    """
    h, w = grid.shape
    for y in range(h):
        for x in range(w):
            v = grid[y, x]
            assert v in NUMBER_TO_SYMBOL, f"Unknown value: {v} {list(NUMBER_TO_SYMBOL.keys())}"
    return [concat(NUMBER_TO_SYMBOL[int(grid[y, x])] for x in range(w))
            for y in range(h)]

def grid_to_text1(grid):
    """Convert the 2D numpy array that we use to represent a warehouse in our code to a string."""
    return "\n".join(grid_to_lines1(grid))

def grid_to_lines2(grid):
    """Convert a 2D numpy array to a list of strings.
        The input is a 2D numpy array that we use to represent a warehouse in our code.
        The output lines are the string representation of the warehouse in part 1.
    """
    def to_line(row):
        line = concat([NUMBER_TO_SYMBOL[v] for v in row])
        line = line.replace("OO", "[]")
        return line
    h, w = grid.shape
    assert w % 2 == 0, f"Expected even width, found {w}"
    return [to_line(grid[y]) for y in range(h)]
    # return [concat(symbol(grid[y, x], x) for x in range(w))
    #         for y in range(h)]

def grid_to_text2(grid):
    """Convert the 2D numpy array that we use to represent a warehouse in our code to a string."""
    return "\n".join(grid_to_lines2(grid))

def robot_position_(warehouse):
    y, x = np.where(warehouse == ROBOT)
    assert len(y) == 1, f"Expected 1 robot, found {len(y)}"
    return (x[0], y[0])

def next_pos_(x, y, move):
    if move == "^":   return (x, y - 1)
    elif move == "v": return (x, y + 1)
    elif move == "<": return (x - 1, y)
    elif move == ">": return (x + 1, y)
    else: raise ValueError(f"Unknown direction: {move}")

def sum_box_coordinates(warehouse):
    """Return the sum of the GPS coordinates of all boxes."""
    h, w = warehouse.shape
    boxes = [(x, y) for y in range(h) for x in range(w) if is_score_box(warehouse[y, x])]
    result = sum(100*y + x for x, y in boxes)
    return result

class Warehouse:
    """ The Warehouse class represents a warehouse with a robot and boxes.
        The warehouse is represented as a 2D numpy array `grid`
        The robot is represented by the value `robot` which is a tuple (x, y)
        The `is_part2` flag is True if the warehouse is the part 2 warehouse.
    """
    def __init__(self, grid, is_part2):
        self.grid = grid
        self.h, self.w = grid.shape
        self.robot = robot_position_(grid)
        self.is_part2 = is_part2
        self.validate()

    @classmethod
    def from_lines(cls, lines, is_part2=False):
        """Create a Warehouse object from a list of strings."""
        grid = lines_to_grid(lines, is_part2)
        return cls(grid, is_part2)

    def __str__(self):
        if not self.is_part2: return grid_to_text1(self.grid)
        return grid_to_text2(self.grid)

    def validate(self):
        if self.is_part2:
            msg, ok = valid_part2_grid(self.grid)
            if not ok:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~")
                print(msg)
                print(self)
                raise ValueError("Invalid grid")

    def __getitem__(self, key):
        return self.grid[key]

    def __setitem__(self, key, value):
        self.grid[key] = value

    def num_kind(self, kind):
        return np.count_nonzero(self.grid == kind)

    def num_kinds(self):
        return {kind: self.num_kind(kind) for kind in (WALL, BOXsingle, BOXleft, BOXright, ROBOT)}

    def equal_kinds(self, kinds2):
        return all(self.num_kinds()[kind] == kinds2[kind] for kind in kinds2)

    def move_simple(self, move):
        """Move the robot in direction `move`."""
        x, y = self.robot
        nx, ny = next_pos_(x, y, move)
        if self[ny, nx] == WALL: return
        if self[ny, nx] == SPACE:
            self[y, x] = SPACE
            self[ny, nx] = ROBOT
            self.robot = (nx, ny)
        elif is_box(self[ny, nx]):
            nnx, nny = nx, ny
            boxes = []
            while is_box(self[nny, nnx]):
                v = self[nny, nnx]
                nnx, nny = next_pos_(nnx, nny, move)
                boxes.append((v, (nnx, nny)))
            if self[nny, nnx] == SPACE:
                for v, (nnx, nny) in boxes: self[nny, nnx] = v
                self[y, x] = SPACE
                self[ny, nx] = ROBOT
                self.robot = (nx, ny)

    def box_pair_(self, nx, ny):
        """Return the pair of boxes that (`nx`,`ny`) is half of."""
        assert is_box(self[ny, nx])
        on_left = self[ny, nx] == BOXleft
        if on_left: assert self[ny, nx + 1] == BOXright
        else:       assert self[ny, nx - 1] == BOXleft
        if on_left: nnx1, nnx2, nny = nx, nx + 1, ny
        else:       nnx1, nnx2, nny = nx - 1, nx, ny
        return [(nnx1, nny), (nnx2, nny)]

    def extend_frontier(self, move, frontier, boxes):
        """ Extend the frontier of the boxes moving in direction `move`.
            `frontier` the boxes that are most advanced in the direction of `move`.
            `boxes` is the set of boxes are being moved.
            Return new_frontier, new_boxes, hit_wall, is_extended where
            - hit_wall is True if the robot hit a wall
            - is_extended is True if the frontier was extended.
        """
        new_frontier = []
        new_boxes = boxes.copy()

        def add_box(nnx, nny):
            """Add the box at (`nnx`,`nny`) to `new_frontier` and `new_boxes`."""
            if (nnx, nny) not in boxes:
                new_frontier.append((nnx, nny))
                new_boxes.add((nnx, nny))

        is_extended = False
        for (nx, ny) in frontier:
            nnx, nny = next_pos_(nx, ny, move)
            if self[nny, nnx] == WALL:
                return frontier, boxes, True, False
            if is_box(self[nny, nnx]):
                box_pair = self.box_pair_(nnx, nny)
                for nnx, nny in box_pair: add_box(nnx, nny)
                is_extended = True
            else:
                new_frontier.append((nx, ny))
        return new_frontier, new_boxes, False, is_extended

    def advanced_boxes_(self, move, nx, ny):
        """ Find all the boxes that will be moved when the boxs at (`nx`,`ny`) moves by `move`.
            Return `boxes`, `hit_wall` where
            - boxes is the set of boxes that will be moved
            - hit_wall is True if the robot hit a wall
        """
        frontier = self.box_pair_(nx, ny)
        boxes = set(frontier)
        for _ in range(100):
            new_frontier, new_boxes, hit_wall, is_extended = self.extend_frontier(move, frontier, boxes)
            if hit_wall: return boxes, True
            if not is_extended: return boxes, False
            frontier = new_frontier
            boxes = new_boxes
        raise ValueError("Unreachable")

    def move_box_pairs(self, move):
        """Move the robot in direction `move` taking into account box pairs."""
        x, y = self.robot
        nx, ny = next_pos_(x, y, move)
        if self[ny, nx] == WALL: return
        if self[ny, nx] == SPACE:
            self[y, x] = SPACE
            self[ny, nx] = ROBOT
            self.robot = (nx, ny)
        elif is_box(self[ny, nx]):
            boxes, hit_wall = self.advanced_boxes_(move, nx, ny)  # List of (x,y) pairs
            if hit_wall: return
            box_vals = {(nnx, nny): self[nny, nnx] for nnx, nny in boxes}
            for (nnx, nny) in boxes: self[nny, nnx] = SPACE
            for (nnx, nny) in boxes:
                v = box_vals[(nnx, nny)]
                nnx, nny = next_pos_(nnx, nny, move)
                assert self[nny, nnx] == SPACE, f"Expected SPACE at {nnx},{nny} found {self[nny, nnx]}"
                self[nny, nnx] = v
            self[y, x] = SPACE
            self[ny, nx] = ROBOT
            self.robot = (nx, ny)
        else: raise ValueError(f"Unknown object: {self[ny, nx]}")

    def move_(self, move):
        kinds0 = self.num_kinds()
        if self.is_part2 and move in "^v":
            self.move_box_pairs(move)
        else:
            self.move_simple(move)
        kinds = self.num_kinds()
        assert self.equal_kinds(kinds0), f"Number of objects changed:\n  {kinds0}\n->{kinds}"
        self.validate()

    def simulate_movements(self, moves, verbose=False):
        for move in moves: self.move_(move)

    def sum_box(self):  return sum_box_coordinates(self.grid)

def parse_input(input_file):
    lines = read_lines(input_file)
    lines = [line.strip() for line in lines]

    warehouse_lines = []
    for i, line in enumerate(lines):
        if line.startswith("#"): warehouse_lines.append(line)
        else: break

    while i < len(lines) and not lines[i]:  i += 1 # Skip empty lines
    lines = lines[i:]
    for j, line in enumerate(lines):
        if not line: break

    moves = concat(lines[:j+1])  # Join all lines into a single string
    return warehouse_lines, moves

def test_sample_data(movement_data_file, moves, is_part2):
    """Test the sample data with the given moves."""
    lines = read_lines(movement_data_file)
    assert lines
    lines = [line.strip() for line in lines]

    warehouse_states = []
    warehouse_lines = []
    for i, line in enumerate(lines):
        if line.startswith("#"): warehouse_lines.append(line)
        elif len(warehouse_lines) >= 3:
            warehouse_states.append(Warehouse.from_lines(warehouse_lines, is_part2))
            warehouse_lines = []
    if len(warehouse_lines) >= 3:
        warehouse_states.append(Warehouse.from_lines(warehouse_lines, is_part2))

    assert len(warehouse_states) == len(moves) + 1, f"moves={len(moves)} != warehouse_states{len(warehouse_states)}"

    warehouse = warehouse_states[0]
    print(f"Initial state\n{warehouse}")

    for i, move in enumerate(moves):
        expected = str(warehouse_states[i])
        actual = str(warehouse)
        assert expected == actual, f"Move {i}: {move}\nexpected\n{expected}\nactual\n{actual}"
        print(f"Move {move}: {i}\n{actual}")
        warehouse.move_(move)

    print(f"Final state:\n{warehouse}\n")
    result = warehouse.sum_box()
    return result

def test_with_sample_data1():
    "Test with the part1 sample data."
    moves = "<^^>>>vv<v>>v<<"
    result = test_sample_data("aoc2024-day15.data.1", moves, is_part2=False)
    assert result == 2028, f"Expected 2028, got {result}"

def test_with_sample_data2():
    "Test with the part2 sample data for doubled obstacles."
    moves = "<vv<<^^<<^^"
    test_sample_data("aoc2024-day15.data.2", moves, is_part2=True)

def solve(input_file, verbose, is_part2=False):
    warehouse_lines, moves = parse_input(input_file)
    if is_part2: warehouse_lines = part1_to_2(warehouse_lines)
    warehouse = Warehouse.from_lines(warehouse_lines, is_part2)
    if verbose:
        print(f"Initial warehouse:\n{warehouse}")
        print(f"Moves: {moves}")

    warehouse.simulate_movements(moves, verbose)
    if verbose: print(f"Final warehouse:\n{warehouse}")
    return warehouse.sum_box()

def part1(input_file, verbose):
    "Solution to part 1. 10092 for the test input. (1451928)"
    result = solve(input_file, verbose, is_part2=False)
    print(f"Part 1: The sum of all boxes' GPS coordinates is: {result}")

def part2(input_file, verbose):
    "Solution to part 2. 9021 for the test input. (1462788)"
    result = solve(input_file, verbose, is_part2=True)
    print(f"Part 2: The sum of all boxes' GPS coordinates is: {result}")

args = parse_args("Advent of Code 2024 - Day 15", "problems/aoc2024-day15-input-test.txt")
if args.testing:
    test_with_sample_data1()
    test_with_sample_data2()
    exit(0)

t0 = time.time()
part1(args.input, args.verbose)
t1 = time.time() - t0
t0 = time.time()
part2(args.input, args.verbose)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
