"""
    https://adventofcode.com/2024/day/9


    The disk map uses a dense format to represent the layout of files and free space on the disk.
    The digits alternate between indicating the length of a file and the length of free space.

    So, a disk map like 12345 would represent a one-block file, two blocks of free space, a
    three-block file, four blocks of free space, and then a five-block file. A disk map like 90909
    would represent three nine-block files in a row (with no free space between them).

    Each file on disk also has an ID number based on the order of the files as they appear before
    they are rearranged, starting with ID 0. So, the disk map 12345 has three files: a one-block
    file with ID 0, a three-block file with ID 1, and a five-block file with ID 2. Using one
    character for each block where digits are the file ID and . is free space, the disk map 12345
    represents these individual blocks:

    0..111....22222

    Part 1:
    ------
    The amphipod would like to move file blocks one at a time from the end of the disk to the
    leftmost free space block (until there are no gaps remaining between file blocks). For the disk
    map 12345, the process looks like this:

    0..111....22222
    02.111....2222.
    022111....222..
    0221112...22...
    02211122..2....
    022111222.....

    The first example (2333133121414131402) requires a few more steps:


    00...111...2...333.44.5555.6666.777.888899
    009..111...2...333.44.5555.6666.777.88889.
    0099.111...2...333.44.5555.6666.777.8888..
    00998111...2...333.44.5555.6666.777.888...
    009981118..2...333.44.5555.6666.777.88....
    0099811188.2...333.44.5555.6666.777.8.....
    009981118882...333.44.5555.6666.777.......
    0099811188827..333.44.5555.6666.77........
    00998111888277.333.44.5555.6666.7.........
    009981118882777333.44.5555.6666...........
    009981118882777333644.5555.666............
    00998111888277733364465555.66.............
    0099811188827773336446555566..............
    The final step of this file-compacting process is to update the filesystem checksum. To
    calculate the checksum, add up the result of multiplying each of these blocks' position with the
    file ID number it contains. The leftmost block is in position 0. If a block contains free space,
    skip it instead.

    Continuing the first example, the first few blocks' position multiplied by its file ID number
    are 0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 = 32, and so on. In this example, the
    checksum is the sum of these, 1928.

    Compact the amphipod's hard drive using the process he requested. What is the resulting
    filesystem checksum?

    Part 2:
    ------
    This time, attempt to move whole files to the leftmost span of free space blocks that could fit
    the file. Attempt to move each file exactly once in order of decreasing file ID number starting
    with the file with the highest file ID number. If there is no span of free space to the left of
    a file that is large enough to fit the file, the file does not move.

"""
import time
from common import parse_args, read_text, MyNamespace as ns

DEBUG = False
VERBOSE = False
SHOW_PROGRESS = False

def numbers_(text):
    "Extracts the digits in `text` and returns them as a list of integers."
    return [int(c) for c in text if c.isdigit()]

def blocks_(numbers):
    """
    Returns `numbers` as a list of blocks, where each block is either a file ID (>= 0) or a
    free space indicator (-1).
    `numbers` is a list of integers where even-indexed elements represent the number of times to
    repeat the file ID (calculated as the index divided by 2), and odd-indexed elements represent
    the number of times to repeat the free space indicator (-1).
    """
    blocks = []
    for i, v in enumerate(numbers):
        file_id = i // 2 if i % 2 == 0 else -1
        for _ in range(v): blocks.append(file_id)
    return blocks

def cluster_(n, v):
    "Create a cluster object with `n` blocks of value `v`."
    return ns(n=n, v=v)

def run_(clist, gap):
    "Create a run object with a list of clusters and a gap."
    return ns(clist=clist.copy(), gap=gap)

def run_len(run):
    "Return the length of a run."
    return sum(c.n for c in run.clist) + run.gap

def show(blocks):
    """
    Return a string representation of `blocks`, a list of blocks. If a block has a value of -1, it's
    represented as a dot ('.'). Otherwise, the block value is converted to a string.
    """
    return "".join(str(b) if b != -1 else "." for b in blocks)

def checksum_(blocks):
    "Calculate and return the checksum of `blocks`."
    return sum(i * v for i, v in enumerate(blocks) if v != -1)

def run_list_(blocks):
    """
    Scans `blocks`, a list of blocks returns them as a list of runs.
   """
    run_list = []
    clist = []
    gap_g = [0]

    def add_run(n, v, last=False):
        "Add a run of n blocks with value v to the clusters or gaps list."
        gap = gap_g[0]
        if v != -1: clist.append(cluster_(n, v))
        else: gap = n
        if v == -1 or last:
            run = run_(clist, gap)
            run_list.append(run)
            clist.clear()
            gap = 0
        gap_g[0] = gap

    n, v0 = 1, blocks[0]
    for i, v in enumerate(blocks[1:]):
        if VERBOSE:
            print(f"{i+1:4}: {v:2}, in_gap: {v0 == -1}, n: {n}, v0: {v0} [{clist},{gap_g[0]}]", end="")
        if v != v0:
            add_run(n, v0)
            n, v0 = 1, v
            if VERBOSE: print(f" -> {run_list}")
        else:
            n += 1
            if VERBOSE: print("")
    if n > 0:
        add_run(n, v0, True)

    return run_list

class RunEncoding:
    """
    RunEncoding class for processing and manipulating run-length encoded blocks.

    Attributes:
        run_list (list): A list of runs representing clusters and gaps in the blocks.
   """
    def __init__(self, blocks):
        """
        Initializes self.run_list with a list of blocks
        """
        if VERBOSE:
            print(f"RunList:- {show(blocks)}")
        run_list = run_list_(blocks)
        self.run_list = run_list
        blocks2 = self.blocks_()
        if VERBOSE:
            print(f"run_list: {run_list}")
            print(f"RunList:- {show(blocks)}")
            print(f"RunList:+ {show(blocks2)}")
        assert len(blocks) == len(blocks2), (len(blocks), len(blocks2))
        for i, (b1, b2) in enumerate(zip(blocks, blocks2)):
            assert b1 == b2, (i, [b1, b2])

    def __str__(self):
        return show(self.blocks_())

    def blocks_(self):
        "Unpack the runs into a list of blocks."
        blocks = []
        for run in self.run_list:
            for c in run.clist:
                for _ in range(c.n):
                    blocks.append(c.v)
            for _ in range(run.gap):
                blocks.append(-1)
        return blocks

    def insert_cluster(self, i, c):
        """
        Inserts cluster `c` into `self.run_list`[`i`] and updates the `clusters` and `gaps` lists.

        Parameters:
        i: The index of the run where the cluster should be inserted.
        c: The cluster to be inserted.

        Modifies:
        The function modifies the `self.run_list`[`i`] run by adding the cluster `c` to its clist
        and reducing the gap by `c.n`.
        """
        run = self.run_list[i]
        run0 = run_(run.clist.copy(), run.gap)
        assert c.n <= run.gap, (c.n, run.gap)
        run.gap -= c.n
        run.clist.append(c)
        len0 = run_len(run0)
        len1 = run_len(run)
        assert len1 == len0, ((len0,run0), (len1, run))
        self.run_list[i] = run

    def defragment_run(self, n):
        """
        Defragments the run at index `n` by attempting to insert its clusters into previous runs
        if there is enough gap to accommodate them. Updates the cluster list of the run at index `n`
        by marking the moved clusters.
        """
        run0 = self.run_list[n]
        removed = []
        for j, c in enumerate(reversed(run0.clist)):
            for i, run in enumerate(self.run_list[:n]):
                if run.gap >= c.n:
                    self.insert_cluster(i, c)
                    removed.append(len(run0.clist) - 1- j)
                    break
        run0.clist = [cluster_(c.n, -1) if j in removed else c for j, c in enumerate(run0.clist)]
        self.run_list[n] = run0
        assert isinstance(self.run_list[0], ns), type(self.run_list[0])

def part1(blocks):
    "Solution to part 1. 1928 for the test input. 6258319840548"
    i, n = 0, len(blocks) - 1
    # print(show(blocks))
    while i < n:
        if blocks[i] != -1:
            i += 1
            continue
        if blocks[n] == -1:
            n -= 1
            continue
        blocks[i], blocks[n] = blocks[n], -1
        i += 1
        n -= 1
        # print(show(blocks))

    checksum = checksum_(blocks)

    if VERBOSE:
        rint(f"{len(blocks)} blocks")
    print(f"Part 1: {checksum}")

def part2(blocks):
    "Solution to part 2. 2858 for the test input. 6286182965311"
    renc = RunEncoding(blocks)

    if SHOW_PROGRESS:
        print(f"RunEncoding:- {len(renc.run_list)} runs")
        state0 = str(renc)
        state00 = state0
        print(f"RunList:- {state00}")
        for i, run in enumerate(renc.run_list):
            print(f"{i:4}: {run_len(run):2} {run.clist} {run.gap:2}")
    for n in range(len(renc.run_list) - 1, -1, -1):
        renc.defragment_run(n)
        if SHOW_PROGRESS:
            state = str(renc)
            if state != state0:
                state0 = state
                print(f"RunList:{n} {state}")
                for i, run in enumerate(renc.run_list):
                    print(f"{i:4}: {run_len(run):2} {run.clist} {run.gap:2}")

    if SHOW_PROGRESS:
        print(f"RunList:- {state00}")
    blocks = renc.blocks_()
    checksum = checksum_(blocks)
    print(f"Part 2: {checksum}")

args = parse_args("Advent of Code 2024 - Day 9", "problems/aoc2024-day9-input-test.txt")
text = read_text(args.input)
numbers = numbers_(text)
blocks = blocks_(numbers)

if DEBUG:
    blocks = blocks[:100]

if VERBOSE:
    print(f"{len(numbers)} numbers")
    print(f"{len(blocks)} blocks")

t0 = time.time()
part1(blocks.copy())
t1 = time.time() - t0
t0 = time.time()
part2(blocks)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
