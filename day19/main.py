"""Day 19 - Advent of Code"""
from __future__ import annotations

from itertools import product
from typing import Dict, List, NamedTuple, Tuple, Union


class Constant(NamedTuple):
    value: str

    def get(self, ctx: Dict[str, Rule]) -> List[str]:
        return [self.value]


class ConcatRule(NamedTuple):
    values: List[str]

    def get(self, ctx: Dict[str, Rule]) -> List[str]:
        expanded = [ctx[rid].get(ctx) for rid in self.values]
        return [''.join(p) for p in product(*expanded)]


class OrRule(NamedTuple):
    options: List[ConcatRule]

    def get(self, ctx: Dict[str, Rule]) -> List[str]:
        return [
            value
            for crule in self.options
            for value in crule.get(ctx=ctx)
        ]


Rule = Union[Constant, ConcatRule, OrRule]


def parse_file(path: str) -> Tuple[Dict[str, Rule], List[str]]:
    with open(path, 'r') as fin:
        rls, msgs = fin.read().split('\n\n')

        rules = {}
        for rule in rls.split('\n'):
            rid, body = rule.split(': ')

            if any(c in body for c in ('a', 'b')):
                body = Constant(value=body.replace('\"', ''))
            elif '|' in body:
                left, right = body.split(' | ')

                body = OrRule(options=[
                    ConcatRule(values=left.split(' ')),
                    ConcatRule(values=right.split(' ')),
                ])
            else:
                body = ConcatRule(values=body.split(' '))

            rules[rid] = body

        messages = msgs.split('\n')

        return rules, messages


def matches_looped_rule_set(rules: Dict[str, Rule], message: str) -> bool:
    # Rule `0` is defined as `8 11`

    # Rule `8`: `42 | 42 8` - that means "one or more repetition of `42`"
    rule_42_values = rules['42'].get(rules)

    # Rule `11`: `42 31 | 42 11 31` - that means the message starts with
    # at least one repetition of `42` and the rest are repetitions of `31`
    # (also at least one such repetition)
    rule_31_values = rules['31'].get(rules)

    # Check how many times the `42` rule matches
    num_42_matches = 0

    while True:
        changed = False

        for value in rule_42_values:
            if message.startswith(value):
                message = message[len(value):]
                num_42_matches += 1
                changed = True
                break

        if not changed:
            break

    if len(message) == 0:
        return False  # Cannot be just a multiple of `42`

    # Check how many times the `31` rule matches
    num_31_matches = 0

    while True:
        changed = False

        for value in rule_31_values:
            if message.endswith(value):
                message = message[:-len(value)]
                num_31_matches += 1
                changed = True
                break

        if not changed:
            break

    # If there is still something left, then the message does not match
    if len(message) > 0:
        return False

    # We need at least one `31` match and at least two matches of `42`
    # (one from rule `8` and one from rule `11`). The number of `42` matches
    # must be larger than the number of `31` matches.
    return (
            num_42_matches >= 2
            and num_31_matches >= 1
            and num_42_matches > num_31_matches
    )


def main():
    # Part 1
    for tf in ('./data/example.txt', './data/input.txt'):
        print('Test file:', tf)

        rules, messages = parse_file(path=tf)

        rule_0_possible_values = rules['0'].get(rules)

        matched_messages = (
            set(messages)
            .intersection(set(rule_0_possible_values))
        )
        print(
            '(Part 1) '
            'Number of messages matched using rule `0`:',
            len(matched_messages),
        )

    # Part 2
    for tf in ('./data/example2.txt', './data/input.txt'):
        print('Test file:', tf)

        rules, messages = parse_file(path=tf)

        num_matched_messages = 0
        for msg in messages:
            if matches_looped_rule_set(rules, msg):
                num_matched_messages += 1

        print(
            '(Part 2) '
            'Number of messages matched using rule `0` (with loops):',
            num_matched_messages,
        )


if __name__ == '__main__':
    main()
