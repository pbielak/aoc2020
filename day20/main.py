"""Day 20 - Advent of Code"""
from collections import Counter, defaultdict
from itertools import product
from typing import Dict, List, NamedTuple, Tuple, Union


def parse_file(path: str) -> Dict[int, List[str]]:
    tiles = {}
    with open(path, 'r') as fin:
        for tile in fin.read().split('\n\n'):
            parts = tile.split('\n')

            tid = int(parts[0].replace('Tile ', '').replace(':', ''))
            image = parts[1:]

            tiles[tid] = image

    return tiles


def extract_borders(tiles: Dict[int, List[str]]) -> Dict[int, List[str]]:
    borders = {}

    for tid, image in tiles.items():
        top = image[0]
        bottom = image[-1]
        left = ''.join([i[0] for i in image])
        right = ''.join([i[-1] for i in image])

        borders[tid] = [top, bottom, left, right]

    return borders


def find_corner_tiles(borders: Dict[int, List[str]]) -> List[int]:
    # For each border (and its reversed version - achieved by rotations,
    # flips, etc.) aggregate all tiles containing it
    border2id = defaultdict(list)

    for tid, bs in borders.items():
        for b in bs:
            key = tuple(sorted([b, b[::-1]]))
            border2id[key].append(tid)

    # We know that if exactly one tile has such border, then it must be
    # located at the outer frame of the image.
    outer_tiles = [ids[0] for ids in border2id.values() if len(ids) == 1]

    # This list will contain duplicates - only if a tile occurred two times
    # it can be a corner tile
    corner_tiles = [
        tid
        for tid, c in Counter(outer_tiles).items()
        if c == 2
    ]
    assert len(corner_tiles) == 4

    return corner_tiles


def main():
    # Part 1
    for tf in ('./data/example.txt', './data/input.txt'):
        print('Test file:', tf)

        tiles = parse_file(path=tf)
        borders = extract_borders(tiles=tiles)
        corner_tiles = find_corner_tiles(borders=borders)

        solution = (
            corner_tiles[0] * corner_tiles[1]
            * corner_tiles[2] * corner_tiles[3]
        )

        print(
            '(Part 1) '
            'Product of corner tile IDs:',
            solution,
        )


if __name__ == '__main__':
    main()
