import clausewitz_parser
from clausewitz_object import ClausewitzObject
from clausewitz_root import ClausewitzRoot

import os
import csv

CULTURES_PATH = os.path.join('game', 'files', '00_cultures.txt')
ADDITIONAL_CULTURES_PATH = os.path.join('game', 'files', '00_additional_cultures.txt')

DATA_PATH = os.path.join('game', 'data', 'cultures.csv')

NAME_COLUMN = 0
TAG_COLUMN = 1
COLOR_COLUMN = 2
RELIGION_COLUMN = 3
TRAITS_COLUMN = 4
OBSESSIONS_COLUMN = 5
MALE_COMMON_NAMES = 6
FEMALE_COMMON_NAMES = 7
COMMON_LAST_NAMES = 8
MALE_REGAL_NAMES = 9
FEMALE_REGAL_NAMES = 10
NOBLE_LAST_NAMES = 11
ETHNICITIES = 12
GRAPHICS = 13

def unparse_cultures(cultures_root: ClausewitzObject):
    data = []
    cultures = cultures_root.get_names()
    for culture in cultures:
        print(culture)
        culture_object: ClausewitzObject = cultures_root.get_named_value(culture)
        row = [None] * 14

        color = culture_object.get_named_value('color')
        religion = culture_object.get_named_value('religion')
        traits = culture_object.get_named_value('traits', default=ClausewitzObject()).get_anonymous_values()
        obsessions = culture_object.get_named_value('obsessions', default=ClausewitzObject()).get_anonymous_values()
        male_common_first_names = culture_object.get_named_value('male_common_first_names', default=ClausewitzObject()).get_anonymous_values()
        female_common_first_names = culture_object.get_named_value('female_common_first_names', default=ClausewitzObject()).get_anonymous_values()
        common_last_names = culture_object.get_named_value('common_last_names', default=ClausewitzObject()).get_anonymous_values()
        male_regal_first_names = culture_object.get_named_value('male_regal_first_names', default=ClausewitzObject()).get_anonymous_values()
        female_regal_first_names = culture_object.get_named_value('female_regal_first_names', default=ClausewitzObject()).get_anonymous_values()
        noble_last_names = culture_object.get_named_value('noble_last_names', default=ClausewitzObject()).get_anonymous_values()
        ethnicities = culture_object.get_named_value('ethnicities', default=ClausewitzObject()).get_name_values()
        graphics = culture_object.get_named_value('graphics')

        if isinstance(color, ClausewitzObject):
            color = ' '.join(color.get_anonymous_values())

        ethnicity_string = ''
        for rate, name in ethnicities.items():
            ethnicity_string = f'{ethnicity_string} {rate}={name};'

        row[TAG_COLUMN] = culture
        row[COLOR_COLUMN] = color
        row[RELIGION_COLUMN] = religion
        row[TRAITS_COLUMN] = ' '.join(traits)
        row[OBSESSIONS_COLUMN] = ' '.join(obsessions)
        row[MALE_COMMON_NAMES] = ' '.join(male_common_first_names)
        row[FEMALE_COMMON_NAMES] = ' '.join(female_common_first_names)
        row[COMMON_LAST_NAMES] = ' '.join(common_last_names)
        row[MALE_REGAL_NAMES] = ' '.join(male_regal_first_names)
        row[FEMALE_REGAL_NAMES] = ' '.join(female_regal_first_names)
        row[NOBLE_LAST_NAMES] = ' '.join(noble_last_names)
        row[ETHNICITIES] = ethnicity_string
        row[GRAPHICS] = graphics

        data.append(row)
    return data

    
cultures_object: ClausewitzRoot = clausewitz_parser.parse_file(CULTURES_PATH)
additional_cultures_object: ClausewitzRoot = clausewitz_parser.parse_file(ADDITIONAL_CULTURES_PATH)

with open(DATA_PATH, 'wt', newline='') as data_file:
    data_writer = csv.writer(data_file)
    data_writer.writerows(unparse_cultures(cultures_object))
    data_writer.writerows(unparse_cultures(additional_cultures_object))