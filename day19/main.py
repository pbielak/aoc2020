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


def main():
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


if __name__ == '__main__':
    main()
