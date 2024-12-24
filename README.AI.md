 # Advent of Code 2024 Solutions

 This repository contains Python solutions for the Advent of Code 2024 challenges. Below is a brief description of each day's problem and solution.

 ## Files:

 1. aoc2024-day1.py
 2. aoc2024-day2.py
 3. aoc2024-day3.py
 4. aoc2024-day4.py
 5. aoc2024-day5.py
 6. aoc2024-day6.py
 7. aoc2024-day7.py
 8. aoc2024-day8.py
 9. aoc2024-day9.py
 10. aoc2024-day10.py
 11. aoc2024-day11.py
 12. aoc2024-day12.py
 13. aoc2024-day13.py
 14. aoc2024-day14.py

 ## Day 1: Number Pair Processing

 1. Part 1 problem: Calculate the sum of absolute differences between corresponding numbers in left and right columns.
 2. Part 1 solution: Parse input, transpose rows to columns, sort each column, calculate absolute differences, and sum them.
 3. Part 2 problem: Calculate total similarity score by multiplying each number in the left column by its occurrence count in the right column, then sum
 products.
 4. Part 2 solution: Parse input, transpose rows to columns, count occurrences in right column, multiply left column numbers by their counts, and sum
 products.

 ## Day 2: Red-Nosed Reactor Safety Reports

 1. Part 1 problem: Determine if reports are safe based on consistent level changes (increasing or decreasing) with adjacent levels differing by 1-3.
 2. Part 1 solution: Parse input, calculate differences between adjacent values, check if all differences are positive or negative and between 1-3, coun
 valid rows.
 3. Part 2 problem: Same as Part 1, but reports are also safe if removing a single level makes them safe.
 4. Part 2 solution: Parse input, check validity as-is, then try removing each value to check if resulting row is valid, count valid rows.

 ## Day 3: Corrupted Memory Instructions

 1. Part 1 problem: Identify valid 'mul' instructions in corrupted memory and calculate the sum of their products.
 2. Part 1 solution: Use regex to find 'mul' instructions, extract and multiply factors, sum all products.
 3. Part 2 problem: Introduce 'do()' and 'don't()' instructions to enable/disable future 'mul' instructions, calculate sum of products for enabled
 instructions.
 4. Part 2 solution: Use regex to find 'do()' and 'don't()' instructions, divide text into spans, calculate sum of products for enabled spans only.

 ## Day 4: Word Search Puzzle

 1. Part 1 problem: Count occurrences of "XMAS" in various directions within a grid.
 2. Part 1 solution: Find positions of X, M, A, S characters, check for "XMAS" sequences in all directions using span vectors, count valid sequences.
 3. Part 2 problem: Find instances of "MAS" forming an X shape in the grid.
 4. Part 2 solution: Find positions of M, A, S characters, check for 'M' and 'S' in diagonal positions forming X shape around each 'A', count valid
 patterns.

 ## Day 5: Safety Manual Updates

 1. Part 1 problem: Identify correctly ordered updates and find the sum of their middle page numbers.
 2. Part 1 solution: Parse input into rules and updates, create rule sets, check updates for validity, find middle page numbers of valid updates, sum
 them.
 3. Part 2 problem: Fix incorrectly ordered updates and find the sum of their middle page numbers.
 4. Part 2 solution: Identify invalid updates, swap pages violating rules until valid, find middle page numbers of fixed updates, sum them.

 ## Day 6: Guard Patrol Simulation

 1. Part 1 problem: Determine how many unique positions a guard visits before escaping a map with obstacles.
 2. Part 1 solution: Parse input map, simulate guard's movement (turn right at obstacles, move forward otherwise), track visited positions, count unique
 positions before exit.
 3. Part 2 problem: Find how many positions, when blocked, would prevent the guard from escaping the map.
 4. Part 2 solution: Implement search function to check escape possibility, iterate through empty positions, add each as obstacle and check if guard can
 escape, count trapping positions.

 ## Day 7: Equation Solving with Custom Operators

 1. Part 1 problem: Determine if operators (+, *) can be inserted between numbers to produce a test value, evaluating left-to-right.
 2. Part 1 solution: Parse input, implement recursive function to check valid operator combinations, count and sum valid equations.
 3. Part 2 problem: Add a new operator (|) for concatenation and solve equations.
 4. Part 2 solution: Extend Part 1 solution to include '|' operator, reuse logic to count and sum valid equations with new operator set.

 ## Day 8: Antenna Grid Analysis

 1. Part 1 problem: Find antinodes where two antennas of same frequency are in line, one twice as far as the other.
 2. Part 1 solution: Parse grid, identify antennas, find same-frequency pairs, calculate antinode positions based on rules, count valid antinodes.
 3. Part 2 problem: Find antinodes at any position in line with at least two same-frequency antennas, regardless of distance.
 4. Part 2 solution: Modify antinode calculation to extend along antenna lines, include antenna positions as potential antinodes, count all valid
 positions.

 ## Day 9: Disk Defragmentation

 1. Part 1 problem: Move file blocks one at a time from end to leftmost free space until no gaps remain, calculate filesystem checksum.
 2. Part 1 solution: Iterate through blocks bidirectionally, swap non-free space blocks from right with free space on left, calculate checksum.
 3. Part 2 problem: Move whole files to leftmost free space that fits, attempt once per file in decreasing ID order, calculate checksum.
 4. Part 2 solution: Create RunEncoding class for block representation, implement defragmentation method to move clusters to earlier runs, process right
 to left, calculate checksum.

 ## Day 10: Topographic Map Trail Analysis

 1. Part 1 problem: Calculate sum of scores for all trailheads, where score is number of 9-height positions reachable from trailhead.
 2. Part 1 solution: Use recursive function to find reachable 9-height positions from each trailhead, iterate through chart to identify trailheads and
 calculate scores.
 3. Part 2 problem: Calculate sum of ratings for all trailheads, where rating is number of distinct complete trails (0 to 9 height sequence) from
 trailhead.
 4. Part 2 solution: Use recursive function to find all distinct complete trails from each trailhead, iterate through chart to count trails for each
 trailhead.

 ## Day 11: Stone Number Simulation

 1. Part 1 problem: Simulate stone number changes for 25 blinks based on specific rules, count final number of stones.
 2. Part 1 solution: Implement rules for number changes, apply rules to all numbers in list for each blink, iterate 25 times, return final list length.
 3. Part 2 problem: Simulate stone number changes for 75 blinks, count final number of stones.
 4. Part 2 solution: Introduce caching mechanism, use dictionaries for number counts and rule results, optimize blinking process for 75 iterations, sum
 final number counts.

 ## Day 12: Garden Plot Fencing Cost

 1. Part 1 problem: Calculate total fencing cost by multiplying each region's area by its perimeter and summing products for all regions.
 2. Part 1 solution: Convert input to 2D numpy array, identify connected components, calculate area and perimeter for each, multiply and sum results.
 3. Part 2 problem: Calculate new fencing cost using number of sides each region has instead of perimeter.
 4. Part 2 solution: Use connected components from Part 1, calculate number of sides for each component using custom algorithm, multiply area by sides a
 sum results.

 ## Day 13: Claw Machine Optimization

 1. Part 1 problem: Calculate minimum tokens needed to win all prizes with given coordinates using two movement buttons.
 2. Part 1 solution: Parse input data, use sympy to solve linear equations for button presses, calculate total cost for solvable machines.
 3. Part 2 problem: Add 10,000,000,000,000 to both X and Y coordinates of each prize, recalculate minimum tokens needed.
 4. Part 2 solution: Modify prize coordinates, repeat process from Part 1 with new coordinates, calculate total cost for solvable machines.

 ## Day 14: Robot Movement Simulation

 1. Part 1 problem: Predict robot positions after 100 seconds in wrapping space, calculate safety factor based on quadrant counts.
 2. Part 1 solution: Parse input for robot positions and velocities, simulate movement for 100 seconds, count robots in each quadrant, multiply counts f
 safety factor.
 3. Part 2 problem: Determine minimum seconds for robots to form a Christmas tree pattern.
 4. Part 2 solution: Implement function to check for tree pattern, simulate movement while checking for pattern, use optimization techniques, return elapsed time when pattern found.

This README.md provides a concise overview of each day's problem and solution, focusing on the key aspects of both parts for each challenge.             
