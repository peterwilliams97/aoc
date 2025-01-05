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
    "Problem1": "In Part 1 of the Reindeer Maze problem, the objective is to determine the lowest score a Reindeer can achieve while navigating from the start tile ('S') to the end tile ('E') in a maze. The Reindeer can move forward one tile at a time, increasing their score by 1 point per step, and can rotate 90 degrees clockwise or counterclockwise, increasing their score by 1000 points per turn. The challenge is to find the optimal path that minimizes the total score, considering both the number of steps and the number of turns required to reach the end tile without moving into walls ('#').",
    "Problem2": "In Part 2 of the Reindeer Maze problem, the goal is to identify all tiles that are part of any best path through the maze, including the start ('S') and end ('E') tiles. After determining the lowest score paths in Part 1, you need to analyze the maze to find which non-wall tiles (S, ., or E) are included in at least one of these optimal paths. This information is crucial for determining the best spots to sit and watch the action, as sitting on these tiles ensures you won't miss any of the Reindeer's movements. The problem requires you to mark all such tiles on the maze, highlighting the paths that contribute to the lowest score.",
    "Solution1": "The part1() function in the aoc2024-day16.py script aims to solve the Reindeer Maze problem by finding the lowest score a Reindeer can achieve while navigating from the start ('S') to the end ('E') tile in a maze. The function utilizes the solve_maze() function, which implements an A* search algorithm to explore possible paths through the maze. The algorithm considers both the number of steps and the number of turns, assigning a penalty of 1 point per step and 1000 points per turn. The solve_maze() function tracks multiple paths and reconstructs all paths that achieve the minimum score, ensuring that all optimal paths are identified. The part1() function then prints the minimum score and the best paths found. While the function effectively finds the optimal paths, it could benefit from additional comments and error handling to improve readability and robustness. Additionally, the function could be optimized further to handle larger mazes more efficiently.",
    "Solution2": "The part2() function in the aoc2024-day16.py script extends the solution from Part 1 by identifying all tiles that are part of any best path through the maze, including the start ('S') and end ('E') tiles. After determining the lowest score paths using the solve_maze() function, which employs an A* search algorithm, part2() analyzes the maze to find which non-wall tiles (S, ., or E) are included in at least one of these optimal paths. The function effectively tracks multiple predecessors for each state to ensure all possible paths are considered, even when paths split and rejoin. It then reconstructs all valid paths from the end to the start, marking the tiles that are part of these paths. While the function successfully identifies and marks all relevant tiles, it could benefit from additional comments and error handling to enhance readability and robustness. Furthermore, optimizing the path reconstruction process could improve performance, especially for larger mazes",
    "Strengths": [
        "Well-organized structure with separate functions for different parts of the solution.",
        "Good use of comments to explain the purpose of functions and key parts of the code.",
        "Efficient use of A* search algorithm for pathfinding.",
        "Clever use of a heuristic function to optimize the search.",
        "Handling of multiple optimal paths, not just finding a single solution.",
        "Use of heapq for efficient priority queue implementation.",
        "Clear separation of Part 1 and Part 2 solutions.",
        "Inclusion of timing information for performance analysis."],
    "Weaknesses": [
        "The solve_maze function is quite long and could potentially be split into smaller, more focused functions.",
        "Some magic numbers are used (e.g. PENALTY_MOVE = 1, PENALTY_TURN = 1000) which could be defined as constants at the top of the file for better maintainability.",
        "The reconstruct_paths function uses recursion, which could potentially lead to stack overflow for very large mazes.",
        "The solution doesn't handle invalid input gracefully (e.g. missing start or end points).",
        "There's some code duplication in the handling of predecessors and visited states."],
    "Issues": [
        "In solve_maze: The handling of multiple paths and predecessors could potentially be memory-intensive for very large mazes.",
        "In reconstruct_paths: The recursive approach could be inefficient for very long paths.",
        "In part2: Creating a set of all tiles in all best paths could be memory-intensive for large mazes with many optimal paths."],
    "Overall": "This solution demonstrates a strong understanding of algorithmic problem-solving and efficient implementation. The use of A* search with a heuristic function is particularly impressive. The code is well-structured and commented, making it easy to understand and maintain. The main areas for improvement are in code organization (breaking down the solve_maze function), handling edge cases, and potentially optimizing memory usage for very large inputs. However, these are relatively minor points in the context of an Advent of Code solution. The solution goes beyond simply solving the problem by handling multiple optimal paths and providing timing information, which shows a high level of thoroughness and attention to detail.",
    "Score": 4
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
    You are judging professional programs
    Your judging criteria are as follows:
    {coding_criteria}
    ---------------------------
    Scores range from 1 to 10, where 1 the least you would expect from a professional programer,
    5 is an average solution for skilled programer, and 10 is the top of Advent of Code solutions.
    If you see inefficient code, code duplication, hardcoded values or fragile code list the
    function names it occurs in in the 'Issues' section.
    IGNORE the absence of type hints.
    Please make the the following judgements when you are given Python Advent of Code solutions.
    Your analysis should include the sections in the following JSON format.
    Format your answers as JSON. Remember to escape special characters such as quotes.

    Example response:
    {CRITIQUE_ANALYSIS}

"""

def analyse_python_file(code: str) -> dict:
    """Analyse a Python solution to an Advent of Code problem and return a structured critique."""
    keys = list(CRITIQUE_ANALYSIS.keys())
    keys_text = f"{keys}".replace("'", '"')

    user_message = f"""
    The following text is a Python solution to an Advent of Code problem
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
