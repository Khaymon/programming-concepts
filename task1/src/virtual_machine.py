import numpy as np

from config import Config


class VirtualMachine:
    def __init__(self, size: int):
        self.config = Config()
        
        self.memory = np.zeros(size, dtype=np.int32)
        self.memory[self.config.ip_address] = self.config.num_registers + self.config.start_function_address
        self.memory[self.config.sp_address] = size - 1
        
        self.memory[self.config.num_registers - 1] = 0
        
    
    def read_address(self, address: int) -> int:
        return self.memory[address]
    
    
    def write_address(self, address: int, value: int) -> None:
        self.memory[address] = value
        
        
    def read_array(self, program: np.ndarray) -> None:
        self.start_address = {}
        self.prototype_reading = False
        
        for idx in range(len(program)):
            self.memory[self.config.num_registers + self.config.start_function_address + idx] = program[idx]
    
    
    def read_file(self, filename: str) -> None:
        with open(filename, 'r') as input_file:
            program_string = input_file.readlines()
        
        program = [int(number) for number in program_string[0].split()]
        self.read_array(program)
        
        
    def next_instruction(self) -> None:
        self.write_address(self.config.ip_address, self.read_address(self.config.ip_address) + self.config.instruction_size)
        
    
    def get_instruction_values(self, address: int) -> np.ndarray:
        return self.memory[address:address + self.config.instruction_size]
    
    
    def get_instruction_id(self, instruction_name: str) -> int:
        return self.config.instructions[instruction_name]
    
    
    def mov(self, destination: int, source: int) -> None:
        self.write_address(destination, self.read_address(source))
        self.next_instruction()
        
    
    def add(self, destination: int, source: int) -> None:
        self.write_address(destination, self.read_address(destination) + self.read_address(source))
        self.next_instruction()
        
        
    def jump(self, destination: int) -> None:
        self.write_address(self.config.ip_address, destination)
        
        
    def read(self, destination: int) -> None:
        self.write_address(destination, int(input()))
        self.next_instruction()
        
        
    def print_register(self, source: int) -> None:
        print(self.read_address(source))
        self.next_instruction()
        
        
    def function_begin(self, function_number: int) -> None:
        self.write_address(self.config.num_registers - 1, 1)
        
        write_index = list(self.memory[self.config.num_registers:self.config.num_registers + self.config.start_function_address]).index(0)
        
        write_index += self.config.num_registers
        self.write_address(write_index, function_number)
        self.write_address(write_index + 1, self.read_address(self.config.ip_address) + self.config.instruction_size)
        
        self.next_instruction()
        
    
    def function_end(self) -> None:
        if self.read_address(self.config.num_registers - 1) == 1:
            self.write_address(self.config.num_registers - 1, 0)
            self.next_instruction()
        else:
            self.write_address(self.config.ip_address, self.read_address(self.read_address(self.config.sp_address) + 1))
            self.pop()
            
    
    def push(self, value: int, move_next: bool = False) -> None:
        self.write_address(self.read_address(self.config.sp_address), value)
        self.write_address(self.config.sp_address, self.read_address(self.config.sp_address) - 1)
        if move_next:
            self.next_instruction()
            
            
    def pop(self, move_next: bool = False) -> None:
        self.write_address(self.config.sp_address, self.read_address(self.config.sp_address) + 1)
        if move_next:
            self.next_instruction()
            
    
    def call(self, function_number: int) -> None:
        self.push(self.read_address(self.config.ip_address) + self.config.instruction_size)
        
        start_address = self.memory[self.config.num_registers:self.config.num_registers + self.config.start_function_address]
        
        for idx in range(len(start_address)):
            if idx % 2 == 1:
                continue
                
            if self.read_address(idx + self.config.num_registers) == function_number:
                self.write_address(self.config.ip_address, start_address[idx + 1])
                
                
    def top(self, destination: int) -> None:
        self.write_address(destination, self.read_address(self.read_address(self.config.sp_address) + 1))
        self.next_instruction()
        
    
    def sub(self, destination: int, source: int) -> None:
        self.write_address(destination, self.read_address(destination) - self.read_address(source))
        self.next_instruction()
        
        
    def assign(self, destination: int, value: int) -> None:
        self.write_address(destination, value)
        self.next_instruction()
        
        
    def ifnill(self, source: int, jump_address: int) -> None:
        if self.read_address(source) == 0:
            self.jump(jump_address)
        else:
            self.next_instruction()
            
            
    def push_register(self, source: int) -> None:
        self.push(self.read_address(source), True)
        
    
    def put_char(self, char_number: int) -> None:
        print(chr(char_number), end='')
        self.next_instruction()
        
    
    def interpret(self) -> bool:
        instruction_number, first_argument, second_argument = self.get_instruction_values(
            self.read_address(self.config.ip_address)
        )
        
        prototype_reading = self.read_address(self.config.num_registers - 1)
        
        if prototype_reading and not instruction_number == self.config.instructions.instructions_dict['FEND']:
            self.next_instruction()
        elif instruction_number == self.config.instructions.instructions_dict['MOV']:
            self.mov(first_argument, second_argument)
        elif instruction_number == self.config.instructions.instructions_dict['ADD']:
            self.add(first_argument, second_argument)
        elif instruction_number == self.config.instructions.instructions_dict['JUMP']:
            self.jump(second_argument)
        elif instruction_number == self.config.instructions.instructions_dict['STOP']:
            return False
        elif instruction_number == self.config.instructions.instructions_dict['READ']:
            self.read(second_argument)
        elif instruction_number == self.config.instructions.instructions_dict['PRINT']:
            self.print_register(second_argument)
        elif instruction_number == self.config.instructions.instructions_dict['FBEG']:
            self.function_begin(second_argument)
        elif instruction_number == self.config.instructions.instructions_dict['FEND']:
            self.function_end()
        elif instruction_number == self.config.instructions.instructions_dict['PUSH']:
            self.push(second_argument, True)
        elif instruction_number == self.config.instructions.instructions_dict['POP']:
            self.pop(True)
        elif instruction_number == self.config.instructions.instructions_dict['CALL']:
            self.call(second_argument)
        elif instruction_number == self.config.instructions.instructions_dict['TOP']:
            self.top(second_argument)
        elif instruction_number == self.config.instructions.instructions_dict['SUB']:
            self.sub(first_argument, second_argument)
        elif instruction_number == self.config.instructions.instructions_dict['ASSIGN']:
            self.assign(first_argument, second_argument)
        elif instruction_number == self.config.instructions.instructions_dict['IFNIL']:
            self.ifnill(first_argument, second_argument)
        elif instruction_number == self.config.instructions.instructions_dict['PUSHREG']:
            self.push_register(second_argument)
        elif instruction_number == self.config.instructions.instructions_dict['PUTC']:
            self.put_char(second_argument)
        
        return True
        
        
    def run_program(self):
        self.memory[self.config.ip_address] = self.config.num_registers + self.config.start_function_address
        self.memory[self.config.sp_address] = len(self.memory) - 1
        self.memory[self.config.num_registers] = 0
        
        while self.interpret():
            continue