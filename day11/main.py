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


def acquire_seats1(seating_grid):
    def count_adjacent(line_id, seat_id, check_for='#'):
        num_adjacent = 0
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i == 0 and j == 0:
                    continue
                try:
                    new_line_id = line_id + i
                    if new_line_id < 0:
                        continue
                    new_seat_id = seat_id + j
                    if new_seat_id < 0:
                        continue
                    check_seat = seating_grid[new_line_id][new_seat_id]
                except IndexError:
                    continue
                if check_seat == check_for:
                    # print(line_id+i, seat_id+j, "is", check_for)
                    num_adjacent += 1
        return num_adjacent

    def seat_acquire(line_id, seat_id, seat):
        # print(line_id, seat_id, count_adjacent(line_id, seat_id))
        if seat == 'L' and count_adjacent(line_id, seat_id) == 0:
            return "#"
        elif seat == '#' and count_adjacent(line_id, seat_id) >= 4:
            return "L"
        return seat

    @apply
    def line_acquire(line_id, seating_line):
        return list(map(apply(partial(seat_acquire, line_id)), enumerate(seating_line)))

    return list(map(line_acquire, enumerate(seating_grid)))


def acquire_seats2(seating_grid):
    def count_adjacent(line_id, seat_id):
        num_adjacent = 0
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i == 0 and j == 0:
                    continue
                for distance in range(1, 100):
                    try:
                        new_line_id = line_id + i * distance
                        if new_line_id < 0:
                            break
                        new_seat_id = seat_id + j * distance
                        if new_seat_id < 0:
                            break
                        check_seat = seating_grid[new_line_id][new_seat_id]
                    except IndexError:
                        break
                    if check_seat == 'L':
                        break
                    if check_seat == '#':
                        # print(line_id+i, seat_id+j, "is", check_for)
                        num_adjacent += 1
                        break
        return num_adjacent

    def seat_acquire(line_id, seat_id, seat):
        # print(line_id, seat_id, count_adjacent(line_id, seat_id))
        if seat == 'L' and count_adjacent(line_id, seat_id) == 0:
            return "#"
        elif seat == '#' and count_adjacent(line_id, seat_id) >= 5:
            return "L"
        return seat

    @apply
    def line_acquire(line_id, seating_line):
        return list(map(apply(partial(seat_acquire, line_id)), enumerate(seating_line)))

    return list(map(line_acquire, enumerate(seating_grid)))





@click.command()
@click.option("--input", required=True, type=click.File("r"), default="input")
@click.option("--part", required=True, type=click.Choice(["1", "2"]), default="2")
def main(input, part):
    # Iterator of lines
    lines = map(lambda x: x.strip(), input.readlines())
#    lines = [
#        "L.LL.LL.LL",
#        "LLLLLLL.LL",
#        "L.L.L..L..",
#        "LLLL.LL.LL",
#        "L.LL.LL.LL",
#        "L.LLLLL.LL",
#        "..L.L.....",
#        "LLLLLLLLLL",
#        "L.LLLLLL.L",
#        "L.LLLLL.LL"
#    ]
    lines = map(lambda x: list(x), lines)
    seating_grid = list(lines)

    if part == '1':
        acquire_seats = acquire_seats1
    if part == '2':
        acquire_seats = acquire_seats2

    for seating_line in seating_grid:
        print(seating_line)
    print()

    while True:
        new_seating_grid = acquire_seats(seating_grid)
        print_grid = "\n".join(["".join(x) for x in new_seating_grid])
        print(print_grid)
        print(print_grid.count('#'))
        print()

        if seating_grid == new_seating_grid:
            return
        seating_grid = new_seating_grid


if __name__ == "__main__":
    main()
