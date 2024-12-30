#!/bin/bash

# This script summarizes python files that solve to Advent of Code problems.
# It reads the files matching a pattern, writes the summaries of them to a file,
# then writes a README.AI.md file that describes the summaries.

summaries_file="summaries.txt"
readme_file="README.AI.md"
readme_temp="README.AI.temp.md"
pattern="aoc2024-day*.py"

# Parse command line options
summarize=true
while getopts ":n" opt; do
  case $opt in
    n)
      summarize=false
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

if [ -f "README.AI.md" ]; then
    old_readme="README.AI.md"
elif [ -f "README.md" ]; then
    old_readme="README.md"
else
    echo "Neither README.AI.md nor README.md exists. Exiting."
    exit 1
fi

file_count=$(ls $pattern 2>/dev/null | wc -l | tr -d '[:space:]')
if [ $file_count -eq 0 ]; then
    echo "No files matching $pattern found."
    exit 1
fi

if $summarize; then
    echo "About to summarize $file_count files matching $pattern"

    > $summaries_file
    for file in $pattern; do
        echo "Summarizing $file"
        echo "Start of $file summary ==========================================================" >> $summaries_file
        ssage "This is the contents of $file. It is a solution to an Advent of Code problem.
            There are 2 parts to the problem. Start by listing the file name $file, then summarize
            the problem, including both parts. Then describe the solutions to parts 1 and 2. Then
            summarize each of your summaries for parts 1 and 2 of the problem and their solutions.
            The python file starts now.
            ==========================================================" < $file >> $summaries_file
        echo "End of $file summary ==========================================================\n\n\n" >> $summaries_file
    done

    echo "Wrote $summaries_file"
fi

ssage "When I ask you to write a README.md, always identify yourself as the author immediately after
    the title and give details about the LLM you are using and how you are using it. Tell us the date y
    ou were built and your authors".

ssage "When I ask you to write a README.md, I mean a markdown file that I can use in github. It
    should have the same layout as the contents of the README.md file below.
    Use a simple #, ##, ### heirarchy and lists.
    -----------------------------
    " < $old_readme

counter=0

# Loop to make ssage comment, run check_readme.py, and exit if check_readme.py has exit code 0
while true; do
    ssage "Write a README.md describing the $file_count python files matching $pattern in this directory.
    You have recently summarised these python files and those summaries are below. Please list the
    matching files. For each Python file, describe parts 1 and 2 of the problem and give brief
    descriptions of their solutions. More explicitly,fFor each Python file write the list:
        1. Part 1 problem,
        2. Part 1 solution,
        3. Part 2 problem,
        4.Part 2 solution.
    Make each of these summaries as succint as possible. Never just say \"calculations\", explain the
    calculations. Use the summaries you saved previously as your main source. The saved summariers
    are below.
    -----------------------------
    " < $summaries_file > $readme_temp

    python3 fix-markdown.py $readme_temp

     # Save a copy of the README.md file with a numbered suffix.
    suffix=$(printf "%03d" $counter)
    cp $readme_temp "README.AI.$suffix.md"
    counter=$((counter + 1))

    # Check the README.md file structure
    output=$(python3 check-readme.py $readme_temp "$pattern")
    exit_code=$?
    if [ $exit_code -eq 0 ]; then
        echo "$readme_temp structure is correct. Done."
        ssage "README.md structure is correct. Thank you!"
        mv $readme_temp $readme_file
        break
    elif [ $exit_code -eq 7 ]; then
        echo "$output" > problems.txt
        echo "$readme_temp structure is incorrect. Fixing.
        \n-------------\n$output\n-------------"

        ssage "README.md structure is incorrect. Remember my layout instructions above. Please fix the following issues when you next write a README.md file. Do NOT tell me how to fix the issues. Rewrite the README.md yourself. Issues:\n       $output"
    else
        echo "Unexpected exit code $exit_code from check-readme.py. Exiting."
        exit 1
    fi
done

echo "Wrote $readme_file"
