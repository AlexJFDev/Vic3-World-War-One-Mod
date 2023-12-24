''' Reads a file from the Clausewitz engine into an object '''

def read_file(path):
    with open(path, 'rt') as file:
        base_dict = {}
        sub_lines = []
        inside_sub = False
        bracket_depth = 0
        left_side = ''
        right_side = ''
        for line in file:
            bracket_depth += line.count('{')
            bracket_depth -= line.count('}')
            if bracket_depth == 0:
                inside_sub = False
                base_dict[left_side] = read_object(sub_lines)

            if inside_sub:
                sub_lines.append(line)

            if '=' in line and not inside_sub:
                left_side, right_side = line.split('=')
                left_side = left_side.strip()
                right_side = right_side.strip()

                sub_lines = []
                inside_sub = True
                sub_lines.append(right_side)
    return base_dict

def read_object(lines):
    base_dict = {}
    sub_lines = []
    inside_sub = False
    bracket_depth = -1
    left_side = ''
    right_side = ''
    for line in lines:
        bracket_depth += line.count('{')
        bracket_depth -= line.count('}')
        if bracket_depth == 0:
            inside_sub = False
            base_dict[left_side] = read_object(sub_lines)

        if inside_sub:
            sub_lines.append(line)

        if '=' in line and not inside_sub:
            left_side, right_side = line.split('=')
            left_side = left_side.strip()
            right_side = right_side.strip()
            print(left_side)

            sub_lines = []
            inside_sub = True
            sub_lines.append(right_side)
    return base_dict