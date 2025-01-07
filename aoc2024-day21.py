"""
    https://adventofcode.com/2024/day/21

    --- Day 21: Keypad Conundrum ---
    As you teleport onto Santa's Reindeer-class starship, The Historians begin to panic: someone
    from their search party is missing. A quick life-form scan by the ship's computer reveals that
    when the missing Historian teleported, he arrived in another part of the ship.

    The door to that area is locked, but the computer can't open it; it can only be opened by
    physically typing the door codes (your puzzle input) on the numeric keypad on the door.

    The numeric keypad has four rows of buttons: 789, 456, 123, and finally an empty gap followed by
      0A. Visually, they are arranged like this:

    +---+---+---+
    | 7 | 8 | 9 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
        | 0 | A |
        +---+---+
    Unfortunately, the area outside the door is currently depressurized and nobody can go near the
    door. A robot needs to be sent instead.

    The robot has no problem navigating the ship and finding the numeric keypad, but it's not
    designed for button pushing: it can't be told to push a specific button directly. Instead, it
    has a robotic arm that can be controlled remotely via a directional keypad.

    The directional keypad has two rows of buttons: a gap / ^ (up) / A (activate) on the first row
    and < (left) / v (down) / > (right) on the second row. Visually, they are arranged like this:

        +---+---+
        | ^ | A |
    +---+---+---+
    | < | v | > |
    +---+---+---+
    When the robot arrives at the numeric keypad, its robotic arm is pointed at the A button in the
    bottom right corner. After that, this directional keypad remote control must be used to maneuver
    the robotic arm: the up / down / left / right buttons cause it to move its arm one button in
    that direction, and the A button causes the robot to briefly move forward, pressing the button
    being aimed at by the robotic arm.

    For example, to make the robot type 029A on the numeric keypad, one sequence of inputs on the
    directional keypad you could use is:

    < to move the arm from A (its initial position) to 0.
    A to push the 0 button.
    ^A to move the arm to the 2 button and push it.
    >^^A to move the arm to the 9 button and push it.
    vvvA to move the arm to the A button and push it.
    In total, there are three shortest possible sequences of button presses on this directional
    keypad that would cause the robot to type 029A: <A^A>^^AvvvA, <A^A^>^AvvvA, and <A^A^^>AvvvA.

    Unfortunately, the area containing this directional keypad remote control is currently
    experiencing high levels of radiation and nobody can go near it. A robot needs to be sent
    instead.

    When the robot arrives at the directional keypad, its robot arm is pointed at the A button in
    the upper right corner. After that, a second, different directional keypad remote control is
    used to control this robot (in the same way as the first robot, except that this one is typing
    on a directional keypad instead of a numeric keypad).

    There are multiple shortest possible sequences of directional keypad button presses that would
    cause this robot to tell the first robot to type 029A on the door. One such sequence is
    v<<A>>^A<A>AvA<^AA>A<vAAA>^A.

    Unfortunately, the area containing this second directional keypad remote control is currently
    -40 degrees! Another robot will need to be sent to type on that directional keypad, too.

    There are many shortest possible sequences of directional keypad button presses that would cause
    this robot to tell the second robot to tell the first robot to eventually type 029A on the door.
    One such sequence is <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A.

    Unfortunately, the area containing this third directional keypad remote control is currently
    full of Historians, so no robots can find a clear path there. Instead, you will have to type
    this sequence yourself.

    Were you to choose this sequence of button presses, here are all of the buttons that would be
    pressed on your directional keypad, the two robots' directional keypads, and the numeric keypad:

    <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
    v<<A>>^A<A>AvA<^AA>A<vAAA>^A
    <A^A>^^AvvvA
    029A
    In summary, there are the following keypads:

    One directional keypad that you are using.
    Two directional keypads that robots are using.
    One numeric keypad (on a door) that a robot is using.
    It is important to remember that these robots are not designed for button pushing. In
    particular, if a robot arm is ever aimed at a gap where no button is present on the keypad, even
    for an instant, the robot will panic unrecoverably. So, don't do that. All robots will initially
    aim at the keypad's A key, wherever it is.

    To unlock the door, five codes will need to be typed on its numeric keypad. For example:

    029A
    980A
    179A
    456A
    379A
    For each of these, here is a shortest sequence of button presses you could type to cause the
    desired code to be typed on the numeric keypad:

    029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
    980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
    179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
    456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
    379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
    The Historians are getting nervous; the ship computer doesn't remember whether the missing
    Historian is trapped in the area containing a giant electromagnet or molten lava. You'll need to
    make sure that for each of the five codes, you find the shortest sequence of button presses
    necessary.

    The complexity of a single code (like 029A) is equal to the result of multiplying these two
    values:

    The length of the shortest sequence of button presses you need to type on your directional
    keypad in order to cause the code to be typed on the numeric keypad; for 029A, this would be 68.
    The numeric part of the code (ignoring leading zeroes); for 029A, this would be 29.
    In the above example, complexity of the five codes can be found by calculating
    68 * 29, 60 * 980, 68 * 179, 64 * 456, and 64 * 379. Adding these together produces 126384.

    Find the fewest number of button presses you'll need to perform in order to cause the robot in
    front of the door to type each code. What is the sum of the complexities of the five codes on
    your list?

    --- Part Two ---
    Just as the missing Historian is released, The Historians realize that a second member of their
    search party has also been missing this entire time!

    A quick life-form scan reveals the Historian is also trapped in a locked area of the ship. Due
    to a variety of hazards, robots are once again dispatched, forming another chain of remote
    control keypads managing robotic-arm-wielding robots.

    This time, many more robots are involved. In summary, there are the following keypads:

    One directional keypad that you are using.
    25 directional keypads that robots are using.
    One numeric keypad (on a door) that a robot is using.
    The keypads form a chain, just like before: your directional keypad controls a robot which is
    typing on a directional keypad which controls a robot which is typing on a directional keypad...
    and so on, ending with the robot which is typing on the numeric keypad.

    The door codes are the same this time around; only the number of robots and directional keypads
    has changed.

    Find the fewest number of button presses you'll need to perform in order to cause the robot in
    front of the door to type each code. What is the sum of the complexities of the five codes on
    your list?
"""
import time
from typing import List, Dict
from common import parse_args, read_lines, number_, concat

class Coord:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

NUMBER_PAD = {
    "A": Coord(2, 0),
    "0": Coord(1, 0),
    "1": Coord(0, 1),
    "2": Coord(1, 1),
    "3": Coord(2, 1),
    "4": Coord(0, 2),
    "5": Coord(1, 2),
    "6": Coord(2, 2),
    "7": Coord(0, 3),
    "8": Coord(1, 3),
    "9": Coord(2, 3)
}

DIRECTION_PAD = {
    "A": Coord(2, 1),
    "^": Coord(1, 1),
    "<": Coord(0, 0),
    "v": Coord(1, 0),
    ">": Coord(2, 0)
}

def complexity_(line: str, num_presses: int) -> int:
    """Return the complexity of `line`."""
    return number_(line) * num_presses

def steps_(direction_presses: List[str]) -> List[List[str]]:
    """Returns the steps resulting from `direction_presses`."""
    steps = []
    current = []
    for char in direction_presses:
        current.append(char)
        if char == "A":
            steps.append(current)
            current = []
    return steps

def numeric_presses_(line: str, start: str) -> List[str]:
    """Returns the numeric presses resulting from `line`."""
    current = NUMBER_PAD[start]
    presses = []

    for char in line:
        dest = NUMBER_PAD[char]
        dx, dy = dest.x - current.x, dest.y - current.y

        horizontal = [">" if dx >= 0 else "<"] * abs(dx)
        vertical = ["^" if dy >= 0 else "v"] * abs(dy)

        if current.y == 0 and dest.x == 0:
            presses.extend(vertical)
            presses.extend(horizontal)
        elif current.x == 0 and dest.y == 0:
            presses.extend(horizontal)
            presses.extend(vertical)
        elif dx < 0:
            presses.extend(horizontal)
            presses.extend(vertical)
        else:
            presses.extend(vertical)
            presses.extend(horizontal)

        current = dest
        presses.append("A")

    return presses

def direction_presses_(numeric_presses: List[str], start: str) -> List[str]:
    """Returns the direction presses resulting from `numeric_presses`."""
    current = DIRECTION_PAD[start]
    direction_presses = []

    for char in numeric_presses:
        dest = DIRECTION_PAD[char]
        dx, dy = dest.x - current.x, dest.y - current.y

        horz = [">" if dx >= 0 else "<"] * abs(dx)
        vert = ["^" if dy >= 0 else "v"] * abs(dy)

        if current.x == 0 and dest.y == 1:
            direction_presses.extend(horz)
            direction_presses.extend(vert)
        elif current.y == 1 and dest.x == 0:
            direction_presses.extend(vert)
            direction_presses.extend(horz)
        elif dx < 0:
            direction_presses.extend(horz)
            direction_presses.extend(vert)
        else:
            direction_presses.extend(vert)
            direction_presses.extend(horz)

        current = dest
        direction_presses.append("A")

    return direction_presses

def num_presses_after_robot(numeric_presses: List[str],
                           num_robots: int, robot: int,
                           cache: Dict[str, List[int]]) -> int:
    """Returns the number of presses after the `robot` robot."""
    key = concat(numeric_presses)
    if key in cache and cache[key][robot - 1] != 0: return cache[key][robot - 1]

    cache.setdefault(key, [0] * num_robots)
    direction_presses = direction_presses_(numeric_presses, "A")
    cache[key][0] = len(direction_presses)

    if robot == num_robots: return len(direction_presses)

    steps = steps_(direction_presses)
    count = 0
    for step in steps:
        cnt = num_presses_after_robot(step, num_robots, robot + 1, cache)
        step_key = concat(step)
        cache.setdefault(step_key, [0] * num_robots)
        cache[step_key][0] = cnt
        count += cnt

    cache[key][robot - 1] = count
    return count

def total_complexity_(lines: List[str], num_robots: int) -> int:
    """Returns the total complexity of `lines`."""
    total_complexity = 0
    cache = {}
    for line in lines:
        presses = numeric_presses_(line, "A")
        num_presses = num_presses_after_robot(presses, num_robots, 1, cache)
        total_complexity += complexity_(line, num_presses)
    return total_complexity

def part1(lines):
    "Solution to part 1. (176650)"
    total_complexity = total_complexity_(lines, 2)
    print(f"Part 1: Total complexity {total_complexity}")

def part2(lines):
    "Solution to part 2. (217698355426872)"
    total_complexity = total_complexity_(lines, 25)
    print(f"Part 2: Total complexity {total_complexity}")

args = parse_args("Advent of Code 2024 - Day 21", "problems/aoc2024-day21-input.txt")

lines = read_lines(args.input)

t0 = time.time()
part1(lines)
t1 = time.time() - t0
t0 = time.time()
part2(lines)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
