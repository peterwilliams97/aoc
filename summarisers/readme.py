"""
   This script is used to summarise Python solutions for Advent of Code 2024.
    It reads the summaries of individual files, combines them, and generates a markdown document.
    Usage: python readme.py <filename1> <filename2> ...
    e.g. python readme.py ../aoc2024-day*.py
"""
import os
import argparse
from file_readme import summarise_files
from build_readme_md import build_readme_markdown

parser = argparse.ArgumentParser(description="Summarise Python solutions to Advent of Code problems.")
parser.add_argument('files', metavar='F', type=str, nargs='+', help='Python solution files to summarise')
parser.add_argument('-f', '--force', action='store_true', help='Force re-analysis of files even if summary already exists')
args = parser.parse_args()

for file in args.files:
    assert os.path.exists(file), f"File not found: {file}"
    assert file.endswith(".py"), f"Invalid file: {file}"

summarise_files(args.files, args.force)
build_readme_markdown()
