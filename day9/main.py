from functools import partial
from itertools import combinations, count, filterfalse
from operator import itemgetter
from sys import exit

import click
from more_itertools import windowed


def check_validity(window):
    preamble = window[:-1]
    check = window[-1]

    integer_tuples = combinations(preamble, 2)
    integer_tuples = filter(lambda int_tuple: sum(int_tuple) == check, integer_tuples)
    return next(integer_tuples, None) != None


def check_decorated_sum(lookup_value, decorated_sum):
    summation, window = decorated_sum
    return summation == lookup_value


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
        decorated_sums = filter(
            partial(check_decorated_sum, first_invalid), decorated_sums
        )
        passed_windows = map(itemgetter(1), decorated_sums)
        solution = next(passed_windows, None)
        if solution:
            minimum, maximum = min(solution), max(solution)
            print(minimum + maximum)
            exit(1)


if __name__ == "__main__":
    main()
