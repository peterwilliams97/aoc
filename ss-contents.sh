#!/bin/bash

for file in aoc2024-day*.py; do
    echo "=== $file ==="
    ssage "This is the content of $file. It is a solution to an Advent of Code problem. Only read it and remember its contents. Don't comment on it now." < $file
done

ssage "Write a README.md that for the git repo containing the above files. Please list the files and a summary of each one. Point out weaknesses in each of the above python files"
