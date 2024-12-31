import os
import csv

import clausewitz_parser
from clausewitz_root import ClausewitzRoot
from clausewitz_object import ClausewitzObject


COUNTRY_DEFINITIONS_PATH = os.path.join('game', 'files', 'common', 'country_definitions')
COUNTRY_DEFINITION_FILE_NAMES = [
    '00_countries.txt',
    '01_africa.txt',
    '01_pacific_and_australasia.txt',
    '99_dynamic.txt'
]
COUNTRY_DEFINITION_FILEPATHS = [os.path.join(COUNTRY_DEFINITIONS_PATH, file_name) for file_name in COUNTRY_DEFINITION_FILE_NAMES]

COUNTRY_DEFINITIONS_CSV_FILEPATH = os.path.join('game', 'data', 'countries.csv')
