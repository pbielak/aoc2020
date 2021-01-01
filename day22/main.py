"""Day 22 - Advent of Code"""
from typing import List, Tuple


def parse_file(path: str) -> Tuple[List[int], List[int]]:
    with open(path, 'r') as fin:
        player_1_deck, player_2_deck = fin.read().split('\n\n')

        player_1_deck = [int(card) for card in player_1_deck.split('\n')[1:]]
        player_2_deck = [int(card) for card in player_2_deck.split('\n')[1:]]
        return player_1_deck, player_2_deck


def play(deck1: List[int], deck2: List[int]):
    while True:
        # If any deck is empty, then return the other one (winning one)
        if not deck1:
            return deck2

        if not deck2:
            return deck1

        # Play round
        p1 = deck1.pop(0)
        p2 = deck2.pop(0)

        if p1 > p2:
            deck1.extend([p1, p2])
        else:
            deck2.extend([p2, p1])


def main():
    # Part 1
    for tf in ('./data/example.txt', './data/input.txt'):
        print('Test file:', tf)

        player_1_deck, player_2_deck = parse_file(path=tf)
        winning_deck = play(deck1=player_1_deck, deck2=player_2_deck)

        winning_player_score = sum(
            (idx + 1) * card
            for idx, card in enumerate(reversed(winning_deck))
        )

        print(
            '(Part 1) '
            'Winning player score:',
            winning_player_score,
        )


if __name__ == '__main__':
    main()
