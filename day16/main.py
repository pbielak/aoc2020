"""Day 16 - Advent of Code"""
from collections import defaultdict
from functools import reduce
from operator import mul
from typing import List, NamedTuple, Tuple


class ValidationRule(NamedTuple):
    name: str
    value_ranges: Tuple[int, int, int, int]

    def matches(self, value: int) -> bool:
        a, b, c, d = self.value_ranges

        return a <= value <= b or c <= value <= d


class TaskInput(NamedTuple):
    validation_rules: List[ValidationRule]
    your_ticket: Tuple[int, ...]
    nearby_tickets: List[Tuple[int, ...]]


def parse_file(path: str) -> TaskInput:
    with open(path, 'r') as fin:
        tmp = fin.read().split('\n\n')

        # Validation rules
        validation_rules: List[ValidationRule] = []

        for vr in tmp[0].split('\n'):
            name, ranges = vr.split(': ')
            first_range, second_range = ranges.split(' or ')
            fr_min, fr_max = first_range.split('-')
            sr_min, sr_max = second_range.split('-')

            validation_rules.append(ValidationRule(
                name=name,
                value_ranges=(
                    int(fr_min), int(fr_max),
                    int(sr_min), int(sr_max),
                )
            ))

        # Your ticket
        your_ticket: Tuple[int, ...] = tuple([
            int(v) for v in tmp[1].replace('your ticket:\n', '').split(',')
        ])

        # Nearby tickets
        nearby_tickets: List[Tuple[int]] = [
            tuple([int(v) for v in ticket.split(',')])
            for ticket in tmp[2].replace('nearby tickets:\n', '').split('\n')
        ]

        return TaskInput(
            validation_rules=validation_rules,
            your_ticket=your_ticket,
            nearby_tickets=nearby_tickets,
        )


def find_invalid_numbers(
    nearby_tickets: List[Tuple[int, ...]],
    validation_rules: List[ValidationRule],
) -> List[int]:
    invalid_numbers = []
    for ticket in nearby_tickets:
        for value in ticket:
            if not any(vr.matches(value) for vr in validation_rules):
                invalid_numbers.append(value)

    return invalid_numbers


def is_valid_ticket(
    ticket: Tuple[int, ...],
    validation_rules: List[ValidationRule],
) -> bool:
    for value in ticket:
        if not any(vr.matches(value) for vr in validation_rules):
            return False
    return True


def match_names(
    tickets: List[Tuple[int, ...]],
    validation_rules: List[ValidationRule],
) -> List[str]:
    num_fields = len(tickets[0])
    names = []
    idxs = []

    while len(names) != num_fields:
        # Get all unused validation rules
        vrs = [vr for vr in validation_rules if vr.name not in names]

        # Check which positions are matched by which rules
        matched_idxs = defaultdict(list)

        for vr in vrs:
            for idx in range(num_fields):
                # Omit already used positions
                if idx in idxs:
                    continue

                if all(vr.matches(t[idx]) for t in tickets):
                    matched_idxs[vr.name].append(idx)

        # Extract rules that only applied to a single position
        for name, i in matched_idxs.items():
            if len(i) == 1:
                names.append(name)
                idxs.append(i[0])

    return [n for n, _ in sorted(zip(names, idxs), key=lambda v: v[1])]


def main():
    for tf in ('./data/example.txt', './data/input.txt'):
        print('Test file:', tf)

        task_input = parse_file(path=tf)

        invalid_numbers = find_invalid_numbers(
            nearby_tickets=task_input.nearby_tickets,
            validation_rules=task_input.validation_rules,
        )
        error_rate = sum(invalid_numbers)

        print(
            '(Part 1) '
            'Ticket scanning error rate:',
            error_rate,
        )

    for tf in ('./data/example2.txt', './data/input.txt'):
        print('Test file:', tf)

        task_input = parse_file(path=tf)

        valid_tickets = [
            ticket
            for ticket in task_input.nearby_tickets
            if is_valid_ticket(
                ticket=ticket,
                validation_rules=task_input.validation_rules,
            )
        ]

        names = match_names(
            tickets=[task_input.your_ticket, *valid_tickets],
            validation_rules=task_input.validation_rules,
        )
        print('Matched names:', names)

        if tf == './data/input.txt':
            departure_values = [
                value
                for name, value in zip(names, task_input.your_ticket)
                if name.startswith('departure')
            ]
            solution = reduce(mul, departure_values)

            print(
                '(Part 2) '
                'Multiplied departure values:',
                solution,
            )


if __name__ == '__main__':
    main()
