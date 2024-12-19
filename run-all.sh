#!/bin/bash

for file in aoc2024-day*.py; do
    echo "Running $file"
    python3 $file
    echo "Done"
    echo
done

