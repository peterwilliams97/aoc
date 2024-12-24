"""
    Check if the README.md file follows the specified structure.
"""
import re, sys, glob
from common import read_lines

PATTERN = "aoc2024-day*.py"
SOLN_FILES = sorted(glob.glob(PATTERN))
RE_SOLN = re.compile(r"aoc2024-day(\d+).py")
RE_DAY = re.compile(r"Day\s+(\d+):", re.IGNORECASE)

def trim_lines(lines):
    """Trim the preamble from the lines.
    e.g.
        Here's a draft README.md based on the summaries provided:

        # Advent of Code 2024 Solutions
    """
    for i, line in enumerate(lines):
        if "#" in line:
            return lines[i:]
    return lines

def soln_day(filename):
    "Return the day number from the filename."
    m = RE_SOLN.search(filename)
    assert m, f"Bad filename: {filename}"
    return int(m.group(1))

def match_soln(line, filename):
    "Return True if line matches the filename."
    if filename in line: return True
    day = soln_day(filename)

    m = RE_DAY.search(line)
    if m:
        return day == int(m.group(1))
    return False

def check_readme_structure(lines):
    """Check if the README.md content `lines` follows the specified structure.
        Returns msg, ok where
        - msg is a message indicating the error and
        -  ok is a boolean indicating if the structure is correct.
    """
    # print(f"{len(lines)} : '{lines[0]}'")
    lines = trim_lines(lines)
    assert lines, "No content in README.md"
    header = lines[0]
    problems = []
    def add(problem): problems.append(problem)

    if not header.startswith("# "):
        add("README.md should start with a level 1 header.")

    subheadings = [line for line in lines if line.startswith("##")]
    for filename in SOLN_FILES:
        matches = [line for line in subheadings if match_soln(line, filename)]
        if not matches:
            add(f"No sub-heading for {filename}")

    # Check for lists
    content = "\n".join(lines)
    dot_lists = re.findall(r'^\s*[-*] ', content, re.MULTILINE)
    num_lists = re.findall(r'^\s*\d+\. ', content, re.MULTILINE)
    if not dot_lists and not num_lists:
        add("No lists found.")

    return "\n".join(problems), not problems

if __name__ == "__main__":
    filename = sys.argv[1]
    lines = read_lines(filename)
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line]
    msg, ok = check_readme_structure(lines)
    print(msg)
    sys.exit(0 if ok else 7)
