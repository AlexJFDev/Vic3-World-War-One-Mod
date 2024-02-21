import os

import clausewitz_parser

FILE_PATH = os.path.join('data', 'combined_cultures.txt')
CSV_PATH = os.path.join('data', 'cultures.csv')

TAG_COLUMN = 1
COLOR_COLUMN = 2
TRAITS_COLUMN = 3
OBSESSIONS_COLUMN = 4
MALE_COMMON_FIRST_NAMES = 5
FEMALE_COMMON_FIRST_NAMES = 6
COMMON_LAST_NAMES = 7
MALE_REGAL_FIRST_NAMES = 8
FEMALE_REGAL_FIRST_NAMES = 9
NOBLE_LAST_NAMES = 10
ETHNICITIES = 11
GRAPHICS = 12

if __name__ == "__main__":
    file_as_object = clausewitz_parser.parse_file(FILE_PATH)

    print(file_as_object.unparse())