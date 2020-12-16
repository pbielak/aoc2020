"""Day 14 - Advent of Code"""
from itertools import product

from typing import Dict, Generator, List, NamedTuple, Union


class MaskInstruction(NamedTuple):
    mask: str


class MemoryWriteInstruction(NamedTuple):
    address: int
    value: int


Instructions = List[Union[MaskInstruction, MemoryWriteInstruction]]


def parse_file(path: str) -> Instructions:
    instructions = []
    with open(path, 'r') as fin:
        for line in fin.readlines():
            if line.startswith('mask'):
                mask = line.split(' = ')[1].strip()

                instructions.append(MaskInstruction(mask=mask))

            elif line.startswith('mem'):
                instr, value = line.split(' = ')

                address = int(instr.replace('mem[', '').replace(']', ''))
                value = int(value)

                instructions.append(MemoryWriteInstruction(
                    address=address,
                    value=value,
                ))

            else:
                raise ValueError(f'Unknown instruction: \"{line}\"')

    return instructions


def apply_mask(value: int, mask: str) -> int:
    for idx, v in enumerate(mask[::-1]):
        if v == '0':
            value = (value & ~(1 << idx))
        elif v == '1':
            value = (value | (1 << idx))

    return value


def execute(instructions: Instructions) -> Dict[int, int]:
    memory = {}
    current_mask = None

    for inst in instructions:
        if isinstance(inst, MaskInstruction):
            current_mask = inst.mask
        elif isinstance(inst, MemoryWriteInstruction):
            value = apply_mask(value=inst.value, mask=current_mask)
            address = inst.address

            memory[address] = value

    return memory


def generate_addresses(address: int, mask: str) -> Generator[int, None, None]:
    # Apply `0`s and `1`s in mask and collect `X` (floating) indexes
    floating = []
    for idx, v in enumerate(mask[::-1]):
        if v == '0':
            continue
        elif v == '1':
            address = (address | (1 << idx))
        elif v == 'X':
            floating.append(idx)

    # Generate all possible addresses with floating
    for vals in product((0, 1), repeat=len(floating)):
        tmp = address
        for idx, v in zip(floating, vals):
            if v == 0:
                tmp = (tmp & ~(1 << idx))
            elif v == 1:
                tmp = (tmp | (1 << idx))
        yield tmp


def execute_v2(instructions: Instructions) -> Dict[int, int]:
    memory = {}
    current_mask = None

    for inst in instructions:
        if isinstance(inst, MaskInstruction):
            current_mask = inst.mask
        elif isinstance(inst, MemoryWriteInstruction):
            value = inst.value
            for addr in generate_addresses(
                address=inst.address,
                mask=current_mask,
            ):
                memory[addr] = value

    return memory


def main():
    for tf in ('./data/example.txt', './data/input.txt'):
        print('Test file:', tf)

        instructions = parse_file(path=tf)

        memory = execute(instructions=instructions)

        solution = sum(v for v in memory.values())

        print(
            '(Part 1) '
            'Sum of all values in memory:',
            solution,
        )

    for tf in ('./data/example2.txt', './data/input.txt'):
        print('Test file:', tf)

        instructions = parse_file(path=tf)

        memory_v2 = execute_v2(instructions=instructions)

        solution_v2 = sum(v for v in memory_v2.values())

        print(
            '(Part 2) '
            'Sum of all values in memory:',
            solution_v2
        )


if __name__ == '__main__':
    main()
