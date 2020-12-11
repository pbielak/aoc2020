"""Day 9 - Advent of Code"""
from typing import List, Set


def parse_file(path: str) -> List[int]:
    with open(path, 'r') as fin:
        return [int(num) for num in fin.readlines()]


def find_invalid_number(numbers: List[int], window: int) -> int:
    buffer = numbers[:window]
    for idx in range(window, len(numbers)):
        current_number = numbers[idx]

        # Check if value fits property
        if not any([
            a + b == current_number
            for a in buffer
            for b in buffer
            if a != b
        ]):
            return current_number

        # Shift buffer
        buffer = [*buffer[1:], current_number]


def find_contiguous_set(
    numbers: List[int],
    invalid_number: int,
    min_set_size: int = 2,
) -> Set[int]:
    for i in range(len(numbers)):
        for j in range(i + min_set_size, len(numbers)):
            vals = numbers[i:j]

            if sum(vals) > invalid_number:
                break

            if sum(vals) == invalid_number:
                return set(vals)


def main():
    test_files = [('./data/example.txt', 5), ('./data/input.txt', 25)]

    for tf, window in test_files:
        print('Test file:', tf)

        numbers = parse_file(path=tf)

        invalid_number = find_invalid_number(numbers=numbers, window=window)

        print(
            '(Part 1) '
            'First number that does not have the property:',
            invalid_number,
        )

        contiguous_set = find_contiguous_set(
            numbers=numbers,
            invalid_number=invalid_number,
        )
        weakness = min(contiguous_set) + max(contiguous_set)

        print(
            '(Part 2) '
            'Encryption weakness of XMAS-encrypted numbers:',
            weakness,
        )


if __name__ == '__main__':
    main()
