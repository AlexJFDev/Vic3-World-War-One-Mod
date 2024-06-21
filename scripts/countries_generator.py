from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

import os
import csv

DEFINITIONS_FILE: str = os.path.join('data', 'country_definitions.csv')
COUNTRIES_FILE: str = os.path.join('mod_files', 'countries.txt')

TAG_COLUMN = 1
COLOR_COLUMN = 2
TIER_COLUMN = 3
CULTURES_COLUMN = 4
CAPITAL_COLUMN = 5
IS_DYNAMIC_COLUMN = 6

def generate_countries(file_path):
    countries_root = ClausewitzRoot()

    with open(file_path, 'r') as definitions_file:
        definitions_file.readline()
        definitions_reader = csv.reader(definitions_file)
        for line in definitions_reader:
            tag = line[TAG_COLUMN]
            color = line[COLOR_COLUMN]
            tier = line[TIER_COLUMN]
            cultures = line[CULTURES_COLUMN]
            capital = line[CAPITAL_COLUMN]
            is_dynamic = line[IS_DYNAMIC_COLUMN]

            country_object = ClausewitzObject()
            if is_dynamic == 'TRUE':
                country_object.add_named_value('dynamic_country_definition', 'yes')
                countries_root.add_named_value(tag, country_object)
                continue

            color_object = ClausewitzObject()
            for component in color.split(' '):
                color_object.add_anonymous_value(component)
            cultures_object = ClausewitzObject()
            for culture in cultures.split(' '):
                cultures_object.add_anonymous_value(culture)

            country_object.add_named_value('tier', tier)
            country_object.add_named_value('capital', capital)
            country_object.add_named_value('country_type', 'recognized')
            country_object.add_named_value('color', color_object)
            country_object.add_named_value('cultures', cultures_object)

            countries_root.add_named_value(tag, country_object)
    return countries_root

if __name__ == '__main__':
    countries_root = generate_countries(DEFINITIONS_FILE)
    with open(COUNTRIES_FILE, 'w') as file:
        file.write(countries_root.unparse())
