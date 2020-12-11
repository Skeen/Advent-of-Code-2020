from math import prod
from collections import Counter
from functools import wraps
from itertools import chain

import click
from more_itertools import pairwise, unzip, split_after


def apply(func):
    @wraps(func)
    def applied(tup):
        return func(*tup)

    return applied


def find_arrangements(integers):
    if integers == []:
        return 1

    start = integers[0] - 1
    valid_adapters = filter(lambda x: x <= start+3, integers)

    def produce_lists(adapter):
        new_start = start + (adapter - start)
        return list(filter(lambda x: x > new_start, integers))

    integer_lists = map(produce_lists, valid_adapters)

    return sum(map(find_arrangements, integer_lists))


@click.command()
@click.option("--input", required=True, type=click.File("r"), default="input")
@click.option("--part", required=True, type=click.Choice(["1", "2"]), default="2")
def main(input, part):
    # Iterator of lines
    lines = map(lambda x: x.strip(), input.readlines())
    # Iterator of integers
    integers = list(map(int, lines))
    # integers = [28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3]
    # integers = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]
    integers = sorted(integers)

    min_jolts = 0
    max_jolts = integers[-1] + 3
    diff_integers = chain([min_jolts], integers, [max_jolts])
    differences = list(map(lambda a,b: b-a, *unzip(pairwise(diff_integers))))

    if part == "1":
        differences = Counter(differences)
        print(differences[1] * differences[3])
    if part == "2":
        # We do not have to consider all possible combinations, as all the
        # combinations will contain certain sequences, namely all sequences
        # will passthrough 3-difference numbers, and thus the sequences on
        # either side of these 3-difference numbers are independent.
        #
        # Thus we can split the problem into several subproblems, one on either
        # side of the 3-difference numbers.
        @apply
        def difference_is_3(index, value):
            """Check if the current index is a 3-difference number."""
            return differences[index] == 3

        # Iterator of subproblems (lists seperated by 3-difference numbers)
        # Each element in the lists are (index, value)
        subproblems = split_after(enumerate(integers), difference_is_3)
        # Map each element in the lists to just value (drop index)
        subproblems = map(lambda element: list(unzip(element)[1]), subproblems)
        # Find number of possible combinations for each block
        sub_counts = map(find_arrangements, subproblems)
        # Multiple the values for all the blocks to get a total
        print(prod(sub_counts))


if __name__ == "__main__":
    main()
