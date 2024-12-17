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

    The first example requires a few more steps:

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
from common import parse_args, read_text

def numbers_(text):
    "Extracts the digits in `text` and returns them as a list of integers."
    return [int(c) for c in text if c.isdigit()]

def blocks_(numbers):
    """
    Unpacks a list of numbers into a list of blocks, where each block is either a file ID or a
    free space indicator.
    `numbers` is a list of integers where even-indexed elements represent the number of times to
    repeat the file ID (calculated as the index divided by 2), and odd-indexed elements represent
    the number of times to repeat the free space indicator (-1).

    Returns: A list of integers where each integer is either a file ID or -1 indicating free space.
    """
    blocks = []
    for i, v in enumerate(numbers):
        if i % 2 == 0:
            for _ in range(v):
                blocks.append(i//2) # file_id
        else:
            for _ in range(v):
                blocks.append(-1) # free space
    return blocks

def show(blocks):
    """
    Converts a list of blocks into a string representation. If a block has a value of -1, it is
    represented as a dot ('.'). Otherwise, the block value is converted to a string.
    """
    return "".join(str(b) if b != -1 else "." for b in blocks)

def checksum_(blocks):
    "Calculate the checksum of the blocks."
    return sum(i * v for i, v in enumerate(blocks) if v != -1)

def clusters_gaps(blocks):
    """
    Analyzes a list of blocks and separates them into clusters and gaps.

    A cluster is a sequence of consecutive blocks with the same value (except -1).
    A gap is a sequence of consecutive blocks with the value -1.

    Args:
        blocks (list): A list of integers representing blocks.

    Returns:
        tuple: A tuple containing two lists:
            - clusters (list of lists): Each inner list represents a cluster with the format [(length, value)].
            - gaps (list): Each element represents the length of a gap.
    """
    # print(f"cluster_gaps {show(blocks)}")
    clusters, gaps = [], []

    def add(n, v):
        if v == -1: gaps.append(n)
        else: clusters.append([(n,v)])

    n, v0 = 1, blocks[0]
    for v in blocks[1:]:
        changed = v != v0
        # print(f"v: {v:2}, in_gap: {v0 == -1}, n: {n}, v0: {v0} -> {changed}")
        if changed:
            add(n, v0)
            n, v0 = 1, v
        else:
            n += 1
    if n > 0:
        add(n, v0)

    return clusters, gaps

def add_cluster(clusters, gaps, i, c):
    """
    Inserts cluster `c` into `gaps`[`i`] and updates the `clusters` and `gaps` lists.

    Parameters:
    clusters (list of lists): A list where each element is a list of clusters.
    gaps (list of int): A list of gap sizes.
    i (int): The index of the gap where the cluster should be inserted.
    c (tuple): The cluster to be inserted, represented as a tuple (n, _), where `n` is the size of the cluster.

    Raises:
    AssertionError: If the size of the cluster `n` is greater than the gap size at index `i`.

    Modifies:
    The function modifies the `clusters` and `gaps` lists in place by adding the cluster `c` to `clusters[i]` and reducing `gaps[i]` by the size of the cluster `n`.
    """
    "insert cluster `c` in `gaps`[`i`]"
    n, _ = c
    assert n <= gaps[i], (n, gaps[i])
    gaps[i] -= n
    clusters[i].append(c)

def unpack_clusters(clusters, gaps):
    "Unpack the clusters and gaps into a list of blocks."
    blocks = []
    for i, c in enumerate(clusters):
        for m, v in c:
            for _ in range(m):
                blocks.append(v)
        if i < len(gaps):
            for _ in range(gaps[i]):
                blocks.append(-1)
    return blocks

def part1(blocks):
    "Solution to part 1. 1928 for the test input."
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

    print(f"{len(blocks)} blocks")
    print(f"Part 1: {checksum}")

def part2(blocks):
    "Solution to part 2. 2858 for the test input.  6182186920537"

    clusters, gaps = clusters_gaps(blocks)
    # print(f"clusters: {clusters}")
    # print(f"gaps: {gaps}")

    n = len(clusters) - 1
    while n >= 0:
        # print(f"{n:4}: {show(unpack_clusters(clusters, gaps))}")
        clist = clusters[n]
        removed = []
        for j, c in enumerate(clist):
            for i, g in enumerate(gaps[:n]):
                if g >= c[0]:
                    add_cluster(clusters, gaps, i, c)
                    removed.append(j)
                    break
        clist = [(m, -1 if j in removed else v) for j, (m,v) in enumerate(clist)]
        clusters[n] = clist
        n -= 1

    blocks = unpack_clusters(clusters, gaps)
    checksum = checksum_(blocks)


    print(f"Part 2: {checksum}")

args = parse_args("Advent of Code 2024 - Day 9", "aoc2024-day9-input-test.txt")
text = read_text(args.input)
# text = "12345"
numbers = numbers_(text)
print(f"{len(numbers)} numbers")
# print(f"numbers: {numbers}")
# assert False, numbers
blocks = blocks_(numbers)

print(f"{len(blocks)} blocks")
# print(f"blocks: {show(blocks)}")
t0 = time.time()
part1(blocks)
t1 = time.time() - t0
blocks = blocks_(numbers)
t0 = time.time()
part2(blocks)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
