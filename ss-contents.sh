#!/bin/bash

for file in aoc2024-day*.py; do
    echo "=== $file ==="
    ssage "This is the content of $file" < $file
done
