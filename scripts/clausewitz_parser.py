from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

import os

FILE_PATH = os.path.join('data', 'super_simple.txt')

def parse_file(path: str) -> ClausewitzRoot:
    root = ClausewitzRoot()
    with open(path, 'rt') as file:
        lines = file.readlines()
        lines.reverse()
        while len(lines) > 0:
            line = lines.pop().strip()
            if '=' in line:
                left_side, right_side = line.split('=', 1)
                root.add_named_value(left_side, right_side)
            elif len(line) > 0:
                root.join_anonymous_values(line.split(' '))
    return root

if __name__ == '__main__':
    file_as_object = parse_file(FILE_PATH)
    print(file_as_object.unparse())
    print(file_as_object.anonymous_values)
    print(file_as_object.name_values)