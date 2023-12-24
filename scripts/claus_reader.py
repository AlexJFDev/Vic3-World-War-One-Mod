''' Reads a file from the Clausewitz engine into an object '''

def read_file(file):
    claus_object = []
    for line in file:
        line = line.strip().split('#')[0]

        if '=' in line:
            left_side, right_side = line.split('=')
            left_side = left_side.strip()
            right_side = right_side.strip()
            claus_object.append((left_side, right_side))
        
    return claus_object