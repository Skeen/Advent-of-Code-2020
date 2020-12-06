from functools import wraps

import click
from more_itertools import split_at


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
    # Iterator of lists of strings
    blocks = split_at(lines, lambda x: x == "")
    # Iterator of lists of sets of chars
    sets = map(lambda block: map(set, block), blocks)
    if part == "1":  # Set of any yes (union)
        set_combiner = set.union
    elif part == "2":  # Set of all yes (intersection)
        set_combiner = set.intersection
    # Iterator of sets of chars (according to set_combiner function)
    sets = map(apply(set_combiner), sets)
    # Iterator of ints (counts of sets)
    count_yes_answers = map(len, sets)
    # Summation of all ints (total count)
    count_yes_answers = sum(count_yes_answers)
    print(count_yes_answers)


if __name__ == "__main__":
    main()
