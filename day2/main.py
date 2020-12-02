from functools import wraps

import click


def apply(func):
    @wraps(func)
    def applied(tup):
        return func(*tup)

    return applied


def parse_line(line):
    policy, password = line.split(": ")
    count, character = policy.split(" ")
    lower, upper = count.split("-")
    return int(lower), int(upper), character, password.strip()


@apply
def filter_invalid1(lower, upper, character, password):
    # Policy: There must be between lower and upper character in the password
    occurences = password.count(character)
    return lower <= occurences <= upper


@apply
def filter_invalid2(lower, upper, character, password):
    # Policy: One of lower and upper index in password must be character
    lower_match = password[lower - 1] == character
    upper_match = password[upper - 1] == character
    return sum([lower_match, upper_match]) == 1


@click.command()
@click.option("--input", required=True, type=click.File("r"), default="input")
@click.option("--policy", required=True, type=click.Choice(["1", "2"]), default="2")
def main(input, policy):
    passwords = map(parse_line, input.readlines())
    if policy == "1":
        passwords = filter(filter_invalid1, passwords)
    elif policy == "2":
        passwords = filter(filter_invalid2, passwords)
    print(len(list(passwords)))


if __name__ == "__main__":
    main()
