"""Day 15 - Advent of Code"""
from typing import List


def simulate_game(starting_numbers: List[int], max_step: int) -> int:
    numbers = {n: [i+1] for i, n in enumerate(starting_numbers)}
    last_spoken = starting_numbers[-1]

    for turn in range(len(starting_numbers) + 1, max_step + 1):
        if len(numbers[last_spoken]) == 1:
            last_spoken = 0
        else:
            diff = numbers[last_spoken][0] - numbers[last_spoken][1]
            last_spoken = diff

        if last_spoken not in numbers:
            numbers[last_spoken] = [turn]
        else:
            numbers[last_spoken] = [turn, numbers[last_spoken][0]]

    return last_spoken


def main():
    test_inputs = {
        2020: [
            ([0, 3, 6], 436),
            ([1, 3, 2], 1),
            ([2, 1, 3], 10),
            ([1, 2, 3], 27),
            ([2, 3, 1], 78),
            ([3, 2, 1], 438),
            ([3, 1, 2], 1836),
        ],
        30_000_000: [
            ([0, 3, 6], 175_594),
            ([1, 3, 2], 2_578),
            ([2, 1, 3], 3_544_142),
            ([1, 2, 3], 261_214),
            ([2, 3, 1], 6_895_259),
            ([3, 2, 1], 18),
            ([3, 1, 2], 362),
        ],
    }
    my_puzzle_input = [19, 20, 14, 0, 9, 1]

    for idx, max_step in enumerate((2020, 30_000_000)):
        assert all(
            simulate_game(starting_numbers=ti, max_step=max_step) == expected
            for ti, expected in test_inputs[max_step]
        )

        print('My input:', my_puzzle_input)
        value = simulate_game(
            starting_numbers=my_puzzle_input,
            max_step=max_step,
        )

        print(f'(Part {idx + 1}) The {max_step}th number is: {value}')


if __name__ == '__main__':
    main()
