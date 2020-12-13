"""Day 13 - Advent of Code"""
from typing import List, Tuple


def parse_file(path: str) -> Tuple[int, List[int]]:
    with open(path, 'r') as fin:
        lines = fin.readlines()
        assert len(lines) == 2

        timestamp = int(lines[0].strip())
        bus_ids = [
            int(bid) if bid != 'x' else 'x'
            for bid in lines[1].split(',')
        ]

        return timestamp, bus_ids


def find_earliest_bus_ID(timestamp: int, bus_ids: List[int]) -> Tuple[int, int]:
    return min([
        (bid, (timestamp // bid) * bid - timestamp + bid)
        for bid in bus_ids
    ], key=lambda v: v[1])


def find_earliest_timestamp(bus_ids: List[int]) -> int:
    """For the example given in the assignment, we have:

    Bus IDs: [7, 13, x, x, 59, x, 31, 19]
    Indexes: [0,  1, 2, 3,  4, 5,  6,  7]

    That means the earliest timestamp `t` should satisfy:
    (t + 0) % 7 = 0
    (t + 1) % 13 = 0
    (t + 4) % 59 = 0
    (t + 6) % 31 = 0
    (t + 7) % 19 = 0

    By expanding the parenthesis:
    t % 7 = 0
    t % 13 = -1 % 13 => t % 13 = 12
    t % 59 = -4 % 59 => t % 59 = 55
    t % 31 = -6 % 31 => t % 31 = 25
    t % 19 = -7 % 19 => t % 19 = 12

    This form indicates the `Chinese remainder theorem`. By applying this
    algorithm we obtain the earliest timestamp `t`, which should be: 1 068 781
    """
    times = [bid for bid in bus_ids if bid != 'x']
    remainders = [-idx % bid for idx, bid in enumerate(bus_ids) if bid != 'x']

    # Inspired by `https://rosettacode.org/wiki/Chinese_remainder_theorem`
    total_product = 1
    for t in times:
        total_product *= t

    total_sum = 0

    for time, remainder in zip(times, remainders):
        p = total_product // time
        total_sum += remainder * mul_inv(p, time) * p

    return total_sum % total_product


def mul_inv(a, b):
    a = a % b
    for x in range(1, b):
        if (a * x) % b == 1:
            return x
    return 1


def main():
    test_files = ['./data/example.txt', './data/input.txt']

    test_cases_part_2 = [
        ([17, 'x', 13, 19], 3_417),
        ([67, 7, 59, 61], 754_018),
        ([67, 'x', 7, 59, 61], 779_210),
        ([67, 7, 'x', 59, 61], 1_261_476),
        ([1789, 37, 47, 1889], 1_202_161_486),
    ]
    assert all(
        find_earliest_timestamp(inp) == outp
        for inp, outp in test_cases_part_2
    )

    for tf in test_files:
        print('Test file:', tf)

        timestamp, bus_ids = parse_file(path=tf)

        bus_ids_part_1 = [bid for bid in bus_ids if bid != 'x']
        earliest_bid, waiting_time = find_earliest_bus_ID(
            timestamp=timestamp,
            bus_ids=bus_ids_part_1,
        )

        solution = earliest_bid * waiting_time
        print(
            '(Part 1) '
            'Bus ID multiplied by the number of minutes to wait:',
            solution,
        )

        earliest_timestamp = find_earliest_timestamp(bus_ids=bus_ids)
        print(
            '(Part 2) '
            'Earliest timestamp that matches requirements:',
            earliest_timestamp,
        )


if __name__ == '__main__':
    main()
