"""Critique Python solutions to Advent of Code problems using Ahthropic CLAUDE.

"""

import os
import sys
import time
import json
from typing import List
from pydantic import BaseModel
from tools import call_anthropics_claude, basename_, day_number, write_text, read_text
from critique_tools import DATA_DIR_CRITIQUES

class AOCCritiqueModel(BaseModel):
    """Model for the critique of a Python solution to an Advent of Code problem."""
    Day: int
    Name: str
    Score: int
    Overall: str
    Problem1: str
    Problem2: str
    Solution1: str
    Solution2: str
    Strengths: List[str]
    Weaknesses: List[str]
    Issues: List[str]

CRITIQUE_ANALYSIS = {

 "Problem1": "Description of Part 1 of the problem.",
 "Problem2": "Description of Part 2 of the problem.",
 "Solution1": "Description of the solution to Part 1.",
 "Solution2": "Description of the solution to Part 2.",

  "Strengths": [
    "Description of strength 1, if there is one.",
    "Description of strength 2, if there is one.",
    "Description of strength 3, if there is one."
  ],
  "Weaknesses": [
    "Description of weakness 1, if there is one.",
    "Description of weakness 2, if there is one."
    "Description of weakness 3, if there is one."
  ],
  "Issues": [
    "Description of 1st main problem in the code, if there is one.",
    "Description of 2nd main problem in the code, if there is one.",
    "Description of 3rd main problem in the code, if there is one."
  ],
 "Overall": "Description of the overall quality of the solution.",
 "Score": 7,
}

if False:
    json.dumps(CRITIQUE_ANALYSIS, indent=2)
    EXAMPLE_CRITIQUE = AOCCritiqueModel(**CRITIQUE_ANALYSIS)
    print(EXAMPLE_CRITIQUE.json())
    exit(68)

# The prompt for telling the LLM to summarise a Python solution to an Advent of Code problem and
# output a JSON response.

with open("coding-criteria.txt") as f: coding_criteria = f.read()
CRITIQUE_SYSTEM_PROMPT = f"""
    You are terse and to the point.
    You are an Advent of Code critic.
    You focus on how well the code addresses the problem.
    You are judging professional programmerss
    Your judging criteria are as follows:
    {coding_criteria}
    ---------------------------
    Scores range from 1 to 10, where 1 the least you would expect from a professional programer,
    5 is an average solution for skilled programer, and 10 is the top of Advent of Code solutions.
    The most important criterion is how well the code addresses the problem it is solving. This
    includes correctness, efficiency, and robustness.
    The next most important criterion is how easy the code is to understand and extend.
    If you see inefficient code, code duplication, or fragile code list the
    function names it occurs in in the 'Issues' section.
    IGNORE the absence of type hints.
    Please make the the following judgements when you are given Python Advent of Code solutions.
    Your analysis should include the sections in the following JSON format.

    Example response:
    {CRITIQUE_ANALYSIS}

"""

def analyse_python_file(code: str) -> dict:
    """Analyse a Python solution to an Advent of Code problem and return a structured critique."""
    keys = list(CRITIQUE_ANALYSIS.keys())
    keys_text = f"{keys}".replace("'", '"')

    user_message = f"""
    The following text is a Python solution to an Advent of Code problem.
    Please analyse this code .
    ````python
    {code}
    ````
    Format your answers as JSON. Remember the JSON keys are {keys_text}.

    ."""
    return call_anthropics_claude(CRITIQUE_SYSTEM_PROMPT, user_message)

def critique_(filename):
    """Critique a Python solution to an Advent of Code problem.
        `filename` is the path to the Python solution file.
        Returns: A validated critique of the solution as a Pydantic model.
    """
    code = read_text(filename)
    analysis = analyse_python_file(code)
    name = os.path.basename(filename)
    analysis["Name"] = name
    analysis["Day"] = day_number(filename)
    return AOCCritiqueModel(**analysis)

def critique_files(file_list, force=False):
    """Critique multiple Python solutions to Advent of Code problems.
        `file_list` is a list of paths to Python solution files.
        `force` forces re-analysis of files even if critiques already exist.
    """
    os.makedirs(DATA_DIR_CRITIQUES, exist_ok=True)
    for i, solution_path in enumerate(file_list):
        critique_path = os.path.join(DATA_DIR_CRITIQUES, basename_(solution_path) + ".json")
        if not force and os.path.exists(critique_path):
            print(f"{i+1:4}: File analysis for {os.path.basename(solution_path)} already exists.")
            continue
        critique = critique_(solution_path)
        write_text(critique_path, critique.model_dump_json(indent=2))
        print(f"{i+1:4}: File analysis for {os.path.basename(solution_path)} saved to {critique_path}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Critique Python solutions to Advent of Code problems.")
    parser.add_argument('files', metavar='F', type=str, nargs='+', help='Python solution files to critique')
    parser.add_argument('-f', '--force', action='store_true', help='Force re-analysis of files even if critique already exists')
    args = parser.parse_args()

    critique_files(args.files, force=args.force)
