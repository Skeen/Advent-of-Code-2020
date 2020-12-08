from functools import partial

import click

test_program_part1 = [
    "nop +0",
    "acc +1",
    "jmp +4",
    "acc +3",
    "jmp -3",
    "acc -99",
    "acc +1",
    "jmp -4",
    "acc +6",
]
test_program_part2 = [
    "nop +0",
    "acc +1",
    "jmp +4",
    "acc +3",
    "jmp -3",
    "acc -99",
    "acc +1",
    "nop -4",
    "acc +6",
]


class InstructionHalt(Exception):
    def __init__(self, state):
        self.state = state


class InfiniteLoopHalt(Exception):
    def __init__(self, state):
        self.state = state


def parse_instruction(line):
    # Strip the input line to be simpler
    instruction, argument = line.split(" ")
    return instruction, int(argument)


def execute_program(instructions):
    visited_instructions = [0] * len(instructions)
    state = {"accumulator": 0, "program_counter": 0}

    def handle_nop(state, argument):
        return state

    def handle_acc(state, argument):
        state["accumulator"] += argument
        return state

    def handle_jmp(state, argument):
        state["program_counter"] += argument - 1
        return state

    opcode_map = {
        "nop": handle_nop,
        "acc": handle_acc,
        "jmp": handle_jmp,
    }

    try:
        while True:
            if visited_instructions[state["program_counter"]] == 1:
                raise InfiniteLoopHalt(state)
            visited_instructions[state["program_counter"]] = 1

            instruction, argument = instructions[state["program_counter"]]
            # print(state, instruction, argument)
            state = opcode_map[instruction](state, argument)
            state["program_counter"] += 1
    except IndexError:
        raise InstructionHalt(state)


assert parse_instruction("nop +0") == ("nop", 0)
assert parse_instruction("jmp +4") == ("jmp", 4)
assert parse_instruction("acc -11") == ("acc", -11)


def generate_mutated_instructions(instructions):
    for x in range(len(instructions)):
        new_instructions = instructions.copy()
        instruction = new_instructions[x]
        if instruction[0] == "jmp":
            new_instructions[x] = ("nop", instruction[1])
        if instruction[0] == "nop":
            new_instructions[x] = ("jmp", instruction[1])
        yield new_instructions


@click.command()
@click.option("--input", required=True, type=click.File("r"), default="input")
@click.option("--part", required=True, type=click.Choice(["1", "2"]), default="2")
def main(input, part):
    # Iterator of lines
    lines = map(lambda x: x.strip(), input.readlines())
    # lines = test_program_part1
    # lines = test_program_part2
    # Iterator of rules
    instructions = map(parse_instruction, lines)
    instructions = list(instructions)
    # Run program
    # print(instructions)
    if part == "1":
        execute_program(instructions)
    elif part == "2":
        # Loop through all mutated programs
        for new_instructions in generate_mutated_instructions(instructions):
            # Keep running, until we find one that terminates with InstructionHalt
            try:
                execute_program(new_instructions)
            except InfiniteLoopHalt:
                continue


if __name__ == "__main__":
    main()
