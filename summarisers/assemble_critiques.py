"""
    Overall Score: 7/10

 The Python solutions for Advent of Code 2024 demonstrate a good understanding of Python programming
 and problem-solving skills. The code is generally well-structured, with separate functions for
 different parts of the problems and good use of helper functions.

 Main Strengths:
 1. Consistent use of modular design across solutions
 2. Good utilization of Python's built-in features and libraries (e.g., NumPy, regular expressions)
 3. Clear separation of concerns in most solutions
 4. Effective use of data structures like sets and dictionaries
 5. Inclusion of timing measurements for performance analysis

 Main Weaknesses:
 1. Inconsistent error handling and input validation across solutions
 2. Some solutions contain hardcoded values that could be parameterized
 3. Lack of comprehensive comments in some complex algorithms
 4. Occasional use of global variables instead of function parameters
 5. Some functions are overly complex and could be broken down further

 Inefficient or Duplicate Code:
 1. is_valid_equation and is_valid_step in day7 solution (inefficient recursive approach)
 2. trailhead_destinations and complete_trails in day10 solution (inefficient recursive implementation)
 3. blink_once and blink_once_cache in day11 solution (slight code duplication)
 4. num_sides_ in day12 solution (complex nested loops)
 5. part1 and part2 in day13 solution (code duplication)
 6. antinodes_ in day8 solution (complex nested loops)
 7. run_list_ and blocks_ in day9 solution (potential inefficiencies)

 To improve the overall quality of the solutions, focus on:
 1. Implementing consistent error handling and input validation
 2. Refactoring complex functions into smaller, more manageable pieces
 3. Reducing code duplication by creating more reusable functions
 4. Adding more comprehensive comments, especially for complex algorithms
 5. Optimizing inefficient algorithms, particularly recursive implementations
 6. Replacing global variables with function parameters or configuration objects
 7. Parameterizing hardcoded values for better flexibility and maintainability
"""

import glob
import json
import os
from typing import List, Dict
from pydantic import BaseModel
from tools import call_anthropics_claude, day_number, read_json, write_text
from critique_tools import OVERALL_CRITIQUE_PATH, FILE_CRITIQUE_PATTERN

class AOCCombineCritiquesModel(BaseModel):
    """Model for the combined analysis of multiple Python solutions for Advent of Code 2024."""
    Score: int
    Overall: str
    Strengths: List[str]
    Weaknesses: List[str]
    Issues: List[str]
    DevelopmentAreas: List[str]


COMBINE_ANALYSIS = {
    "Strengths": [
        "Consistent use of modular design across solutions",
        "Good utilization of Python's built-in features and libraries (e.g., NumPy, regular expressions)",
        "Clear separation of concerns in most solutions",
        "Effective use of data structures like sets and dictionaries",
        "Inclusion of timing measurements for performance analysis"
    ],
    "Weaknesses": [
        "Inconsistent error handling and input validation across solutions",
        "Some solutions contain hardcoded values that could be parameterized",
        "Lack of comprehensive comments in some complex algorithms",
        "Occasional use of global variables instead of function parameters",
        "Some functions are overly complex and could be broken down further"
    ],
    "Issues": [
        "is_valid_equation and is_valid_step in day7 solution (inefficient recursive approach)",
        "trailhead_destinations and complete_trails in day10 solution (inefficient recursive implementation)",
        "blink_once and blink_once_cache in day11 solution (slight code duplication)",
        "num_sides_ in day12 solution (complex nested loops)",
        "part1 and part2 in day13 solution (code duplication)",
        "antinodes_ in day8 solution (complex nested loops)",
        "run_list_ and blocks_ in day9 solution (potential inefficiencies)"
    ],
    "DevelopmentAreas": [
        "Implementing consistent error handling and input validation",
        "Refactoring complex functions into smaller, more manageable pieces",
        "Reducing code duplication by creating more reusable functions",
        "Adding more comprehensive comments, especially for complex algorithms",
        "Optimizing inefficient algorithms, particularly recursive implementations",
        "Replacing global variables with function parameters or configuration objects",
        "Parameterizing hardcoded values for better flexibility and maintainability"
    ],
    "Overall": "The programmer demonstrates strong modular design, effective use of Python's features, and strategic data structure choices, but needs to improve error handling, code parameterization, and function simplicity while addressing inefficiencies and redundancies in specific solutions.",

    "Score": 2,

}

COMBINE_PROMPT = """
    You are an Advent of Code critic.
    You have recently rated {len(file_analyses)} python files and those rating summaries are below.
    You now need to the developer's coding patterns the overall performance in all the Python files
    and list

    1. The main strengths
    2. The main weaknesses.
    3. The functions that are inefficient or have duplicate or fragile code or have other issues. Be sure  to list the function names these issue occur in in the 'Issues' section. These can be copied from the individual file analyses..
    4. A broad description of the overall performance of the Python files.
    5. Overall skill level on a scale of 1 to 10 where 1 is beginner level, 5 is an average solution and 10 is the top of Advent of Code solutions.
    6. Recommendations for growth.

    Format the response as JSON with these sections, providing specific examples where possible.
    The JSON you output should have the following format:
    {COMBINE_ANALYSIS}

"""

def analyze_programmer_patterns(file_analyses: List[Dict]) -> dict:
    """ Analyzes multiple Python file assessments to identify programmer patterns.
        `file_analyses` is a list of analysis results for multiple Python solutions to
        Advent of Code problems.
        Returns: Comprehensive analysis of programmer patterns as a dictionary.
    """
    # Extract individual analysis data.
    analysis_data = []
    for path in file_analyses:
        data = read_json(path)
        day = day_number(path)
        data["File"] = path
        data["Title"] = f"Analysis of Day {day}"
        analysis_data.append(data)

    user_message = f"""
    Please analyze this programmer's patterns based on analyses of {len(file_analyses)} Python files.

    Here is the aggregated data:
    ```
    {json.dumps(analysis_data, indent=2)}
    ```

    Provide a comprehensive assessment in JSON format focusing on patterns, strengths, and areas for growth.
    Remember the keys in the JSON should be {list(COMBINE_ANALYSIS.keys())}.
    """

    return call_anthropics_claude(COMBINE_PROMPT, user_message)

def combine_critiques(force=False):
    """Combine the critiques of multiple Python solutions for Advent of Code 2024."""
    if not force and os.path.exists(OVERALL_CRITIQUE_PATH):
        print(f"Combined analysis already exists at {OVERALL_CRITIQUE_PATH}")
        return
    file_analyses = sorted(glob.glob(FILE_CRITIQUE_PATTERN))
    analysis = analyze_programmer_patterns(file_analyses)
    combined = AOCCombineCritiquesModel(**analysis)
    write_text(OVERALL_CRITIQUE_PATH, combined.model_dump_json(indent=2))
    print(f"Combined analysis saved to {OVERALL_CRITIQUE_PATH}")

if __name__ == '__main__':
    combine_critiques(force=True)
