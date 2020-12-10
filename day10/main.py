from collections import Counter

from functools import lru_cache
from itertools import chain

import click
from more_itertools import pairwise, unzip


@lru_cache(maxsize=0)
def find_arrangements(start, integers):
    valid_adapters = list(filter(lambda x: x <= start+3, integers))
    if valid_adapters == []:
        return 1

    count = 0
    for valid_adapter in valid_adapters:
        new_start = (start + (valid_adapter - start))
        count += find_arrangements(
            new_start,
            [x for x in integers if x>new_start],
        )
    return count


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
    print(min_jolts, max_jolts)
    print(len(integers))
    print(integers)

    if part == "1":
        integers = chain([min_jolts], integers, [max_jolts])
        differences = list(map(lambda a,b: b-a, *unzip(pairwise(integers))))
        differences = Counter(differences)
        print(differences)
        print(differences[1] * differences[3])
    if part == "2":
        splits = list(map(lambda a,b: b-a == 3, *unzip(pairwise(integers))))
        splits = [min_jolts] + [x for i,x in enumerate(integers) if splits[i-1]] + [max_jolts]
        sub_counts = map(
            lambda start, end: find_arrangements(start, [x for x in integers if x>start and x<=end]),
            *unzip(pairwise(splits))
        )
        from math import prod
        print(prod(sub_counts))
    

if __name__ == "__main__":
    main()
