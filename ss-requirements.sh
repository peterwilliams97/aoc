#!/bin/bash

# This script writes a requirements.txt for Python files matching a pattern.

imports_file="imports.txt"
requirements_file="requirements.txt"
requirements_temp="requirements.temp.txt"
pattern="aoc2024-day*.py"
error_log="pip_errors.log"

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

file_count=$(ls $pattern 2>/dev/null | wc -l | tr -d '[:space:]')
if [ $file_count -eq 0 ]; then
    echo "No files matching $pattern found."
    exit 1
fi

if $summarize; then
    echo "About to find imports in $file_count files matching $pattern"
    ssage "I am about to find imports in $file_count files matching $pattern. These are the imports that will need to be pip installed, not local imports. I will prompt you once for each Python file"

    > $imports_file
    for file in $pattern; do
        echo "Finding imports in $file"
        echo "Start of $file imports ==========================================================" >> $imports_file
        ssage "This is the contents of $file. Find all the imports in it. Python file starts now.\n==========================================================\n" < $file >> $imports_file
        echo "End of $file summary ==========================================================\n\n\n" >> $imports_file
    done

    echo "Wrote $imports_file"
fi

counter=0

# Loop to make ssage comment, run check_readme.py, and exit if check_readme.py has exit code 0
while true; do
    ssage "Write a requirements.txt for the $file_count python files matching $pattern in this directory. You have recently found the imports for these python files and your responses are below. Write a valid requirement.txt file the at I use in \n  pip install -r requirement.txt\n Do NOT write a description of how to write requirement.txt\n The requirement.txt should select the versions installed on this computer.\n-----------------------------\n" < $imports_file > $requirements_temp

    # Save a copy of the requirements file with a numbered suffix
    suffix=$(printf "%03d" $counter)
    cp $requirements_temp "requirements.$suffix.txt"
    counter=$((counter + 1))

    # Check if $requirements_temp is a valid pip requirements file
    pip install --dry-run -r $requirements_temp > /dev/null 2> $error_log
    pip_exit_code=$?

    if [ $pip_exit_code -eq 0 ]; then
        echo "$requirements_temp is a valid pip requirements file."
        ssage "This requirements.txt structure is correct. Thank you!"
        break
    else
        echo -e "$requirements_temp is not a valid pip requirements file.\n" < $error_log
        ssage "This requirements.txt structure is incorrect. pip install requirements.txt gives an error. Please regenerate this file. Do NOT tell me how to fix it.. The pip error message is below.\n-----------------------------\n" < $error_log
    fi

    # Exit the loop if counter >= 3
    if [ $counter -ge 5 ]; then
        echo "Reached maximum number of attempts ($counter). Done."
        break
    fi
done

mv $requirements_temp $requirements_file
echo "Wrote $requirements_file"
