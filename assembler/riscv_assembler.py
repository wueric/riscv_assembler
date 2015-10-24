import argparse

def reverse_dict_with_iterable (dictionary):
    rev = {}
    for key, value in dictionary.items():
        for item in value:
            rev[item] = key
    return rev

TYPES_TO_INSTRUCTION = {
    'U_TYPE' : set(['LUI', 'AUIPC']),
    'UJ_TYPE' : set(['JAL']),
    'SB_TYPE' : set(['BEQ', 'BNE', 'BLT', 'BGE', 'BLTU', 'BGEU']),
    'I_TYPE' : set(['JALR', 'LB', 'LH', 'LW', 'LBU', 'LHU', 'ADDI', 'SLTI', 'SLTIU', 'XORI', 'ORI', 'ANDI', 'SLLI', 'SRLI', 'SRAI']),
    'S_TYPE' : set(['SB', 'SH', 'SW']),
    'R_TYPE': set(['ADD', 'SUB', 'SLL', 'SLT', 'SLTU', 'XOR', 'SRL', 'SRA', 'OR', 'AND'])
}

INSTRUCTION_TO_TYPE = reverse_dict_with_iterable(TYPES_TO_INSTRUCTION)

OPCODES = {
    'LUI' : '0110111',
    'AUIPC' : '0010111',
    'JAL' : '1101111',
    'JALR' : '1100111',
    'BEQ' : '1100011',
    'BNE' : '1100011',
    'BLT' : '1100011',
    'BGE' : '1100011',
    'BLTU' : '1100011',
    'BGEU' : '1100011',
    'LB' : '0000011',
    'LH' : '0000011',
    'LW' : '0000011',
    'LBU' : '0000011',
    'LHU' : '0000011',
    'SB' : '0100011',
    'SH' : '0100011',
    'SW' : '0100011',
    'ADDI' : '0010011',
    'SLTI' : '0010011',
    'SLTIU' : '0010011',
    'XORI' : '0010011',
    'ORI' : '0010011',
    'ANDI' : '0010011',
    'SLLI' : '0010011',
    'SRLI' : '0010011',
    'SRAI' : '0010011',
    'ADD' : '0110011',
    'SUB' : '0110011',
    'SLL' : '0110011',
    'SLT' : '0110011',
    'SLTU' : '0110011',
    'XOR' : '0110011',
    'SRL' : '0110011',
    'SRA' : '0110011',
    'OR' : '0110011',
    'AND' : '0110011'
}

FUNCT_CODES = {
    'JALR' : '000',
    'BEQ' : '000',
    'BNE' : '001',
    'BLT' : '100',
    'BGE' : '101',
    'BLTU' : '110',
    'BGEU' : '111',
    'LB' : '000',
    'LH' : '001',
    'LW' : '010',
    'LBU' : '100',
    'LHU' : '101',
    'SB' : '000',
    'SH' : '001',
    'SW' : '010',
    'ADDI' : '000',
    'SLTI' : '010',
    'SLTIU' : '011',
    'XORI' : '100',
    'ORI' : '110',
    'ANDI' : '111',
    'SLLI' : '001',
    'SRLI' : '101',
    'SRAI' : '101',
    'ADD' : '000',
    'SUB' : '000',
    'SLL' : '001',
    'SLT' : '010',
    'SLTU' : '011',
    'XOR' : '100',
    'SRL' : '101',
    'SRA' : '101',
    'OR' : '110',
    'AND' : '111'
}

R_I_TYPE_UPPER_SEVEN_BITS_NORMAL = '0000000'
R_I_TYPE_UPPER_SEVEN_BITS_ALT = '0100000'


def generate_binary_from_instruction (instruction_text):

    '''
    >>> U_type_test = 'LUI x4,0xFF'
    >>> generate_binary_from_instruction(U_type_test)
    '00000000000011111111001000110111'
    >>> UJ_type_test = 'JAL x4,0xF0'
    >>> generate_binary_from_instruction(UJ_type_test)
    '00011110000000000000001001101111'
    >>> S_type_test = 'SB x7,x31,0x99'
    >>> generate_binary_from_instruction(S_type_test)
    '00001001111100111000110010100011'
    >>> SB_type_test = 'BEQ x7,x8,0x335'
    >>> generate_binary_from_instruction(SB_type_test)
    '00110010100000111000101001100011'
    >>> I_type_test = 'SRAI x9,x8,0x4'
    >>> generate_binary_from_instruction(I_type_test)
    '01000000010001000101010010010011'
    >>> I_type_test = 'SRLI x9,x8,0x4'
    >>> generate_binary_from_instruction(I_type_test)
    '00000000010001000101010010010011'
    >>> R_type_test = 'OR x10,x8,x31'
    >>> generate_binary_from_instruction(R_type_test)
    '00000001111101000110010100110011'
    >>> R_type_test = 'SUB x10,x8,x30'
    >>> generate_binary_from_instruction(R_type_test)
    '01000001111001000000010100110011'
    '''
    calculate_register_number_from_name = lambda x: int(x[1:])

    instruction_name, remainder = instruction_text.split()
    instruction_values = remainder.replace(" ", "").split(',')
    instruction_type = INSTRUCTION_TO_TYPE[instruction_name]

    if instruction_type == 'U_TYPE':
        # unpack u-type instruction
        assert len(instruction_values) == 2
        
        register_name = calculate_register_number_from_name(instruction_values[0])
        immediate_value = int(instruction_values[1], 0) # convert immediate to integer
        
        # get the bottom 20 bits
        immediate_bottom_bits = immediate_value & 0xFFFFF

        instruction_binary = '{0:020b}{1:05b}{2}'.format(immediate_bottom_bits,
                                                        register_name,
                                                        OPCODES[instruction_name])

        assert len(instruction_binary) == 32
        return instruction_binary
        
    elif instruction_type == 'UJ_TYPE':
        # unpack uj-type instruction
        assert len(instruction_values) == 2

        register_name = calculate_register_number_from_name(instruction_values[0])
        immediate_value = int(instruction_values[1], 0) # convert immediate to integer
        # get bottom 20 bits of immediate
        immediate_bottom_bits = immediate_value & 0xFFFFF
        
        # pack immedate bits into binary string
        immediate_binary_string = '{0:01b}{1:010b}{2:01b}{3:08b}'.format(
            (immediate_bottom_bits >> 19) & 0x1,
            (immediate_bottom_bits & 0x3FF),
            (immediate_bottom_bits >> 10) & 0x1,
            (immediate_bottom_bits >> 11) & 0xFF)

        instruction_binary = '{0}{1:05b}{2}'.format(immediate_binary_string,
            register_name,
            OPCODES[instruction_name])

        assert len(instruction_binary) == 32
        return instruction_binary

    elif instruction_type == 'SB_TYPE':

        # unpack sb-type instruction

        assert len(instruction_values) == 3
        
        rs1_name = calculate_register_number_from_name(instruction_values[0])
        rs2_name = calculate_register_number_from_name(instruction_values[1])

        # get bottom 12 bits of immediate
        immediate_value = int(instruction_values[2], 0) & 0xFFF

        # pack upper half of immediate
        immediate_upper_bits_string = '{0:01b}{1:06b}'.format(
            (immediate_value >> 11) & 0x1,
            (immediate_value >> 5) & 0x3F)

        # pack lower half of immediate
        immediate_lower_bits_string = '{0:04b}{1:01b}'.format(
            (immediate_value >> 1) & 0xF,
            (immediate_value >> 10) & 0x1)

        instruction_binary = '{0}{1:05b}{2:05b}{3}{4}{5}'.format(
            immediate_upper_bits_string,
            rs2_name,
            rs1_name,
            FUNCT_CODES[instruction_name],
            immediate_lower_bits_string,
            OPCODES[instruction_name]
        )

        assert len(instruction_binary) == 32
        return instruction_binary

    elif instruction_type == 'S_TYPE':
        assert len(instruction_values) == 3
        
        rs1_name = calculate_register_number_from_name(instruction_values[0])
        rs2_name = calculate_register_number_from_name(instruction_values[1])
        immediate_value = int(instruction_values[2], 0) & 0xFFF

        immediate_upper_half = '{0:07b}'.format(immediate_value >> 5)
        immediate_lower_half = '{0:05b}'.format(immediate_value & 0x1F)

        instruction_binary = '{0}{1:05b}{2:05b}{3}{4}{5}'.format(
            immediate_upper_half,
            rs2_name,
            rs1_name,
            FUNCT_CODES[instruction_name],
            immediate_lower_half,
            OPCODES[instruction_name]
        )

        assert len(instruction_binary) == 32

        return instruction_binary

    elif instruction_type == 'I_TYPE':
        # unpack i-type instruction

        assert len(instruction_values) == 3
        
        rd_name = calculate_register_number_from_name(instruction_values[0])
        rs1_name = calculate_register_number_from_name(instruction_values[1])

        immediate_value = int(instruction_values[2], 0) & 0xFFF


        immediate_binary_string = ''
        if instruction_name == 'SLLI' or instruction_name == 'SRLI' \
                or instruction_name == 'SRAI':

            if instruction_name == 'SRAI':
                immediate_binary_string = '{0}{1:05b}'.format(
                    R_I_TYPE_UPPER_SEVEN_BITS_ALT,
                    immediate_value & 0x1F)
            else:
                immediate_binary_string = '{0}{1:05b}'.format(
                    R_I_TYPE_UPPER_SEVEN_BITS_NORMAL,
                    immediate_value & 0x1F)

        else:
            immediate_binary_string = '{0:012b}'.format(immediate_value)

        assert len(immediate_binary_string) == 12

        instruction_binary = '{0}{1:05b}{2}{3:05b}{4}'.format(
            immediate_binary_string,
            rs1_name,
            FUNCT_CODES[instruction_name],
            rd_name,
            OPCODES[instruction_name])

        assert len(instruction_binary) == 32
        return instruction_binary

    elif instruction_type == 'R_TYPE':
        # unpack r-type instruction
        assert len(instruction_values) == 3
        rd_name = calculate_register_number_from_name(instruction_values[0])
        rs1_name = calculate_register_number_from_name(instruction_values[1])
        rs2_name = calculate_register_number_from_name(instruction_values[2])

        special_instructions = set(['SUB', 'SRA'])
        upper_bit_pattern = R_I_TYPE_UPPER_SEVEN_BITS_ALT if instruction_name in special_instructions else R_I_TYPE_UPPER_SEVEN_BITS_NORMAL

        instruction_binary = '{0}{1:05b}{2:05b}{3}{4:05b}{5}'.format(
            upper_bit_pattern,
            rs2_name,
            rs1_name,
            FUNCT_CODES[instruction_name],
            rd_name,
            OPCODES[instruction_name]
        )

        assert len(instruction_binary) == 32
        return instruction_binary

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Convert RISC-V assembly to binary vectors')
    parser.add_argument('asmfile', type=str, help='asm file')

    args = parser.parse_args()
    
    assembly_file_path = args.asmfile

    assembly_file_root_name = assembly_file_path.split('.')[0]
    binary_file_path = '{0}.riscv_bin'.format(assembly_file_root_name)

    with open(assembly_file_path, 'r') as assembly_file:
        with open(binary_file_path, 'w') as binary_file:
            assembly_lines = assembly_file.readlines()
            for line in assembly_lines:
                line = line.strip('\n')
                instruction_as_binary = generate_binary_from_instruction(line)
                binary_file.write('{0}\n'.format(instruction_as_binary))

    print 'Completed'
