"""
   This script is used to critique Python solutions for Advent of Code 2024.
    It reads the critiques of individual files, combines them, and generates a markdown document.
    Usage: python critique.py <filename1> <filename2> ...
    e.g. python critique.py ../aoc2024-day*.py
"""
import argparse
from file_critique import critique_files
from assemble_critiques import combine_critiques
from build_critique_md import build_critique_markdown

parser = argparse.ArgumentParser(description="Critique Python solutions to Advent of Code problems.")
parser.add_argument('files', metavar='F', type=str, nargs='+', help='Python solution files to critique')
parser.add_argument('-f', '--force', action='store_true', help='Force re-analysis of files even if critique already exists')
args = parser.parse_args()

critique_files(args.files, args.force)
combine_critiques(args.force)
build_critique_markdown()
