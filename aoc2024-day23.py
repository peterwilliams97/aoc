"""
    https://adventofcode.com/2024/day/23

    --- Day 23: LAN Party ---
    As The Historians wander around a secure area at Easter Bunny HQ, you come across posters for a
    LAN party scheduled for today! Maybe you can find it; you connect to a nearby datalink port and
    download a map of the local network (your puzzle input).

    The network map provides a list of every connection between two computers. For example:

    kh-tc
    qp-kh
    de-cg
    ka-co
    yn-aq
    qp-ub
    cg-tb
    vc-aq
    tb-ka
    wh-tc
    yn-cg
    kh-ub
    ta-co
    de-co
    tc-td
    tb-wq
    wh-td
    ta-ka
    td-qp
    aq-cg
    wq-ub
    ub-vc
    de-ta
    wq-aq
    wq-vc
    wh-yn
    ka-de
    kh-ta
    co-tc
    wh-qp
    tb-vc
    td-yn
    Each line of text in the network map represents a single connection; the line kh-tc represents a
    connection between the computer named kh and the computer named tc. Connections aren't
    directional; tc-kh would mean exactly the same thing.

    LAN parties typically involve multiplayer games, so maybe you can locate it by finding groups of
    connected computers. Start by looking for sets of three computers where each computer in the set
    is connected to the other two computers.

    In this example, there are 12 such sets of three inter-connected computers:

    aq,cg,yn
    aq,vc,wq
    co,de,ka
    co,de,ta
    co,ka,ta
    de,ka,ta
    kh,qp,ub
    qp,td,wh
    tb,vc,wq
    tc,td,wh
    td,wh,yn
    ub,vc,wq
    If the Chief Historian is here, and he's at the LAN party, it would be best to know that right
    away. You're pretty sure his computer's name starts with t, so consider only sets of three
    computers where at least one computer's name starts with t. That narrows the list down to 7 sets
    of three inter-connected computers:

    co,de,ta
    co,ka,ta
    de,ka,ta
    qp,td,wh
    tb,vc,wq
    tc,td,wh
    td,wh,yn
    Find all the sets of three inter-connected computers. How many contain at least one computer
    with a name that starts with t?

    Your puzzle answer was 1000.

    The first half of this puzzle is complete! It provides one gold star: *

    --- Part Two ---
    There are still way too many results to go through them all. You'll have to find the LAN party
    another way and go there yourself.

    Since it doesn't seem like any employees are around, you figure they must all be at the LAN
    party. If that's true, the LAN party will be the largest set of computers that are all connected
    to each other. That is, for each computer at the LAN party, that computer will have a connection
    to every other computer at the LAN party.

    In the above example, the largest set of computers that are all connected to each other is made
    up of co, de, ka, and ta. Each computer in this set has a connection to every other computer in
    the set:

    ka-co
    ta-co
    de-co
    ta-ka
    de-ta
    ka-de
    The LAN party posters say that the password to get into the LAN party is the name of every
    computer at the LAN party, sorted alphabetically, then joined together with commas. (The people
    running the LAN party are clearly a bunch of nerds.) In this example, the password would be co,de,ka,ta.

    What is the password to get into the LAN party?

"""
import time
from collections import defaultdict
from typing import List, Dict, Set, Tuple
from common import read_lines, parse_args

def graph_(lines: List[str]) -> Dict[str, Set[str]]:
    "Return an adjacency list of connected computers."
    graph = defaultdict(set)
    for line in lines:
        key1, key2 = line.split('-')
        graph[key1].add(key2)
        graph[key2].add(key1)
    return graph

def triplets_(graph: Dict[str, Set[str]]) -> Set[Tuple[str, str, str]]:
    "Return the set of triplets of connected computers"
    triplets = set()
    for key1, adjacents in graph.items():
        if len(adjacents) < 2: continue
        for key2 in adjacents:
            for key3 in adjacents:
                if key2 == key3: continue
                if key3 in graph[key2]:
                    triplets.add(tuple(sorted([key1, key2, key3])))
    return triplets

def num_t_triplets_(triplets: Set[Tuple[str, str, str]]) -> int:
    "Return the number of triplets that contain a computer starting with 't'"
    return sum(1 for trip in triplets if any(key.startswith('t') for key in trip))

def bron_kerbosch(R: Set[str],
                  P: Set[str],
                  X: Set[str],
                  graph: Dict[str, Set[str]],
                  cliques: List[Set[str]]) -> None:
    """
    Bron-Kerbosch algorithm to find all maximal cliques in an undirected graph.

    Parameters:
    - R: Set of vertices in the current clique.
    - P: Set of vertices that are candidates to be added to the clique.
    - X: Set of vertices that are already processed and should not be added.
    - graph: Dictionary representation of the adjacency list of the graph.
    - cliques: List to store all maximal cliques.
    """
    if not P and not X:
        cliques.append(R)
        return

    for v in list(P):
        bron_kerbosch(R.union({v}), P.intersection(graph[v]), X.intersection(graph[v]), graph, cliques)
        P.remove(v)
        X.add(v)
    return cliques

def max_clique_(graph: Dict[str, Set[str]]) -> List[str]:
    "Return the largest clique in the graph."
    all_computers = set(graph.keys())
    cliques = bron_kerbosch(set(), all_computers, set(), graph, [])
    return max(cliques, key=len)

def part1(lines):
    "Solution to part 1. (1000)"
    num_t_triplets = num_t_triplets_(triplets_(graph))
    print(f"Part 1: number of triplets starting with t is {num_t_triplets}")

def part2(grid):
    "Solution to part 2. (cf,ct,cv,cz,fi,lq,my,pa,sl,tt,vw,wz,yd)"
    max_clique = max_clique_(graph)
    print(f"Part 2: Max clique is {",".join(sorted(max_clique))}")

args = parse_args("Advent of Code 2024 - Day 23", "problems/aoc2024-day23-input.txt")

lines = read_lines(args.input)
graph = graph_(lines)

t0 = time.time()
part1(graph)

t1 = time.time() - t0
t0 = time.time()
part2(graph)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
