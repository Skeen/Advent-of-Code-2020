import click


def parse_instruction(line):
    # Strip the input line to be simpler
    instruction, argument = line.split(" ")
    return instruction, int(argument)


assert parse_instruction("nop +0") == ("nop", 0)
assert parse_instruction("jmp +4") == ("jmp", 4)
assert parse_instruction("acc -11") == ("acc", -11)


def lines_to_instructions(lines):
    instructions = map(parse_instruction, lines)
    instructions = list(instructions)
    return instructions


test_program_part1 = lines_to_instructions(
    [
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
)


def transform_instruction(instruction):
    opcode_map = {
        "acc": "acc",
        "jmp": "nop",
        "nop": "jmp",
    }
    instruction, argument = instruction
    return opcode_map[instruction], argument


assert transform_instruction(("nop", 0)) == ("jmp", 0)
assert transform_instruction(("jmp", 4)) == ("nop", 4)
assert transform_instruction(("acc", -11)) == ("acc", -11)


test_program_part2 = test_program_part1.copy()
test_program_part2[-2] = transform_instruction(test_program_part2[-2])


class InstructionHalt(Exception):
    def __init__(self, state):
        self.state = state


class InfiniteLoopHalt(Exception):
    def __init__(self, state):
        self.state = state


def execute_program(instructions):
    state = {"accumulator": 0, "program_counter": 0}

    def handle_nop(state, argument):
        return state

    def handle_acc(state, argument):
        state["accumulator"] += argument
        return state

    def handle_jmp(state, argument):
        state["program_counter"] += argument - 1
        return state

    def handle_hlt(state, argument):
        raise InfiniteLoopHalt(state)

    opcode_map = {
        "nop": handle_nop,
        "acc": handle_acc,
        "jmp": handle_jmp,
        "hlt": handle_hlt,
    }

    try:
        while True:
            instruction, argument = instructions[state["program_counter"]]
            # Set run instructions to infinite loop halt instructions
            instructions[state["program_counter"]] = ("hlt", 0)
            # print(state, instruction, argument)
            # Execute instruction
            state = opcode_map[instruction](state, argument)
            state["program_counter"] += 1
    except IndexError:
        raise InstructionHalt(state)


def generate_mutated_instructions(instructions):
    for x in range(len(instructions)):
        new_instruction = transform_instruction(instructions[x])
        yield instructions[:x] + [new_instruction] + instructions[x + 1 :]


@click.command()
@click.option("--input", required=True, type=click.File("r"), default="input")
@click.option("--part", required=True, type=click.Choice(["1", "2"]), default="2")
def main(input, part):
    # Iterator of lines
    lines = map(lambda x: x.strip(), input.readlines())
    instructions = lines_to_instructions(lines)
    # Run program
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
