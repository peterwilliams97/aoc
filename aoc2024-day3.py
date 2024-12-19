"""
    https://adventofcode.com/2024/day/3

    Part 1:
    ------
    For example, consider the following section of corrupted memory:

    xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
    Only the four highlighted sections are real mul instructions. Adding up the result of each
    instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

    Part 2:
    ------
    There are two new instructions you'll need to handle:

    The do() instruction enables future mul instructions.
    The don't() instruction disables future mul instructions.
    Only the most recent do() or don't() instruction applies. At the beginning of the program,
    mul instructions are enabled.

    For example:

    xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
    This corrupted memory is similar to the example from before, but this time the mul(5,5) and
    mul(11,8) instructions are disabled because there is a don't() instruction before them. The
    other mul instructions function normally, including the one at the end that gets re-enabled by
    a do() instruction.
"""
import re
from common import parse_args, read_text, MyNamespace as ns

RE_MUL = re.compile(r"mul\((\d+),(\d+)\)")
RE_DO = re.compile(r"do(?:n't)?\(\)")

def sum_total(text):
    matches = RE_MUL.finditer(text)
    factors = [(int(match.group(1)), int(match.group(2))) for match in matches]
    products = [a*b for a, b in factors]
    return sum(products)

def spans_(text):
    boundaries = RE_DO.finditer(text)
    i0, on0 = 0, True
    spans = []
    for m in boundaries:
        i1 = m.start()
        on = m.group() == "do()"
        if on0 == on:
            continue
        span = ns(i0=i0, i1=i1, on=on0)
        spans.append(span)
        i0, on0 = m.end(), on
    if i0 < len(text):
        spans.append(ns(i0=i0, i1=len(text), on=on0))
    return spans

def part1(text):
    "Solution to part 1. 48 for the test input."
    total = sum_total(text)
    print(f"Part 1: {total}")

def part2(text):
    "Solution to part 2. 4 for aoc2024-day3-input-test2.txt."
    spans = spans_(text)
    totals = [sum_total(text[span.i0:span.i1]) for span in spans if span.on]
    print(f"Part 2: {sum(totals)}")

args = parse_args("Advent of Code 2024 - Day 3", "aoc2024-day3-input-test.txt")
text = read_text(args.input)
part1(text)
part2(text)
