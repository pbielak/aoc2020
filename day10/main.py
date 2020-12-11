"""Day 10 - Advent of Code"""
from itertools import groupby
from functools import reduce
from operator import mul
from typing import Dict, List


def parse_file(path: str) -> List[int]:
    with open(path, 'r') as fin:
        return [int(num) for num in fin.readlines()]


def count_jolt_differences(jolts: List[int]) -> Dict[int, int]:
    differences = [b - a for a, b in zip(jolts, jolts[1:])]
    return {diff: differences.count(diff) for diff in set(differences)}


def count_arrangements(jolts: List[int]) -> int:
    """Counts number of different arrangements.

    We need to find all blocks of "one differences". For each block size we can
    manually compute the number of different removals (arrangements) of the
    power adapters, i.e. (where "_" means a removed adapter),

    Block: [1]
    Arrangements:
    - [1]
    Total: 1

    Block: [1, 1]
    Arrangements:
    - [1, 1]
    - [_, 1]
    Total: 2

    Block: [1, 1, 1]
    Arrangements:
    - [1, 1, 1]
    - [_, 1, 1]
    - [1, _, 1]
    - [_, _, 1]
    Total: 4


    Block: [1, 1, 1, 1]
    Arrangements:
    - [1, 1, 1, 1]
    - [_, 1, 1, 1]
    - [1, _, 1, 1]
    - [1, 1, _, 1]
    - [_, _, 1, 1]
    - [1, _, _, 1]
    - [_, 1, _, 1]
    Total: 7

    For longer block sizes the pattern can be also computed but in the input
    examples there is no such block.
    """
    _BLOCK_SIZE_TO_NUM_ARRANGEMENTS = {
        1: 1,
        2: 2,
        3: 4,
        4: 7,
    }

    differences = [b - a for a, b in zip(jolts, jolts[1:])]
    one_block_lengths = [
        len(list(values))
        for difference, values in groupby(differences)
        if difference == 1
    ]

    num_arrangements_for_blocks = [
        _BLOCK_SIZE_TO_NUM_ARRANGEMENTS[block_size]
        for block_size in one_block_lengths
    ]

    return reduce(mul, num_arrangements_for_blocks)


def main():
    test_files = ['./data/example.txt', './data/input.txt']

    for tf in test_files:
        print('Test file:', tf)

        adapter_jolts = parse_file(path=tf)

        # Add input and device jolts
        adapter_jolts = [
            0, *sorted(adapter_jolts), max(adapter_jolts) + 3
        ]

        counts = count_jolt_differences(jolts=adapter_jolts)
        solution = counts[1] * counts[3]

        print(
            '(Part 1) '
            'Number of 1-jolt differences multiplied by '
            'the number of 3-jolt differences:',
            solution,
        )

        num_arrangements = count_arrangements(jolts=adapter_jolts)

        print(
            '(Part 2) '
            'Number of different arrangements:',
            num_arrangements,
        )


if __name__ == '__main__':
    main()
