"""Day 21 - Advent of Code"""
from collections import defaultdict
from typing import Dict, List, Set, Tuple

Food = Tuple[List[str], List[str]]


def parse_file(path: str) -> List[Food]:
    food = []
    with open(path, 'r') as fin:
        for line in fin.readlines():
            ingredients, allergens = line.split('(')
            ingredients = ingredients.strip().split(' ')
            allergens = (
                allergens
                .strip()
                .replace('contains', '')
                .replace(')', '')
                .replace(' ', '')
                .split(',')
            )
            food.append((ingredients, allergens))
    return food


def get_unique_ingredients_and_allergens(
    food: List[Food]
) -> Tuple[Set[str], Set[str]]:
    all_ingredients = set()
    all_allergens = set()

    for ingredients, allergens in food:
        all_ingredients.update(ingredients)
        all_allergens.update(allergens)

    return all_ingredients, all_allergens


def get_allergen_to_ingredient_mapping(
    food: List[Food]
) -> Dict[str, str]:
    # Each ingredient -> 0/1 allergen
    # Each allergen -> 1 ingredient
    alg2posing = defaultdict(set)  # Allergen to possible ingredients

    for ingredients, allergens in food:
        for a in allergens:

            if a not in alg2posing.keys():
                alg2posing[a] = set(ingredients)
            else:
                alg2posing[a] = (
                    alg2posing[a]
                    .intersection(set(ingredients))
                )

    mapping = {}
    while alg2posing:
        for allergen, possible_ingredients in alg2posing.items():
            if len(possible_ingredients) == 1:
                assert allergen not in mapping.keys()
                mapping[allergen] = list(possible_ingredients)[0]

        alg2posing = {
            allergen: [
                pi
                for pi in possible_ingredients
                if pi not in mapping.values()
            ]
            for allergen, possible_ingredients in alg2posing.items()
            if allergen not in mapping.keys()
        }

    return mapping


def main():
    # Part 1
    for tf in ('./data/example.txt', './data/input.txt'):
        print('Test file:', tf)

        food = parse_file(path=tf)

        all_ingredients, all_allergens = get_unique_ingredients_and_allergens(
            food=food
        )
        allergen2ingredient = get_allergen_to_ingredient_mapping(food=food)

        ingredients_without_allegrens = (
            all_ingredients - set(allergen2ingredient.values())
        )

        count = 0
        for ingredients, _ in food:
            for i in ingredients:
                if i in ingredients_without_allegrens:
                    count += 1

        print(
            '(Part 1) '
            'Number of occurrences of non-allergen ingredients:',
            count,
        )

        dangerous_ingredients = ','.join([
            e[1]
            for e in
            sorted(allergen2ingredient.items(), key=lambda x: x[0])
        ])

        print(
            '(Part 2) '
            'Canonical dangerous ingredient list:',
            dangerous_ingredients
        )


if __name__ == '__main__':
    main()
