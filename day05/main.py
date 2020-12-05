"""Day 5 - Advent of Code"""
from typing import List


def parse_file(path: str) -> List[str]:
    with open(path, 'r') as fin:
        return [row.strip() for row in fin.readlines()]


def parse_seat_id(encoded_seat_id: str) -> int:
    row = int(
        encoded_seat_id[:7].replace('F', '0').replace('B', '1'),
        base=2,
    )

    column = int(
        encoded_seat_id[7:].replace('L', '0').replace('R', '1'),
        base=2,
    )

    return row * 8 + column


def get_my_seat_id(seat_ids: List[int]) -> int:
    ssi = sorted(seat_ids)
    seats_with_gaps = [(i, j) for i, j in zip(ssi, ssi[1:]) if i + 1 != j]
    assert len(seats_with_gaps) == 1
    return seats_with_gaps[0][0] + 1


def main():
    test_files = ['./data/example.txt', './data/input.txt']

    for tf in test_files:
        print('Test file:', tf)

        boarding_passes = parse_file(path=tf)
        seat_ids = [
            parse_seat_id(encoded_seat_id)
            for encoded_seat_id in boarding_passes
        ]

        max_seat_id = max(seat_ids)
        print('(Part 1) Highest seat ID:', max_seat_id)

        if tf != './data/example.txt':
            my_seat_id = get_my_seat_id(seat_ids)
            print('(Part 2) My seat ID:', my_seat_id)

        print('-------')


if __name__ == '__main__':
    main()
