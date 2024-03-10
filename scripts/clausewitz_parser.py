from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

import os

import csv

FILE_PATH = os.path.join('data', 'test.txt')

# There is a bug with one line objects

def parse_file(path: str) -> ClausewitzRoot:
    root = ClausewitzRoot()
    return root

def parse_object(chars: list[str]) -> ClausewitzObject:
    clausewitz_object = ClausewitzObject()

    on_left = True
    left_side = ''
    while len(chars) > 0:
        current = chars.pop(0)
        if (on_left):
            left_side += current
        print(current, end='')
    return clausewitz_object

if __name__ == '__main__':
    with open(FILE_PATH, 'rt') as file:
        string = file.read()
        chars = [*string]

        file_as_object: ClausewitzObject = parse_object(chars)

        print(file_as_object.unparse())
