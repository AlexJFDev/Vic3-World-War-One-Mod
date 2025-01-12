from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

import os
import csv

LAWS_FILE: str = os.path.join('mod', 'data', 'country_laws.csv')
INSTITUTIONS_FILE: str = os.path.join('mod', 'data', 'country_institutions.csv')

DOMESTIC_LAWS_FILE: str = os.path.join('mod', 'files', 'domestic_laws.txt')

LAWS_COUNTRY_COLUMN = 0
LAWS_TAG_COLUMN = 1
LAWS_START_COLUMN = 2
LAWS_END_COLUMN = 25

INSTITUTIONS_COUNTRY_COLUMN = 0
INSTITUTIONS_TAG_COLUMN = 1
INSTITUTIONS_COLUMNS = (
    (2, 'institution_colonial_affairs'),
    (3, 'institution_social_security'),
    (4, 'institution_workplace_safety'),
    (5, 'institution_schools'),
    (6, 'institution_police'),
    (7, 'institution_health_system'),
    (8, 'institution_home_affairs')
)
INSTITUTIONS_TAXATION_COLUMN = 9
INSTITUTIONS_MARKET_CAPITAL_COLUMN = 10

def generate_laws(laws_path: str, institutions_path: str) -> ClausewitzRoot:
    domestic_root = ClausewitzRoot()
    domestic_laws = ClausewitzObject()
    domestic_root.add_named_value('COUNTRIES', domestic_laws)

    with open(laws_path, 'r') as laws_file:
        laws_file.readline() # Skip first line
        laws_reader = csv.reader(laws_file)
        for row, values in enumerate(laws_reader):
            country_tag: str = values[LAWS_TAG_COLUMN]
            laws = values[LAWS_START_COLUMN: LAWS_END_COLUMN]

            tag_object = ClausewitzObject()
            domestic_laws.add_named_value(f'c:{country_tag}', tag_object)
            for law in laws:
                if law == '': continue
                tag_object.add_named_value('activate_law', f'law_type:{law}')


    with open(institutions_path, 'r') as institutions_file:
        institutions_file.readline() # Skip first line
        institutions_reader = csv.reader(institutions_file)
        for row, values in enumerate(institutions_reader):
            country_tag: str = values[INSTITUTIONS_TAG_COLUMN]

            tag_object = domestic_laws.get_value_named(f'c:{country_tag}')

            if tag_object is None:
                tag_object = ClausewitzObject()
                domestic_laws.add_named_value(f'c:{country_tag}', tag_object)
            for column, institution in INSTITUTIONS_COLUMNS:
                level = values[column]
                if level == '' or level == '0': continue

                institution_object = ClausewitzObject()
                institution_object.add_named_value('institution', institution)
                institution_object.add_named_value('level', level)

                tag_object.add_named_value('set_institution_investment_level', institution_object)

            tax_level = values[INSTITUTIONS_TAXATION_COLUMN]
            if tax_level != '':
                tag_object.add_named_value('set_tax_level', tax_level)
            market_capital = values[INSTITUTIONS_MARKET_CAPITAL_COLUMN]
            if market_capital != '':
                tag_object.add_named_value('set_market_capital', market_capital)
    return domestic_root

if __name__ == '__main__':
    domestic_root = generate_laws(LAWS_FILE, INSTITUTIONS_FILE)
    with open(DOMESTIC_LAWS_FILE, 'w') as file:
        file.write(domestic_root.unparse())