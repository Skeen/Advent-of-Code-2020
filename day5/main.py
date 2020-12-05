from functools import wraps
from itertools import count

import click


def apply(func):
    @wraps(func)
    def applied(tup):
        return func(*tup)

    return applied


def bsp_to_seat_row(bsp):
    # Split seat number into parts
    row = bsp[:7]
    col = bsp[7:]
    # Convert from non-standard binary to binary
    row = row.replace('F', '0').replace('B', '1')
    col = col.replace('L', '0').replace('R', '1')
    # Convert from binary to integers
    row = int(row, 2)
    col = int(col, 2)
    return row, col


def row_col_to_seat_id(row, col):
    seat_id = row * 8 + col
    return seat_id


assert bsp_to_seat_row("FBFBBFFRLR") == (44, 5)
assert bsp_to_seat_row("BFFFBBFRRR") == (70, 7)
assert bsp_to_seat_row("FFFBBBFRRR") == (14, 7)
assert bsp_to_seat_row("BBFFBBFRLL") == (102, 4)

assert row_col_to_seat_id(44, 5) == 357
assert row_col_to_seat_id(70, 7) == 567
assert row_col_to_seat_id(14, 7) == 119
assert row_col_to_seat_id(102, 4) == 820


@click.command()
@click.option("--input", required=True, type=click.File("r"), default="input")
@click.option("--part", required=True, type=click.Choice(["1", "2"]), default="2")
def main(input, part):
    # Iterator of lines
    lines = map(lambda x: x.strip(), input.readlines())
    seats = map(bsp_to_seat_row, lines)
    seat_ids = map(apply(row_col_to_seat_id), seats)

    if part == "1":
        print(max(seat_ids))
    else:
        print(set(range(11, 835)) - set(seat_ids))


if __name__ == "__main__":
    main()
