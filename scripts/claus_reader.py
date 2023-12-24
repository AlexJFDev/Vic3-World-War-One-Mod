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
    while(len(stack) != 0):
        line = stack.pop()
        print(line)