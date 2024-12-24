"""
    https://adventofcode.com/2024/day/12

    Each garden plot grows only a single type of plant and is indicated by a single letter on your
    map. When multiple garden plots are growing the same type of plant and are touching
    (horizontally or vertically), they form a region. For example:

    AAAA
    BBCD
    BBCC
    EEEC
    This 4x4 arrangement includes garden plots growing five different types of plants
    (labeled A, B, C, D, and E), each grouped into their own region.

    In order to accurately calculate the cost of the fence around a single region, you need to know
    that region's area and perimeter.

    The area of a region is simply the number of garden plots the region contains. The above map's
    type A, B, and C plants are each in a region of area 4. The type E plants are in a region of
    area 3; the type D plants are in a region of area 1.

    Each garden plot is a square and so has four sides. The perimeter of a region is the number of
    sides of garden plots in the region that do not touch another garden plot in the same region.
    The type A and C plants are each in a region with perimeter 10. The type B and E plants are each
    in a region with perimeter 8. The lone D plot forms its own region with perimeter 4.

    Visually indicating the sides of plots in each region that contribute to the perimeter using
    - and |, the above map's regions' perimeters are measured as follows:

    +-+-+-+-+
    |A A A A|
    +-+-+-+-+   +-+
                |D|
    +-+-+   +-+ +-+
    |B B|   |C|
    +   +   + +-+
    |B B|   |C C|
    +-+-+   +-+ +
            |C|
    +-+-+-+ +-+
    |E E E|
    +-+-+-+

    Part 1:

    The price of fence required for a region is found by multiplying that region's area by its
    perimeter. The total price of fencing all regions on a map is found by adding together the price
    of fence for every region on the map.

    Part 2:

    Under the bulk discount, instead of using the perimeter to calculate the price, you need to use
    the number of sides each region has. Each straight section of fence counts as a side, regardless
    of how long it is.

    Consider this example again:

    AAAA
    BBCD
    BBCC
    EEEC
    The region containing type A plants has 4 sides, as does each of the regions containing plants
    of type B, D, and E. However, the more complex region containing the plants of type C has 8
    sides!
"""
import time, sys
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from common import parse_args, read_rows

VERBOSE = False

np.set_printoptions(linewidth=10_000, threshold=144 * 144 * 25)

def rows_to_img(rows):
    """Convert a `rows`, a list of strings, to a 2D numpy array.
        Return `img`, `r2i` where
        - img is the image as a 2D numpy array where each pixel is an integer.
        - r2i is a dictionary mapping characters in `rows` to the corresponding numbers in `img`.
    """
    h, w = len(rows), len(rows[0])
    img = np.zeros((h, w), dtype=int)
    r2i = {}
    n_types = 0
    for y in range(h):
        for x in range(w):
            c = rows[y][x]
            if c not in r2i:
                n_types += 1
                r2i[c] = n_types
            img[y, x] = r2i[c]
    return img, r2i

IMAGE_DIR = "images-day12"
os.makedirs(IMAGE_DIR, exist_ok=True)

def csv_name_(counter, base): return os.path.join(IMAGE_DIR, f"{base}{counter:03d}.csv")
def img_name_(counter, base): return os.path.join(IMAGE_DIR, f"{base}{counter:03d}.png")

def expand_img(img, min_size):
    "Expand `img` to `min_size` x `min_size` ."
    h, w = img.shape
    if h >= min_size and w >= min_size:
        return img
    n = max(min_size // h, min_size // w)
    expanded = np.repeat(img, n, axis=0)
    expanded = np.repeat(expanded, n, axis=1)
    return expanded

# The following code is setting up tiles for visualizing an image with gaps and sides.

T = 5              # Tile size
U = T // 2         # Left or top border of mark in border tiles
V = T + 1 - U      # Bottom or right border of mark in border tiles
IMAGE_TILE = np.ones((T, T), dtype=int)     # A full tile for input image
VBORD_TILE = np.zeros((T, T), dtype=int)    # A vertical border tile
HBORD_TILE = np.zeros((T, T), dtype=int)    # A horizontal border tile
VBORD_TILE[:, U::V] = 1
HBORD_TILE[U::V, :] = 1

def compose_img(img, vbords, hbords):
    """Draw an image of `img` and the vertical and horizontal borders `vbords` and `hbords`.
    img, vbords and hbords are 2D numpy arrays. All have been computed and they are the same size.
    vbords[x, y] is True if there is a vertical side between img[x, y] and [x+1, y].
    hbords[x, y] is True if there is a horizontal side between img[x, y] and [x, y+1].
    Draws `img` with full `T`x`T` tiles, and vbords and hbords with 1x`T` tiles.
    """
    h, w = img.shape
    assert vbords.shape == (h, w), f"vsides={vbords.shape} img={img.shape}"
    assert hbords.shape == (h, w), f"hsides={hbords.shape} img={img.shape}"

    def gap(v): return 2 * v +1

    H, W = gap(T * h), gap(T * w)
    composite = np.zeros((H, W), dtype=int)

    def draw_tile(yy, xx, tile): composite[T*yy:T*yy+T, T*xx:T*xx+T] = tile

    for y in range(h):
        for x in range(w):
            if img[y, x]:    draw_tile(gap(y),      gap(x),     IMAGE_TILE)
            if vbords[y, x]: draw_tile(gap(y),      gap(x) + 1, VBORD_TILE)
            if hbords[y, x]: draw_tile( gap(y) + 1, gap(x),     HBORD_TILE)
    return composite

def draw_img_with_gaps(counter, img, vbords, hbords, base):
    "Draw image with gaps between pixels. For debugging."
    np.savetxt(csv_name_(counter, base), img, delimiter=",", fmt="%d")

    gapped = compose_img(img, vbords, hbords)
    y_max = np.amax(gapped, axis=1)
    x_max = np.amax(gapped, axis=0)
    y0, y1 = np.nonzero(y_max)[0][[0, -1]]
    x0, x1 = np.nonzero(x_max)[0][[0, -1]]

    img_name = img_name_(counter, base)
    inverse = 1 - gapped
    trimmed = inverse[y0:y1+1, x0:x1+1]
    hh, ww = trimmed.shape
    assert hh == y1 - y0 + 1, f"hh={hh} y1={y1} y0={y0}"
    assert ww == x1 - x0 + 1, f"ww={ww} x1={x1} x0={x0}"
    trimmed = expand_img(trimmed, 600)
    try:
        plt.imsave(img_name, trimmed, cmap='gray', format='png')
    except Exception as e:
        print(f"Error saving {img_name}: inverse={inverse} trimmed={trimmed.shape}", file=sys.stderr)
        raise
    return img_name

def connected_components_(img):
    """
    Identify and label connected components in `img`, a 2D image.
    Returns: `connected_components`, `o2i`
        - connected_components: A list of 2D numpy arrays, for each  connected component in `img`.
        - o2i {o: i}: `o` of a connected component to the original
    """
    w, h = img.shape
    unique = sorted(np.unique(img))
    if len(unique) == 1:
        return [img], {0: 0}

    connected_components, o2i  = [], {}
    for u in unique:
        cpt = np.zeros((h, w), dtype=int)
        cpt[img == u] = 1
        labeled, n = ndimage.label(cpt)
        for i in range(1, n+1):
            conn = np.zeros((h, w), dtype=int)
            conn[labeled == i] = 1
            connected_components.append(conn)
            o2i[len(connected_components)-1] = u
    return connected_components, o2i

VERT_LEFT, VERT_RIGHT, HORZ_TOP, HORZ_BOTTOM = 1, 2, 4, 8

def vert_horz_(img, y, x):
    """Return (vert_left, vert_right), (horz_top, horz_bottom) where
        - `vert_left`  is True if there is a vertical    edge between (y, x) and (y, x+1) and img[y, x] is 0
        - `vert_right` is True if there is a vertical    edge between (y, x) and (y, x+1) and img[y, x+1] is 0
        - `horz_top`    is True if there is a horizontal edge between (y, x) and (y+1, x) and img[y, x] is 0
        - `horz_bottom` is True if there is a horizontal edge between (y, x) and (y+1, x) and img[y+1, x] is 0
        Theses are the edges that are not shared with another pixel in the connected component.
    """
    vert_left = img[y, x] == 0 and img[y, x+1] != 0
    vert_right = img[y, x] != 0 and img[y, x+1] == 0
    horz_top = img[y, x] == 0 and img[y+1, x] != 0
    horz_bottom = img[y, x] != 0 and img[y+1, x] == 0
    return (vert_left, vert_right), (horz_top, horz_bottom)

def num_edges(img, y, x):
    "Return the number of edges at pixel (y, x) in `img`."
    (vert_left, vert_right), (horz_top, horz_bottom) = vert_horz_(img, y, x)
    vert = vert_left + vert_right
    horz = horz_top + horz_bottom
    return int(vert) + int(horz)

def vh_(img, y, x):
    "Return vert_horz_(img, y, x) as a bit mask."
    (vert_left, vert_right), (horz_top, horz_bottom) = vert_horz_(img, y, x)
    return vert_left * VERT_LEFT + vert_right * VERT_RIGHT + horz_top * HORZ_TOP + horz_bottom * HORZ_BOTTOM

def edge_count_(img):
    """Return an image `edge_count` where edge_count[y,x] is the number of non-zero neigbours of
        pixel (y, x) in `img` offset by (2,2).
    """
    # Pad the image with zeros so we don't have to check for edge conditions.
    img = np.pad(img, 2, mode='constant', constant_values=0)

    h,w = img.shape
    edge_count = np.zeros((h, w), dtype=int)
    for y in range(1, h-1):
        for x in range(1,w-1):
            edge_count[y, x] = num_edges(img, y, x)
    return edge_count

def edge_counts_(connected_components):
    "Return the edge count for each connected component."
    return [edge_count_(cpt) for cpt in connected_components]

def num_sides_(counter, img, verbose=False):
    """Return the number of sides in the connected component `img`.
        A side is a straight line of pixels that is not shared with another pixel in the connected
        component.
    """
    # Pad the image with zeros so we don't have to check for edge conditions.
    img = np.pad(img, 2, mode='constant', constant_values=0)

    h,w = img.shape
    # vertical edges for row y are between img[y, x] and img[y, x+1]
    # horizontal edges for column x are between img[y, x] and img[y+1, x]
    edge = np.zeros((h, w), dtype=int)
    for y in range(0, h-1):
        for x in range(0, w-1):
            edge[y, x] = vh_(img, y, x)
    num_sides = 0
    if verbose:
        print(f"num_sides_ counter={counter} {img.shape}")
    vsides = np.zeros((h, w), dtype=int)
    hsides = np.zeros((h, w), dtype=int)

    if verbose:
        vedges = np.zeros((h, w), dtype=int)
        hedges = np.zeros((h, w), dtype=int)
        for y in range(1, h-1):
            for x in range(1,w-1):
                if edge[y, x] & VERT_LEFT:   vedges[y, x] = 1
                if edge[y, x] & VERT_RIGHT:  vedges[y, x] = 1
                if edge[y, x] & HORZ_TOP :   hedges[y, x] = 1
                if edge[y, x] & HORZ_BOTTOM: hedges[y, x] = 1
        draw_img_with_gaps(counter, img, vedges, hedges, "edges")

        y0, x0 = h, w
        y1, x1 = 0, 0
        for y in range(1, h-1):
            for x in range(1,w-1):
                if edge[y, x]:
                    y0, y1 = min(y0, y), max(y1, y)
                    x0, x1 = min(x0, x), max(x1, x)

    last_y = None
    for y in range(h):
        for x in range(w):
            vh = edge[y, x]
            vert_left = vh & VERT_LEFT
            vert_right = vh & VERT_RIGHT
            horz_top = vh & HORZ_TOP
            horz_bottom = vh & HORZ_BOTTOM

            if vert_left:
                num_sides += 1
                vsides[y, x] = 1
                for dy in range(h):
                    if edge[y+dy, x] & VERT_LEFT == 0: break
                    edge[y+dy, x] &= ~VERT_LEFT
            if vert_right:
                num_sides += 1
                vsides[y, x] = 1
                for dy in range(h):
                    if edge[y+dy, x] & VERT_RIGHT == 0: break
                    edge[y+dy,x] &= ~VERT_RIGHT
            if horz_top:
                num_sides += 1
                hsides[y, x] = 1
                for dx in range(w):
                    if edge[y, x+dx] & HORZ_TOP == 0: break
                    edge[y, x+dx] &= ~HORZ_TOP
            if horz_bottom:
                num_sides += 1
                hsides[y, x] = 1
                for dx in range(w):
                    if edge[y, x+dx] & HORZ_BOTTOM == 0: break
                    edge[y, x+dx] &= ~HORZ_BOTTOM

            if verbose:
                if vh:
                    if last_y is not None and last_y != y: print()
                    v_s0 = "V0" if vert_left else " "
                    v_s1 = "V1" if vert_right else " "
                    h_s0 = "H0" if horz_top else " "
                    h_s1 = "H1" if horz_bottom else " "
                    print(f"y={y-y0:2} x={x-x0:2} | {v_s0} {v_s1} {h_s0} {h_s1} | sides={num_sides}")
                    last_y = y

    if verbose:
        print(f"{draw_img_with_gaps(counter, img, vsides, hsides, "sides")} num_sides={num_sides}")
    return num_sides

def sides_(connected_components):
    "Return the number of sides for each connected component."
    sides = [num_sides_(i, cpt, VERBOSE) for i, cpt in enumerate(connected_components)]
    return sides

def part1(img):
    "Solution to part 1. 1930 for the test input. (1431440)"
    connected_components, _ = connected_components_(img)
    if VERBOSE:
        print(f"connected_components={len(connected_components)}")
        for i, cpt in enumerate(connected_components):
            print(f"Component {i+1}: {np.sum(cpt)}")
            print(f"{cpt}")

    edges = edge_counts_(connected_components)

    area_perimeter = []
    for i, (cpt, edge) in enumerate(zip(connected_components, edges)):
        area = int((cpt == 1).sum())
        perimeter = int(edge.sum())
        area_perimeter.append((area, perimeter))

    if VERBOSE:
        for i, (area, perimeter) in enumerate(area_perimeter):
            print(f"{i+1:4}: {area} x {perimeter} = {area*perimeter}")
        print(f"Total: {sum(area*perimeter for area, perimeter in area_perimeter)}")

    print(f"Part 1: {sum(area*perimeter for area, perimeter in area_perimeter)}", flush=True)

def part2(img):
    "Solution to part 2. 1206 for the test input. (869070)"
    connected_components, o2i = connected_components_(img)
    if VERBOSE:
        print(f"connected_components={len(connected_components)}")
        for o, cpt in enumerate(connected_components):
            print(f"Component {o+1}:\n{cpt}")

    sides = sides_(connected_components)

    area_sides = []
    for o, (cpt, n_sides) in enumerate(zip(connected_components, sides)):
        area = int((cpt == 1).sum())
        area_sides.append((area, n_sides))

    if VERBOSE:
        print(f"r2i={sorted(r2i.items())}")
        i2r = {v: k for k, v in r2i.items()}
        for o, (area, n_sides) in enumerate(area_sides):
            i = o2i[o]
            char = i2r[i]
            print(f"{o+1:4}: {char} {area} x {n_sides} = {area*n_sides}")

    print(f"Part 2: {sum(area*perimeter for area, perimeter in area_sides)}", flush=True)

def test_sides():
    counter = 22
    cpt = np.loadtxt(csv_name_(counter, "sides"), delimiter=",", dtype=int)
    num_sides_(counter, cpt, verbose=True)
    exit(22)

args = parse_args("Advent of Code 2024 - Day 12", "problems/aoc2024-day12-input-test.txt")
if args.verbose: VERBOSE = True
rows = read_rows(args.input)
img, r2i = rows_to_img(rows)

t0 = time.time()
part1(img)
t1 = time.time() - t0
t0 = time.time()
part2(img)
t2 = time.time() - t0
print(f"Part 1: {t1:.1f} sec")
print(f"Part 2: {t2:.1f} sec")
