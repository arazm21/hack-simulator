import argparse
import os
import json
from typing import List

from Assembler import Assembler
from Simulator import Simulator

def filter_file(lines: List[str]) -> List[str]:
    return [line.strip() for line in lines if line.strip() and (line.strip()[0] == '0' or line.strip()[0] == '1')]

def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip() and not line.startswith('//')]

def main():
    parser = argparse.ArgumentParser(description="Hack simulation")
    parser.add_argument("filename", type=str, help="The name of the file to process")
    parser.add_argument("--cycles", type=int, default=5000, help="The number of cycles to run")
    args = parser.parse_args()

    lines = read_file(args.filename)
    assembler = Assembler.create()

    if args.filename.endswith(".asm"):
        binary_commands = list(assembler.assemble(lines))
    elif args.filename.endswith(".hack"):
        binary_commands = filter_file(lines)
    else:
        raise ValueError("Unsupported file type. Please provide a .asm or .hack file")
    # for com in binary_commands:
    #     print(com)
    simulator = Simulator(binary_commands, args.cycles)

    changed_ram = simulator.run()

    sorted_changed_ram = dict(sorted(changed_ram.items()))

    output_filename = os.path.splitext(args.filename)[0] + ".json"
    with open(output_filename, 'w') as outfile:
        json.dump({"RAM": sorted_changed_ram}, outfile, indent=4)

    print(f"Simulation completed. Changed RAM addresses and their final values have been saved to {output_filename}")

if __name__ == '__main__':
    main()
