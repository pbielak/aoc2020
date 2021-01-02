"""Day 20 - Advent of Code"""
from __future__ import annotations

from math import sqrt
from typing import Generator, List, NamedTuple, Optional

from tqdm import tqdm

# For clarity the pattern includes `-` instead of spaces
SEA_MONSTER_PATTERN = """
------------------#-
#----##----##----###
-#--#--#--#--#--#---
    """
# The sea monster consists of 15 `#` - here we write down their indexes
SEA_MONSTER_HEIGHT = len(SEA_MONSTER_PATTERN.strip().split('\n'))
SEA_MONSTER_WIDTH = len(SEA_MONSTER_PATTERN.strip().split('\n')[0])
SEA_MONSTER_INDEXES = [
    (col, row)  # (x, y)
    for row, line in enumerate(SEA_MONSTER_PATTERN.strip().split('\n'))
    for col, c in enumerate(line)
    if c == '#'
]
assert len(SEA_MONSTER_INDEXES) == 15


class Tile(NamedTuple):
    tid: int
    pixels: List[str]

    def flip(self, how: str) -> Tile:
        if how == 'horizontal':  # left-right
            return Tile(
                tid=self.tid,
                pixels=[line[::-1] for line in self.pixels]
            )
        elif how == 'vertical':  # upside-down
            return Tile(tid=self.tid, pixels=self.pixels[::-1])
        else:
            raise ValueError(
                'Parameter `how` must be either `horizontal` or `vertical`'
            )

    def transpose(self) -> Tile:
        pixels = [[None for _ in range(self.width)] for _ in range(self.height)]

        for x in range(self.width):
            for y in range(self.height):
                pixels[x][y] = self.pixels[y][x]

        pixels = [''.join(line) for line in pixels]

        return Tile(
            tid=self.tid,
            pixels=pixels,
        )

    def rotate(self, how: str) -> Tile:
        # Assume rotation always by 90 degrees
        if how == 'left':
            return self.transpose().flip('vertical')
        elif how == 'right':
            return self.flip('vertical').transpose()
        else:
            raise ValueError(f'Unknown rotation: {how}')

    def border(self, which: str) -> str:
        if which == 'top':
            return self.pixels[0]
        elif which == 'bottom':
            return self.pixels[-1]
        elif which == 'left':
            return ''.join([line[0] for line in self.pixels])
        elif which == 'right':
            return ''.join([line[-1] for line in self.pixels])
        else:
            raise ValueError(f'Unknown border: {which}')

    @property
    def width(self):
        return len(self.pixels[0])

    @property
    def height(self):
        return len(self.pixels)

    def __repr__(self):
        return f'Tile {self.tid}\n' + '\n'.join(self.pixels)


def parse_file(path: str) -> List[Tile]:
    tiles = []
    with open(path, 'r') as fin:
        for tile in fin.read().split('\n\n'):
            parts = tile.split('\n')

            tid = int(parts[0].replace('Tile ', '').replace(':', ''))
            image = parts[1:]

            tiles.append(Tile(tid=tid, pixels=image))

    return tiles


def align_tiles(tiles: List[Tile]) -> List[List[Tile]]:
    upper_left_tile = _find_upper_left_tile(tiles=tiles)

    image_size = int(sqrt(len(tiles)))
    grid = [[None for _ in range(image_size)] for _ in range(image_size)]
    grid[0][0] = upper_left_tile

    # Find the first row of the grid
    used_tiles = {upper_left_tile.tid}

    for col in tqdm(range(1, image_size), desc='Fill first row'):
        tiles = [t for t in tiles if t.tid not in used_tiles]

        for tile in tiles:
            res = find_matching_border(
                target_border=grid[0][col - 1].border('right'),
                other_tile=tile,
                flip_type='vertical',
                border_location='left',
            )

            if res:
                assert grid[0][col - 1].border('right') == res.border('left')
                grid[0][col] = res
                used_tiles.add(res.tid)

    assert all(cell is not None for cell in grid[0])

    # Fill every column using the found elements in the first row
    positions = [
        (col, row)
        for col in range(image_size)
        for row in range(1, image_size)
    ]
    for col, row in tqdm(positions, desc='Fill columns'):
        tiles = [t for t in tiles if t.tid not in used_tiles]
        for tile in tiles:
            res = find_matching_border(
                target_border=grid[row - 1][col].border('bottom'),
                other_tile=tile,
                flip_type='horizontal',
                border_location='top',
            )

            if res:
                assert grid[row - 1][col].border('bottom') == res.border('top')
                grid[row][col] = res
                used_tiles.add(res.tid)

    assert all(cell is not None for line in grid for cell in line)

    return grid


def _find_upper_left_tile(tiles: List[Tile]) -> Tile:
    upper_left_tiles = []

    for current_tile in tqdm(tiles, desc='Find upper left tile'):
        no_top_match = all(
            find_matching_border(
                target_border=current_tile.border(which='top'),
                other_tile=tile,
                flip_type='horizontal',
                border_location='bottom',
            ) is None
            for tile in tiles
            if tile.tid != current_tile.tid
        )

        no_left_match = all(
            find_matching_border(
                target_border=current_tile.border(which='left'),
                other_tile=tile,
                flip_type='vertical',
                border_location='right',
            ) is None
            for tile in tiles
            if tile.tid != current_tile.tid
        )

        if no_top_match and no_left_match:
            upper_left_tiles.append(current_tile)

    assert len(upper_left_tiles) == 1
    return upper_left_tiles[0]


def find_matching_border(
    target_border: str,
    other_tile: Tile,
    flip_type: str,
    border_location: str,
) -> Optional[Tile]:
    if other_tile.border(border_location) == target_border:
        return other_tile

    if other_tile.flip(flip_type).border(border_location) == target_border:
        return other_tile.flip(flip_type)

    for _ in range(3):  # Max 3 rotations
        other_tile = other_tile.rotate('left')
        if other_tile.border(border_location) == target_border:
            return other_tile

        if other_tile.flip(flip_type).border(border_location) == target_border:
            return other_tile.flip(flip_type)

    return None


def construct_image(grid: List[List[Tile]]) -> Tile:
    image = []
    N = len(grid)
    tile_size = grid[0][0].width

    for row in range(N):
        for tile_row in range(1, tile_size - 1):

            image_line = ''

            for col in range(N):
                tile = grid[row][col]
                image_line += tile.pixels[tile_row][1:-1]

            image.append(image_line)

    # The image can be put into the tile data structure (already implemented
    # flipping and rotation)
    return Tile(tid=-1, pixels=image)


def count_monsters(image: Tile) -> int:
    num_monsters = 0

    for start_x in range(image.width - SEA_MONSTER_WIDTH + 1):
        for start_y in range(image.height - SEA_MONSTER_HEIGHT + 1):
            if all(
                image.pixels[start_y + offset_y][start_x + offset_x] == '#'
                for offset_x, offset_y in SEA_MONSTER_INDEXES
            ):
                num_monsters += 1

    return num_monsters


def get_image_transforms(image: Tile) -> Generator[Tile, None, None]:
    all_flips = ('horizontal', 'vertical')

    yield image

    for flip_type in all_flips:
        yield image.flip(flip_type)

    for _ in range(3):  # Max 3 rotations
        image = image.rotate('left')
        yield image

        for flip_type in all_flips:
            yield image.flip(flip_type)


def main():

    for tf in ('./data/example.txt', './data/input.txt'):
        print('Test file:', tf)

        tiles = parse_file(path=tf)
        grid = align_tiles(tiles=tiles)
        N = len(grid)

        # Part 1
        solution = (
            grid[0][0].tid * grid[0][N - 1].tid
            * grid[N - 1][0].tid * grid[N - 1][N - 1].tid
        )
        print(
            '(Part 1) '
            'Product of corner tile IDs:',
            solution,
        )

        # Part 2
        image = construct_image(grid=grid)
        num_monsters = max(
            count_monsters(img)
            for img in get_image_transforms(image=image)
        )

        num_all_hashes = len([
            c
            for line in image.pixels
            for c in line
            if c == '#'
        ])
        num_monster_hashes = len(SEA_MONSTER_INDEXES) * num_monsters
        water_roughness = num_all_hashes - num_monster_hashes

        print(
            '(Part 2) '
            'The habitat\'s water roughness:',
            water_roughness,
        )


if __name__ == '__main__':
    main()
