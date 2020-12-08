"""Day 8 - Advent of Code"""
from dataclasses import dataclass
from copy import deepcopy
from typing import List


@dataclass
class Instruction:
    opcode: str
    argument: int


def parse_file(path: str) -> List[Instruction]:
    instructions = []

    with open(path, 'r') as fin:
        for line in fin.readlines():
            opcode, argument = line.strip().split(' ')
            argument = int(argument)

            instructions.append(Instruction(opcode=opcode, argument=argument))

    return instructions


def execute_code(instructions: List[Instruction]):
    # Registers
    registers = {
        'acc': 0,
        'pc': 0,
    }

    # Keep track of already executed commands (prevent infinite loop)
    execution_history = []
    infinite_loop_found = False

    while True:
        ins = instructions[registers['pc']]

        execution_history.append(registers['pc'])

        if ins.opcode == 'nop':
            registers['pc'] += 1
        elif ins.opcode == 'acc':
            registers['acc'] += ins.argument
            registers['pc'] += 1
        elif ins.opcode == 'jmp':
            registers['pc'] += ins.argument
        else:
            raise RuntimeError(f'Unknown instruction: {ins}')

        if registers['pc'] == len(instructions):
            break

        if registers['pc'] in execution_history:
            infinite_loop_found = True
            break

    return registers, execution_history, infinite_loop_found


def fix_program(instructions: List[Instruction]):
    # Find all `nop` and `jmp` instructions (their indexes)
    nop_jmp_instructions_idxs = [
        i
        for i, ins in enumerate(instructions)
        if ins.opcode in ('nop', 'jmp')
    ]

    # For any of those instructions, flip them and run the program
    for idx in nop_jmp_instructions_idxs:
        ins_cpy = deepcopy(instructions)

        if ins_cpy[idx].opcode == 'nop':
            ins_cpy[idx].opcode = 'jmp'
        elif ins_cpy[idx].opcode == 'jmp':
            ins_cpy[idx].opcode = 'nop'
        else:
            raise RuntimeError(
                'We should have either a `nop` or a `jmp` instruction here'
            )

        registers, _, infinite_loop_found = execute_code(instructions=ins_cpy)

        if not infinite_loop_found:
            return registers

    raise RuntimeError('Program could not be fixed!')


def main():
    test_files = ['./data/example.txt', './data/input.txt']

    for tf in test_files:
        print('Test file:', tf)

        instructions = parse_file(path=tf)

        registers, execution_history, infinite_loop_found = execute_code(
            instructions=instructions,
        )
        assert infinite_loop_found

        print(
            '(Part 1) '
            'Accumulator value before infinite loop:',
            registers['acc'],
        )

        registers_after_fix = fix_program(instructions=instructions)
        print(
            '(Part 2) '
            'Accumulator value after termination of fixed program:',
            registers_after_fix['acc'],
        )
        print('-------')


if __name__ == '__main__':
    main()
