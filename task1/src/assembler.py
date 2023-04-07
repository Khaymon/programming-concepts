from config import Config


class Assembler:
    def __init__(self):
        self.program_text = []
        self.config = Config()
    
    def read_file(self, filename):
        with open(filename) as f:
            self.program_text = f.readlines()
            self.program_text = [line.strip() for line in self.program_text]
            
    def create_putcs_for_putstr(self, putstr_instruction):
        has_label = False
        if putstr_instruction.find(':') != -1 and putstr_instruction.find(':') < putstr_instruction.find('PUTSTR'):
            label = putstr_instruction[:putstr_instruction.find(':') + 1]
            has_label = True
        
        chars = list(putstr_instruction[putstr_instruction.find('PUTSTR') + len('PUTSTR '):])
        
        chars.append('\n')  
        
        result_instructions = []
        for char in chars:
            if has_label:
                result_instructions.append(label + ' PUTC ' + str(ord(char)))
                has_label = False
            result_instructions.append('PUTC ' + str(ord(char)))
            
        return result_instructions
            
    def replace_all_putstr_with_putcs(self):
        new_program_text = []
        
        for i, line in enumerate(self.program_text):
            
            if line.find('PUTSTR') != -1:
                new_instructions = self.create_putcs_for_putstr(line)
                for instruction in new_instructions:
                    new_program_text.append(instruction)
                continue
                
            new_program_text.append(line)
                
        self.program_text = new_program_text
    
            
    def replace_labels_with_cell_numbers(self):
        label_to_num = {}
        
        result = []
        
        for i, line in enumerate(self.program_text):
            if line.find(':') != -1:
                label = line[:line.find(':')]
                label_to_num[label] = i
                line = line[line.find(':') + 1:]
            line = line.strip()
            result.append(line)
            
        lines = result
        result = []
        
        for line in lines:
            for label, num in label_to_num.items():
                line = line.replace(label, str(num * self.config.instruction_size + self.config.num_registers + self.config.start_function_address))
            result.append(line)
        self.program_text = result
        
        
    def convert_to_static(self, string_parameter):
        if string_parameter in self.config.registers.registers_dict:
            return self.config.registers.registers_dict[string_parameter]
        return int(string_parameter)
        
    def convert_string_to_code(self, string):
        string_params = string.split()
        
        string_params[0] = self.config.instructions.instructions_dict[string_params[0]]
        
        if len(string_params) < 3:
            if len(string_params) == 2:
                string_params.append(self.convert_to_static(string_params[1]))
                string_params[1] = 0
            if len(string_params) == 1:
                string_params.append(0)
                string_params.append(0)
        else:
            string_params[1] = self.convert_to_static(string_params[1])
            string_params[2] = self.convert_to_static(string_params[2])
        
        return string_params
    
    
    def generate_bytecode(self):
        self.replace_all_putstr_with_putcs()
        self.replace_labels_with_cell_numbers()
        
        byte_code = []
        
        for instruction in self.program_text:
            instr_byte_code = self.convert_string_to_code(instruction)
            for code in instr_byte_code:
                byte_code.append(code)
        
        return byte_code
    
    
    def assembly(self, program_file, bytecode_file):
        self.read_file(program_file)
        bytecode = self.generate_bytecode()
        
        with open(bytecode_file, 'w') as outfile:
            for code in bytecode:
                outfile.write("%d " % code)