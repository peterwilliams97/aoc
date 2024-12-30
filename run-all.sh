#!/bin/bash

file_count=$(ls $pattern 2>/dev/null | wc -l | tr -d '[:space:]')
if [ $file_count -eq 0 ]; then
    echo "No files matching $pattern found."
    exit 1
fi

counter=0
for file in aoc2024-day*.py; do
    counter=$((counter + 1))
    echo "Running $file ($counter of $file_count)"
    python3 $file
    exit_code=$?
    if [ $exit_code -ne 0 ]; then
        echo "Error: $file failed with exit code $exit_code."
        exit $exit_code
    fi
    echo "Done with $file"
done

