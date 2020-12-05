"""Day 1 - Advent of Code"""
from typing import List, Tuple


def find_pairs_summing_to_const(
    values: List[int],
    const: int = 2020,
) -> Tuple[int, int]:
    v = tuple(set(values).intersection(set([const - v for v in values])))
    assert len(v) == 2
    assert sum(v) == const
    return v


def find_triplets_summing_to_const(
    values: List[int],
    const: int = 2020,
) -> Tuple[int, int, int]:
    all_pairs = [(a, b) for a in values for b in values if a != b]
    v = tuple(
        set(values)
        .intersection(set([const - (a + b) for a, b in all_pairs]))
    )
    assert len(v) == 3
    assert sum(v) == const
    return v


def main():
    test_files = ['./data/example.txt', './data/input.txt']

    for tf in test_files:
        print('Test file:', tf)
        with open(tf, 'r') as fin:
            values = [int(v.strip()) for v in fin.readlines()]

            x, y = find_pairs_summing_to_const(values)
            print('Pairs =>', '(X, Y):', (x, y), 'X * Y:', x * y)

            x, y, z = find_triplets_summing_to_const(values)
            print('Triplets =>', '(X, Y, Z):', (x, y, z), 'X * Y * Z:', x * y * z)
        print('-------')


if __name__ == '__main__':
    main()
