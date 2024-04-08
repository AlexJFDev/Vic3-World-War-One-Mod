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

    left_of_equals = True
    left_data = ''
    right_data = ''
    while len(chars) > 0:
        current_char = chars.pop(0)
        if current_char == '{':
            new_object = parse_object(chars)
            if (left_of_equals):
                clausewitz_object.add_anonymous_value(new_object)
            else:
                clausewitz_object.add_named_value(left_data, new_object)
                left_of_equals = True
                left_data = ''
                right_data = ''
        elif current_char == '}': 
            if left_of_equals:
                if left_data != '':
                    clausewitz_object.add_anonymous_value(left_data)
            else:
                clausewitz_object.add_named_value(left_data, right_data)
            break
        elif current_char == '=':
            left_of_equals = False
        elif current_char == '\n':
            if left_of_equals:
                if left_data != '':
                    clausewitz_object.add_anonymous_value(left_data)
            else:
                clausewitz_object.add_named_value(left_data, right_data)
            left_of_equals = True
            left_data = ''
            right_data = ''
        elif current_char.isspace():
            pass
        elif (left_of_equals):
            left_data += current_char
        else:
            right_data += current_char
    return clausewitz_object

if __name__ == '__main__':
    with open(FILE_PATH, 'rt') as file:
        string = file.read()
        chars = [*string]

        file_as_object: ClausewitzObject = parse_object(chars)

        print(file_as_object.unparse(separator='*'))
