from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Dict


@dataclass
class Assembler:
    symbol_table: Dict[str, int] = field(default_factory=lambda: {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "R0": 0,
        "R1": 1,
        "R2": 2,
        "R3": 3,
        "R4": 4,
        "R5": 5,
        "R6": 6,
        "R7": 7,
        "R8": 8,
        "R9": 9,
        "R10": 10,
        "R11": 11,
        "R12": 12,
        "R13": 13,
        "R14": 14,
        "R15": 15,
        "SCREEN": 16384,
        "KBD": 24576,
    })

    @classmethod
    def create(cls) -> Assembler:
        return cls()

    def assemble(self, assembly: Iterable[str]) -> List[str]:
        assembly = self.remove_comments_and_empty_lines(assembly)
        self.add_labels(assembly)
        self.add_variables(assembly)
        return self.translate_assembly(assembly)

    def remove_comments_and_empty_lines(self, assembly: Iterable[str]) -> List[str]:
        cleaned_assembly: List[str] = []
        for line in assembly:
            line = line.split("//")[0].strip()
            if line:
                cleaned_assembly.append(line)
        return cleaned_assembly

    def add_labels(self, assembly: List[str]) -> None:
        i = 0
        for line in assembly:
            if line.startswith("("):
                label = line[1:-1]
                self.symbol_table[label] = i
            else:
                i += 1

    def add_variables(self, assembly: List[str]) -> None:
        next_address = 16
        for line in assembly:
            if line.startswith("@") and not line[1:].isdigit():
                symbol = line[1:]
                if symbol not in self.symbol_table:
                    self.symbol_table[symbol] = next_address
                    next_address += 1

    def translate_assembly(self, assembly: List[str]) -> List[str]:
        binary_instructions: List[str] = []
        for line in assembly:
            if line.startswith("@"):
                binary_instructions.append(self.translate_a_instruction(line))
            elif not line.startswith("("):
                binary_instructions.append(self.translate_c_instruction(line))
        return binary_instructions

    def translate_a_instruction(self, line: str) -> str:
        address = line[1:]
        if address.isdigit():
            address_value = int(address)
        else:
            address_value = self.symbol_table.get(address, 0)  # Default to 0 if not found
        return format(address_value, "016b")

    def translate_c_instruction(self, line: str) -> str:
        comp = dest = jump = ""

        if "=" in line:
            dest, comp = line.split("=")
        else:
            comp = line

        if ";" in comp:
            comp, jump = comp.split(";")

        comp_bin = {
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "M": "1110000",
            "!D": "0001101",
            "!A": "0110001",
            "!M": "1110001",
            "-D": "0001111",
            "-A": "0110011",
            "-M": "1110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "M+1": "1110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "M-1": "1110010",
            "D+A": "0000010",
            "D+M": "1000010",
            "D-A": "0010011",
            "D-M": "1010011",
            "A-D": "0000111",
            "M-D": "1000111",
            "D&A": "0000000",
            "D&M": "1000000",
            "D|A": "0010101",
            "D|M": "1010101",
        }.get(comp, "0000000")

        dest_bin = {
            "": "000",
            "M": "001",
            "D": "010",
            "MD": "011",
            "DM": "011",
            "A": "100",
            "AM": "101",
            "MA": "101",
            "AD": "110",
            "DA": "110",
            "AMD": "111",
        }.get(dest, "000")

        jump_bin = {
            "": "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111",
        }.get(jump, "000")

        return "111" + comp_bin + dest_bin + jump_bin
