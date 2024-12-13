"""
    Functions used by multiple solutions.
"""
from types import SimpleNamespace
import re
import argparse

RE_NUMBERS = re.compile(r"\d+")
def numbers_(text):
    return [int(s) for s in RE_NUMBERS.findall(text)]

def parse_args(description, default_input):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--input', default=default_input, help="Input file path")
    return parser.parse_args()

def read_lines(filename):
    return open(filename).read().splitlines()
