"""Day 7 - Advent of Code"""
from typing import List


def parse_file(path: str) -> List[dict]:
    bag_rules = []

    with open(path, 'r') as fin:
        for line in fin.readlines():
            line = (
                line
                .strip()
                .replace('bags', '')
                .replace('bag', '')
                .replace('.', '')
                .replace('  ', ' ')
            )
            parent_bag_color, inner_bag_colors = line.split('contain')

            parent_bag_color = parent_bag_color.strip()

            if 'no other' in inner_bag_colors:
                inner_bag_colors = []
            else:
                inner_bag_colors = [
                    ibc.strip()
                    for ibc in inner_bag_colors.split(',')
                ]
                inner_bag_colors = [
                    {
                        'num': int(ibc.split(' ')[0]),
                        'color': ' '.join(ibc.split(' ')[1:]),
                    }
                    for ibc in inner_bag_colors
                ]

            bag_rules.append({
                'parent': parent_bag_color,
                'inner': inner_bag_colors,
            })

        return bag_rules


def get_bags_containing(
    bag_rules: List[dict],
    target_bag_color: str,
) -> List[str]:
    bags_containing_target = set()

    # Find parents of `target_bar_color`
    parents = [
        br['parent']
        for br in bag_rules
        if any(
            ibc['color'] == target_bag_color
            for ibc in br['inner']
        )
    ]
    bags_containing_target.update(parents)

    # Find bags containing every parent
    for parent in parents:
        bags = get_bags_containing(
            bag_rules=bag_rules,
            target_bag_color=parent,
        )
        bags_containing_target.update(bags)

    return list(bags_containing_target)


def get_num_bags_inside(
    bag_rules: List[dict],
    start_bag_color: str,
) -> int:
    num_bags_inside = 1

    # Find inner bags of `start_bag_color`
    inner_bags = [
        inner
        for br in bag_rules
        for inner in br['inner']
        if br['parent'] == start_bag_color
    ]

    # Find bags inside `inner_bags` bags
    for inner_bag in inner_bags:
        num_bags = get_num_bags_inside(
            bag_rules=bag_rules,
            start_bag_color=inner_bag['color'],
        )
        num_bags_inside += inner_bag['num'] * num_bags

    return num_bags_inside


def main():
    test_files = [
        './data/example.txt',
        './data/example2.txt',
        './data/input.txt',
    ]

    for tf in test_files:
        print('Test file:', tf)

        bag_rules = parse_file(path=tf)

        bags_containing_target = get_bags_containing(
            bag_rules=bag_rules,
            target_bag_color='shiny gold',
        )
        print(
            '(Part 1) '
            'Number of distinct bag colors containing a `shiny gold` bag:',
            len(bags_containing_target),
        )

        num_bags_inside = get_num_bags_inside(
            bag_rules=bag_rules,
            start_bag_color='shiny gold',
        )
        print(
            '(Part 2) '
            'Number of individual bags inside a `shiny gold` bag:',
            num_bags_inside - 1,
        )

        print('-------')


if __name__ == '__main__':
    main()
