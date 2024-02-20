import os

import clausewitz_parser

FILE_PATH = os.path.join('data', 'combined_cultures.txt')
CSV_PATH = os.path.join('data', 'cultures.csv')

file_as_object = clausewitz_parser.parse_file(FILE_PATH)

print(file_as_object.unparse())