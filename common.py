"""
    Functions used by multiple solutions.
"""
import re
import argparse
from types import SimpleNamespace

concat = "".join

RE_NUMBERS = re.compile(r"\d+")
def numbers_(text):
    return [int(s) for s in RE_NUMBERS.findall(text)]

def parse_args(description, default_input):
    """Parses command-line arguments.
        `description` is a Description of the program.
        `default_input` is the path of default problem data file.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--input', default=default_input, help=f"Input file path (default: {default_input})")
    parser.add_argument('-t', '--testing', action='store_true', help='Enable testing mode')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    return parser.parse_args()

def read_text(filename):
    with open(filename) as f: text = f.read()
    return text.strip()

def read_lines(filename):
    return read_text(filename).splitlines()

def read_rows(filename):
    lines = read_lines(filename)
    rows = [list(line) for line in lines]
    for i, row in enumerate(rows):
        assert len(row) == len(rows[0]), f"Rows have different lengths\nrow[0]={rows[i-1]}\nrow[{i}]={row}"
    return rows

def char_positions(rows, char):
    "Returns `positions` where positions((y,x)) exists if rows[y][x] == `char`."
    positions = set()
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c == char: positions.add((y, x))
    return frozenset(positions)

class MyNamespace(SimpleNamespace):
    "SimpleNamespace with a simpler str/repr."
    def __str__(self):
        return f"{self.__dict__}"
    def __repr__(self):
        return f"{self.__dict__}"

def clean_map_text(text):
    lines = text.split("\n")
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line]
    return "\n".join(lines)

def aoc_map_(lines, symbols):
    """Returns an AOC map which consists of lines of text, where each line is a row of the map. e.g.
        ###############
        #.......#....E#
        #.#.###.#.###^#
        #.....#.#...#^#
        ###############
        `lines` is a list of strings, typically read from a file.
        `symbols` is a string of all allowed characters in the map.
    """
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line]
    assert lines, "No lines in map"
    assert "#" in symbols, f"Map must have # symbols={symbols}"
    i0, i1 = None, len(lines)
    for i, line in enumerate(lines):
        if i0 is None:
            if line.startswith("#"): i0 = i
        else:
            if not line.startswith("#"):
                i1 = i
                break
    assert i0 is not None, "No map start"

    aoc_map = lines[i0:i1]
    for line in aoc_map:
        assert len(line) == len(aoc_map[0]), f"Rows have different lengths\naoc_map[0]={aoc_map[0]}\naoc_map[{i}]={line}"
        for c in line:
            assert c in symbols, f"Unexpected character in map: '{c}' in '{line}', allowed: {symbols}"
    return aoc_map

def string_to_aoc_map(text, symbols):
    "Converts a string to an AOC map."
    lines = text.split("\n")
    return aoc_map_(lines, symbols)

def read_aoc_map(filename, symbols):
    "Reads a map file, which consists of lines of text, where each line is a row of the map."
    lines = read_lines(filename)
    return aoc_map_(lines, symbols)

def mark_aoc_map(aoc_map, path, char):
    "Returns a modified map with the path marked with `char`."
    rows = [list(row) for row in aoc_map]
    for y,x in path: rows[y][x] = char
    return [concat(row) for row in rows]

# Grid functions
# Grid is a 2D array of cells, where each cell is a number.
# num_to_symbol is a dictionary that maps numbers to symbols.

def aoc_map_to_grid(aoc_map, symbol_to_num):
    return [[symbol_to_num[c] for c in line] for line in aoc_map]

def grid_to_aoc_map(grid, num_to_symbol):
    return ["".join(num_to_symbol[c] for c in row) for row in grid]

GRID_SPACE = ""

def grid_to_string(aoc_map, num_to_symbol):
    "Converts an 2D grid to a string. "
    w, h = len(aoc_map[0]), len(aoc_map)
    header = GRID_SPACE.join([str(x % 10) for x in range(w)])
    lines = []
    lines.append(f" + {header}")
    for y, row in enumerate(aoc_map):
        line = GRID_SPACE.join([num_to_symbol[c] for c in row])
        line = f"{y:2d} {line}"
        lines.append(line)
    return "\n".join(lines)
