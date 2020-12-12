"""Day 11 - Advent of Code"""
from typing import Callable, List, Optional


EMPTY_SEAT = 'L'
OCCUPIED_SEAT = '#'
FLOOR = '.'


def parse_file(path: str) -> List[List[str]]:
    with open(path, 'r') as fin:
        return [list(line.strip()) for line in fin.readlines()]


def get_direct_neighbors(
    layout: List[List[str]],
    row: int, col: int,
    height: int, width: int,
) -> List[str]:
    neighbors = []

    # Add `up`
    if row >= 1:
        neighbors.append(layout[row - 1][col])

    # Add `down`
    if row < height - 1:
        neighbors.append(layout[row + 1][col])

    # Add `left`
    if col >= 1:
        neighbors.append(layout[row][col - 1])

    # Add `right`
    if col < width - 1:
        neighbors.append(layout[row][col + 1])

    # Add `left-up`
    if (col >= 1) and (row >= 1):
        neighbors.append(layout[row - 1][col - 1])

    # Add `right-up`
    if (col < width - 1) and (row >= 1):
        neighbors.append(layout[row - 1][col + 1])

    # Add `left-down`
    if (col >= 1) and (row < height - 1):
        neighbors.append(layout[row + 1][col - 1])

    # Add `right-down`
    if (col < width - 1) and (row < height - 1):
        neighbors.append(layout[row + 1][col + 1])

    # Return just seats
    neighbors = [n for n in neighbors if n in (EMPTY_SEAT, OCCUPIED_SEAT)]
    return neighbors


def get_visible_neighbors(
    layout: List[List[str]],
    row: int, col: int,
    height: int, width: int,
) -> List[str]:
    UP = list(reversed(range(row)))
    DOWN = list(range(row + 1, height))
    LEFT = list(reversed(range(col)))
    RIGHT = list(range(col + 1, width))

    neighbors = []

    # Check `up` direction
    neighbors.append(_get_seat_type([
        layout[r][col]
        for r in UP
    ]))

    # Check `down` direction
    neighbors.append(_get_seat_type([
        layout[r][col]
        for r in DOWN
    ]))

    # Check `left` direction
    neighbors.append(_get_seat_type([
        layout[row][c]
        for c in LEFT
    ]))

    # Check `right` direction
    neighbors.append(_get_seat_type([
        layout[row][c]
        for c in RIGHT
    ]))

    # Check `left-up` direction
    neighbors.append(_get_seat_type([
        layout[r][c]
        for r, c in zip(UP, LEFT)
    ]))

    # Check `right-up` direction
    neighbors.append(_get_seat_type([
        layout[r][c]
        for r, c in zip(UP, RIGHT)
    ]))

    # Check `left-down` direction
    neighbors.append(_get_seat_type([
        layout[r][c]
        for r, c in zip(DOWN, LEFT)
    ]))

    # Check `right-down` direction
    neighbors.append(_get_seat_type([
        layout[r][c]
        for r, c in zip(DOWN, RIGHT)
    ]))

    neighbors = [n for n in neighbors if n in (OCCUPIED_SEAT, EMPTY_SEAT)]
    return neighbors


def _get_seat_type(neighbors: List[str]) -> Optional[str]:
    if not neighbors:
        return None

    for idx in range(len(neighbors)):
        if neighbors[idx] in (OCCUPIED_SEAT, EMPTY_SEAT):
            return neighbors[idx]

    assert all([n == FLOOR for n in neighbors])
    return FLOOR


def simulate(
    seats_layout: List[List[str]],
    neighbor_fn: Callable,
    tolerance: int,
) -> List[List[str]]:
    height, width = len(seats_layout), len(seats_layout[0])

    prev_layout, current_layout = seats_layout, []

    while True:
        # Perform single simulation step
        for row in range(height):
            current_row = []
            for col in range(width):
                current_seat = prev_layout[row][col]

                neighbor_seats = neighbor_fn(
                    layout=prev_layout,
                    row=row, col=col,
                    height=height, width=width,
                )

                if (
                    current_seat == EMPTY_SEAT
                    and all(ns == EMPTY_SEAT for ns in neighbor_seats)
                ):
                    current_row.append(OCCUPIED_SEAT)
                elif (
                    current_seat == OCCUPIED_SEAT
                    and neighbor_seats.count(OCCUPIED_SEAT) >= tolerance
                ):
                    current_row.append(EMPTY_SEAT)
                else:
                    current_row.append(current_seat)

            current_layout.append(current_row)

        # Check if changed
        if prev_layout == current_layout:
            return current_layout
        else:
            prev_layout, current_layout = current_layout, []


def main():
    test_files = ['./data/example.txt', './data/input.txt']

    for tf in test_files:
        print('Test file:', tf)

        seats_layout = parse_file(path=tf)

        final_seats_layout = simulate(
            seats_layout=seats_layout,
            neighbor_fn=get_direct_neighbors,
            tolerance=4,
        )
        num_occupied_seats = sum(row.count('#') for row in final_seats_layout)

        print(
            '(Part 1) '
            'Number of occupied seats:',
            num_occupied_seats,
        )

        final_seats_layout = simulate(
            seats_layout=seats_layout,
            neighbor_fn=get_visible_neighbors,
            tolerance=5,
        )
        num_occupied_seats = sum(row.count('#') for row in final_seats_layout)

        print(
            '(Part 2) '
            'Number of occupied seats:',
            num_occupied_seats,
        )


if __name__ == '__main__':
    main()
