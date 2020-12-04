import string
from functools import partial

import click
from more_itertools import first, flatten, ilen, split_at


def filter_required_keys(passport):
    # Set of keys we expect valid passports to have (cid optional)
    required_keys = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

    return required_keys.issubset(passport.keys())


def filter_integer(key, lower, upper, passport):
    integer = int(passport[key])
    return lower <= integer <= upper


filter_birth_year = partial(filter_integer, "byr", 1920, 2002)
filter_issue_year = partial(filter_integer, "iyr", 2010, 2020)
filter_expire_year = partial(filter_integer, "eyr", 2020, 2030)


def filter_height(passport):
    height = passport["hgt"]
    if "in" in height:
        lower = 59
        upper = 76
    elif "cm" in height:
        lower = 150
        upper = 193
    else:  # No units --> Invalid
        return False
    height = int(height[:-2])  # strip off cm/in
    return lower <= height <= upper


def filter_hair_color(passport):
    allowed = set(string.hexdigits)

    hair_color = iter(passport["hcl"])
    return first(hair_color) == "#" and set(hair_color).issubset(allowed)


def filter_eye_color(passport):
    allowed = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}

    eye_color = passport["ecl"]
    return eye_color in allowed


def filter_passport_id(passport):
    passport_id = passport["pid"]
    return passport_id.isdecimal() and len(passport_id) == 9


@click.command()
@click.option("--input", required=True, type=click.File("r"), default="input")
@click.option("--part", required=True, type=click.Choice(["1", "2"]), default="2")
def main(input, part):
    # Iterator of lines
    lines = map(lambda x: x.strip(), input.readlines())
    # Iterator of key-value pair strings
    entries = flatten(map(lambda x: x.split(" "), lines))
    # Iterator of key-value pair tuples
    entries = map(lambda x: x.split(":"), entries)
    # Iterator of lists of key-value pairs (split on empty string)
    blocks = split_at(entries, lambda x: x == [""])
    # Iterator of dicts
    dicts = map(dict, blocks)

    # Start applying filters, and print length
    dicts = filter(filter_required_keys, dicts)
    if part == "2":
        dicts = filter(filter_birth_year, dicts)
        dicts = filter(filter_issue_year, dicts)
        dicts = filter(filter_expire_year, dicts)
        dicts = filter(filter_height, dicts)
        dicts = filter(filter_hair_color, dicts)
        dicts = filter(filter_eye_color, dicts)
        dicts = filter(filter_passport_id, dicts)
    print(ilen(dicts))


if __name__ == "__main__":
    main()
