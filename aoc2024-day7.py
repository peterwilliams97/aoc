"""
    https://adventofcode.com/2024/day/7
    190: 10 19
    3267: 81 40 27
    83: 17 5
    156: 15 6
    7290: 6 8 6 15
    161011: 16 10 13
    192: 17 8 14
    21037: 9 7 18 13
    292: 11 6 16 20

    Part 1:
    ------
    Each line represents a single equation. The test value appears before the colon on each line;
    it is your job to determine whether the remaining numbers can be combined with operators to
    produce the test value.

    Operators are always evaluated left-to-right, not according to precedence rules. Furthermore,
    numbers in the equations cannot be rearranged. Glancing into the jungle, you can see elephants
    holding two different types of operators: add (+) and multiply (*).

    Only three of the above equations can be made true by inserting operators:

    190: 10 19 has only one position that accepts an operator: between 10 and 19. Choosing + would
    give 29, but choosing * would give the test value (10 * 19 = 190).
    3267: 81 40 27 has two positions for operators. Of the four possible configurations of the
    operators, two cause the right side to match the test value: 81 + 40 * 27 and 81 * 40 + 27
    both equal 3267 (when evaluated left-to-right)!
    292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.

    Part 2:

"""
import time
from common import parse_args, read_lines

def equation_(line):
    "Parse an equation line."
    result_str, numbers_str = line.split(":")
    result = int(result_str)
    numbers = list(map(int, numbers_str.split()))
    return result, numbers

def parse_input(lines):
    "Parse the input into a list of rules and a list of updates."
    return [equation_(line) for line in lines]

def is_valid_step(result, current, numbers, operators):
    "Return True if the step is valid, False otherwise."
    if current > result: return False
    if len(numbers) == 0: return result == current

    for op in operators:
        if op == '+':
            new = current + numbers[0]
        elif op == '*':
            new = current * numbers[0]
        elif op == '|':
            new = int(str(current) + str(numbers[0]))
        if is_valid_step(result, new, numbers[1:], operators):
            return True
    return False

def is_valid_equation(result, numbers, operators):
    "Return True if the equation is valid, False otherwise."
    current = numbers[0]
    return is_valid_step(result, current, numbers[1:], operators)

def valid_equations(equations, operators):
    "Return a list of valid equations."
    valid = [eq for eq in equations if is_valid_equation(*eq, operators)]
    # print(f"Part 1: {len(equations)}")
    # for i, eq in enumerate(equations):
    #     print(f"{i+1:2}: {eq}")
    # print(f"Part 1: {len(valid)}")
    # for i, eq in enumerate(valid):
    #     print(f"{i+1:2}: {eq}")
    return valid

def part1(lines):
    "Solution to part 1. 3749 for the test input."
    operators = ['+', '*']
    equations = [equation_(line) for line in lines]
    valid = valid_equations(equations, operators)
    total = sum([v[0] for v in valid])
    print(f"Part 1: {total}")

def part2(lines):
    "Solution to part 2. 11387 for the test input."
    operators = ['+', '*', '|']
    equations = [equation_(line) for line in lines]
    valid = valid_equations(equations, operators)
    total = sum([v[0] for v in valid])
    print(f"Part 2: {total}")

args = parse_args("Advent of Code 2024 - Day 7", "aoc2024-day7-input-test.txt")
lines = read_lines(args.input)
t0 = time.time()
part1(lines)
t1 = time.time() - t0
t0 = time.time()
part2(lines)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
