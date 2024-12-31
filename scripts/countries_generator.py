from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

import os
import csv

DEFINITIONS_FILE: str = os.path.join('mod', 'data', 'country_definitions.csv')
COUNTRIES_FILE: str = os.path.join('mod', 'files', 'countries.txt')

NAME_COLUMN = 0
TAG_COLUMN = 1
COLOR_COLUMN = 2
TIER_COLUMN = 3
CULTURES_COLUMN = 4
REGION_COLUMN = 5
CAPITAL_COLUMN = 6
IS_NAMED_FROM_CAPITAL_COLUMN = 7
IS_DYNAMIC_COLUMN = 8

BOOLEAN_VALUES = {
    True : 'yes',
    False : 'no'
}

def generate_countries(file_path: str):
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
            named_from_capital = line[IS_NAMED_FROM_CAPITAL_COLUMN]

            country_object = ClausewitzObject()
            if is_dynamic.lower() == 'true':
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
            if capital != '':
                country_object.add_named_value('capital', capital)
            country_object.add_named_value('country_type', 'recognized')
            country_object.add_named_value('color', color_object)
            country_object.add_named_value('cultures', cultures_object)
            if named_from_capital.lower() == 'true':
                country_object.add_named_value('is_named_from_capital', 'yes')

            countries_root.add_named_value(tag, country_object)
    return countries_root

if __name__ == '__main__':
    countries_root = generate_countries(DEFINITIONS_FILE)
    with open(COUNTRIES_FILE, 'w') as file:
        file.write(countries_root.unparse())
