import os
import csv

import clausewitz_parser
from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject

import colorsys

COUNTRY_DEFINITIONS_PATH = os.path.join('game', 'files', 'common', 'country_definitions')
COUNTRY_DEFINITION_FILE_NAMES = [
    '00_countries.txt',
    '01_africa.txt',
    '01_pacific_and_australasia.txt',
    '99_dynamic.txt'
]
COUNTRY_DEFINITION_FILEPATHS = [os.path.join(COUNTRY_DEFINITIONS_PATH, file_name) for file_name in COUNTRY_DEFINITION_FILE_NAMES]

GAME_COUNTRY_DEFINITIONS_CSV_FILEPATH = os.path.join('game', 'data', 'countries.csv')

MOD_COUNTRY_DEFINITIONS_CSV_FILEPATH = os.path.join('mod', 'data', 'country_definitions.csv')

COUNTRY_NAME_COLUMN = 0
COUNTRY_TAG_COLUMN = 1
COUNTRY_COLOR_COLUMN = 2
COUNTRY_TIER_COLUMN = 3
COUNTRY_CULTURES_COLUMN = 4
COUNTRY_RELIGION_COLUMN = 5
COUNTRY_CAPITAL_COLUMN = 6
COUNTRY_NAMED_FROM_CAPITAL_COLUMN = 7
COUNTRY_IS_DYNAMIC_COLUMN = 8
COUNTRY_NUMBER_COLUMNS = 9

# function to get a rgb color from HSV string or ClausewitzObject
def extract_rgb(color: str | ClausewitzObject) -> tuple[int, int, int]:
    """
    Extracts the RGB values from a string or a ClausewitzObject.\n
    The string must be in the format format: hsv{ float  float  float } OR hsv360{ int  int  int }\n
    The ClausewitzObject must have 3 anonymous values.
    """
    if isinstance(color, str):
        if color.startswith('hsv360'):
            color = color[8:-2].split()
            hue = float(color[0]) / 360
            saturation = float(color[1]) / 100
            value = float(color[2]) / 100
        else:
            color = color[5:-2].split()
            hue = float(color[0])
            saturation = float(color[1])
            value = float(color[2])
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
    else:
        values = color.get_anonymous_values()
        return (values[0], values[1], values[2])

TRUE_VALUES = ['true', 'yes', '1', 't', 'y']
FALSE_VALUES = ['false', 'no', '0', 'f', 'n']
def extract_boolean(value: str, default=None) -> bool:
    """
    Convert a string representation of a boolean value to a boolean type.
    """
    if type(value) != str:
        return default
    value = value.strip().lower()
    if value in TRUE_VALUES:
        return True
    if value in FALSE_VALUES:
        return False
    return default


def unparse_country_file(filepath: str) -> dict:
    countries = {}

    countries_root: ClausewitzRoot = clausewitz_parser.parse_path(filepath)
    country_pairs: dict[str, list[ClausewitzObject]] = countries_root.get_name_value_pairs()
    for tag, country in country_pairs.items():
        country: ClausewitzObject = country[0]
        is_dynamic: bool = extract_boolean(country.get_value_named('dynamic_country_definition'), default=False)
        if is_dynamic:
            country = [''] * COUNTRY_NUMBER_COLUMNS
            country[COUNTRY_TAG_COLUMN] = tag
            country[COUNTRY_IS_DYNAMIC_COLUMN] = True
            continue
        color: tuple[int, int, int] = extract_rgb(country.get_value_named('color'))
        tier: str = country.get_value_named('tier')
        cultures: list[str] = country.get_value_named('cultures').get_anonymous_values()[:-1] # Gets a hanging ''
        capital: str = country.get_value_named('capital')
        religion: str = country.get_value_named('religion') 
        is_named_from_capital: bool = extract_boolean(country.get_value_named('is_named_from_capital'), default=False)

        country = [''] * COUNTRY_NUMBER_COLUMNS
        country[COUNTRY_TAG_COLUMN] = tag
        country[COUNTRY_COLOR_COLUMN] = f'{color[0]} {color[1]} {color[2]}'
        country[COUNTRY_TIER_COLUMN] = tier
        country[COUNTRY_CULTURES_COLUMN] = ' '.join(cultures)
        country[COUNTRY_RELIGION_COLUMN] = religion
        country[COUNTRY_CAPITAL_COLUMN] = capital
        country[COUNTRY_NAMED_FROM_CAPITAL_COLUMN] = is_named_from_capital
        country[COUNTRY_IS_DYNAMIC_COLUMN] = False

        countries[tag] = country

    return countries

def write_countries_csv(countries: dict[str, list[str]], filepath: str):
    with open(filepath, 'w', newline='') as file:
        file.write('Name,Tag,Color,Tier,Cultures,Religion,Capital,Named from Capital,Is Dynamic\n')
        csv_writer = csv.writer(file)
        for tag, country in countries.items():
            csv_writer.writerow(country)

def read_countries_csv(filepath: str) -> dict[str, list[str]]:
    countries = {}
    with open(filepath, 'r') as file:
        file.readline() # skip header
        csv_reader = csv.reader(file)
        for row in csv_reader:
            countries[row[COUNTRY_TAG_COLUMN]] = row
    return countries

if __name__ == '__main__':
    game_countries = {}
    for filepath in COUNTRY_DEFINITION_FILEPATHS:
        game_countries.update(unparse_country_file(filepath))
    write_countries_csv(game_countries, GAME_COUNTRY_DEFINITIONS_CSV_FILEPATH)

    mod_countries = read_countries_csv(MOD_COUNTRY_DEFINITIONS_CSV_FILEPATH)

    for tag, country in game_countries.items():
        if tag not in mod_countries.keys():
            mod_countries[tag] = country
        mod_countries[tag][COUNTRY_NAMED_FROM_CAPITAL_COLUMN] = country[COUNTRY_NAMED_FROM_CAPITAL_COLUMN]

    write_countries_csv(mod_countries, MOD_COUNTRY_DEFINITIONS_CSV_FILEPATH)