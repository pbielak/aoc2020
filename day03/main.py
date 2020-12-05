"""Day 3 - Advent of Code"""
from functools import reduce
from operator import mul
from typing import List


def count_trees_on_path(
    grid: List[str],
    right: int = 3,
    down: int = 1,
) -> int:
    num_trees = 0

    position = 0
    for idx in range(0, len(grid), down):
        if idx == 0:
            continue

        position = ((position + right) % len(grid[idx]))

        if grid[idx][position] == '#':
            num_trees += 1

    return num_trees


def main():
    test_files = ['./data/example.txt', './data/input.txt']

    ALL_SLOPES = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]

    for tf in test_files:
        print('Test file:', tf)

        with open(tf, 'r') as fin:
            grid = [row.strip() for row in fin]

            num_trees = count_trees_on_path(grid=grid)
            print('(Part 1) Number of trees:', num_trees)

            prod_num_trees = reduce(
                mul,
                [
                    count_trees_on_path(grid=grid, right=r, down=d)
                    for r, d in ALL_SLOPES
                ],
            )
            print('(Part 2) Product of number of trees:', prod_num_trees)

        print('-------')


if __name__ == '__main__':
    main()
