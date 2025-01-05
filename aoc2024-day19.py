"""
    https://adventofcode.com/2024/day/19

    --- Linen Layout ---
    Today, The Historians take you up to the hot springs on Gear Island! Very suspiciously,
    absolutely nothing goes wrong as they begin their careful search of the vast field of helixes.

    Could this finally be your chance to visit the onsen next door? Only one way to find out.

    After a brief conversation with the reception staff at the onsen front desk, you discover that
    you don't have the right kind of money to pay the admission fee. However, before you can leave,
    the staff get your attention. Apparently, they've heard about how you helped at the hot springs,
    and they're willing to make a deal: if you can simply help them arrange their towels, they'll
    let you in for free!

    Every towel at this onsen is marked with a pattern of colored stripes. There are only a few
    patterns, but for any particular pattern, the staff can get you as many towels with that pattern
    as you need. Each stripe can be white (w), blue (u), black (b), red (r), or green (g). So, a
    towel with the pattern ggr would have a green stripe, a green stripe, and then a red stripe, in
    that order. (You can't reverse a pattern by flipping a towel upside-down, as that would cause
    the onsen logo to face the wrong way.)

    The Official Onsen Branding Expert has produced a list of designs - each a long sequence of
    stripe colors - that they would like to be able to display. You can use any towels you want, but
    all of the towels' stripes must exactly match the desired design. So, to display the design
    rgrgr, you could use two rg towels and then an r towel, an rgr towel and then a gr towel, or
    even a single massive rgrgr towel (assuming such towel patterns were actually available).

    To start, collect together all of the available towel patterns and the list of desired designs
    (your puzzle input). For example:

    r, wr, b, g, bwu, rb, gb, br

    brwrr
    bggr
    gbbr
    rrbgbr
    ubwu
    bwurrg
    brgr
    bbrgwb
    The first line indicates the available towel patterns; in this example, the onsen has unlimited
    towels with a single red stripe (r), unlimited towels with a white stripe and then a red stripe
    (wr), and so on.

    After the blank line, the remaining lines each describe a design the onsen would like to be able
    to display. In this example, the first design (brwrr) indicates that the onsen would like to be
    able to display a black stripe, a red stripe, a white stripe, and then two red stripes, in that
    order.

    Not all designs will be possible with the available towels. In the above example, the designs
    are possible or impossible as follows:

    brwrr can be made with a br towel, then a wr towel, and then finally an r towel.
    bggr can be made with a b towel, two g towels, and then an r towel.
    gbbr can be made with a gb towel and then a br towel.
    rrbgbr can be made with r, rb, g, and br.
    ubwu is impossible.
    bwurrg can be made with bwu, r, r, and g.
    brgr can be made with br, g, and r.
    bbrgwb is impossible.
    In this example, 6 of the eight designs are possible with the available towel patterns.

    To get into the onsen as soon as possible, consult your list of towel patterns and desired
    designs carefully. How many designs are possible?

    --- Part Two ---
    The staff don't really like some of the towel arrangements you came up with. To avoid an endless
    cycle of towel rearrangement, maybe you should just give them every possible option.

    Here are all of the different ways the above example's designs can be made:

    brwrr can be made in two different ways: b, r, wr, r or br, wr, r.

    bggr can only be made with b, g, g, and r.

    gbbr can be made 4 different ways:

    g, b, b, r
    g, b, br
    gb, b, r
    gb, br
    rrbgbr can be made 6 different ways:

    r, r, b, g, b, r
    r, r, b, g, br
    r, r, b, gb, r
    r, rb, g, b, r
    r, rb, g, br
    r, rb, gb, r
    bwurrg can only be made with bwu, r, r, and g.

    brgr can be made in two different ways: b, r, g, r or br, g, r.

    ubwu and bbrgwb are still impossible.

    Adding up all of the ways the towels in this example could be arranged into the desired designs
    yields 16 (2 + 1 + 4 + 6 + 1 + 2).

    They'll let you into the onsen as soon as you have the list. What do you get if you add up the
    number of different ways you could make each design?

"""
import time
from functools import lru_cache
from common import parse_args, read_lines

def lines_to_towels_and_designs(lines):
    """ Return a tuple of patterns and designs from `lines`.
        `lines` is a list of strings.
    """
    lines = [line.strip() for line in lines]
    patterns = lines[0].split(", ")
    designs = lines[1:]
    designs = [design for design in designs if design]
    assert len(patterns) == len(set(patterns))
    assert all(patterns)
    assert all(d == d.strip() for d in designs)
    patterns.sort(key=lambda x: (-len(x),x))
    print(f"patterns: {[p for p in patterns if len(p) <= 2]}")
    return patterns, designs

global_towels = []

@lru_cache(maxsize=None)
def dfs_all(design, depth):
    """ Returns n, ok where
        - n is the number of ways `design` can be made by joining a combination of `towels`.
        - ok is True if `design` can made by joining a combination of `towels`.
        `global_towels` is a list of available towel patterns.
        `design` is the desired design.
        Check if `design` starts with any of the patterns, and if so, recursively check
        design[len(pattern):].
    """
    if len(design) == 0: return 1, True
    n, match = 0, False
    for pattern in global_towels:
        if design[:len(pattern)] == pattern:
            m, ok = dfs_all(design[len(pattern):], depth + 1)
            if ok:
                n += m
                match = True
    return n, match

def num_valid_designs(towels, design):
    """ Returns the number of ways `design` can be made by joining a combination of `towels`.
        `towels` is a list of available towel patterns.
        `design` is the desired design.
    """
    global global_towels
    global_towels = towels
    n, _ = dfs_all(design, 0)
    return n

def Q(text): return f"'{text}'"

def test1():
    patterns = ['r', 'wr', 'b', 'g', 'bwu', 'rb', 'gb', 'br']
    designs = ['brwrr', 'bggr', 'gbbr', 'rrbgbr', 'ubwu', 'bwurrg', 'brgr', 'bbrgwb']
    valids = [True, True, True, True, False, True, True, False]
    for design, expected in zip(designs, valids):
        actual = num_valid_designs(patterns, design) > 0
        print(f"{Q(design):8}: got {actual:1}, expected {expected:1}")
        assert actual == expected

def part1(towels, designs):
    "Solution to part 1. 6 for the test input. (353)"
    count = sum(num_valid_designs(towels, design) > 0 for design in designs)
    print(f"Part 1: {count} of {len(designs)} designs are valid")

def part2(towels, designs):
    "Solution to part 2. 16 for the test input. (880877787214477)"
    count = sum(num_valid_designs(towels, design) for design in designs)
    print(f"Part 2: {count} designs are possible")

args = parse_args("Advent of Code 2024 - Day 19", "problems/aoc2024-day19-input-test.txt")

if args.testing:
    test1()
    exit()

lines = read_lines(args.input)
towels, designs = lines_to_towels_and_designs(lines)

t0 = time.time()
part1(towels, designs)
t1 = time.time() - t0
t0 = time.time()
part2(towels, designs)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
