"""Day 12 - Advent of Code"""
from dataclasses import dataclass
import math
from typing import List, Tuple


@dataclass
class Point2D:
    x: int
    y: int


def parse_file(path: str) -> List[Tuple[str, int]]:
    with open(path, 'r') as fin:
        return [
            (line[0], int(line[1:]))
            for line in fin.readlines()
        ]


def rotate(
    point: Point2D,
    how: str,
    angle: int,
    ref_point: Point2D = Point2D(x=0, y=0),
) -> Point2D:
    def cos(value: int):
        return round(math.cos(math.radians(value)), 1)

    def sin(value: int):
        return round(math.sin(math.radians(value)), 1)

    # If dealing with "right" turns translate the problem to a "left" turn
    if how == 'R':
        angle = 360 - angle

    px, py = point.x, point.y
    ox, oy = ref_point.x, ref_point.y

    x = cos(angle) * (px - ox) - sin(angle) * (py - oy) + ox
    y = sin(angle) * (px - ox) + cos(angle) * (py - oy) + oy

    return Point2D(int(x), int(y))


def navigate_ship(instructions: List[Tuple[str, int]]) -> Point2D:
    position = Point2D(x=0, y=0)
    direction = Point2D(x=1, y=0)

    for action, value in instructions:
        if action == 'N':
            position.y += value
        elif action == 'S':
            position.y -= value
        elif action == 'E':
            position.x += value
        elif action == 'W':
            position.x -= value
        elif action in ('L', 'R'):
            direction = rotate(point=direction, how=action, angle=value)
        elif action == 'F':
            position.x += direction.x * value
            position.y += direction.y * value
        else:
            raise ValueError(f'Unknown action: {action}{value}')

    return position


def navigate_ship_using_waypoint(
    instructions: List[Tuple[str, int]],
    waypoint_x: int,
    waypoint_y: int,
) -> Point2D:
    position = Point2D(x=0, y=0)
    waypoint = Point2D(x=waypoint_x, y=waypoint_y)

    for action, value in instructions:
        if action == 'N':
            waypoint.y += value
        elif action == 'S':
            waypoint.y -= value
        elif action == 'E':
            waypoint.x += value
        elif action == 'W':
            waypoint.x -= value
        elif action in ('L', 'R'):
            tmp_point = rotate(
                point=Point2D(waypoint.x + position.x, waypoint.y + position.y),
                how=action,
                angle=value,
                ref_point=position,
            )
            waypoint = Point2D(
                x=tmp_point.x - position.x,
                y=tmp_point.y - position.y,
            )
        elif action == 'F':
            position.x += waypoint.x * value
            position.y += waypoint.y * value
        else:
            raise ValueError(f'Unknown action: {action}{value}')

    return position


def main():
    test_files = ['./data/example.txt', './data/input.txt']

    for tf in test_files:
        print('Test file:', tf)

        instructions = parse_file(path=tf)

        final_position = navigate_ship(instructions=instructions)
        mh_distance = abs(final_position.x) + abs(final_position.y)

        print(
            '(Part 1) '
            'Ship\'s Manhattan distance from starting position:',
            mh_distance,
        )

        final_position_using_waypoint = navigate_ship_using_waypoint(
            instructions=instructions,
            waypoint_x=10,
            waypoint_y=1,
        )
        mh_distance_waypoint = (
            abs(final_position_using_waypoint.x)
            + abs(final_position_using_waypoint.y)
        )

        print(
            '(Part 2) '
            'Ship\'s Manhattan distance from starting position '
            '(using waypoint):',
            mh_distance_waypoint,
        )


if __name__ == '__main__':
    main()
