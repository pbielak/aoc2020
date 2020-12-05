"""Day 2 - Advent of Code"""
from collections import Counter, namedtuple
from typing import List


InputRow = namedtuple('InputRow', ['min', 'max', 'character', 'password'])


def parse_file(path: str) -> List[InputRow]:
    rows = []
    with open(path, 'r') as fin:
        for row in fin:
            allowed_range, character, password = row.strip().split(' ')
            min_val, max_val = [int(v) for v in allowed_range.split('-')]
            character = character.replace(':', '')

            rows.append(InputRow(
                min=min_val,
                max=max_val,
                character=character,
                password=password,
            ))
    return rows


def is_valid_password_range(
    password: str,
    character: str,
    min_occurrences: int,
    max_occurrences: int,
) -> bool:
    all_character_counts = Counter(password)
    character_count = all_character_counts[character]
    return min_occurrences <= character_count <= max_occurrences


def is_valid_password_position(
    password: str,
    character: str,
    first_position: int,
    second_position: int,
) -> bool:
    return (
        (password[first_position - 1] == character)
        ^ (password[second_position - 1] == character)
    )


def main():
    test_files = ['./data/example.txt', './data/input.txt']

    for tf in test_files:
        print('Test file:', tf)
        input_rows = parse_file(path=tf)
        solution_range = len([
            row
            for row in input_rows
            if is_valid_password_range(
                password=row.password,
                character=row.character,
                min_occurrences=row.min,
                max_occurrences=row.max,
            )
        ])
        print('(Part 1 - Range) Number of valid password:', solution_range)

        solution_pos = len([
            row
            for row in input_rows
            if is_valid_password_position(
                password=row.password,
                character=row.character,
                first_position=row.min,
                second_position=row.max,
            )
        ])
        print('(Part 2 - Positions) Number of valid password:', solution_pos)

        print('-------')


if __name__ == '__main__':
    main()
