"""
    This module provides functions for summarising Python solutions to Advent of Code problems.
"""

import os
import sys
import time
import json
from typing import List
from pydantic import BaseModel
from tools import call_anthropics_claude, basename_, day_number, read_text
from readme_tools import DATA_DIR_README

class AOCReadmeModel(BaseModel):
    """Model for the critique of a Python solution to an Advent of Code problem."""
    Day: int
    Name: str
    Title: str
    Problem1: str
    Problem2: str
    Solution1: str
    Solution2: str

# Example README analysis for a Python solution to an Advent of Code problem.
README_ANALYSIS = {
    "Title": "Corrupted Memory Processing",
    "Problem1": "Identify valid multiplication instructions (mul(a,b)) and calculate their sum.",
    "Problem2": "Introduce do() and don't() instructions to enable/disable future mul instructions.",
    "Solution1": "Uses regex to find mul(a,b) patterns, extracts numbers, multiplies them, and sums results.",
    "Solution2": "Uses regex to find do() and don't() instructions, splits text into spans, applies Part 1 solution to enabled spans only."
}

if False:
    json.dumps(README_ANALYSIS, indent=2)
    EXAMPLE_README = AOCReadmeModel(**README_ANALYSIS)
    print(EXAMPLE_README.json())
    exit(68)

# The prompt for telling the LLM to summarise a Python solution to an Advent of Code problem and
# output a JSON response.

README_SYSTEM_PROMPT = f"""
    You are terse and to the point.
    You are an Advent of Code problem and solution summarizer.
    You read Python solutions to Advent of Code problems and provide a structured summary.
    Advent of Code problems have two parts.
    Each summary should include
    1. A description of the Part 1 problem
    2. A description of the solution to Part 1
    3. A description of the Part 2 problem
    4. A description of the solution to Part 2
    5. A title for the overall problem. The title should be a concise summary of the problem, probably a few words.

    Example response:
    {README_ANALYSIS}

"""

def analyse_python_file(code: str) -> dict:
    keys = list(README_ANALYSIS.keys())
    keys_text = f"{keys}".replace("'", '"')

    """Analyse a Python solution to an Advent of Code problem and return a structured summary."""
    user_message = f"""
    The following text is a Python solution to an Advent of Code problem
    Please analyse this code .
    ````python
    {code}
    ````
    Format your answers as JSON. Remember the JSON keys are {keys_text}.

    ."""
    return call_anthropics_claude(README_SYSTEM_PROMPT, user_message)

def summarise(filename):
    """Summarise a Python solution to an Advent of Code problem.
        `filename` is the path to the Python solution file.
        Returns: A validated critique of the solution as a Pydantic model.
    """
    code = read_text(filename)
    try: analysis = analyse_python_file(code)
    except Exception as e:
        print(f"Error analysing {filename}: {e}")
        raise
    name = os.path.basename(filename)
    analysis["Name"] = name
    analysis["Day"] = day_number(filename)
    return AOCReadmeModel(**analysis)

def summarise_files(file_list, force=False):
    """Summarise multiple Python solutions to Advent of Code problems.
        `file_list` is a list of paths to Python solution files.
        `force` forces re-analysis of files even if summaries already exist.
    """
    os.makedirs(DATA_DIR_README, exist_ok=True)
    for i, solution_path in enumerate(file_list):
        assert os.path.exists(solution_path), f"File not found: {solution_path}"
        summary_path = os.path.join(DATA_DIR_README, basename_(solution_path) + ".json")
        if not force and os.path.exists(summary_path):
            print(f"{i+1:4}: File analysis for {os.path.basename(solution_path)} already exists.")
            continue
        summary = summarise(solution_path)
        with open(summary_path, "w") as f: f.write(summary.model_dump_json(indent=2))
        print(f"{i+1:4}: File analysis for {os.path.basename(solution_path)} saved to {summary_path}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Critique Python solutions to Advent of Code problems.")
    parser.add_argument('files', metavar='F', type=str, nargs='+', help='Python solution files to critique')
    parser.add_argument('-f', '--force', action='store_true', help='Force re-analysis of files even if critique already exists')
    args = parser.parse_args()

    summarise_files(args.files, force=args.force)
