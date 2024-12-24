"""
    https://adventofcode.com/2023/day/2
"""
import time
import re
import math
from common import read_lines, parse_args

KEYS = ["red", "green", "blue"]
MAX_CUBES = {"red": 12, "green": 13, "blue": 14}

RE_TITLE = re.compile(r"Game\s+(\d+)")
RE_VAL = re.compile(r"(\d+)\s+(\S+)")

def parse_value(value_str):
    match = RE_VAL.search(value_str)
    if match:
        return int(match.group(1)), match.group(2)
    assert False, f"Invalid value: {value_str}"

def parse_group(game):
    values = [parse_value(v) for v in game.split(",")]
    return {k: v for v, k in values}

def parse_line(line):
    title_str, game_str = line.split(":")
    draws_str = game_str.split(";")
    game_id = int(RE_TITLE.search(title_str).group(1))
    draws = [parse_group(drw) for drw in draws_str]
    return game_id, draws

def max_cubes(draws):
    k_max = {}
    for value in draws:
        for k, v in value.items():
            k_max[k] = max(k_max.get(k, 0), v)
    return {k: v for k, v in k_max.items()}

def allowed_max(total):
    return all(v <= MAX_CUBES[k] for k, v in total.items())

def show(draw):
    return [draw.get(k, 0) for k in KEYS]

def power_(draw):
    return math.prod(draw.values())

def part1(lines):
    print(f"Max cubes: {MAX_CUBES}")
    allowed_ids = []
    for i, line in enumerate(lines):
        game_id, draws = parse_line(line)
        draw_max = max_cubes(draws)
        allowed = allowed_max(draw_max)
        if allowed:
            allowed_ids.append(game_id)

        if i < 5 or allowed or True:
            print(f"{i:4}: Game {game_id:2}:: {allowed} total={show(draw_max)} draws={[show(d) for d in draws]}")

    id_sum = sum(allowed_ids)
    print(f"Sum of allowed game IDs: {id_sum} {allowed_ids}")

def part2(lines):
    power_list = []
    for i, line in enumerate(lines):
        game_id, draws = parse_line(line)
        draw_max = max_cubes(draws)
        power = power_(draw_max)
        power_list.append(power)

        print(f"{i+1:4}: Game {game_id:2}:: power={power} total={show(draw_max)} draws={[show(d) for d in draws]}")

    power_sum = sum(power_list)
    print(f"Sum of powers: {power_sum} {power_list}")

args = parse_args("Advent of Code 2024 - Day 1", "aoc2023-day2-input-test.txt")
lines = read_lines(args.input)

t0 = time.time()
part1(lines)
t1 = time.time() - t0
t0 = time.time()
part2(lines)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
