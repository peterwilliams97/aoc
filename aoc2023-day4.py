"""
    https://adventofcode.com/2023/day/4

    Card   1: 36 15 12 91 47 98 59 46 83 86 | 86 34 88  7 36 82 90 32 83 56 27 45 49 69 91 47 98 59 13 15 68 12 17 11 46

    Part 1:
    ------
    The numbers before the | are "winning numbers"
    The numbers after the | are "your numbers"
    Points are scored by matching your numbers with winning numbers:

    First match = 1 point
    Each additional match doubles the points
    No matches = 0 points
    For example, if you have 4 matches on a card, you get 8 points (1×2×2×2).

    Part 2:
    ------
    You win copies of the scratchcards below the winning card equal to the number of matches.
    So, if card 10 were to have 5 matching numbers, you would win one copy each of cards
    11, 12, 13, 14, and 15.

    Copies of scratchcards are scored like normal scratchcards and have the same card number as the
    card they copied. So, if you win a copy of card 10 and it has 5 matching numbers, it would then
    win a copy of the same cards that the original card 10 won: cards 11, 12, 13, 14, and 15.
    This process repeats until none of the copies cause you to win any more cards.
"""
import re
from common import MyNamespace as ns, parse_args

RE_NUMBERS = re.compile(r"\d+")
def numbers_(text):
    return [int(s) for s in RE_NUMBERS.findall(text)]

def decode_line(line):
    """Return a tuple (name, values) from `line` such as the one above."""
    _, values_str = line.split(":")
    win_str, mine_str = values_str.split("|")
    win, mine = numbers_(win_str), numbers_(mine_str)
    return ns(win=win, mine=mine)

def wins_(card):
    """Return the number of elements in `mine` that are in `win`."""
    return len(set(card.win) & set(card.mine))

def score_(wins):
    """n = number of elements in `mine` that are in `win`.
       Return 2 ** (n - 1) if n > 0 or 0 otherwise.
    """
    if wins == 0: return 0
    return 2 ** (wins - 1)

def score_line(line):
    """Return the score of a card from a line of text."""
    card = decode_line(line)
    wins = wins_(card)
    return score_(wins)

def part1(lines):
    "Solution to part 1. 13 for the test input."
    scores = [score_line(line) for line in lines]
    print(f"Part 1: {sum(scores)}")

def part2(lines):
    "Solution to part 2. 30 for the test input."
    cards = [decode_line(line) for line in lines]
    card_wins = {i: wins_(card) for i, card in enumerate(cards)}
    card_nums = {i: 1 for i in range(len(cards))}
    for i in range(len(cards)):
        wins = card_wins[i]
        for j in range(i+1, i + wins+1):
            card_nums[j] += card_nums[i]
    print(f"Part 2: {sum(card_nums.values())}")

args = parse_args("Advent of Code 2023 - Day 4", "aoc2023-day4-input-test.txt")
lines = open(args.input).read().splitlines()
part1(lines)
part2(lines)
