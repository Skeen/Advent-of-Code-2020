from functools import partial

import click

test_program = ["nop +0", "acc +1", "jmp +4", "acc +3", "jmp -3", "acc -99", "acc +1", "jmp -4", "acc +6"]


def parse_instruction(line):
    # Strip the input line to be simpler
    instruction, argument = line.split(" ")
    return instruction, int(argument)


def execute_program(instructions):
    visited_instructions = [0] * len(instructions)
    state = {
        'accumulator': 0,
        'program_counter': 0
    }

    def handle_nop(state, argument):
        return state

    def handle_acc(state, argument):
        state['accumulator'] += argument
        return state

    def handle_jmp(state, argument):
        state['program_counter'] += argument - 1
        return state

    opcode_map = {
        'nop': handle_nop,
        'acc': handle_acc,
        'jmp': handle_jmp,
    }

    while True:
        if visited_instructions[state['program_counter']] == 1:
            return state['accumulator']
        visited_instructions[state['program_counter']] = 1

        instruction, argument = instructions[state['program_counter']]
        print(state, instruction, argument)
        state = opcode_map[instruction](state, argument)
        state['program_counter'] += 1


assert parse_instruction("nop +0") == ("nop", 0)
assert parse_instruction("jmp +4") == ("jmp", 4)
assert parse_instruction("acc -11") == ("acc", -11)


@click.command()
@click.option("--input", required=True, type=click.File("r"), default="input")
@click.option("--part", required=True, type=click.Choice(["1", "2"]), default="2")
def main(input, part):
    # Iterator of lines
    lines = map(lambda x: x.strip(), input.readlines())
    #lines = test_program
    # Iterator of rules
    instructions = map(parse_instruction, lines)
    instructions = list(instructions)
    # Run program
    print(instructions)
    print(execute_program(instructions))


if __name__ == "__main__":
    main()
