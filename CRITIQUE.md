# Advent of Code 2024 Python Solutions Critique

This document provides a critique of the Python solutions for Advent of Code 2024.
            It was generated by the [critique.py](summarisers/critique.py) script.

18 Python solutions were analysed.

## Overall

_The provided solutions demonstrate a strong understanding of Python programming and algorithmic problem-solving. The codebase showcases effective use of data structures, algorithms, and Python features like list comprehensions and functional programming techniques. The modular design and separation of concerns contribute to code readability and maintainability. However, there are opportunities for improvement in areas such as code documentation, error handling, performance optimization, and memory management. With focused effort on addressing these areas, the codebase can become more robust, efficient, and maintainable, further enhancing the developer's skills and ability to tackle complex problems._

**Overall Score**: 8/10

**Main Strength**:
1. Good understanding of Python data structures and built-in functions
1. Effective use of modular design and separation of concerns
1. Clever application of algorithms like Dijkstra's, A* search, and depth-first search
1. Utilization of caching and memoization techniques for performance optimization
1. Well-structured and readable code with meaningful variable names
1. Inclusion of test cases and timing information for performance analysis

**Main Weaknesses**:
1. Lack of comments and docstrings in some solutions, hindering code readability and maintainability
1. Limited error handling and input validation, reducing robustness
1. Potential performance issues for large inputs due to inefficient algorithms or data structures
1. Hardcoded constants and magic numbers, making the code less configurable
1. Occasional code duplication and repetitive logic

**Main Issues**:
1. Recursive approaches in some solutions could lead to stack overflow for large inputs
1. Nested loops and inefficient data structures in certain functions, impacting performance
1. Memory-intensive operations like creating copies of grids or storing entire paths
1. Potential integer overflow or precision issues when dealing with large numbers

**Areas for Improvement**:
1. Improve code documentation with comments and docstrings for better readability and maintainability
1. Implement robust error handling and input validation to handle edge cases and invalid inputs
1. Optimize algorithms and data structures for better performance on large inputs
1. Refactor code to eliminate code duplication and improve modularity
1. Explore alternative approaches or data structures for memory-intensive operations
1. Consider using constants or configuration files for hardcoded values

## Files Analyzed

### Day 1: [aoc2024-day1.py](aoc2024-day1.py)

**Score**: 7/10

**Strengths**:
- Clear separation of concerns with separate functions for Part 1 and Part 2
- Effective use of Python's built-in functions (zip, sorted, abs)
- Good use of list comprehensions and functional programming techniques
- Well-structured and readable code with meaningful variable names
- Inclusion of timing information for performance analysis

**Weaknesses**:
- Lack of comments or docstrings explaining the logic behind the solutions
- No error handling or input validation
- Hardcoded test input file path

**Issues**:
- The part2() function could potentially be optimized by using a defaultdict instead of manually initializing counts to 0
- The timing information is printed after the solutions, which could be confusing if the output is long

### Day 2: [aoc2024-day2.py](aoc2024-day2.py)

**Score**: 8/10

**Strengths**:
- Clear separation of concerns with separate functions for different tasks.
- Effective use of Python data structures and built-in functions (e.g. zip, list comprehensions).
- Good use of helper functions (diff_, pos_neg, is_valid_, is_valid_tol).
- Well-structured and readable code with meaningful variable names.
- Handles both parts of the problem in separate functions.
- Includes test input and common utility functions.

**Weaknesses**:
- Lack of comments explaining the purpose and logic of some functions (e.g. diff_, pos_neg).
- No error handling or input validation for malformed input lines.
- Potential performance issues for very large input sizes due to the use of list comprehensions and unnecessary conversions between lists and sets.

**Issues**:
- No issues identified in the provided code.

### Day 3: [aoc2024-day3.py](aoc2024-day3.py)

**Score**: 7/10

**Strengths**:
- Clear separation of concerns with separate functions for Part 1 and Part 2.
- Effective use of regular expressions to parse the input string.
- Good use of list comprehensions and generator expressions.
- Well-structured and readable code with meaningful variable names.
- Modular design with helper functions like sum_total() and spans_().

**Weaknesses**:
- Lack of error handling for invalid input formats.
- No comments or docstrings explaining the purpose and logic of functions.
- Potential performance issues for very large input strings due to the use of regular expressions.

**Issues**:
- In spans_(): The function assumes that the input string starts with multiplication instructions enabled, which may not always be the case.
- In part2(): The function calculates the sum of products for each enabled span separately, which could be inefficient for large inputs with many spans.

### Day 4: [aoc2024-day4.py](aoc2024-day4.py)

**Score**: 7/10

**Strengths**:
- Clear separation of concerns with separate functions for Part 1 and Part 2.
- Effective use of helper functions (char_positions) and list comprehensions.
- Good use of nested loops and conditional checks to explore all possible cases.
- Clever approach to generating offsets for Part 1 and checking diagonal directions for Part 2.
- Well-structured and readable code with meaningful variable names.

**Weaknesses**:
- Lack of comments explaining the logic and approach for each part.
- Potential performance issues for larger grids due to nested loops and checking all offsets.
- No error handling or input validation for invalid or malformed grids.
- Hardcoded character sequences ('XMAS' and 'MAS') instead of using variables or constants.

**Issues**:
- In part1: Checking all offsets for each 'X' position could be inefficient for larger grids.
- In part2: Nested loops and checking all diagonal directions could be slow for larger grids.

### Day 5: [aoc2024-day5.py](aoc2024-day5.py)

**Score**: 7/10

**Strengths**:
- Clear separation of concerns with separate functions for parsing input, checking validity, fixing updates, and solving each part of the problem.
- Effective use of Python data structures like defaultdict and sets for representing rules.
- Good use of helper functions like rule_sets_, parse_input, is_valid_update, fix_one_update, and fixed_update_.
- Well-structured and readable code with meaningful variable names and comments.

**Weaknesses**:
- The fix_one_update and fixed_update_ functions could be optimized for better performance, especially for larger inputs.
- The solution assumes that the input is well-formed and does not handle invalid inputs or edge cases.
- The code could benefit from additional comments explaining the logic behind some of the functions.

**Issues**:
- In fix_one_update: The nested loops could potentially lead to inefficient performance for large inputs.
- In fixed_update_: The while loop could potentially run indefinitely if the update cannot be fixed, leading to an infinite loop.

### Day 6: [aoc2024-day6.py](aoc2024-day6.py)

**Score**: 8/10

**Strengths**:
- Well-structured and modular code with separate functions for parsing input, solving each part, and helper functions.
- Effective use of Python data structures (sets, frozensets, deque) and built-in functions.
- Good use of caching (lru_cache) to optimize the escaped_ function.
- Clear and concise variable names and comments explaining the purpose of functions.
- Inclusion of test input and timing information for performance analysis.

**Weaknesses**:
- The escaped_ function uses recursion, which could potentially lead to stack overflow for very large inputs.
- The part2() function could be optimized further for better performance, especially for larger maps.
- Error handling and input validation could be improved to handle edge cases or invalid inputs.

**Issues**:
- In escaped_: The recursive approach could be inefficient for very large maps.
- In part2: The breadth-first search could be memory-intensive for large maps with many potential obstruction positions.

### Day 7: [aoc2024-day7.py](aoc2024-day7.py)

**Score**: 7/10

**Strengths**:
- Clear separation of concerns with modular functions
- Effective use of recursion to explore all possible operator combinations
- Good use of helper functions and list comprehensions
- Well-structured and readable code with meaningful variable names
- Handles both parts of the problem with minimal code duplication

**Weaknesses**:
- Lack of comments explaining the purpose and logic of some functions
- No error handling or input validation
- Potential performance issues for large inputs due to recursive approach

**Issues**:
- In is_valid_step: Recursive approach could lead to stack overflow for large inputs
- In operate: Potential integer overflow when concatenating large numbers using '|'

### Day 8: [aoc2024-day8.py](aoc2024-day8.py)

**Score**: 7/10

**Strengths**:
- Modular design with separate functions for different tasks (parsing input, solving Part 1 and Part 2, etc.)
- Effective use of numpy arrays for efficient grid representation and manipulation
- Clever use of sets and sorting to handle antenna pairs and antinodes
- Handling of both Part 1 and Part 2 within the same solve() function, with a flag to control the behavior
- Inclusion of timing information for performance analysis

**Weaknesses**:
- Lack of comments and docstrings for better code readability and maintainability
- Potential performance issues for larger grids or more antennas due to the nested loops and sorting operations
- Limited error handling and input validation
- Hardcoded values (e.g. MARK = 9) could be defined as constants at the top of the file

**Issues**:
- In antinodes_: The nested loops and sorting operations could become inefficient for larger inputs.
- In solve: The construction of the img array and the sym_num dictionary could be optimized for better performance.
- In solve: The handling of exclusions could be simplified or optimized.

### Day 9: [aoc2024-day9.py](aoc2024-day9.py)

**Score**: 7/10

**Strengths**:
- Well-structured and modular code with separate functions for different tasks.
- Effective use of custom data structures (e.g. `cluster_`, `run_`) to represent the problem state.
- Good use of helper functions (e.g. `numbers_`, `blocks_`, `show`, `run_list_`) to break down the problem into smaller parts.
- Clear separation of Part 1 and Part 2 solutions.
- Inclusion of timing information for performance analysis.

**Weaknesses**:
- Lack of comments and docstrings to explain the purpose and functionality of some functions and classes.
- Potential inefficiency in the `defragment_run` method, which may not scale well for larger inputs.
- Limited error handling and input validation.
- Some code duplication in the handling of runs and clusters.

**Issues**:
- In `defragment_run`: The nested loop approach may not be efficient for large inputs with many runs and clusters.
- In `RunEncoding`: The `blocks_` method may be inefficient for large inputs, as it reconstructs the entire list of blocks from the runs.

### Day 10: [aoc2024-day10.py](aoc2024-day10.py)

**Score**: 7/10

**Strengths**:
- Clear separation of concerns with separate functions for different tasks.
- Effective use of Python data structures (sets, lists, and tuples).
- Good use of recursion to explore all possible paths.
- Well-structured and readable code with meaningful variable names.

**Weaknesses**:
- Lack of comments explaining the purpose and logic of the `trailhead_destinations` and `complete_trails` functions.
- Potential inefficiency for large inputs due to recursive approach.
- No error handling or input validation.

**Issues**:
- In `trailhead_destinations` and `complete_trails`: Recursive approach could lead to stack overflow for large inputs.
- In `part1` and `part2`: No input validation or error handling for invalid maps.

### Day 11: [aoc2024-day11.py](aoc2024-day11.py)

**Score**: 8/10

**Strengths**:
- Clear separation of concerns with separate functions for different tasks.
- Effective use of dictionaries to store and update counts of unique numbers.
- Caching of rule applications to avoid redundant computations.
- Well-structured and readable code with meaningful variable names and comments.
- Inclusion of timing information for performance analysis.

**Weaknesses**:
- The apply_rule() function could be optimized further for better performance.
- The blink_once_cache() function has some nested loops, which could be optimized.
- The solution doesn't handle invalid inputs or edge cases.

**Issues**:
- In apply_rule(): The string conversion and slicing operations could be inefficient for very large numbers.
- In blink_once_cache(): The nested loops and dictionary lookups could be slow for large inputs.

### Day 12: [aoc2024-day12.py](aoc2024-day12.py)

**Score**: 8/10

**Strengths**:
- Well-structured and modular code with separate functions for different tasks.
- Effective use of NumPy for efficient array operations and image processing.
- Clever use of bit masks and padding to simplify edge case handling.
- Visualization of intermediate steps for debugging and understanding.
- Handling of both Part 1 and Part 2 of the problem.
- Inclusion of timing information for performance analysis.

**Weaknesses**:
- Lack of comments and docstrings for some functions, making it harder to understand their purpose and implementation details.
- Potential memory inefficiency for very large inputs due to the use of NumPy arrays.
- Hardcoded values for tile sizes and other constants, which could be made more configurable.
- Verbose output and visualization code, which could be separated from the main solution for better readability.

**Issues**:
- In num_sides_(): The nested loops and edge case handling could potentially be optimized for better performance.
- In edge_counts_(): The nested loops could potentially be optimized for better performance.
- In compose_img(): The nested loops could potentially be optimized for better performance.

### Day 13: [aoc2024-day13.py](aoc2024-day13.py)

**Score**: 7/10

**Strengths**:
- Well-structured and modular code with separate functions for parsing, solving, and handling parts 1 and 2.
- Effective use of regular expressions for parsing input data.
- Utilization of NumPy arrays and SymPy for efficient numerical computations and equation solving.
- Clear separation of concerns with helper functions like xy_(), parse_machine(), parse_input(), fractional(), and is_int().
- Inclusion of test cases (test_solve()) for verifying the correctness of the solve() function.
- Printing of solution details for each machine, providing transparency and aiding debugging.

**Weaknesses**:
- Lack of error handling for invalid input or edge cases (e.g. no solution exists).
- Limited comments explaining the purpose and logic of certain functions or code blocks.
- Potential performance issues for large inputs due to the use of SymPy's symbolic equation solving.
- Hardcoded tolerance value (TOL) for determining integer solutions, which may not be optimal for all cases.
- Redundant conversion of NumPy arrays to lists and back in some places (e.g. print statements).

**Issues**:
- In solve(): The use of SymPy's symbolic equation solving may not scale well for large inputs or complex equations.
- In part1() and part2(): Lack of error handling for cases where no solution exists for a machine.
- In parse_input(): Potential performance issue for large inputs due to the use of list comprehensions and unnecessary conversions.

### Day 14: [aoc2024-day14.py](aoc2024-day14.py)

**Score**: 7/10

**Strengths**:
- Well-structured code with separate functions for different parts of the problem.
- Good use of regular expressions to parse the input lines.
- Efficient simulation of robot motion by wrapping around the edges.
- Clever use of a hash function to detect repeated configurations.
- Visualization of robot positions using matplotlib.
- Inclusion of test cases for input parsing.

**Weaknesses**:
- Lack of error handling for invalid input formats.
- Limited comments explaining the logic behind certain functions or conditions.
- Hardcoded constants for corner size and maximum fraction of points in corners.
- Potential performance issues for larger input sizes or longer simulations.

**Issues**:
- In is_tree(): The conditions for detecting a Christmas tree pattern may be too specific or restrictive.
- In part2(): The simulation runs for a fixed number of iterations (10_000_000), which may not be sufficient for all inputs.

### Day 15: [aoc2024-day15.py](aoc2024-day15.py)

**Score**: 7/10

**Strengths**:
- Well-structured and modular code with separate functions for different tasks.
- Effective use of NumPy arrays to represent the warehouse and perform operations.
- Good use of helper functions and classes to encapsulate functionality.
- Handling of both Part 1 and Part 2 scenarios with appropriate modifications.
- Inclusion of test cases and sample data for verification.
- Clear separation of concerns between parsing input, simulating movements, and calculating results.
- Use of Python's built-in functions and data structures (e.g. `zip`, `enumerate`, sets).

**Weaknesses**:
- Lack of comments and docstrings to explain the purpose and functionality of some functions and classes.
- Potential performance issues for very large warehouse layouts or long move sequences.
- Limited error handling and input validation.
- Hardcoded values for certain constants (e.g. `BOX_BASE`, `SPACE`, `WALL`, etc.).
- Repetitive code in some places (e.g. `SYMBOL_TO_NUMBER_1` and `SYMBOL_TO_NUMBER`).

**Issues**:
- In the `move_box_pairs` method, the handling of box pairs and frontier extension could be optimized for better performance.
- In the `advanced_boxes_` method, the use of a fixed loop limit (100) could potentially cause issues for very large warehouse layouts.
- In the `grid_to_lines2` function, the use of string concatenation and replacement could be inefficient for large grids.

### Day 16: [aoc2024-day16.py](aoc2024-day16.py)

**Score**: 9/10

**Strengths**:
- Well-organized structure with separate functions for different parts of the solution.
- Good use of comments to explain the purpose of functions and key parts of the code.
- Efficient use of A* search algorithm for pathfinding.
- Clever use of a heuristic function to optimize the search.
- Handling of multiple optimal paths, not just finding a single solution.
- Use of heapq for efficient priority queue implementation.
- Clear separation of Part 1 and Part 2 solutions.
- Inclusion of timing information for performance analysis.

**Weaknesses**:
- The solve_maze function is quite long and could potentially be split into smaller, more focused functions.
- Some magic numbers are used (e.g. PENALTY_MOVE = 1, PENALTY_TURN = 1000) which could be defined as constants at the top of the file for better maintainability.
- The reconstruct_paths function uses recursion, which could potentially lead to stack overflow for very large mazes.
- The solution doesn't handle invalid input gracefully (e.g. missing start or end points).
- There's some code duplication in the handling of predecessors and visited states.

**Issues**:
- In solve_maze: The handling of multiple paths and predecessors could potentially be memory-intensive for very large mazes.
- In reconstruct_paths: The recursive approach could be inefficient for very long paths.
- In part2: Creating a set of all tiles in all best paths could be memory-intensive for large mazes with many optimal paths.

### Day 17: [aoc2024-day17.py](aoc2024-day17.py)

**Score**: 7/10

**Strengths**:
- Well-structured and modular code with separate functions for different tasks.
- Effective use of regular expressions for parsing input.
- Good use of helper functions and functional programming techniques (e.g. `partial`).
- Inclusion of test cases and a testing mechanism.
- Clear separation of Part 1 and Part 2 solutions.
- Handling of edge cases and potential infinite loops.

**Weaknesses**:
- Lack of comments and docstrings explaining the purpose and functionality of some functions.
- Potential performance issues for large programs or input sizes due to the recursive nature of the `dfs` function.
- Limited error handling and input validation.
- Hardcoded constants (e.g. `MAX_ITERATIONS`, `INVALID_OUTPUT`) that could be made more configurable.

**Issues**:
- In `dfs`: The recursive approach could lead to stack overflow for very large programs or input sizes.
- In `execute_program`: The loop condition could be optimized to avoid unnecessary iterations.

### Day 18: [aoc2024-day18.py](aoc2024-day18.py)

**Score**: 7/10

**Strengths**:
- Well-structured code with separate functions for different tasks
- Good use of Python data structures (lists, sets) and built-in functions (heapq)
- Efficient implementation of the Uniform Cost Search algorithm
- Handles both Part 1 and Part 2 of the problem
- Includes test cases and examples for verification

**Weaknesses**:
- Limited error handling and input validation
- Lack of comments explaining the algorithm and key functions
- Potential performance issues for larger grids or more falling bytes
- Hardcoded grid dimensions and maximum number of bytes

**Issues**:
- In solve_grid: The reconstruction of the path using reconstruct_path() could be inefficient for very long paths due to the recursive approach.
- In part2: The approach of creating a copy of the grid for each falling byte could be memory-intensive for larger grids or more falling bytes.
