from functools import partial

import click


def parse_line_to_rule(line):
    # Strip the input line to be simpler
    line = line.replace(" bags", "")
    line = line.replace(" bag", "")
    line = line.rstrip(".")
    # Split the input line on contains, then split the right hand side on comma
    container, contents = line.split(" contain ")
    contents = contents.split(", ")
    # Remove no other bags, as to get an empty list
    contents = filter(lambda x: x != "no other", contents)
    # Split count and bag color
    contents = map(lambda x: x.split(" ", 1), contents)
    return container, list(contents)


assert parse_line_to_rule("dark orange bags contain 3 bright white bags, 4 muted yellow bags.") == ("dark orange", [["3", "bright white"], ["4", "muted yellow"]])
assert parse_line_to_rule("bright white bags contain 1 shiny gold bag.") == ("bright white", [["1", "shiny gold"]])
assert parse_line_to_rule("faded blue bags contain no other bags.") == ("faded blue", [])


def find_bag_containing(rules, looking_for):
    for bag, contents in rules.items():
        for count, content in contents:
            if looking_for in content:
                yield bag
                yield from find_bag_containing(rules, bag)


def find_bags_under(rules, under, printer=print):
    contents = rules[under]
    printer("checking", under, contents)
    if contents == []:
        printer("-> no other bags returning 1")
        return 1

    amount = 1
    for count, content in contents:
        subtree = find_bags_under(rules, content, printer=partial(printer, "\t"))
        amount += int(count) * subtree
        printer("->", "count", count, "subtree", subtree, "(", int(count)*subtree, ")")
    printer("->", "amount", amount)
    return amount


@click.command()
@click.option("--input", required=True, type=click.File("r"), default="input")
@click.option("--part", required=True, type=click.Choice(["1", "2"]), default="2")
def main(input, part):
    # Iterator of lines
    lines = map(lambda x: x.strip(), input.readlines())
    # Iterator of rules
    rules = map(parse_line_to_rule, lines)
    rules = list(rules)
    # Dict of rules (bag --> contents)
    rules = dict(rules)

    if part == "1":
        bag_tree = find_bag_containing(rules, "shiny gold")
        print(len(set(bag_tree)))
    elif part == "2":
        printer = lambda *args: None
        # printer = print
        bag_count = find_bags_under(rules, "shiny gold", printer)
        print(bag_count - 1)  # We do not count the shiny gold bag


if __name__ == "__main__":
    main()
