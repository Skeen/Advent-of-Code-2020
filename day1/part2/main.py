from itertools import combinations
from math import prod

import click


def sum_to_2020(int_tuple):
    return sum(int_tuple) == 2020


@click.command()
@click.option("--input", required=True, type=click.File("r"), default="input")
@click.option("--factors", required=True, type=click.INT, default=3)
def main(input, factors):
    integers = map(int, input.readlines())
    integer_tuples = combinations(integers, factors)
    integer_tuples = filter(sum_to_2020, integer_tuples)
    results = map(prod, integer_tuples)
    print(list(results))


if __name__ == "__main__":
    main()
