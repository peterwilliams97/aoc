#!/bin/bash

for file in aoc2024-day*.py; do
    echo "=== $file ==="
    ssage "This is the content of $file. It is a solution to an Advent of Code problem. Does it solve the problem as stated in the file header comments?. If not, point out its shortcomings" < $file
done

