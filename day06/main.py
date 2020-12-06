"""Day 6 - Advent of Code"""
from collections import Counter
from typing import List


def parse_file(path: str) -> List[List[str]]:
    with open(path, 'r') as fin:
        return [
            group.split('\n')
            for group in fin.read().split('\n\n')
        ]


def count_any_answer(forms: List[List[str]]) -> int:
    return sum([len(set(''.join(group))) for group in forms])


def count_all_answer(forms: List[List[str]]) -> int:
    total = 0
    for group in forms:
        group_size = len(group)
        answer_counts = Counter(''.join(group))
        total += len([
            answer
            for answer, count in answer_counts.items()
            if count == group_size
        ])

    return total


def main():
    test_files = ['./data/example.txt', './data/input.txt']

    for tf in test_files:
        print('Test file:', tf)

        forms = parse_file(path=tf)

        num_any_answer = count_any_answer(forms=forms)
        print('(Part 1) Sum of distinct "any" answer counts:', num_any_answer)

        num_all_answer = count_all_answer(forms=forms)
        print('(Part 2) Sum of distinct "all" answer counts:', num_all_answer)

        print('-------')


if __name__ == '__main__':
    main()
