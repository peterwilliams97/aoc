"""
    https://adventofcode.com/2024/day/17

    --- Day 17: Chronospatial Computer ---
    The Historians push the button on their strange device, but this time, you all just feel like
    you're falling.

    "Situation critical", the device announces in a familiar voice. "Bootstrapping process failed.
    Initializing debugger...."

    The small handheld device suddenly unfolds into an entire computer! The Historians look around
    nervously before one of them tosses it to you.

    This seems to be a 3-bit computer: its program is a list of 3-bit numbers (0 through 7),
    like 0,1,2,3. The computer also has three registers named A, B, and C, but these registers
    aren't limited to 3 bits and can instead hold any integer.

    The computer knows eight instructions, each identified by a 3-bit number (called the
    instruction's opcode). Each instruction also reads the 3-bit number after it as an input; this
    is called its operand.

    A number called the instruction pointer identifies the position in the program from which the
    next opcode will be read; it starts at 0, pointing at the first 3-bit number in the program.
    Except for jump instructions, the instruction pointer increases by 2 after each instruction is
    processed (to move past the instruction's opcode and its operand). If the computer tries to read
    an opcode past the end of the program, it instead halts.

    So, the program 0,1,2,3 would run the instruction whose opcode is 0 and pass it the operand 1,
    then run the instruction having opcode 2 and pass it the operand 3, then halt.

    There are two types of operands; each instruction specifies the type of its operand. The value
    of a literal operand is the operand itself. For example, the value of the literal operand 7 is
    the number 7. The value of a combo operand can be found as follows:

    Combo operands 0 through 3 represent literal values 0 through 3.
    Combo operand 4 represents the value of register A.
    Combo operand 5 represents the value of register B.
    Combo operand 6 represents the value of register C.
    Combo operand 7 is reserved and will not appear in valid programs.
    The eight instructions are as follows:

    The adv instruction (opcode 0) performs division. The numerator is the value in the A register.
    The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an
    operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of
    the division operation is truncated to an integer and then written to the A register.

    The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's
    literal operand, then stores the result in register B.

    The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby
    keeping only its lowest 3 bits), then writes that value to the B register.

    The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register
    is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if
    this instruction jumps, the instruction pointer is not increased by 2 after this instruction.

    The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then
    stores the result in register B. (For legacy reasons, this instruction reads an operand but
    ignores it.)

    The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs
    that value. (If a program outputs multiple values, they are separated by commas.)

    The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is
    stored in the B register. (The numerator is still read from the A register.)

    The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is
    stored in the C register. (The numerator is still read from the A register.)

    Here are some examples of instruction operation:

    If register C contains 9, the program 2,6 would set register B to 1.
    If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
    If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and
      leave 0 in register A.
    If register B contains 29, the program 1,7 would set register B to 26.
    If register B contains 2024 and register C contains 43690, the program 4,0 would set register B
      to 44354.
    The Historians' strange device has finished initializing its debugger and is displaying some
    information about the program it is trying to run (your puzzle input). For example:

    Register A: 729
    Register B: 0
    Register C: 0

    Program: 0,1,5,4,3,0
    Your first task is to determine what the program is trying to output. To do this, initialize the
    registers to the given values, then run the given program, collecting any output produced by out
    instructions. (Always join the values produced by out instructions with commas.) After the above
    program halts, its final output will be 4,6,3,5,6,3,5,2,1,0.

    Using the information provided by the debugger, initialize the registers to the given values,
    then run the program. Once it halts, what do you get if you use commas to join the values it
    output into a single string?

    --- Part Two ---
    Digging deeper in the device's manual, you discover the problem: this program is supposed to
    output another copy of the program! Unfortunately, the value in register A seems to have been
    corrupted. You'll need to find a new value to which you can initialize register A so that the
    program's output instructions produce an exact copy of the program itself.

    For example:

    Register A: 2024
    Register B: 0
    Register C: 0

    Program: 0,3,5,4,3,0
    This program outputs a copy of itself if register A is instead initialized to 117440. (The
    original initial value of register A, 2024, is ignored.)

    What is the lowest positive initial value for register A that causes the program to output a
    copy of itself?
"""
import time
import re
from functools import partial
from common import parse_args, read_lines

RE_REGISTER = re.compile(r"Register\s+([A-C]):\s*(\d+)")
RE_PROGRAM = re.compile(r"Program:\s*(.*)")

def parse_program(lines):
    registers = {}
    program = []
    for line in lines:
        m = RE_REGISTER.search(line)
        if m:
            registers[m.group(1)] = int(m.group(2))
            continue
        m = RE_PROGRAM.search(line)
        if m:
            program = [int(x) for x in m.group(1).split(",")]
    return program, registers

def reg_str(registers):
    "Return a string representation of the registers."
    parts = [f"{k}={registers.get(k, 0):2}" for k in "ABC"]
    return " ".join(parts)

# NOP = 8
ADV = 0
BXL = 1
BST = 2
JNZ = 3
BXC = 4
OUT = 5
BDV = 6
CDV = 7

def result_(output):
    "Return a string representation of the output."
    return ",".join(str(x) for x in output)

def combo_(registers, operand):
    "Return the combo value of the operand."
    assert 0 <= operand < 7, f"Invalid operand {operand}"
    return operand if operand < 4 else registers["ABC"[operand - 4]]

MAX_INTERATIONS = 1000
INVALID_OUTPUT = [999]

def execute_program(program, registers):
    "Execute the program and return the output."
    output = []
    ip = 0

    iterations = 0

    while ip < len(program):
        iterations += 1
        if iterations > 1000: return INVALID_OUTPUT # Prevent infinite loops
        opcode, operand = program[ip], program[ip + 1]
        combo = combo_(registers, operand)
        ip += 2
        if   opcode == ADV: registers["A"] = registers["A"] >> combo
        elif opcode == BDV: registers["B"] = registers["A"] >> combo
        elif opcode == CDV: registers["C"] = registers["A"] >> combo
        elif opcode == BXL: registers["B"] ^= operand
        elif opcode == BXC: registers["B"] ^= registers["C"]
        elif opcode == BST: registers["B"] = combo & 7
        elif opcode == OUT: output.append(combo & 7)
        elif opcode == JNZ:
            if registers["A"] != 0: ip = operand
        else: raise Exception(f"Unknown opcode {opcode}")
    return output

def output0_(program, a):
    "Return the output[0] of the program for the given value of register A."
    registers = {"A": a, "B": 0, "C": 0}
    return execute_program(program, registers)[0]

def dfs(program, pos, a0):
    """Depth-first search for the value of register A that produces the output `program`.

        `program`: The program's instructions and expected output.
        `pos`: The current position in the program, starting from the end.
        `a0`: The current value of register A. (a0 covers program[pos+1:]).
        Returns: Register A value that produces the output program[pos+1:].

        Base Case: If `pos` is less than 0, the search has reached the beginning of the
            program, and `a0` is returned. (a0 it covers program)
        Iterative Search: The function iterates over `a0` << 3 to (`a0` << 3) + 7,the potential
            values for register A shifted left by 3 bits.
        Output Check: For each value of `a`, if program[pos] == output0_(a), recurse to find
            `a1` = dfs(program, pos - 1, a), the register A value for (`pos` - 1).

        This search is guaranteed to find the correct value of register A because the program
        the output is the low 3 bits of the register A value shifted left by 3 bits and possibly
        XORed with a constant or another register value which in turn is the low 3 bits of the
        register A value shifted left by 3 bits
    """
    N = 3 # Number of bits
    if pos < 0: return a0
    for a in range(a0 << N, (a0 << N) + (1 << N)):
        if output0_(program, a) == program[pos]:
            a1 = dfs(program, pos - 1, a)
            if a1 >= 0: return a1
    return -1

def test_program(program, registers, expected_output, verbose):
    "Test the program against the expected output."
    output = execute_program(program, registers, verbose)
    result = result_(output)
    assert result == expected_output, f"{program}: Expected '{expected_output}', got '{result}'"
    print(f"Test passed: {result}")

def test1(verbose):
    """
        If register C contains 9, the program 2,6 would set register B to 1.
        If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
        If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and
        leave 0 in register A.
        If register B contains 29, the program 1,7 would set register B to 26.
        If register B contains 2024 and register C contains 43690, the program 4,0 would set register B
        to 44354.
    """
    test = partial(test_program, verbose=verbose)

    test([2, 6],             {"C": 9},    "")
    test([5, 0, 5, 1, 5, 4], {"A": 10},   "0,1,2")
    test([0, 1, 5, 4, 3, 0], {"A": 2024}, "4,2,5,6,7,7,7,7,3,1,0")
    test([1, 7],             {"B": 29},   "")
    test([4, 0],             {"B": 2024, "C": 43690}, "44354")

def part1(program, registers):
    """Solution to part 1. "4,6,3,5,6,3,5,2,1,0" for the test input. ("1,7,6,5,1,0,5,0,7")"""
    output = execute_program(program, registers)
    result = result_(output)
    print(f"Part 1: The program output is: {result}")

def part2(program):
    "Solution to part 2. 45 for the test input. (236555995274861)"
    a = dfs(program, len(program) - 1, 0)
    if a < 0:
        print("No solution found")
        return
    registers = {"A": a, "B": 0, "C": 0}
    output = execute_program(program, registers)
    if output != program:
        print(f"Output {output}\ndoes not match program {program})")
        return
    print(f"Part 2: Register A is {a}")

args = parse_args("Advent of Code 2024 - Day 17", "problems/aoc2024-day17-input-test.txt")

lines = read_lines(args.input)
if args.testing:
    test1(args.verbose)
    exit()

program, registers = parse_program(lines)
t0 = time.time()
part1(program, registers)
t1 = time.time() - t0
t0 = time.time()
part2(program)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
