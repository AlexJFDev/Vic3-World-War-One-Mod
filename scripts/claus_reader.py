''' Reads a file from the Clausewitz engine into an object '''

def read_path(path):
    with open(path, 'rt') as file:
        return read_file(file)

def read_file(file):
    stack = []
    for line in file:
        stack.insert(0, line)
    return read_stack(stack)
        
def read_stack(stack):
    claus_object = []
    bracket_depth = 0
    while(len(stack) != 0):
        line = stack.pop().strip().split('#')[0]
        bracket_depth += line.count('{')
        bracket_depth -= line.count('}')
        print(line, bracket_depth)
        if '=' in line:
            left_side, right_side = line.split('=', 1)
            left_side = left_side.strip()
            right_side = right_side.strip()

            if right_side[0] == '{':
                stack.append(right_side[1:])
                claus_object.append((left_side, read_stack(stack)))
                bracket_depth -= 1
            else:
                claus_object.append((left_side, right_side))
        if bracket_depth == -1:
            break

    return claus_object