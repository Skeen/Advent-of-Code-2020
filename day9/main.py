from itertools import combinations, count, filterfalse
from operator import itemgetter

import click
from more_itertools import windowed


def check_validity(window):
    preamble = window[:-1]
    check = window[-1]

    integer_tuples = combinations(preamble, 2)
    integer_tuples = filter(lambda int_tuple: sum(int_tuple) == check, integer_tuples)
    return next(integer_tuples, None) != None


@click.command()
@click.option("--input", required=True, type=click.File("r"), default="input")
@click.option("--part", required=True, type=click.Choice(["1", "2"]), default="2")
def main(input, part):
    # Iterator of lines
    lines = map(lambda x: x.strip(), input.readlines())
    # Iterator of integers
    integers = list(map(int, lines))
    # Iterator of windows
    windows = windowed(integers, 26)
    # Iterator of invalid windows
    invalid = filterfalse(check_validity, windows)
    # Iterator of invalid numbers
    invalid = map(itemgetter(25), invalid)
    # First invalid number
    first_invalid = next(invalid)
    print(first_invalid)

    for num_factors in count(2):
        windows = list(windowed(integers, num_factors))
        sums = map(sum, windows)
        decorated_sums = zip(sums, windows)
        for summation, window in decorated_sums:
            if summation == first_invalid:
                minimum, maximum = min(window), max(window)
                print(minimum, maximum)
                print(minimum + maximum)
                from sys import exit

                exit(1)


if __name__ == "__main__":
    main()
