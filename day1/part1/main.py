import operator
from functools import wraps
from itertools import product, tee

import click


def apply(func):
    @wraps(func)
    def applied(tup):
        return func(*tup)

    return applied


@apply
def sum_to_2020(x, y):
    return x + y == 2020


@click.command()
@click.option("--input", required=True, type=click.File("r"), default="input")
def main(input):
    integers = map(int, input.readlines())
    integer_pairs = product(*tee(integers))
    integer_tuples = filter(sum_to_2020, integer_pairs)
    results = map(apply(operator.mul), integer_tuples)
    print(list(results))


if __name__ == "__main__":
    main()
