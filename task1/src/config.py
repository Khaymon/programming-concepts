class InstructionsConfig:
    instructions_dict = {
        'JUMP': 0,
        'PRINT': 1,
        'ADD': 2,
        'CALL': 3,
        'SUB': 4,
        'TOP': 5,
        'STOP': 6,
        'PUSHREG':7, 
        'FBEG': 8,
        'FEND': 9,
        'PUSH': 10,
        'POP': 11,
        'MOV': 12,
        'ASSIGN':13, 
        'IFNIL':14, 
        'READ': 15,
        'PUTC':16,
    }
    
    
class RegistersConfig:
    registers_dict = {
        'ip': 0, 
        'sp': 1, 
        'r1': 2, 
        'r2': 3, 
        'r3': 4, 
        'r4': 5, 
        'r5': 6, 
        'r6': 7, 
        'rf': 8
    }


class Config:
    num_registers = 9
    ip_address = 0
    sp_address = 1
    start_function_address = 10
    instruction_size = 3
    
    instructions = InstructionsConfig()
    registers = RegistersConfig()