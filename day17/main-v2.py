"""Day 17 - Advent of Code (alternative solution)"""
from collections import defaultdict
from typing import Dict, List, Tuple

DEBUG = True

ACTIVE = '#'
INACTIVE = '.'

Point3D = Tuple[int, int, int]
Point4D = Tuple[int, int, int, int]


def parse_file(path: str) -> List[List[str]]:
    with open(path, 'r') as fin:
        return [list(line) for line in fin.read().split('\n')]


def get_neighbor_positions_3d(
    x: int, y: int, z: int
) -> List[Point3D]:
    return [
        (xn, yn, zn)
        for xn in (x - 1, x, x + 1)
        for yn in (y - 1, y, y + 1)
        for zn in (z - 1, z, z + 1)
        if (xn, yn, zn) != (x, y, z)
    ]


def simulate_3d(
    layer0: List[List[str]],
    num_steps: int,
) -> Dict[Point3D, str]:
    grid = {}

    # Set initial layer values (z = 0)
    for y in range(len(layer0)):
        for x in range(len(layer0[0])):
            grid[(x, y, 0)] = layer0[y][x]

    for step in range(num_steps):
        # Make a copy of the grid
        new_grid = grid.copy()

        # Get all active cubes
        active_cubes = [
            (x, y, z)
            for (x, y, z), value in grid.items()
            if value == ACTIVE
        ]

        # For every active cube pass active state to neighbors
        activations = defaultdict(int)
        for x, y, z in active_cubes:
            for xn, yn, zn in get_neighbor_positions_3d(x=x, y=y, z=z):
                activations[(xn, yn, zn)] += 1

        # If any active cube had no active neighbors it won't show up in the
        # dict, so we need to add it separately
        for x, y, z in active_cubes:
            if (x, y, z) not in activations.keys():
                activations[(x, y, z)] = 0

        # Apply rules
        for (x, y, z), num_active in activations.items():
            current_cube = grid.get((x, y, z), INACTIVE)

            if current_cube == ACTIVE:
                if num_active not in (2, 3):
                    new_grid[(x, y, z)] = INACTIVE
            elif current_cube == INACTIVE:
                if num_active == 3:
                    new_grid[(x, y, z)] = ACTIVE

        # Update grid
        grid = new_grid

        # Debug
        if DEBUG:
            num_active = list(grid.values()).count(ACTIVE)
            num_total = len(grid.keys())
            print(
                f'Step: {step + 1} -> '
                f'Num active / total: {num_active}/{num_total}'
            )

    return grid


def get_neighbor_positions_4d(
    x: int, y: int, z: int, w: int
) -> List[Point4D]:
    return [
        (xn, yn, zn, wn)
        for xn in (x - 1, x, x + 1)
        for yn in (y - 1, y, y + 1)
        for zn in (z - 1, z, z + 1)
        for wn in (w - 1, w, w + 1)
        if (xn, yn, zn, wn) != (x, y, z, w)
    ]


def simulate_4d(
    layer0: List[List[str]],
    num_steps: int,
) -> Dict[Point4D, str]:
    grid = {}

    # Set initial layer values (z = 0, w = 0)
    for y in range(len(layer0)):
        for x in range(len(layer0[0])):
            grid[(x, y, 0, 0)] = layer0[y][x]

    for step in range(num_steps):
        # Make a copy of the grid
        new_grid = grid.copy()

        # Get all active cubes
        active_cubes = [
            (x, y, z, w)
            for (x, y, z, w), value in grid.items()
            if value == ACTIVE
        ]

        # For every active cube pass active state to neighbors
        activations = defaultdict(int)
        for x, y, z, w in active_cubes:
            for xn, yn, zn, wn in get_neighbor_positions_4d(x=x, y=y, z=z, w=w):
                activations[(xn, yn, zn, wn)] += 1

        # If any active cube had no active neighbors it won't show up in the
        # dict, so we need to add it separately
        for x, y, z, w in active_cubes:
            if (x, y, z, w) not in activations.keys():
                activations[(x, y, z, w)] = 0

        # Apply rules
        for (x, y, z, w), num_active in activations.items():
            current_cube = grid.get((x, y, z, w), INACTIVE)

            if current_cube == ACTIVE:
                if num_active not in (2, 3):
                    new_grid[(x, y, z, w)] = INACTIVE
            elif current_cube == INACTIVE:
                if num_active == 3:
                    new_grid[(x, y, z, w)] = ACTIVE

        # Update grid
        grid = new_grid

        # Debug
        if DEBUG:
            num_active = list(grid.values()).count(ACTIVE)
            num_total = len(grid.keys())
            print(
                f'Step: {step + 1} -> '
                f'Num active / total: {num_active}/{num_total}'
            )

    return grid


def main():
    for tf in ('./data/example.txt', './data/input.txt'):
        print('Test file:', tf)

        layer0 = parse_file(path=tf)

        final_grid_3d = simulate_3d(layer0=layer0, num_steps=6)
        num_active_cubes_3d = list(final_grid_3d.values()).count(ACTIVE)
        print(
            '(Part 1) '
            '[3D] Number of active cubes after six cycles:',
            num_active_cubes_3d,
        )

        final_grid_4d = simulate_4d(layer0=layer0, num_steps=6)
        num_active_cubes_4d = list(final_grid_4d.values()).count(ACTIVE)
        print(
            '(Part 2) '
            '[4D] Number of active cubes after six cycles:',
            num_active_cubes_4d,
        )


if __name__ == '__main__':
    main()
