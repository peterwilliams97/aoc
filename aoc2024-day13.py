"""
    https://adventofcode.com/2024/day/13

    Each machine contains one prize; to win the prize, the claw must be positioned exactly above the
    prize on both the X and Y axes.

    You wonder: what is the smallest number of tokens you would have to spend to win as many prizes
    as possible? You assemble a list of every machine's button behavior and prize location (your
    puzzle input). For example:

    Button A: X+94, Y+34
    Button B: X+22, Y+67
    Prize: X=8400, Y=5400

    Button A: X+26, Y+66
    Button B: X+67, Y+21
    Prize: X=12748, Y=12176

    Button A: X+17, Y+86
    Button B: X+84, Y+37
    Prize: X=7870, Y=6450

    Button A: X+69, Y+23
    Button B: X+27, Y+71
    Prize: X=18641, Y=10279

    Part 1:
    Figure out how to win as many prizes as possible. What is the fewest tokens you would have to
    spend to win all possible prizes?

    Part 2:
    As you go to win the first prize, you discover that the claw is nowhere near where you expected
    it would be. Due to a unit conversion error in your measurements, the position of every prize is
    actually 10000000000000 higher on both the X and Y axis!

    Add 10000000000000 to the X and Y position of every prize. After making this change, the example
    above would now look like this:

    Button A: X+94, Y+34
    Button B: X+22, Y+67
    Prize: X=10000000008400, Y=10000000005400

    Button A: X+26, Y+66
    Button B: X+67, Y+21
    Prize: X=10000000012748, Y=10000000012176

    Button A: X+17, Y+86
    Button B: X+84, Y+37
    Prize: X=10000000007870, Y=10000000006450

    Button A: X+69, Y+23
    Button B: X+27, Y+71
    Prize: X=10000000018641, Y=10000000010279
    Now, it is only possible to win a prize on the second and fourth claw machines. Unfortunately,
    it will take many more than 100 presses to do so.

    Using the corrected prize coordinates, figure out how to win as many prizes as possible. What is
    the fewest tokens you would have to spend to win all possible prizes?
"""
import time
import re
import numpy as np
import sympy as sp
from common import parse_args, read_lines

RE_BUT_A = re.compile(r"Button A: X\+(\d+), Y\+(\d+)")
RE_BUT_B = re.compile(r"Button B: X\+(\d+), Y\+(\d+)")
RE_PRIZE = re.compile(r"Prize: X=(\d+), Y=(\d+)")
REGEXES = [RE_BUT_A, RE_BUT_B, RE_PRIZE]

def xy_(regex, line):
    "Return a 1-D np array of the x and y parsed from `line` with `regex`."
    m = regex.match(line)
    assert m, f"Bad line: '{line}'"
    xy = map(int, m.groups())
    return np.array(list(xy))

def parse_machine(triplet):
    "Parse a machine from a list of three strings."
    return [xy_(regex, line) for regex, line in zip(REGEXES, triplet)]

def parse_input(lines):
    "Parse the input into a list of dictionaries."
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line]
    assert len(lines) % 3 == 0, f"Bad number of lines: {len(lines)}"
    return [parse_machine(lines[i:i+3]) for i in range(0, len(lines), 3)]

def fractional(x):
    "Return the fractional part of `x`."
    return x - int(round(x))

TOL = 1e-6
def is_int(a, b):
    "Return True if a and b are within tolerance of an integer."
    return abs(fractional(a)) < TOL and abs(fractional(b)) < TOL

def solve(X, Y, Z):
    """
    Solve the equation a`X` + b`Y` = `Z` for scalars a and b where X, Y, and Z are 1D integer arrays.
    Returns: `a` and `b`, and a boolean indicating if the solution is exact.
    """
    # Solve the system using sympy's solve_linear_system
    a, b = sp.symbols('a b')
    equations = [a * X[i] + b * Y[i] - Z[i] for i in range(len(X))]
    solution = sp.solve(equations, (a, b))

    if not solution: return None, None, False

    a_val = solution[a]
    b_val = solution[b]
    exact_solution = np.allclose(np.array(a_val * X + b_val * Y, dtype=np.int64), Z)
    exact_solution = exact_solution and is_int(a_val, b_val)
    return a_val, b_val, exact_solution

def test_solve():
    X = np.array([94, 34])
    Y = np.array([22, 67])
    Z = np.array([8400, 5400])
    a, b, ok = solve(X, Y, Z)
    assert ok and a == 80 and b == 40, f"Failed: a = {a}, b = {b}"

def part1(lines):
    "Solution to part 1. 480 for the test input. (29877)"
    machines = parse_input(lines)
    total = 0
    for i, machine in enumerate(machines):
        a, b, ok = solve(machine[0], machine[1], machine[2])
        if ok:
            cost = 3 * a + b
            l = [[int(v) for v in p] for p in machine]
            print(f"Machine {i+1:4}: {l}: a = {a}, b = {b} -> {cost} tokens.")
            total += cost
    print(f"Part 1: {total} tokens.")

def part2(lines):
    "Solution to part 2. 875318608908 for the test input. (99423413811305)"
    DELTA = 10_000_000_000_000
    machines = parse_input(lines)
    for i, machine in enumerate(machines):
        before = machine.copy()
        a,b,p = machine
        machine = [a, b, p+DELTA]
        msg = f"\n  {machine[2][0]} !=\n  {before[2][0] + DELTA}  was\n  {before[2][0]}"
        assert machine[2][0] == before[2][0] + DELTA, msg
        assert machine[2][1] == before[2][1] + DELTA
        machines[i] = machine
    total = 0
    for i, machine in enumerate(machines):
        a, b, ok = solve(machine[0], machine[1], machine[2])
        if ok:
            cost = 3 * a + b
            l = [[int(v) for v in p] for p in machine]
            print(f"Machine {i+1:4}: {l}: a = {a}, b = {b} -> {cost} tokens.")
            total += cost
    print(f"Part 2: {total} tokens.")

args = parse_args("Advent of Code 2024 - Day 13", "problems/aoc2024-day13-input-test.txt")
if args.testing:
    test_solve()
    exit(0)

lines = read_lines(args.input)
t0 = time.time()
part1(lines)
t1 = time.time() - t0
t0 = time.time()
part2(lines)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
