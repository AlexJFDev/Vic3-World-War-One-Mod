from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

import os

import csv

FILE_PATH = os.path.join('data', '00_states.txt')
CSV_PATH = os.path.join('data', 'state_regions.csv')

# There is a bug with one line objects

def parse_file(path: str) -> ClausewitzRoot:
    root = ClausewitzRoot()
    with open(path, 'rt') as file:
        lines = file.readlines()
        if lines[0][0:3] == 'ï»¿':
            lines[0] = lines[0][3:]
        lines.reverse()
        while len(lines) > 0:
            line = lines.pop().strip()
            if '=' in line:
                left_side, right_side = line.split('=', 1)
                left_side = left_side.strip()
                right_side = right_side.strip()
                if right_side[0] == '{':
                    lines.append(right_side[1:])
                    root.add_named_value(left_side, parse_object(lines))
                else:
                    root.add_named_value(left_side, right_side)
            elif len(line) > 0:
                split_line = line.split(' ')
                if '}' in split_line:
                    split_line.remove('}')
                root.join_anonymous_values(split_line)
    return root

def parse_object(lines: list[str]) -> ClausewitzObject:
    clausewitz_object = ClausewitzObject()
    while len(lines) > 0:
        line = lines.pop().strip()
        if '=' in line:
            left_side, right_side = line.split('=', 1)
            left_side = left_side.strip()
            right_side = right_side.strip()

            if left_side[0] == '}':
                left_side = left_side[1:]
            if right_side[-1] == '}':
                right_side = right_side[:-1]
            
            if right_side[0] == '{':
                lines.append(right_side[1:])
                clausewitz_object.add_named_value(left_side, parse_object(lines))
            else:
                clausewitz_object.add_named_value(left_side, right_side)
        elif len(line) > 0:
            if line[-1] == '}':
                split_line = line[:-1].split(' ')
            else:
                split_line = line.split(' ')
            if split_line[0] != '':
                clausewitz_object.join_anonymous_values(split_line)
        if '}' in line:
            return clausewitz_object
    return clausewitz_object

if __name__ == '__main__':
    file_as_object: ClausewitzRoot = parse_file(FILE_PATH)

    with open(CSV_PATH, 'w') as file:
        csv_writer = csv.writer(file)
        states: dict[str, ClausewitzObject] = file_as_object.get_named_value('STATES').get_name_values()

        for state_name, state_data in states.items():
            owners: list[ClausewitzObject] = state_data[0].get_named_values("create_state")
            provinces: list = []
            for owner in owners:
                provinces.extend(owner.get_named_value('owned_provinces').get_anonymous_values())
            csv_writer.writerow([state_name, ' '.join(provinces)])
