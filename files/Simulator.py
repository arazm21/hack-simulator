from typing import List, Dict

class Simulator:
    def __init__(self, instructions: List[str], cycles: int) -> None:
        self.instructions: List[str] = instructions
        self.pc: int = 0  # Program counter
        self.registers: Dict[str, int] = {'A': 0, 'D': 0}
        self.ram: List[int] = [0] * 32768  # Hack computer has 32K RAM
        self.cycles: int = cycles
        self.memory_interactions: Dict[int, int] = {}

    def run(self) -> Dict[int, int]:
        max_cycles: int = self.cycles
        current_cycles: int = 0
        while self.pc < len(self.instructions) and current_cycles < max_cycles:
            instruction: str = self.instructions[self.pc]
            self.execute_instruction(instruction)
            current_cycles += 1
            self.pc += 1

        return self.memory_interactions

    def execute_instruction(self, instruction: str) -> None:
        if instruction[0] == '0':  # A-instruction
            self.registers['A'] = int(instruction[1:], 2)
        else:  # C-instruction
            comp: str = instruction[3:10]
            dest: str = instruction[10:13]
            jump: str = instruction[13:16]

            result: int = self.compute(comp)
            self.set_destination(dest, result)
            self.handle_jump(jump, result)

    def compute(self, comp: str) -> int:
        a: int = self.registers['A']
        d: int = self.registers['D']
        m: int = self.ram[a]

        if comp == '0101010':
            return 0
        elif comp == '0111111':
            return 1
        elif comp == '0111010':
            return -1
        elif comp == '0001100':
            return d
        elif comp == '0110000':
            return a
        elif comp == '1110000':
            return m
        elif comp == '0001101':
            return ~d
        elif comp == '0110001':
            return ~a
        elif comp == '1110001':
            return ~m
        elif comp == '0001111':
            return -d
        elif comp == '0110011':
            return -a
        elif comp == '1110011':
            return -m
        elif comp == '0011111':
            return d + 1
        elif comp == '0110111':
            return a + 1
        elif comp == '1110111':
            return m + 1
        elif comp == '0001110':
            return d - 1
        elif comp == '0110010':
            return a - 1
        elif comp == '1110010':
            return m - 1
        elif comp == '0000010':
            return d + a
        elif comp == '1000010':
            return d + m
        elif comp == '0010011':
            return d - a
        elif comp == '1010011':
            return d - m
        elif comp == '0000117':
            return a - d
        elif comp == '1000117':
            return m - d
        elif comp == '0000000':
            return d & a
        elif comp == '1000000':
            return d & m
        elif comp == '0010101':
            return d | a
        elif comp == '1010101':
            return d | m
        else:
            raise ValueError('Invalid comp field')

    def set_destination(self, dest: str, result: int) -> None:
        if dest[1] == '1':
            self.registers['D'] = result
        if dest[2] == '1':
            self.ram[self.registers['A']] = result
            self.memory_interactions[self.registers['A']] = result
        if dest[0] == '1':
            self.registers['A'] = result

    def handle_jump(self, jump: str, result: int) -> None:
        if jump == '001' and result > 0:
            self.pc = self.registers['A'] - 1
        elif jump == '010' and result == 0:
            self.pc = self.registers['A'] - 1
        elif jump == '011' and result >= 0:
            self.pc = self.registers['A'] - 1
        elif jump == '100' and result < 0:
            self.pc = self.registers['A'] - 1
        elif jump == '101' and result != 0:
            self.pc = self.registers['A'] - 1
        elif jump == '110' and result <= 0:
            self.pc = self.registers['A'] - 1
        elif jump == '111':
            self.pc = self.registers['A'] - 1
