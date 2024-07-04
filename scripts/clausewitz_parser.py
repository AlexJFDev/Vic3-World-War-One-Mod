from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

import os

import csv

FILE_PATH = os.path.join('data', 'test.txt')

# There is a bug with one line objects

def parse_path(path: str) -> ClausewitzRoot:
    with open(path, 'rt') as file:
        string = file.read()
    chars = [*string]

    file_as_object = parse_char_list(chars)

    root = ClausewitzRoot(name_values=file_as_object.get_name_values(), anonymous_values=file_as_object.get_anonymous_values())
    return root

def parse_file(file) -> ClausewitzRoot:
    string = file.read()
    chars = [*string]

    file_as_object = parse_char_list(chars)

    root = ClausewitzRoot(name_values=file_as_object.get_name_values(), anonymous_values=file_as_object.get_anonymous_values())
    return root

def parse_char_list(chars: list[str]) -> ClausewitzObject:
    clausewitz_object = ClausewitzObject()

    left_of_equals = True
    left_data = ['']
    right_data = ''
    while len(chars) > 0:
        current_char = chars.pop(0)
        if current_char == '{':
            if len(right_data) > 0:
                new_object = f'{right_data}{parse_typed_object(chars)}'
            else:
                new_object = parse_char_list(chars)
            if (left_of_equals):
                clausewitz_object.add_anonymous_value(new_object)
            else:
                clausewitz_object.add_named_value(left_data[0], new_object)
                left_of_equals = True
                left_data = ['']
                right_data = ''
        
        elif current_char == '}': 
            if left_of_equals:
                if len(left_data) > 1 or len(left_data[0]) > 0:
                    clausewitz_object.add_anonymous_values(*left_data)
            else:
                clausewitz_object.add_named_value(left_data[0], right_data)
            break
        
        elif current_char == '=':
            left_of_equals = False
        
        elif current_char == '\n':
            if left_of_equals:
                if len(left_data) > 1 or len(left_data[0]) > 0:
                    clausewitz_object.add_anonymous_values(*left_data)
            else:
                clausewitz_object.add_named_value(left_data[0], right_data)
            left_of_equals = True
            left_data = ['']
            right_data = ''
        
        elif current_char.isspace():
            if len(left_data[-1]) > 0:
                left_data.append('')

        elif current_char == '#':
            while current_char != '\n':
                current_char = chars.pop(0)
        
        elif (left_of_equals):
            left_data[-1] += current_char
        
        else:
            right_data += current_char
        
    return clausewitz_object

def parse_typed_object(chars: list[str]) -> str:
    data = ''
    current_char = chars.pop(0)
    while(current_char != '}'):
        data += current_char
        current_char = chars.pop(0)
    return f'{"{"}{data}{"}"}'

if __name__ == '__main__':
    file_as_object = parse_path(FILE_PATH)
    print(file_as_object.unparse())

        
