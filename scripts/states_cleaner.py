FILE_PATH = 'small_states.txt'

if __name__ == '__main__':
    bracket_depth = 0
    with open(FILE_PATH, 'rt') as file:
        file_dict = {}
        for line in file:
            if '=' in line:
                left_side, right_side = line.split('=')