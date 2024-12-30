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
    # print(f"i0={i0} i1={i1} len(aoc_map)={len(aoc_map)}")
    # for i, line in enumerate(aoc_map):
    #     print(f"{i:2d}: '{line}' {len(line)}")
    for line in aoc_map:
        assert len(line) == len(aoc_map[0]), f"Rows have different lengths\naoc_map[0]={aoc_map[0]}\naoc_map[{i}]={line}"
        for c in line:
            assert c in symbols, f"Unexpected character in map: '{c}' in '{line}', allowed: {symbols}"
    return aoc_map

def string_to_aoc_map(text, symbols):
    "Converts a string to an AOC map."
    lines = text.split("\n")
    # lines = text.splitlines()
    # lines2 = text.split("\n")
    # assert len(lines) == len(lines2), f"splitlines() != split('\\n') {len(lines)} {len(lines2)}"
    # for i, (line1, line2) in enumerate(zip(lines, lines2)):
    #     assert line1 == line2, f"lines[{i}] != lines2[{i}]\n{line1}\n{line2}"
    return aoc_map_(lines, symbols)

def read_aoc_map(filename, symbols):
    "Reads a map file, which consists of lines of text, where each line is a row of the map."
    lines = read_lines(filename)
    return aoc_map_(lines, symbols)

def mark_aoc_map(aoc_map, path, char):
    "Returns a modified map with the path marked with `char`."
    rows = [list(row) for row in aoc_map]
    for y,x in path:
        # if rows[y][x] == ".":
        rows[y][x]  = char
    return [concat(row) for row in rows]
