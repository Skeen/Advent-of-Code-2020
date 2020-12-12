from math import prod
from collections import Counter
from functools import wraps
from itertools import chain
from functools import partial

import click
from more_itertools import pairwise, unzip, split_after


def apply(func):
    @wraps(func)
    def applied(tup):
        return func(*tup)

    return applied



@click.command()
@click.option("--input", required=True, type=click.File("r"), default="input")
@click.option("--part", required=True, type=click.Choice(["1", "2"]), default="2")
def main(input, part):
    # Iterator of lines
    lines = map(lambda x: x.strip(), input.readlines())
    #lines = [
    #    "F10",
    #    "N3",
    #    "F7",
    #    "R90",
    #    "F11",
    #]
    direction = "E"
    pos_x = 0
    pos_y = 0

    def next_direction(direction):
        if direction == "E":
            return "S"
        elif direction == "S":
            return "W"
        elif direction == "W":
            return "N"
        elif direction == "N":
            return "E"

    def prev_direction(direction):
        if direction == "E":
            return "N"
        elif direction == "N":
            return "W"
        elif direction == "W":
            return "S"
        elif direction == "S":
            return "E"

    for instruction in lines:
        command = instruction[0]
        value = int(instruction[1:])
        if command == "F":
            if direction == "E":
                pos_x += value
            elif direction == "W":
                pos_x -= value
            elif direction == "N":
                pos_y += value
            elif direction == "S":
                pos_y -= value
        elif command == "N":
            pos_y += value
        elif command == "S":
            pos_y -= value
        elif command == "E":
            pos_x += value
        elif command == "W":
            pos_x -= value
        elif command == "R":
            while value != 0:
                direction = next_direction(direction)
                value -= 90
        elif command == "L":
            while value != 0:
                direction = prev_direction(direction)
                value -= 90

    print(pos_x, pos_y)
    print(abs(pos_x) + abs(pos_y))


if __name__ == "__main__":
    main()
