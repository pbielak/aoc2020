"""Day 18 - Advent of Code"""
from typing import Callable, List, Tuple


def parse_file(path: str) -> List[str]:
    with open(path, 'r') as fin:
        return [line.strip() for line in fin.readlines()]


def find_parenthesis(expression: str) -> Tuple[int, int]:
    """Returns the `start` and `end` indexes of the parenthesis expression."""
    start_idx = -1
    num_nested = 0

    for idx, c in enumerate(list(expression)):
        if c == '(':
            if start_idx == -1:
                start_idx = idx
            else:
                num_nested += 1
        if c == ')':
            if num_nested == 0:
                return start_idx, idx
            else:
                num_nested -= 1

    raise RuntimeError('Should not happen')


def _compute_same_precedence(expression: str) -> int:
    """Multiplication and addition have the same precedence."""
    assert all(s not in expression for s in ('(', ')'))

    tokens = expression.split(' ')
    assert tokens[0].isdigit()

    result = int(tokens[0])
    last_op = None

    for token in tokens[1:]:
        if token in ('+', '*'):
            last_op = token
        elif token.isdigit():
            if last_op == '+':
                result += int(token)
            elif last_op == '*':
                result *= int(token)
            else:
                raise ValueError(f'Illegal last operator: {last_op}')
        else:
            raise ValueError(f'Illegal token: {token}')

    return result


def _compute_diff_precedence(expression: str) -> int:
    """Addition is evaluated **before** multiplication."""
    assert all(s not in expression for s in ('(', ')'))

    tokens = expression.split(' ')

    # While there is addition to compute
    while '+' in tokens:
        # Find first addition
        add_idx = tokens.index('+')

        # Compute the sum
        res = int(tokens[add_idx - 1]) + int(tokens[add_idx + 1])

        # Replace the addition expression with the computed sum
        tokens = [*tokens[:add_idx - 1], str(res), *tokens[add_idx + 2:]]

    # If there is nothing else to compute, then just return the value
    if len(tokens) == 1:
        return int(tokens[0])

    # Now perform the remaining multiplications
    product = 1
    for token in tokens:
        if token.isdigit():
            product *= int(token)

    return product


def compute(
    expression: str,
    simple_compute_fn: Callable[[str], int],
) -> int:
    # If there are any parenthesis
    while any(s in expression for s in ('(', ')')):
        start_idx, end_idx = find_parenthesis(expression=expression)
        ex = expression[start_idx:end_idx + 1]

        # Compute while cutting off parenthesis
        res = compute(expression=ex[1:-1], simple_compute_fn=simple_compute_fn)

        expression = expression.replace(ex, str(res))

    # Handle simple expression without parenthesis
    result = simple_compute_fn(expression)

    return result


def main():
    test_cases = [
        '1 + 2 * 3 + 4 * 5 + 6',
        '1 + (2 * 3) + (4 * (5 + 6))',
        '2 * 3 + (4 * 5)',
        '5 + (8 * 3 + 9 + 3 * 4 * 3)',
        '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))',
        '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2',
    ]

    tf = './data/input.txt'
    print('Test file:', tf)

    expressions = parse_file(path=tf)

    # Part 1 - multiplication and addition have same precedence
    same_precedence_results = [71, 51, 26, 437, 12240, 13632]
    assert all(
        compute(ex, _compute_same_precedence) == res
        for ex, res in zip(test_cases, same_precedence_results)
    )

    all_expressions_sum = sum([
        compute(expression=ex, simple_compute_fn=_compute_same_precedence)
        for ex in expressions
    ])
    print(
        '(Part 1) '
        'Sum of all expressions:',
        all_expressions_sum,
    )

    # Part 2 - addition is evaluated **before** multiplication
    diff_precedence_results = [231, 51, 46, 1445, 669060, 23340]
    assert all(
        compute(ex, _compute_diff_precedence) == res
        for ex, res in zip(test_cases, diff_precedence_results)
    )

    all_expressions_sum = sum([
        compute(expression=ex, simple_compute_fn=_compute_diff_precedence)
        for ex in expressions
    ])
    print(
        '(Part 2) '
        'Sum of all expressions:',
        all_expressions_sum,
    )


if __name__ == '__main__':
    main()
