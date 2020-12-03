from functools import partial, wraps
from itertools import count

import click
from more_itertools import iter_except


def apply(func):
    @wraps(func)
    def applied(tup):
        return func(*tup)

    return applied


def check_for_tree(area, x, y):
    x_index = x % len(area[0])
    return area[y][x_index] == "#"


@click.command()
@click.option("--input", required=True, type=click.File("r"), default="input")
@click.option("--x-step", required=True, type=click.INT, default=3)
@click.option("--y-step", required=True, type=click.INT, default=1)
def main(input, x_step, y_step):
    # Create a list of lists of characters
    # First index is y-coordinate, second index is x-coordinate
    area = list(map(list, map(lambda x: x.strip(), input.readlines())))

    # Seed and apply our check_for_tree function, such that it can be called
    # with an x,y index and return a boolean as to whether we found a tree
    tree_checker = apply(partial(check_for_tree, area))

    # Create an infinite iterator with the correct slope
    slope = zip(count(step=x_step), count(step=y_step))

    # Convert each iterator step to a boolean indicating whether there is a
    # tree or not, at the given position
    path_iter = map(tree_checker, slope)

    # Limit the iterator to run until the first IndexError occurs
    # (so the iterator is no longer infinite)
    path_iter = iter_except(partial(next, path_iter), IndexError)

    # Sum up the iterator of booleans, i.e. count the number of True's
    print(sum(path_iter))


if __name__ == "__main__":
    main()
