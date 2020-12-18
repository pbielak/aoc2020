"""Day 17 - Advent of Code"""
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

        # Get all cubes to consider
        all_xyz_to_consider = [
            (xn, yn, zn)
            for x, y, z in grid.keys()
            for xn, yn, zn in get_neighbor_positions_3d(x=x, y=y, z=z)
        ]

        # For every cube get its state and the number of active neighbors
        for x, y, z in all_xyz_to_consider:
            current_cube = grid.get((x, y, z), INACTIVE)
            ns = [
                grid.get((xn, yn, zn), INACTIVE)
                for xn, yn, zn in get_neighbor_positions_3d(x=x, y=y, z=z)
            ]
            num_active_neighbors = ns.count(ACTIVE)

            # Apply rules
            if current_cube == ACTIVE:
                if num_active_neighbors not in (2, 3):
                    new_grid[(x, y, z)] = INACTIVE
            elif current_cube == INACTIVE:
                if num_active_neighbors == 3:
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

        # Get all cubes to consider
        all_xyzw_to_consider = [
            (xn, yn, zn, wn)
            for x, y, z, w in grid.keys()
            for xn, yn, zn, wn in get_neighbor_positions_4d(x=x, y=y, z=z, w=w)
        ]

        # For every cube get its state and the number of active neighbors
        for x, y, z, w in all_xyzw_to_consider:
            current_cube = grid.get((x, y, z, w), INACTIVE)
            ns = [
                grid.get((xn, yn, zn, wn), INACTIVE)
                for xn, yn, zn, wn in get_neighbor_positions_4d(
                    x=x, y=y, z=z, w=w
                )
            ]
            num_active_neighbors = ns.count(ACTIVE)

            # Apply rules
            if current_cube == ACTIVE:
                if num_active_neighbors not in (2, 3):
                    new_grid[(x, y, z, w)] = INACTIVE
            elif current_cube == INACTIVE:
                if num_active_neighbors == 3:
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
