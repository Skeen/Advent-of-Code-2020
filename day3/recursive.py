from math import prod

import click


def check_for_tree(area, x, y):
    x_index = x % len(area[0])
    return area[y][x_index] == "#"


def recursive_check(area, x_step, y_step):
    def descend(x, y):
        try:
            return (
                int(check_for_tree(area, x, y)) +
                descend(x + x_step, y + y_step)
            )
        except IndexError:
            return 0
    return descend


@click.command()
@click.option("--input", required=True, type=click.File("r"), default="input")
@click.option("--part", required=True, type=click.Choice(["1", "2"]), default="2")
def main(input, part):
    area = list(map(list, map(lambda x: x.strip(), input.readlines())))

    slopes = [(3, 1)]
    if part == "2":
        slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

    print(prod(recursive_check(area, x_step, y_step)(0,0) for x_step, y_step in slopes))


if __name__ == "__main__":
    main()
